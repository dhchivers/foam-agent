# Cavity Flow Template

This is a classic OpenFOAM test case - the lid-driven cavity flow.

## Description

A square cavity with three fixed walls and one moving wall (lid) at the top. The moving wall drives the flow inside the cavity, creating a characteristic vortex pattern.

## Case Setup

- **Solver**: icoFoam (incompressible, laminar)
- **Geometry**: 0.1m x 0.1m square cavity
- **Mesh**: 20x20 cells (can be refined)
- **Moving wall velocity**: 1 m/s

## Files Included

- `blockMeshDict` - Mesh definition
- `controlDict` - Simulation control
- `fvSchemes` - Numerical schemes
- `fvSolution` - Equation solvers

## Usage

1. Create new case in FoamAgent
2. Copy these files to the appropriate directories
3. Run blockMesh
4. Run icoFoam solver
5. Visualize results

## Expected Results

The flow develops a primary vortex in the center of the cavity with secondary vortices in the corners at higher Reynolds numbers.
