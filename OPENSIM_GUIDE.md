# OpenSim Integration Guide

## Overview

OpenSim is an open-source software system for biomechanical modeling, simulation, and analysis. It enables the study of musculoskeletal dynamics, movement simulation, and biomechanical performance analysis. In FoamAgent, OpenSim is integrated to provide biomechanical and musculoskeletal simulation capabilities alongside CFD, rigid body dynamics, particle physics, and electromagnetics.

**Key Capabilities:**
- Musculoskeletal modeling (bones, muscles, ligaments, tendons)
- Forward dynamics simulation
- Inverse kinematics and dynamics
- Static optimization and computed muscle control
- Motion tracking and analysis
- Custom model building and modification

**Version:** OpenSim-Core 4.5.1

## Quick Start

### Verify OpenSim Installation

```bash
# Access the container shell
./scripts/shell.sh

# Check OpenSim version
opensim-cmd --version

# Verify libraries are loaded
ldd /opt/opensim/bin/opensim-cmd | grep -i opensim

# Check environment
echo $OPENSIM_HOME
```

### Basic Workflow

1. **Create/Load a Model** - Define musculoskeletal geometry
2. **Configure Simulation** - Set initial conditions and parameters
3. **Run Analysis** - Execute kinematics, dynamics, or optimization
4. **Visualize Results** - Examine motion and forces
5. **Export Data** - Save results for further analysis

## Architecture

### Directory Structure

```
/opt/opensim/
├── bin/              # OpenSim executables
├── lib/              # Shared libraries
├── include/          # Header files
└── sdk/              # Development resources

~/opensim-workspace/  # Recommended working directory
├── models/           # .osim model files
├── motions/          # .mot motion files
├── results/          # Simulation output
└── scripts/          # Analysis scripts
```

### Core Components

- **SimBody**: Multibody dynamics engine (automatically built with OpenSim)
- **OpenSim Core**: Musculoskeletal modeling and simulation
- **Model Files (.osim)**: XML-based model definitions
- **Motion Files (.mot)**: Trajectory and kinematic data
- **Storage Files (.sto)**: Time-series results

## Creating Your First Simulation

### Example 1: Arm Reaching Motion

```bash
# Create workspace
mkdir -p ~/opensim-workspace/arm-example
cd ~/opensim-workspace/arm-example

# Create a simple arm model script (Python-like syntax for illustration)
cat > arm_model.py << 'EOF'
import opensim as osim

# Load example arm model
model = osim.Model("/opt/opensim/Resources/Models/Arm26/arm26.osim")

# Set initial state
state = model.initSystem()

# Configure forward dynamics
manager = osim.Manager(model)
manager.setIntegratorAccuracy(1.0e-5)

# Run simulation
state.setTime(0.0)
manager.initialize(state)
state = manager.integrate(2.0)  # 2 seconds

# Save results
print("Simulation complete!")
EOF

# Note: Python bindings disabled in this build
# Use XML-based workflow instead
```

### Example 2: Gait Analysis (XML-Based)

```xml
<!-- gait_setup.xml -->
<OpenSimDocument Version="30000">
    <AnalyzeTool name="GaitAnalysis">
        <model_file>gait2392_simbody.osim</model_file>
        <initial_time>0.0</initial_time>
        <final_time>1.0</final_time>
        
        <AnalysisSet>
            <objects>
                <Kinematics name="kinematics">
                    <in_degrees>true</in_degrees>
                </Kinematics>
                <Actuation name="actuation">
                    <step_interval>1</step_interval>
                </Actuation>
            </objects>
        </AnalysisSet>
    </AnalyzeTool>
</OpenSimDocument>
```

```bash
# Run gait analysis
opensim-cmd run-tool gait_setup.xml
```

### Example 3: Inverse Kinematics

```bash
# Create IK setup
cat > ik_setup.xml << 'EOF'
<OpenSimDocument Version="30000">
    <InverseKinematicsTool name="IK_Tool">
        <model_file>subject_model.osim</model_file>
        <time_range>0 2</time_range>
        <marker_file>experimental_markers.trc</marker_file>
        <output_motion_file>results/ik_motion.mot</output_motion_file>
        <accuracy>1.0e-5</accuracy>
    </InverseKinematicsTool>
</OpenSimDocument>
EOF

# Run inverse kinematics
opensim-cmd run-tool ik_setup.xml
```

## Model Development

### Loading Example Models

```bash
# OpenSim ships with example models
ls /opt/opensim/Resources/Models/

# Common examples:
# - Arm26: 2D arm with 6 muscles
# - Gait2392: Full-body gait model
# - Leg39: Lower extremity with 39 muscles
```

### Creating Custom Models

```xml
<!-- simple_pendulum.osim -->
<OpenSimDocument Version="30000">
    <Model name="SimplePendulum">
        <BodySet>
            <objects>
                <Body name="rod">
                    <mass>1.0</mass>
                    <mass_center>0 -0.5 0</mass_center>
                    <inertia>0.084 0.084 0.001 0 0 0</inertia>
                </Body>
            </objects>
        </BodySet>
        
        <JointSet>
            <objects>
                <PinJoint name="pin">
                    <parent_body>ground</parent_body>
                    <child_body>rod</child_body>
                    <location_in_parent>0 0 0</location_in_parent>
                    <location_in_child>0 0.5 0</location_in_child>
                </PinJoint>
            </objects>
        </JointSet>
    </Model>
</OpenSimDocument>
```

## Analysis Tools

### 1. Forward Dynamics

Simulate muscle-driven movement:

```xml
<ForwardTool name="forward">
    <model_file>model.osim</model_file>
    <initial_time>0</initial_time>
    <final_time>1.0</final_time>
    <controls_file>muscle_controls.xml</controls_file>
    <results_directory>./forward_results</results_directory>
</ForwardTool>
```

### 2. Static Optimization

Calculate muscle forces for known motion:

```xml
<StaticOptimization name="static_opt">
    <model_file>model.osim</model_file>
    <coordinates_file>motion.mot</coordinates_file>
    <force_set_files>actuators.xml</force_set_files>
</StaticOptimization>
```

### 3. Computed Muscle Control (CMC)

Track experimental motion:

```xml
<CMCTool name="cmc">
    <model_file>model.osim</model_file>
    <desired_kinematics_file>experimental_motion.mot</desired_kinematics_file>
    <time_range>0 1.5</time_range>
    <target_dt>0.01</target_dt>
</CMCTool>
```

### 4. Muscle Analysis

```xml
<MuscleAnalysis name="muscle_analysis">
    <model_file>model.osim</model_file>
    <coordinates_file>motion.mot</coordinates_file>
    <compute_moments>true</compute_moments>
</MuscleAnalysis>
```

## Coupling with Other Physics Engines

### OpenSim + OpenFOAM: Biofluid Dynamics

Model blood flow through vessels with musculoskeletal constraints:

```bash
# 1. Run OpenSim to compute vessel deformation
opensim-cmd run-tool vessel_motion.xml

# 2. Extract wall positions
opensim-cmd analyze -model vessel.osim -motion results/vessel_motion.mot

# 3. Apply to OpenFOAM mesh as moving boundary
# (Custom script to convert .mot to OpenFOAM pointDisplacement)

# 4. Run CFD with moving mesh
blockMesh
moveDynamicMesh -checkAMI
pimpleFoam
```

### OpenSim + Newton Dynamics: Human-Object Interaction

Combine musculoskeletal control with external rigid bodies:

```python
# Conceptual coupling workflow:
# 1. OpenSim computes muscle forces and joint torques
# 2. Export contact forces at hands/feet
# 3. Import into Newton Dynamics as applied forces
# 4. Newton simulates object dynamics
# 5. Feed back object reaction forces to OpenSim
```

### OpenSim + Geant4: Medical Physics

Model radiation dose to anatomically accurate geometry:

```bash
# 1. Export OpenSim bone geometry
opensim-cmd export-geometry model.osim bones.obj

# 2. Convert to GDML for Geant4
mesh2gdml bones.obj bones.gdml

# 3. Run radiation transport simulation
# (Geant4 macro with GDML geometry)
```

## Visualization

### OpenSim GUI (Not Available in This Build)

This container build focuses on command-line tools. For GUI visualization:

1. Export results from container
2. Open in local OpenSim GUI application
3. Or use ParaView for basic geometry visualization

### ParaView Integration

```bash
# Export OpenSim geometry to VTK format
opensim-cmd export-vtk model.osim model.vtk

# Open in ParaView
paraview model.vtk
```

### Motion Playback

```bash
# Generate motion frames
opensim-cmd analyze \
    -model model.osim \
    -motion results/motion.mot \
    -output frames/ \
    -frame-interval 0.01

# Create animation (requires ffmpeg)
apt-get install ffmpeg
ffmpeg -framerate 30 -i frames/frame_%04d.png -c:v libx264 motion.mp4
```

## Performance Optimization

### Simulation Speed

```xml
<!-- Reduce accuracy for faster simulation -->
<integrator_accuracy>1.0e-3</integrator_accuracy>  <!-- Default: 1.0e-5 -->

<!-- Use smaller time steps -->
<time_step>0.01</time_step>

<!-- Disable unnecessary analyses -->
<analyze_forces>false</analyze_forces>
```

### Parallel Processing

OpenSim simulations are typically sequential, but you can parallelize:

```bash
# Run multiple parameter variations in parallel
for param in 0.5 1.0 1.5 2.0; do
    (
        sed "s/PARAM_VALUE/$param/" template.xml > config_$param.xml
        opensim-cmd run-tool config_$param.xml
    ) &
done
wait
```

### Memory Management

```bash
# Monitor memory usage
free -h

# For large models, increase available memory:
# Adjust Docker resources in Docker Desktop settings
# Recommended: 8GB+ RAM for complex musculoskeletal models
```

## Common Workflows

### Workflow 1: Motion Capture Analysis

```bash
# 1. Load experimental marker data (.trc)
# 2. Scale generic model to subject
opensim-cmd run-tool scale_setup.xml

# 3. Inverse kinematics
opensim-cmd run-tool ik_setup.xml

# 4. Inverse dynamics
opensim-cmd run-tool id_setup.xml

# 5. Static optimization or CMC
opensim-cmd run-tool so_setup.xml

# 6. Analyze results
opensim-cmd analyze -model scaled_model.osim -motion ik_results.mot
```

### Workflow 2: Parameter Study

```bash
#!/bin/bash
# Study effect of muscle strength on jump height

for strength in 0.8 1.0 1.2 1.4; do
    mkdir -p results/strength_$strength
    
    # Modify model
    sed "s/<max_isometric_force>1000/<max_isometric_force>$((1000*strength))/" \
        base_model.osim > model_$strength.osim
    
    # Run forward simulation
    sed "s/MODEL_FILE/model_$strength.osim/" \
        forward_template.xml > forward_$strength.xml
    opensim-cmd run-tool forward_$strength.xml
    
    # Extract jump height
    python3 analyze_jump.py results/strength_$strength/states.sto
done
```

### Workflow 3: Custom Muscle Model

```xml
<!-- Define custom muscle properties -->
<Thelen2003Muscle name="custom_muscle">
    <max_isometric_force>1000.0</max_isometric_force>
    <optimal_fiber_length>0.087</optimal_fiber_length>
    <tendon_slack_length>0.266</tendon_slack_length>
    <pennation_angle>0.0</pennation_angle>
    <activation_time_constant>0.010</activation_time_constant>
    <deactivation_time_constant>0.040</deactivation_time_constant>
</Thelen2003Muscle>
```

## Troubleshooting

### Issue: "Model failed to initialize"

**Solution:**
```bash
# Check model file syntax
opensim-cmd -validate model.osim

# Verify all referenced files exist
grep -o 'file>.*</.*file' model.osim

# Check coordinate ranges
# Ensure initial pose is within joint limits
```

### Issue: "Simulation diverged"

**Causes:**
- Too large time step
- Excessive muscle activation
- Joint limit violations
- Numerical instability

**Solutions:**
```xml
<!-- Reduce time step -->
<time_step>0.001</time_step>

<!-- Increase accuracy -->
<integrator_accuracy>1.0e-6</integrator_accuracy>

<!-- Enable constraint enforcement -->
<enforce_constraints>true</enforce_constraints>
```

### Issue: "Library not found"

```bash
# Check LD_LIBRARY_PATH
echo $LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/opt/opensim/lib:$LD_LIBRARY_PATH

# Verify library installation
ls -la /opt/opensim/lib/
ldconfig -p | grep -i opensim
```

### Issue: "Cannot find model file"

```bash
# Use absolute paths
OPENSIM_HOME=/opt/opensim

# Or relative to working directory
cd ~/opensim-workspace
./run_simulation.sh
```

## Data Formats

### .osim (Model Files)

XML format defining:
- Bodies, joints, muscles
- Geometry and visualization
- Forces and constraints

### .mot (Motion Files)

Tab-delimited time-series data:
```
time    hip_flexion_r    knee_angle_r    ankle_angle_r
0.00    10.5            5.2             -15.3
0.01    10.7            5.5             -15.1
...
```

### .sto (Storage Files)

Similar to .mot, stores simulation results:
- States, controls, forces
- Muscle activations
- Joint reactions

### .trc (Marker Trajectories)

Motion capture marker positions:
```
PathFileType    4
DataRate        100
...
```

## Best Practices

### Model Development

1. **Start Simple**: Begin with minimal model, add complexity incrementally
2. **Validate Geometry**: Check mass, inertia, joint ranges
3. **Test Incrementally**: Run static poses before dynamic simulation
4. **Document Changes**: Track model modifications and versions

### Simulation Setup

1. **Appropriate Time Steps**: 0.001-0.01s for most applications
2. **Convergence Testing**: Verify results with finer tolerances
3. **Initial Conditions**: Ensure valid starting pose
4. **Actuator Limits**: Set realistic muscle force bounds

### Analysis

1. **Sanity Checks**: Verify kinematic consistency
2. **Energy Conservation**: Monitor for unrealistic energy changes
3. **Muscle Activation**: Check 0-1 range, physiological patterns
4. **Joint Loads**: Compare to experimental/literature values

### Data Management

1. **Organize Results**: Use consistent directory structure
2. **Version Control**: Track model and setup files with git
3. **Metadata**: Document simulation parameters
4. **Backup**: Save important results outside container

## Resources

### Official Documentation

- OpenSim Documentation: https://simtk-confluence.stanford.edu/display/OpenSim/Documentation
- API Reference: https://simtk.org/api_docs/opensim/api_docs/
- User Forum: https://simtk.org/forums/viewforum.php?f=91

### Example Models

- SimTK Model Repository: https://simtk.org/projects/opensim
- OpenSim Examples: https://github.com/opensim-org/opensim-models

### Tutorials

- OpenSim Tutorials: https://simtk-confluence.stanford.edu/display/OpenSim/Tutorials
- Best Practices Guide: https://simtk-confluence.stanford.edu/display/OpenSim/Best+Practices

### Scientific Publications

- Delp et al. (2007): OpenSim software overview
- Seth et al. (2018): OpenSim 4.0 release
- Rajagopal et al. (2016): Full-body musculoskeletal model

### Community

- GitHub Issues: https://github.com/opensim-org/opensim-core/issues
- Mailing List: opensim-users@simtk.org
- SimTK Forums: https://simtk.org/forums/

## Next Steps

1. **Explore Examples**: Run tutorial models to understand workflow
2. **Create Custom Model**: Build model specific to your research question
3. **Integrate with CFD**: Couple with OpenFOAM for biofluid applications
4. **Couple Physics**: Combine with Newton/Geant4 for multi-physics scenarios
5. **Optimize Performance**: Profile and accelerate your simulations
6. **Contribute**: Share models and improvements with community

## See Also

- [MULTIPHYSICS.md](MULTIPHYSICS.md) - Multi-physics coupling strategies
- [README.md](README.md) - FoamAgent overview
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - General troubleshooting guide
