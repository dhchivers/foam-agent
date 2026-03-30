#!/usr/bin/env python3
"""
libfive Bridge - Execute libfive scripts and export geometry

This module provides a bridge between the Qt GUI and libfive for
functional representation (F-Rep) 3D modeling and mesh export.

libfive uses functional representations where objects are defined by
mathematical functions f(x,y,z) that return signed distances.
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import Optional, Dict, Any, Union
import traceback


class LibfiveBridge:
    """
    Bridge for executing libfive scripts and exporting geometry.
    
    libfive uses functional representations (F-Rep) where objects are
    defined as mathematical functions. This provides different capabilities
    than boundary representation (B-Rep) tools like CADQuery.
    """
    
    def __init__(self, work_dir: str = "/work"):
        """
        Initialize the libfive bridge.
        
        Args:
            work_dir: Working directory for file operations
        """
        self.work_dir = Path(work_dir)
        self.work_dir.mkdir(parents=True, exist_ok=True)
        
    def execute_script(self, script: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a libfive Python script and return the result.
        
        Args:
            script: libfive Python script as string
            params: Optional parameters to inject into script
            
        Returns:
            Dictionary with 'success', 'result', 'error', and 'metadata'
        """
        try:
            # Import libfive (done here to catch import errors gracefully)
            try:
                import libfive
                from libfive.stdlib import *
            except ImportError as e:
                return {
                    'success': False,
                    'result': None,
                    'error': f'libfive not available: {str(e)}. Ensure libfive is installed.',
                    'metadata': {}
                }
            
            # Prepare namespace with libfive and parameters
            namespace = {
                'libfive': libfive,
                'params': params or {},
            }
            
            # Import common libfive functions into namespace
            try:
                from libfive.stdlib import (
                    sphere, box, cylinder, cone, torus,
                    union, intersection, difference,
                    translate, scale, rotate_x, rotate_y, rotate_z,
                    extrude_z, revolve_y,
                    shell, offset, clearance,
                    X, Y, Z  # Coordinate variables
                )
                namespace.update({
                    'sphere': sphere,
                    'box': box,
                    'cylinder': cylinder,
                    'cone': cone,
                    'torus': torus,
                    'union': union,
                    'intersection': intersection,
                    'difference': difference,
                    'translate': translate,
                    'scale': scale,
                    'rotate_x': rotate_x,
                    'rotate_y': rotate_y,
                    'rotate_z': rotate_z,
                    'extrude_z': extrude_z,
                    'revolve_y': revolve_y,
                    'shell': shell,
                    'offset': offset,
                    'clearance': clearance,
                    'X': X, 'Y': Y, 'Z': Z,
                })
            except ImportError:
                pass  # Some functions may not be available
            
            # Execute the script
            exec(script, namespace)
            
            # Look for 'result' or 'shape' in namespace
            result = None
            if 'result' in namespace:
                result = namespace['result']
            elif 'shape' in namespace:
                result = namespace['shape']
            else:
                # Try to find any libfive Tree object
                for key, value in namespace.items():
                    if hasattr(value, '__class__') and 'Tree' in str(value.__class__):
                        result = value
                        break
            
            if result is None:
                return {
                    'success': False,
                    'result': None,
                    'error': 'No libfive result found. Ensure script defines a "result" or "shape" variable.',
                    'metadata': {}
                }
            
            # Calculate metadata
            metadata = self._get_geometry_metadata(result)
            
            return {
                'success': True,
                'result': result,
                'error': None,
                'metadata': metadata
            }
            
        except Exception as e:
            return {
                'success': False,
                'result': None,
                'error': f"{type(e).__name__}: {str(e)}",
                'traceback': traceback.format_exc(),
                'metadata': {}
            }
    
    def _get_geometry_metadata(self, obj) -> Dict[str, Any]:
        """Extract metadata from a libfive object."""
        metadata = {}
        try:
            # libfive Tree objects have limited introspection
            # We can get bounds if available
            metadata['type'] = 'libfive.Tree'
            
            # Try to get the mathematical expression representation
            if hasattr(obj, '__str__'):
                metadata['description'] = 'F-Rep shape'
                
        except Exception as e:
            metadata['error'] = str(e)
            
        return metadata
    
    def export_stl(
        self, 
        result, 
        output_path: Union[str, Path],
        bounds: Optional[tuple] = None,
        resolution: float = 10.0,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Export libfive result to STL file.
        
        Args:
            result: libfive Tree object
            output_path: Path to output STL file
            bounds: Tuple of ((xmin, xmax), (ymin, ymax), (zmin, zmax))
                   If None, attempts to auto-detect or uses default
            resolution: Resolution for meshing (voxels per unit)
            **kwargs: Additional export options
            
        Returns:
            Dictionary with success status and file info
        """
        try:
            import libfive
            
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Set default bounds if not provided
            if bounds is None:
                # Default bounds: -10 to 10 in each dimension
                bounds = ((-10, 10), (-10, 10), (-10, 10))
            
            # Convert bounds to libfive format
            region = libfive.Region(
                libfive.vec3(*[b[0] for b in bounds]),
                libfive.vec3(*[b[1] for b in bounds])
            )
            
            # Generate mesh
            mesh = libfive.Mesh.render(result, region, resolution)
            
            # Save to STL
            mesh.save_stl(str(output_path))
            
            file_size = output_path.stat().st_size
            
            # Analyze the STL
            from stl_converter import STLConverter
            converter = STLConverter()
            mesh_stats = converter.analyze_mesh(str(output_path))
            
            return {
                'success': True,
                'file': str(output_path),
                'size': file_size,
                'format': 'STL',
                'bounds': bounds,
                'resolution': resolution,
                'mesh_stats': mesh_stats
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"{type(e).__name__}: {str(e)}",
                'traceback': traceback.format_exc()
            }
    
    def export_orthographic_images(
        self,
        result,
        output_dir: Union[str, Path],
        bounds: Optional[tuple] = None,
        resolution: int = 1024,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Export orthographic projection images (XY, XZ, YZ views).
        
        Args:
            result: libfive Tree object
            output_dir: Directory to save images
            bounds: Bounding region
            resolution: Image resolution in pixels
            **kwargs: Additional options
            
        Returns:
            Dictionary with success status and file paths
        """
        try:
            import libfive
            
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Set default bounds if not provided
            if bounds is None:
                bounds = ((-10, 10), (-10, 10), (-10, 10))
            
            region = libfive.Region(
                libfive.vec3(*[b[0] for b in bounds]),
                libfive.vec3(*[b[1] for b in bounds])
            )
            
            outputs = {}
            
            # XY view (top)
            xy_path = output_dir / "view_xy.png"
            libfive.Image.render_2d(result, region, resolution).save(str(xy_path))
            outputs['xy'] = str(xy_path)
            
            # XZ view (front) - requires rotating or adjusting bounds
            # YZ view (side)
            # Note: libfive's 2D rendering is primarily for XY plane
            # For other views, we'd need to render and rotate
            
            return {
                'success': True,
                'outputs': outputs,
                'resolution': resolution
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"{type(e).__name__}: {str(e)}",
                'traceback': traceback.format_exc()
            }
    
    def auto_detect_bounds(self, result, samples: int = 100) -> tuple:
        """
        Attempt to auto-detect reasonable bounds for a libfive shape.
        
        This is a heuristic and may not work for all shapes.
        
        Args:
            result: libfive Tree object
            samples: Number of samples per axis for detection
            
        Returns:
            Tuple of ((xmin, xmax), (ymin, ymax), (zmin, zmax))
        """
        # Default bounds - this is a placeholder
        # More sophisticated bound detection would require evaluating the function
        return ((-10, 10), (-10, 10), (-10, 10))


def main():
    """Command-line interface for libfive bridge."""
    parser = argparse.ArgumentParser(description='libfive Bridge - Execute scripts and export geometry')
    parser.add_argument('--script', type=str, help='libfive script to execute')
    parser.add_argument('--script-file', type=str, help='Path to libfive script file')
    parser.add_argument('--stl-output', type=str, help='Output STL file path')
    parser.add_argument('--bounds', type=str, help='Bounds as JSON: [[xmin,xmax],[ymin,ymax],[zmin,zmax]]')
    parser.add_argument('--resolution', type=float, default=10.0, help='Mesh resolution')
    parser.add_argument('--params', type=str, help='JSON string of parameters')
    parser.add_argument('--work-dir', type=str, default='/work', help='Working directory')
    
    args = parser.parse_args()
    
    # Initialize bridge
    bridge = LibfiveBridge(work_dir=args.work_dir)
    
    # Get script content
    if args.script:
        script = args.script
    elif args.script_file:
        with open(args.script_file, 'r') as f:
            script = f.read()
    else:
        print(json.dumps({'success': False, 'error': 'No script provided'}))
        sys.exit(1)
    
    # Parse parameters
    params = None
    if args.params:
        try:
            params = json.loads(args.params)
        except:
            print(json.dumps({'success': False, 'error': 'Invalid JSON parameters'}))
            sys.exit(1)
    
    # Parse bounds
    bounds = None
    if args.bounds:
        try:
            bounds_list = json.loads(args.bounds)
            bounds = tuple(tuple(b) for b in bounds_list)
        except:
            print(json.dumps({'success': False, 'error': 'Invalid bounds format'}))
            sys.exit(1)
    
    # Execute script
    result_dict = bridge.execute_script(script, params)
    
    if not result_dict['success']:
        print(json.dumps(result_dict))
        sys.exit(1)
    
    result = result_dict['result']
    output = {
        'success': True,
        'metadata': result_dict['metadata'],
        'exports': {}
    }
    
    # Export STL if requested
    if args.stl_output:
        stl_result = bridge.export_stl(
            result, 
            args.stl_output, 
            bounds=bounds,
            resolution=args.resolution
        )
        output['exports']['stl'] = stl_result
    
    # Print result as JSON
    print(json.dumps(output, indent=2))
    

if __name__ == '__main__':
    main()
