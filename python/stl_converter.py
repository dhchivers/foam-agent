#!/usr/bin/env python3
"""
STL Converter - Utilities for STL/STEP conversion and mesh processing

This module provides tools for converting between STEP and STL formats,
analyzing mesh quality, and performing mesh operations.
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import numpy as np


class STLConverter:
    """
    Utilities for STL/STEP conversion and mesh analysis.
    """
    
    def __init__(self):
        """Initialize the STL converter."""
        pass
    
    def step_to_stl(
        self, 
        input_path: str, 
        output_path: str,
        resolution: float = 0.1,
        linear_deflection: float = 0.001,
        angular_deflection: float = 0.5
    ) -> Dict[str, Any]:
        """
        Convert STEP file to STL using CADQuery.
        
        Args:
            input_path: Path to input STEP file
            output_path: Path to output STL file
            resolution: Mesh resolution (smaller = finer)
            linear_deflection: Linear deflection for tessellation
            angular_deflection: Angular deflection in degrees
            
        Returns:
            Dictionary with conversion results
        """
        try:
            import cadquery as cq
            
            # Import STEP file
            result = cq.importers.importStep(input_path)
            
            # Export to STL
            cq.exporters.export(
                result,
                output_path,
                tolerance=linear_deflection,
                angularTolerance=angular_deflection
            )
            
            # Analyze the output
            stats = self.analyze_mesh(output_path)
            
            return {
                'success': True,
                'input': input_path,
                'output': output_path,
                'mesh_stats': stats
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"{type(e).__name__}: {str(e)}"
            }
    
    def analyze_mesh(self, stl_path: str) -> Dict[str, Any]:
        """
        Analyze STL mesh and return statistics.
        
        Args:
            stl_path: Path to STL file
            
        Returns:
            Dictionary with mesh statistics
        """
        try:
            from stl import mesh as stl_mesh
            
            # Load STL file
            mesh = stl_mesh.Mesh.from_file(stl_path)
            
            # Calculate statistics
            stats = {
                'num_triangles': len(mesh.vectors),
                'volume': self._calculate_volume(mesh),
                'surface_area': self._calculate_surface_area(mesh),
                'bounding_box': self._get_bounding_box(mesh),
                'is_closed': self._check_if_closed(mesh),
                'file_size': os.path.getsize(stl_path)
            }
            
            # Check mesh quality
            stats['quality'] = self._assess_quality(mesh)
            
            return stats
            
        except Exception as e:
            return {
                'error': f"{type(e).__name__}: {str(e)}"
            }
    
    def _calculate_volume(self, mesh) -> float:
        """Calculate mesh volume using numpy-stl."""
        try:
            volume, cog, inertia = mesh.get_mass_properties()
            return float(volume)
        except:
            return 0.0
    
    def _calculate_surface_area(self, mesh) -> float:
        """Calculate total surface area."""
        try:
            areas = mesh.areas
            return float(np.sum(areas))
        except:
            return 0.0
    
    def _get_bounding_box(self, mesh) -> Dict[str, Any]:
        """Get bounding box dimensions."""
        try:
            minx = miny = minz = float('inf')
            maxx = maxy = maxz = float('-inf')
            
            for point in mesh.points:
                minx = min(minx, point[0])
                miny = min(miny, point[1])
                minz = min(minz, point[2])
                maxx = max(maxx, point[0])
                maxy = max(maxy, point[1])
                maxz = max(maxz, point[2])
            
            return {
                'min': [float(minx), float(miny), float(minz)],
                'max': [float(maxx), float(maxy), float(maxz)],
                'dimensions': [
                    float(maxx - minx),
                    float(maxy - miny),
                    float(maxz - minz)
                ],
                'center': [
                    float((maxx + minx) / 2),
                    float((maxy + miny) / 2),
                    float((maxz + minz) / 2)
                ]
            }
        except:
            return {}
    
    def _check_if_closed(self, mesh) -> bool:
        """Check if mesh is watertight (closed)."""
        try:
            # A mesh is closed if every edge is shared by exactly 2 triangles
            # This is a simplified check
            return mesh.is_closed()
        except:
            return False
    
    def _assess_quality(self, mesh) -> Dict[str, Any]:
        """Assess mesh quality."""
        quality = {
            'has_degenerate_triangles': False,
            'min_edge_length': float('inf'),
            'max_edge_length': float('-inf'),
            'avg_edge_length': 0.0
        }
        
        try:
            edge_lengths = []
            
            for triangle in mesh.vectors:
                # Calculate edge lengths
                e1 = np.linalg.norm(triangle[1] - triangle[0])
                e2 = np.linalg.norm(triangle[2] - triangle[1])
                e3 = np.linalg.norm(triangle[0] - triangle[2])
                
                edge_lengths.extend([e1, e2, e3])
                
                # Check for degenerate triangles (very small area)
                if min(e1, e2, e3) < 1e-6:
                    quality['has_degenerate_triangles'] = True
            
            if edge_lengths:
                quality['min_edge_length'] = float(np.min(edge_lengths))
                quality['max_edge_length'] = float(np.max(edge_lengths))
                quality['avg_edge_length'] = float(np.mean(edge_lengths))
                quality['aspect_ratio'] = quality['max_edge_length'] / quality['min_edge_length']
        
        except Exception as e:
            quality['error'] = str(e)
        
        return quality
    
    def repair_mesh(self, input_path: str, output_path: str) -> Dict[str, Any]:
        """
        Attempt to repair common mesh issues.
        
        Args:
            input_path: Path to input STL file
            output_path: Path to output repaired STL file
            
        Returns:
            Dictionary with repair results
        """
        try:
            import trimesh
            
            # Load mesh with trimesh
            mesh = trimesh.load(input_path)
            
            # Perform repairs
            trimesh.repair.fix_normals(mesh)
            trimesh.repair.fill_holes(mesh)
            
            # Export repaired mesh
            mesh.export(output_path)
            
            # Analyze repaired mesh
            stats = self.analyze_mesh(output_path)
            
            return {
                'success': True,
                'input': input_path,
                'output': output_path,
                'repairs_applied': ['fix_normals', 'fill_holes'],
                'mesh_stats': stats
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"{type(e).__name__}: {str(e)}"
            }
    
    def scale_mesh(
        self, 
        input_path: str, 
        output_path: str,
        scale_factor: float = 1.0
    ) -> Dict[str, Any]:
        """
        Scale mesh by a factor.
        
        Args:
            input_path: Path to input STL file
            output_path: Path to output STL file
            scale_factor: Scaling factor (1.0 = no change)
            
        Returns:
            Dictionary with scaling results
        """
        try:
            from stl import mesh as stl_mesh
            
            # Load mesh
            mesh = stl_mesh.Mesh.from_file(input_path)
            
            # Scale all vertices
            mesh.vectors *= scale_factor
            
            # Save scaled mesh
            mesh.save(output_path)
            
            return {
                'success': True,
                'input': input_path,
                'output': output_path,
                'scale_factor': scale_factor
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"{type(e).__name__}: {str(e)}"
            }


def main():
    """Command-line interface for STL converter."""
    parser = argparse.ArgumentParser(description='STL Converter - Mesh processing utilities')
    parser.add_argument('command', choices=['analyze', 'convert', 'repair', 'scale'],
                       help='Command to execute')
    parser.add_argument('--input', required=True, help='Input file path')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--scale', type=float, default=1.0, help='Scale factor for scaling')
    parser.add_argument('--resolution', type=float, default=0.1, help='Resolution for conversion')
    
    args = parser.parse_args()
    
    converter = STLConverter()
    result = {}
    
    if args.command == 'analyze':
        result = converter.analyze_mesh(args.input)
    
    elif args.command == 'convert':
        if not args.output:
            print(json.dumps({'success': False, 'error': 'Output file required for conversion'}))
            sys.exit(1)
        result = converter.step_to_stl(args.input, args.output, resolution=args.resolution)
    
    elif args.command == 'repair':
        if not args.output:
            print(json.dumps({'success': False, 'error': 'Output file required for repair'}))
            sys.exit(1)
        result = converter.repair_mesh(args.input, args.output)
    
    elif args.command == 'scale':
        if not args.output:
            print(json.dumps({'success': False, 'error': 'Output file required for scaling'}))
            sys.exit(1)
        result = converter.scale_mesh(args.input, args.output, scale_factor=args.scale)
    
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
