---
id: urdf-to-sim
title: URDF to Simulation
sidebar_position: 4
---

# URDF to Simulation

Converting URDF (Unified Robot Description Format) models to simulation environments is a critical step in humanoid robot development. This chapter covers the process of transforming URDF descriptions into functional simulation models for Gazebo, Isaac Sim, and other simulation platforms.

## URDF to Simulation Workflow

### Conversion Process Overview

The process of converting URDF to simulation involves several key steps:

1. **URDF Validation**: Verify the URDF is valid and complete
2. **Xacro Processing**: Expand macros and include files
3. **Collision Geometry**: Optimize for simulation performance
4. **Inertial Properties**: Validate for physical accuracy
5. **Sensor Integration**: Add simulation-specific sensor definitions
6. **Plugin Configuration**: Add simulation plugins and controllers

### Basic Conversion Command

```bash
# Convert URDF to simulation-ready format
xacro input.urdf.xacro > output.urdf

# Validate URDF
check_urdf output.urdf

# Visualize the robot
urdf_to_graphiz output.urdf
```

## Gazebo Integration

### Gazebo-Specific Tags

Adding Gazebo-specific elements to URDF:

```xml
<?xml version="1.0"?>
<robot name="h1" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Include the base URDF -->
  <xacro:include filename="$(find h1_description)/urdf/h1.urdf.xacro" />

  <!-- Gazebo plugins -->
  <gazebo>
    <plugin name="gazebo_ros_control" filename="libgazebo_ros_control.so">
      <robotNamespace>/h1</robotNamespace>
      <robotSimType>gazebo_ros_control/DefaultRobotHWSim</robotSimType>
    </plugin>
  </gazebo>

  <!-- Gazebo materials -->
  <gazebo reference="h1_torso_link">
    <material>Gazebo/White</material>
    <mu1>0.8</mu1>
    <mu2>0.8</mu2>
    <kp>1000000.0</kp>
    <kd>100.0</kd>
    <min_depth>0.001</min_depth>
    <max_vel>1.0</max_vel>
  </gazebo>

  <!-- Sensor integration -->
  <gazebo reference="h1_imu_link">
    <sensor name="h1_imu" type="imu">
      <always_on>true</always_on>
      <update_rate>100</update_rate>
      <imu>
        <angular_velocity>
          <x>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>2e-4</stddev>
            </noise>
          </x>
          <y>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>2e-4</stddev>
            </noise>
          </y>
          <z>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>2e-4</stddev>
            </noise>
          </z>
        </angular_velocity>
      </imu>
    </sensor>
  </gazebo>

</robot>
```

### Collision Mesh Optimization

For simulation performance, optimize collision meshes:

```xml
<!-- Use simplified collision geometry for simulation -->
<gazebo reference="h1_upper_arm_link">
  <collision>
    <surface>
      <contact>
        <ode>
          <kp>10000000</kp>
          <kd>1000</kd>
          <max_vel>100.0</max_vel>
          <min_depth>0.001</min_depth>
        </ode>
      </contact>
      <friction>
        <ode>
          <mu>0.8</mu>
          <mu2>0.8</mu2>
        </ode>
      </friction>
    </surface>
  </collision>
</gazebo>

<!-- Use detailed visual geometry -->
<link name="h1_upper_arm_link">
  <visual>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <mesh filename="package://h1_description/meshes/upper_arm.dae"/>
    </geometry>
    <material name="gray">
      <color rgba="0.5 0.5 0.5 1.0"/>
    </material>
  </visual>
  <collision>
    <!-- Simplified collision geometry for better performance -->
    <geometry>
      <mesh filename="package://h1_description/meshes/upper_arm_collision.dae"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="2.5"/>
    <origin xyz="0.01 0 0.05"/>
    <inertia ixx="0.005" ixy="0" ixz="0.001" iyy="0.006" iyz="0" izz="0.003"/>
  </inertial>
</link>
```

## Isaac Sim Integration

### USD Conversion

Converting URDF to USD for Isaac Sim:

```python
# Using Omniverse's URDF Importer
import omni
from omni.isaac.urdf_importer import _urdf_importer

def import_urdf_to_isaac(urdf_path, usd_path):
    """Import URDF to Isaac Sim as USD"""
    urdf_interface = _urdf_importer.acquire_urdf_interface()

    # Import the URDF
    imported_robot = urdf_interface.parse_urdf(urdf_path)

    # Convert to USD
    urdf_interface.import_robot(
        urdf_path,
        usd_path,
        imported_robot,
        up_axis="Z",
        merge_fixed_joints=False
    )

    return usd_path
```

### Isaac Sim Specific Configuration

```python
# Isaac Sim robot configuration
import omni
from pxr import Gf, UsdGeom, PhysxSchema

def configure_isaac_robot(usd_path, robot_name):
    """Configure robot for Isaac Sim physics"""
    stage = omni.usd.get_context().get_stage()

    # Get robot prim
    robot_prim = stage.GetPrimAtPath(f"/World/{robot_name}")

    # Configure articulation root
    articulation_root = PhysxSchema.PhysxArticulationRootAPI.Apply(robot_prim)
    articulation_root.GetSolverPositionIterationCountAttr().Set(8)
    articulation_root.GetSolverVelocityIterationCountAttr().Set(8)

    # Configure drive properties for each joint
    for prim in robot_prim.GetAllChildren():
        if prim.GetTypeName() == "PhysicsJoint":
            joint_api = PhysxSchema.PhysxJointAPI(prim)
            # Configure joint limits, stiffness, damping
            configure_joint_properties(joint_api)

def configure_joint_properties(joint_api):
    """Configure joint properties for humanoid simulation"""
    # Set joint drive parameters
    joint_api.GetStiffnessAttr().Set(1000.0)
    joint_api.GetDampingAttr().Set(100.0)
    joint_api.GetMaxJointVelocityAttr().Set(10.0)
```

> [!hardware]
> **Hardware Note**: When converting the Unitree H1 URDF to Isaac Sim, special attention must be paid to the joint drive parameters to match the physical robot's actuator characteristics. The stiffness and damping values should reflect the real robot's compliance control capabilities.

## Mesh Processing for Simulation

### Collision Mesh Generation

Creating optimized collision meshes:

```python
import numpy as np
from scipy.spatial import ConvexHull
import trimesh

def generate_collision_mesh(visual_mesh_path, output_path, simplification_factor=0.1):
    """Generate simplified collision mesh from visual mesh"""
    # Load the visual mesh
    visual_mesh = trimesh.load(visual_mesh_path)

    # Option 1: Convex hull (fastest, less accurate)
    if simplification_factor < 0.1:
        convex_hull = visual_mesh.convex_hull
        collision_mesh = convex_hull
    # Option 2: Simplified mesh (balanced performance/accuracy)
    else:
        simplified_faces = int(len(visual_mesh.faces) * simplification_factor)
        collision_mesh = visual_mesh.simplify_quadric_decimation(simplified_faces)

    # Save the collision mesh
    collision_mesh.export(output_path)
    return output_path

def create_primitive_collision(link_name, link_geometry):
    """Create primitive collision geometry for simple shapes"""
    if link_geometry['type'] == 'box':
        dimensions = link_geometry['size']
        # Create box collision mesh
        box_mesh = trimesh.creation.box(dimensions)
        return box_mesh
    elif link_geometry['type'] == 'cylinder':
        radius = link_geometry['radius']
        height = link_geometry['length']
        # Create cylinder collision mesh
        cylinder_mesh = trimesh.creation.cylinder(radius, height)
        return cylinder_mesh
    elif link_geometry['type'] == 'sphere':
        radius = link_geometry['radius']
        # Create sphere collision mesh
        sphere_mesh = trimesh.creation.icosphere(subdivisions=2, radius=radius)
        return sphere_mesh
```

### Inertial Property Validation

Validating inertial properties for simulation stability:

```python
def validate_inertial_properties(urdf_path):
    """Validate inertial properties in URDF"""
    import xml.etree.ElementTree as ET

    tree = ET.parse(urdf_path)
    root = tree.getroot()

    errors = []

    for link in root.findall('.//link'):
        inertial = link.find('inertial')
        if inertial is not None:
            mass_elem = inertial.find('mass')
            if mass_elem is not None:
                mass = float(mass_elem.get('value'))
                if mass <= 0:
                    errors.append(f"Link {link.get('name')}: Mass must be positive")

            inertia_elem = inertial.find('inertia')
            if inertia_elem is not None:
                ixx = float(inertia_elem.get('ixx'))
                iyy = float(inertia_elem.get('iyy'))
                izz = float(inertia_elem.get('izz'))

                # Check positive definiteness of inertia matrix
                if ixx <= 0 or iyy <= 0 or izz <= 0:
                    errors.append(f"Link {link.get('name')}: Inertia diagonal elements must be positive")

                # Check triangle inequality for inertia values
                if not (ixx + iyy >= izz and iyy + izz >= ixx and izz + ixx >= iyy):
                    errors.append(f"Link {link.get('name')}: Inertia values violate triangle inequality")

    return errors

def compute_inertial_from_mesh(mesh_path, density=1000):
    """Compute inertial properties from mesh volume"""
    mesh = trimesh.load(mesh_path)

    # Calculate volume and mass
    volume = mesh.volume
    mass = volume * density

    # Calculate inertia tensor
    mesh_mass = trimesh.mass_properties(mesh, density=density)
    inertia_tensor = mesh_mass['inertia']

    return {
        'mass': mass,
        'inertia': inertia_tensor,
        'center_of_mass': mesh_mass['center_mass']
    }
```

## Sensor Integration in Simulation

### Camera Integration

Adding camera sensors to simulation:

```xml
<!-- In URDF with Gazebo tags -->
<link name="h1_camera_optical_frame">
  <inertial>
    <mass value="0.01"/>
    <origin xyz="0 0 0"/>
    <inertia ixx="0.0001" ixy="0" ixz="0" iyy="0.0001" iyz="0" izz="0.0001"/>
  </inertial>
</link>

<joint name="h1_camera_joint" type="fixed">
  <parent link="h1_head"/>
  <child link="h1_camera_optical_frame"/>
  <origin xyz="0.05 0 0.1" rpy="0 0 0"/>
</joint>

<gazebo reference="h1_camera_optical_frame">
  <sensor name="h1_camera" type="camera">
    <update_rate>30</update_rate>
    <camera name="head_camera">
      <horizontal_fov>1.3962634</horizontal_fov> <!-- 80 degrees -->
      <image>
        <width>640</width>
        <height>480</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.1</near>
        <far>100</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
      <frame_name>h1_camera_optical_frame</frame_name>
      <min_depth>0.1</min_depth>
      <max_depth>10.0</max_depth>
    </plugin>
  </sensor>
</gazebo>
```

### LiDAR Integration

Adding LiDAR sensors for humanoid navigation:

```xml
<link name="h1_lidar_link">
  <inertial>
    <mass value="0.5"/>
    <origin xyz="0 0 0"/>
    <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.001"/>
  </inertial>
</link>

<joint name="h1_lidar_joint" type="fixed">
  <parent link="h1_torso_link"/>
  <child link="h1_lidar_link"/>
  <origin xyz="0.1 0 0.2" rpy="0 0 0"/>
</joint>

<gazebo reference="h1_lidar_link">
  <sensor name="h1_lidar" type="ray">
    <ray>
      <scan>
        <horizontal>
          <samples>720</samples>
          <resolution>1</resolution>
          <min_angle>-3.14159</min_angle>
          <max_angle>3.14159</max_angle>
        </horizontal>
        <vertical>
          <samples>16</samples>
          <resolution>1</resolution>
          <min_angle>-0.261799</min_angle> <!-- -15 degrees -->
          <max_angle>0.261799</max_angle>   <!-- 15 degrees -->
        </vertical>
      </scan>
      <range>
        <min>0.1</min>
        <max>25.0</max>
        <resolution>0.01</resolution>
      </range>
    </ray>
    <plugin name="lidar_controller" filename="libgazebo_ros_laser.so">
      <topic_name>/h1/lidar_scan</topic_name>
      <frame_name>h1_lidar_link</frame_name>
    </plugin>
  </sensor>
</gazebo>
```

## Controller Integration

### ROS 2 Control Configuration

Setting up controllers for simulation:

```yaml
# config/h1_controllers.yaml for simulation
controller_manager:
  ros__parameters:
    update_rate: 500  # Hz
    use_sim_time: true

    joint_state_broadcaster:
      type: joint_state_broadcaster/JointStateBroadcaster

    h1_joint_trajectory_controller:
      type: joint_trajectory_controller/JointTrajectoryController

    h1_imu_sensor_broadcaster:
      type: imu_sensor_broadcaster/IMUSensorBroadcaster

h1_joint_trajectory_controller:
  ros__parameters:
    joints:
      - h1_left_hip_yaw_joint
      - h1_left_hip_roll_joint
      - h1_left_hip_pitch_joint
      - h1_left_knee_joint
      - h1_left_ankle_pitch_joint
      - h1_left_ankle_roll_joint
      # ... add all joints
    command_interfaces:
      - position
    state_interfaces:
      - position
      - velocity

h1_imu_sensor_broadcaster:
  ros__parameters:
    sensor_name: h1_imu
    frame_id: h1_imu_link
```

### Gazebo Controller Plugin

```xml
<gazebo>
  <plugin name="gazebo_ros_control" filename="libgazebo_ros_control.so">
    <robotNamespace>/h1</robotNamespace>
    <robotSimType>gazebo_ros_control/DefaultRobotHWSim</robotSimType>
    <legacyModeNS>true</legacyModeNS>
  </plugin>
</gazebo>
```

## Simulation-Specific Optimizations

### Performance Tuning

Optimizing URDF for simulation performance:

```xml
<!-- Physics optimization for humanoid simulation -->
<gazebo>
  <self_collide>0</self_collide>  <!-- Disable self-collision if not needed -->
  <enable_wind>0</enable_wind>
  <max_step_size>0.001</max_step_size>
  <real_time_factor>1.0</real_time_factor>
  <real_time_update_rate>1000.0</real_time_update_rate>
</gazebo>

<!-- Per-link optimizations -->
<gazebo reference="h1_lower_leg_link">
  <mu1>0.8</mu1>
  <mu2>0.8</mu2>
  <fdir1>1 0 0</fdir1>  <!-- Friction direction -->
  <kp>10000000</kp>    <!-- Contact stiffness -->
  <kd>1000</kd>        <!-- Contact damping -->
  <max_vel>100.0</max_vel>
  <min_depth>0.001</min_depth>
</gazebo>
```

### Collision Filtering

For complex humanoid robots, use collision filtering:

```xml
<!-- Define collision groups to avoid unnecessary collision checks -->
<gazebo>
  <collision>
    <surface>
      <contact>
        <collide_without_contact>0</collide_without_contact>
        <collide_without_contact_bitmask>1</collide_without_contact_bitmask>
      </contact>
    </surface>
  </collision>
</gazebo>

<!-- Use joint constraints instead of collision for connected parts -->
<gazebo reference="h1_hip_joint">
  <implicitSpringDamper>1</implicitSpringDamper>
</gazebo>
```

## Validation and Testing

### Simulation Validation Tools

```python
import subprocess
import os

def validate_urdf_for_simulation(urdf_path):
    """Validate URDF for simulation compatibility"""
    validation_results = {}

    # Check URDF validity
    try:
        result = subprocess.run(['check_urdf', urdf_path],
                              capture_output=True, text=True)
        validation_results['urdf_valid'] = result.returncode == 0
        validation_results['urdf_errors'] = result.stderr
    except FileNotFoundError:
        validation_results['urdf_valid'] = False
        validation_results['error'] = "check_urdf command not found"

    # Check for required simulation elements
    with open(urdf_path, 'r') as f:
        content = f.read()

    validation_results['has_gazebo_plugins'] = '<gazebo>' in content
    validation_results['has_imu_sensors'] = 'type="imu"' in content
    validation_results['has_controllers'] = 'gazebo_ros_control' in content

    return validation_results

def test_simulation_spawn(urdf_path, world_file):
    """Test if robot can be spawned in simulation"""
    try:
        # Try to spawn robot in Gazebo
        spawn_cmd = f"ros2 run gazebo_ros spawn_entity.py -file {urdf_path} -entity test_robot -x 0 -y 0 -z 1.0"
        result = subprocess.run(spawn_cmd, shell=True, capture_output=True, text=True)

        return result.returncode == 0
    except Exception as e:
        print(f"Simulation spawn test failed: {e}")
        return False
```

## Debugging Common Issues

### Joint Configuration Issues

Common problems and solutions:

```xml
<!-- Problem: Joint limits too restrictive -->
<!-- Solution: Ensure limits match physical robot -->
<joint name="h1_left_knee_joint" type="revolute">
  <parent link="h1_left_hip_pitch_link"/>
  <child link="h1_left_knee_link"/>
  <origin xyz="0 0 -0.2" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <!-- Verify these limits match the physical robot -->
  <limit lower="0.0" upper="2.4" effort="400" velocity="4.0"/>
  <dynamics damping="2.0" friction="0.5"/>
</joint>

<!-- Problem: Inertial properties causing instability -->
<!-- Solution: Use realistic values -->
<link name="h1_foot_link">
  <inertial>
    <mass value="0.8"/>  <!-- Realistic mass for foot -->
    <origin xyz="0.05 0 -0.05"/>  <!-- COM offset -->
    <!-- Calculate realistic inertia tensor -->
    <inertia ixx="0.001" ixy="0" ixz="0.0001" iyy="0.002" iyz="0" izz="0.0015"/>
  </inertial>
</link>
```

### Sensor Configuration Issues

```xml
<!-- Proper sensor configuration -->
<gazebo reference="h1_imu_link">
  <!-- Ensure sensor is always on and has proper update rate -->
  <sensor name="h1_imu_sensor" type="imu">
    <always_on>true</always_on>
    <update_rate>100</update_rate>
    <pose>0 0 0 0 0 0</pose>  <!-- Verify pose is correct -->
    <imu>
      <angular_velocity>
        <x>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>2e-4</stddev>
          </noise>
        </x>
      </angular_velocity>
    </imu>
  </sensor>
</gazebo>
```

## Best Practices

### URDF to Simulation Guidelines

1. **Modular Design**: Use Xacro for complex humanoid models
2. **Validation**: Always validate URDF before simulation
3. **Performance**: Optimize collision meshes for simulation speed
4. **Realism**: Match simulation parameters to physical robot
5. **Documentation**: Maintain clear documentation of changes
6. **Testing**: Test incremental changes to avoid complex debugging

### File Organization

```
h1_simulation/
├── urdf/
│   ├── h1.gazebo.xacro      # Gazebo-specific additions
│   ├── h1.isaac.xacro       # Isaac Sim-specific additions
│   └── h1.urdf.xacro        # Base robot description
├── meshes/
│   ├── visual/              # High-resolution visual meshes
│   └── collision/           # Simplified collision meshes
├── config/
│   ├── controllers.yaml     # Controller configurations
│   └── sensors.yaml         # Sensor configurations
└── worlds/
    └── h1_world.world       # Simulation world
```

## Summary

Converting URDF models to simulation environments requires careful attention to physics properties, sensor integration, and performance optimization. For humanoid robots like the Unitree H1, the conversion process must preserve the complex kinematic structure while optimizing for simulation efficiency. Proper validation and testing ensure that simulation results accurately reflect real-world robot behavior, enabling effective development and testing of humanoid robot algorithms.