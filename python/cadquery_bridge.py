#!/usr/bin/env python3
"""
CADQuery Bridge - Execute CADQuery scripts and export geometry

This module provides a bridge between the Qt GUI and CADQuery for
parametric 3D modeling, STEP/STL export, and geometry validation.
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import Optional, Dict, Any, Union
import traceback


class CADQueryBridge:
    """
    Bridge for executing CADQuery scripts and exporting geometry.
    """
    
    def __init__(self, work_dir: str = "/work"):
        """
        Initialize the CADQuery bridge.
        
        Args:
            work_dir: Working directory for file operations
        """
        self.work_dir = Path(work_dir)
        self.work_dir.mkdir(parents=True, exist_ok=True)
        
    def execute_script(self, script: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a CADQuery script and return the result.
        
        Args:
            script: CADQuery Python script as string
            params: Optional parameters to inject into script
            
        Returns:
            Dictionary with 'success', 'result', 'error', and 'metadata'
        """
        try:
            # Import CADQuery (done here to catch import errors gracefully)
            import cadquery as cq
            
            # Prepare namespace with CADQuery and parameters
            namespace = {
                'cq': cq,
                'cadquery': cq,
                'params': params or {},
            }
            
            # Execute the script
            exec(script, namespace)
            
            # Look for 'result' or 'show_object' in namespace
            result = None
            if 'result' in namespace:
                result = namespace['result']
            elif 'show_object' in namespace:
                # CADQuery OCP viewer compatibility
                result = namespace['show_object']
            else:
                # Try to find any Workplane or Shape object
                for key, value in namespace.items():
                    if isinstance(value, (cq.Workplane, cq.Shape)):
                        result = value
                        break
            
            if result is None:
                return {
                    'success': False,
                    'result': None,
                    'error': 'No CADQuery result found. Ensure script defines a "result" variable.',
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
        """Extract metadata from a CADQuery object."""
        import cadquery as cq
        
        metadata = {}
        try:
            if isinstance(obj, cq.Workplane):
                # Get bounding box
                bbox = obj.val().BoundingBox()
                metadata['bounding_box'] = {
                    'xmin': bbox.xmin, 'xmax': bbox.xmax,
                    'ymin': bbox.ymin, 'ymax': bbox.ymax,
                    'zmin': bbox.zmin, 'zmax': bbox.zmax,
                    'center': [bbox.center.x, bbox.center.y, bbox.center.z],
                    'dimensions': [bbox.xlen, bbox.ylen, bbox.zlen]
                }
                
                # Try to get volume (may fail for non-solids)
                try:
                    solids = obj.solids().vals()
                    if solids:
                        total_volume = sum(s.Volume() for s in solids)
                        metadata['volume'] = total_volume
                        metadata['num_solids'] = len(solids)
                except:
                    pass
                    
                # Get face count
                try:
                    faces = obj.faces().vals()
                    metadata['num_faces'] = len(faces)
                except:
                    pass
                    
        except Exception as e:
            metadata['error'] = str(e)
            
        return metadata
    
    def export_step(self, result, output_path: Union[str, Path], **kwargs) -> Dict[str, Any]:
        """
        Export CADQuery result to STEP file.
        
        Args:
            result: CADQuery Workplane or Shape
            output_path: Path to output STEP file
            **kwargs: Additional export options
            
        Returns:
            Dictionary with success status and file info
        """
        try:
            import cadquery as cq
            
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Export STEP
            if isinstance(result, cq.Workplane):
                cq.exporters.export(result, str(output_path))
            else:
                # Try direct export for Shape objects
                cq.exporters.export(result, str(output_path))
            
            file_size = output_path.stat().st_size
            
            return {
                'success': True,
                'file': str(output_path),
                'size': file_size,
                'format': 'STEP'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"{type(e).__name__}: {str(e)}",
                'traceback': traceback.format_exc()
            }
    
    def export_stl(self, result, output_path: Union[str, Path], 
                   linear_deflection: float = 0.001,
                   angular_deflection: float = 0.5,
                   **kwargs) -> Dict[str, Any]:
        """
        Export CADQuery result to STL file.
        
        Args:
            result: CADQuery Workplane or Shape
            output_path: Path to output STL file
            linear_deflection: Linear deflection for tessellation (smaller = finer)
            angular_deflection: Angular deflection in degrees
            **kwargs: Additional export options
            
        Returns:
            Dictionary with success status and file info
        """
        try:
            import cadquery as cq
            
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Export STL with tessellation parameters
            if isinstance(result, cq.Workplane):
                cq.exporters.export(
                    result, 
                    str(output_path),
                    tolerance=linear_deflection,
                    angularTolerance=angular_deflection
                )
            else:
                cq.exporters.export(
                    result, 
                    str(output_path),
                    tolerance=linear_deflection,
                    angularTolerance=angular_deflection
                )
            
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
                'mesh_stats': mesh_stats
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"{type(e).__name__}: {str(e)}",
                'traceback': traceback.format_exc()
            }


def main():
    """Command-line interface for CADQuery bridge."""
    parser = argparse.ArgumentParser(description='CADQuery Bridge - Execute scripts and export geometry')
    parser.add_argument('--script', type=str, help='CADQuery script to execute')
    parser.add_argument('--script-file', type=str, help='Path to CADQuery script file')
    parser.add_argument('--step-output', type=str, help='Output STEP file path')
    parser.add_argument('--stl-output', type=str, help='Output STL file path')
    parser.add_argument('--params', type=str, help='JSON string of parameters')
    parser.add_argument('--work-dir', type=str, default='/work', help='Working directory')
    
    args = parser.parse_args()
    
    # Initialize bridge
    bridge = CADQueryBridge(work_dir=args.work_dir)
    
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
    
    # Export STEP if requested
    if args.step_output:
        step_result = bridge.export_step(result, args.step_output)
        output['exports']['step'] = step_result
    
    # Export STL if requested
    if args.stl_output:
        stl_result = bridge.export_stl(result, args.stl_output)
        output['exports']['stl'] = stl_result
    
    # Print result as JSON
    print(json.dumps(output, indent=2))
    

if __name__ == '__main__':
    main()
