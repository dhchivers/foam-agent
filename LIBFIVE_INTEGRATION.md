# libfive Integration - Phase 1 Extension

**Date:** March 30, 2026  
**Status:** ✅ Complete  
**Commit:** `8bb8061`

---

## Overview

Extended Phase 1 to add **libfive** support, providing functional representation (F-Rep) parametric modeling as a complement to CADQuery's boundary representation (B-Rep) approach.

## What is libfive?

libfive is a framework for solid modeling using **functional representations (F-Rep)**, where objects are defined as mathematical functions `f(x,y,z)` that return signed distances. This is fundamentally different from boundary representation used by CADQuery.

**Key Differences:**

| Feature | CADQuery (B-Rep) | libfive (F-Rep) |
|---------|------------------|-----------------|
| Representation | Edges, faces, vertices | Mathematical functions |
| File Format | STEP, IGES, STL | STL only (mesh from function) |
| Operations | Sketch-extrude workflow | Signed distance functions |
| Best For | Mechanical parts, assemblies | Organic shapes, mathematical forms |
| Precision | Exact geometry | Resolution-dependent mesh |

## Implementation Details

### 1. Dockerfile Changes

**Build libfive from Source:**

```dockerfile
# Build and install libfive from source for F-Rep solid modeling
RUN cd /opt && \
    git clone https://github.com/libfive/libfive.git && \
    cd libfive && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr/local \
          -DCMAKE_BUILD_TYPE=Release \
          .. && \
    make -j$(nproc) && \
    make install && \
    ldconfig && \
    cd /opt && \
    rm -rf libfive
```

**Dependencies Added:**
- `libeigen3-dev` - Linear algebra library
- `libpng-dev` - Image export support
- `libboost-all-dev` - Boost libraries for C++

**Environment Variables:**
```dockerfile
ENV LIBFIVE_INSTALL=/usr/local
ENV PATH=${LIBFIVE_INSTALL}/bin:${PATH}
ENV LD_LIBRARY_PATH=${LIBFIVE_INSTALL}/lib:${LD_LIBRARY_PATH}
ENV PYTHONPATH=${LIBFIVE_INSTALL}/lib/python3/dist-packages:${PYTHONPATH}
```

**Build Time:** Adds approximately 5-10 minutes to container build (depending on CPU cores)

### 2. Python libfive Bridge (`python/libfive_bridge.py`) - 353 Lines

#### Features:

1. **Script Execution**
   - Execute libfive Python scripts
   - Import common functions from `libfive.stdlib`
   - Parameter injection support
   - Comprehensive error handling

2. **STL Export**
   - Mesh generation from F-Rep functions
   - Configurable bounds and resolution
   - Mesh quality analysis via STLConverter integration

3. **Orthographic Images**
   - Export 2D projections (XY, XZ, YZ views)
   - PNG format for preview

4. **Bounds Management**
   - Manual bounds specification
   - Auto-detection heuristics
   - Default bounds fallback

#### Usage Example:

```python
from libfive_bridge import LibfiveBridge

# Initialize bridge
bridge = LibfiveBridge(work_dir="/work")

# Define libfive script
script = '''
from libfive.stdlib import *

# Create a sphere
s = sphere(10, [0, 0, 0])

# Create a box
b = box([-5, -5, -5], [5, 5, 5])

# Union them
result = union(s, b)
'''

# Execute script
result = bridge.execute_script(script)

# Export to STL with bounds
bridge.export_stl(
    result['result'],
    "/work/output.stl",
    bounds=((-15, 15), (-15, 15), (-15, 15)),
    resolution=20.0  # voxels per unit
)
```

#### Command-Line Interface:

```bash
python3 /app/python/libfive_bridge.py \
  --script-file my_shape.py \
  --stl-output output.stl \
  --bounds "[[-10,10],[-10,10],[-10,10]]" \
  --resolution 15
```

### 3. AI Prompt Extensions (`python/ai_prompts.py`)

#### New System Prompt:

```python
LIBFIVE_SYSTEM_PROMPT = """You are an expert in functional representation (F-Rep) 
3D modeling using libfive. Generate valid libfive Python code from natural language 
descriptions.

Key requirements:
1. Always assign the final geometry to a variable named 'result' or 'shape'
2. Import necessary functions from libfive.stdlib
3. Use signed distance functions and CSG operations
4. Objects are defined as mathematical functions f(x,y,z)
5. Common operations: sphere, box, cylinder, union, intersection, difference
"""
```

#### Five New Examples:

1. **Basic Sphere**
   ```python
   from libfive.stdlib import *
   result = sphere(5, [0, 0, 0])
   ```

2. **Box**
   ```python
   from libfive.stdlib import *
   result = box([-5, -5, -5], [5, 5, 5])
   ```

3. **Cylinder**
   ```python
   from libfive.stdlib import *
   cyl = cylinder(5, -10, 10)
   result = cyl
   ```

4. **Union Operation**
   ```python
   from libfive.stdlib import *
   s = sphere(5, [0, 0, 0])
   b = box([-3, -3, -3], [3, 3, 3])
   result = union(s, b)
   ```

5. **Boolean Difference**
   ```python
   from libfive.stdlib import *
   s = sphere(10, [0, 0, 0])
   c = cylinder(3, -15, 15)
   result = difference(s, c)
   ```

#### New Methods:

- `build_libfive_prompt()` - Generate prompts for libfive code
- `generate_libfive_template()` - Templates for common shapes

### 4. Updated Files

| File | Changes | Lines Added |
|------|---------|-------------|
| `Dockerfile` | Added libfive build, dependencies, env vars | +28 |
| `python/libfive_bridge.py` | New module | +353 |
| `python/ai_prompts.py` | libfive prompts and templates | +165 |
| `python/__init__.py` | Export LibfiveBridge | +3 |
| `python/README.md` | libfive documentation | +40 |
| **Total** | | **+589** |

## Testing Guide

### 1. Build Container

```bash
./scripts/build.sh
```

**Expected build time:** 15-30 minutes (includes libfive compilation)

### 2. Verify libfive Installation

```bash
# Start container
./scripts/run.sh

# In container terminal (via web browser at localhost:6080)
python3 -c "import libfive; print('libfive version:', libfive.__version__)"
python3 -c "from libfive.stdlib import *; print('stdlib imported successfully')"
```

### 3. Test Simple Shape

```bash
# Create a test script
cat > /work/test_libfive.py << 'EOF'
from libfive.stdlib import *

# Create a sphere
result = sphere(10, [0, 0, 0])
EOF

# Execute and export
python3 /app/python/libfive_bridge.py \
  --script-file /work/test_libfive.py \
  --stl-output /work/test_libfive.stl \
  --bounds "[[-15,15],[-15,15],[-15,15]]" \
  --resolution 15

# Verify the file exists
ls -lh /work/test_libfive.stl
```

### 4. Test Complex Shape

```bash
# Create union of sphere and box
cat > /work/test_union.py << 'EOF'
from libfive.stdlib import *

s = sphere(8, [0, 0, 0])
b = box([-5, -5, -5], [5, 5, 10])
result = union(s, b)
EOF

python3 /app/python/libfive_bridge.py \
  --script-file /work/test_union.py \
  --stl-output /work/union.stl \
  --resolution 20
```

### 5. Test Mesh Quality

```bash
# Analyze generated mesh
python3 /app/python/stl_converter.py analyze --input /work/test_libfive.stl
```

**Expected output:**
```json
{
  "num_triangles": 1280,
  "volume": 4188.79,
  "surface_area": 1256.64,
  "is_closed": true,
  "quality": {
    "min_edge_length": 0.5,
    "max_edge_length": 2.1,
    "avg_edge_length": 1.2
  }
}
```

## Use Cases

### When to Use libfive vs CADQuery

**Use libfive for:**
- Mathematical surfaces and implicit functions
- Organic/sculptural shapes
- Procedurally generated geometry
- Shapes defined by equations
- Smooth blending operations
- Lattice structures

**Use CADQuery for:**
- Mechanical parts with precise dimensions
- Parts requiring STEP export for CAM
- Assembly modeling
- Engineering drawings
- Parametric mechanical designs
- Sheet metal parts

## Known Limitations

1. **No STEP Export:** libfive uses F-Rep, not boundary representation
   - Can only export STL meshes
   - Resolution affects file size and accuracy

2. **Bounds Required:** Must specify bounding box for mesh generation
   - Automatic bounds detection is basic
   - User must know approximate object size

3. **Python Only:** No Guile bindings in this container
   - Studio GUI not built (we have our own Qt GUI)
   - Python is sufficient for our use case

4. **Memory Usage:** High resolution meshes can be large
   - `resolution=10` → moderate detail
   - `resolution=20` → high detail, larger files
   - `resolution=50` → very high detail, memory intensive

## Integration with Workflow

libfive will be integrated into the Qt GUI in future phases:

**Phase 2 (Planned):**
- CADWidget will support both CADQuery and libfive modes
- Mode selector: "Boundary Rep (CADQuery)" vs "Functional Rep (libfive)"
- AI agent will detect which mode based on user input

**Phase 3 (Planned):**
- 3D viewer will render both STEP (from CADQuery) and STL (from libfive)
- Side-by-side comparison of approaches

**Example Workflow:**
```
User: "Create a sphere-box union"
  ↓
AI detects: Simple CSG → suggests libfive
  ↓
Generate libfive code
  ↓
Execute → STL mesh
  ↓
Visualize in Qt viewer
  ↓
Export STL to OpenFOAM
```

## Performance Notes

**Build Impact:**
- Container build time: +8-12 minutes
- Final image size: +~150MB

**Runtime:**
- libfive mesh generation: Fast (< 1 second for simple shapes at low resolution)
- High resolution (50+): Can take several seconds
- Memory: ~10-100MB per shape depending on complexity

## Future Enhancements

1. **Bounds Auto-Detection:** Improve heuristics by sampling the function
2. **Adaptive Resolution:** Variable resolution based on curvature
3. **GPU Rendering:** Integrate libfive's GPU renderer for real-time preview
4. **Hybrid Modeling:** Combine CADQuery and libfive in single workflow
5. **Custom Operators:** Add user-defined signed distance functions

## Resources

- **libfive GitHub:** https://github.com/libfive/libfive
- **libfive Examples:** https://libfive.com/examples
- **F-Rep Tutorial:** https://en.wikipedia.org/wiki/Function_representation
- **SDF User Group:** https://sdfug.discourse.group/

---

## Commit Information

```
commit 8bb8061
Author: FoamAgent Development Team
Date: March 30, 2026

Add libfive support for F-Rep parametric modeling

- Updated Dockerfile to build libfive from source
- Created libfive_bridge.py Python utility (353 lines)
- Added libfive prompts and templates to ai_prompts.py
- Updated Python package exports and documentation
```

---

**libfive Integration Complete ✅**

Ready for Phase 2 implementation with dual CAD engine support!
