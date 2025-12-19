---
id: urdf-modeling
title: URDF Modeling
sidebar_position: 3
---

# URDF Modeling

Unified Robot Description Format (URDF) is the standard for representing robot models in ROS. For humanoid robots like the Unitree H1, accurate URDF modeling is critical for simulation, control, and visualization.

## URDF Fundamentals

### Basic Structure

URDF is an XML format that describes a robot's physical and kinematic properties:

```xml
<?xml version="1.0"?>
<robot name="h1">
  <!-- Links represent rigid bodies -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.1 0.1 0.1"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.1 0.1 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>

  <!-- Joints connect links -->
  <joint name="base_to_link1" type="revolute">
    <parent link="base_link"/>
    <child link="link1"/>
    <origin xyz="0 0 0.1" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-3.14" upper="3.14" effort="100" velocity="1.0"/>
  </joint>

  <link name="link1">
    <!-- Link definition -->
  </link>
</robot>
```

### Key Components

- **Links**: Rigid bodies with mass, geometry, and inertia properties
- **Joints**: Connections between links with kinematic constraints
- **Materials**: Visual appearance properties
- **Transmissions**: Mapping between actuators and joints

## Humanoid Robot Specifics

### Kinematic Chain Structure

Humanoid robots have complex kinematic structures:

- **Torso**: Central body with multiple attachment points
- **Arms**: Shoulder, elbow, and wrist joints for manipulation
- **Legs**: Hip, knee, and ankle joints for locomotion
- **Head**: Neck joints for vision system orientation

### Degrees of Freedom

The Unitree H1 has 25+ degrees of freedom:

- **Legs**: 6 DOF each (hip yaw, hip roll, hip pitch, knee, ankle pitch, ankle roll)
- **Arms**: 6 DOF each (shoulder pitch, shoulder roll, elbow, wrist pitch, wrist yaw, wrist roll)
- **Torso**: 1-3 DOF (waist yaw, pitch, roll)
- **Head**: 2-3 DOF (neck pitch, yaw, roll)

```xml
<!-- Example H1 leg structure -->
<link name="h1_left_hip_yaw_link">
  <visual>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <mesh filename="package://h1_description/meshes/hip_yaw.dae"/>
    </geometry>
    <material name="gray">
      <color rgba="0.5 0.5 0.5 1.0"/>
    </material>
  </visual>
  <collision>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <mesh filename="package://h1_description/meshes/hip_yaw_collision.dae"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="2.5"/>
    <origin xyz="0.01 0 0.05"/>
    <inertia ixx="0.005" ixy="0" ixz="0.001" iyy="0.006" iyz="0" izz="0.003"/>
  </inertial>
</link>

<joint name="h1_left_hip_yaw_joint" type="revolute">
  <parent link="h1_pelvis"/>
  <child link="h1_left_hip_yaw_link"/>
  <origin xyz="0 0.095 0" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-1.57" upper="1.57" effort="300" velocity="5.0"/>
  <dynamics damping="1.0" friction="0.1"/>
</joint>
```

## Visual and Collision Properties

### Mesh Files

Humanoid robots use complex mesh files for accurate representation:

- **Visual Meshes**: High-resolution meshes for rendering
- **Collision Meshes**: Simplified meshes for collision detection
- **File Formats**: DAE, STL, OBJ, and URDF mesh formats

> [!hardware]
> **Hardware Note**: The Unitree H1 URDF includes detailed collision meshes that match the physical robot's dimensions to ensure accurate simulation and collision avoidance.

### Material Definitions

```xml
<material name="h1_black">
  <color rgba="0.1 0.1 0.1 1.0"/>
</material>

<material name="h1_gray">
  <color rgba="0.4 0.4 0.4 1.0"/>
</material>

<material name="h1_red">
  <color rgba="0.8 0.2 0.2 1.0"/>
</material>
```

## Inertial Properties

### Mass Distribution

Accurate inertial properties are crucial for simulation:

- **Mass**: Weight of each link
- **Center of Mass**: Offset from joint origin
- **Inertia Tensor**: Resistance to rotational motion

### Inertia Calculation

For complex shapes, use CAD tools or approximation methods:

```python
# Example calculation for a humanoid link
def calculate_inertia_box(mass, width, height, depth):
    """Calculate inertia tensor for a box"""
    ixx = (1/12) * mass * (height**2 + depth**2)
    iyy = (1/12) * mass * (width**2 + depth**2)
    izz = (1/12) * mass * (width**2 + height**2)
    return ixx, iyy, izz, 0, 0, 0  # ixy, ixz, iyz assumed 0 for symmetric objects
```

## Joint Specifications

### Joint Types

- **Revolute**: Rotational joint with limits (most common in humanoid robots)
- **Continuous**: Rotational joint without limits
- **Prismatic**: Linear sliding joint
- **Fixed**: No movement (for sensors or attachments)

### Joint Limits and Dynamics

```xml
<joint name="h1_left_knee_joint" type="revolute">
  <parent link="h1_left_hip_pitch_link"/>
  <child link="h1_left_knee_link"/>
  <origin xyz="0 0 -0.2" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>  <!-- Knee rotates about Y axis -->
  <limit lower="0" upper="2.4" effort="400" velocity="4.0"/>
  <dynamics damping="2.0" friction="0.5"/>
  <safety_controller k_position="10" k_velocity="1.0"
                    soft_lower_limit="0.05" soft_upper_limit="2.35"/>
</joint>
```

## Sensors in URDF

### IMU Integration

```xml
<link name="h1_imu_link">
  <inertial>
    <mass value="0.01"/>
    <origin xyz="0 0 0"/>
    <inertia ixx="0.0001" ixy="0" ixz="0" iyy="0.0001" iyz="0" izz="0.0001"/>
  </inertial>
</link>

<joint name="h1_imu_joint" type="fixed">
  <parent link="h1_pelvis"/>
  <child link="h1_imu_link"/>
  <origin xyz="0.0 0.0 0.05" rpy="0 0 0"/>
</joint>

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
```

### Camera Integration

```xml
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
  <origin xyz="0.05 0 0" rpy="0 0 0"/>
</joint>
```

## Gazebo Integration

### Physics Properties

```xml
<gazebo reference="h1_left_foot_link">
  <mu1>0.8</mu1>
  <mu2>0.8</mu2>
  <kp>1000000.0</kp>
  <kd>100.0</kd>
  <min_depth>0.001</min_depth>
  <max_vel>1.0</max_vel>
  <material>Gazebo/Black</material>
  <turn Gravity="1"/>
</gazebo>
```

### Transmission Definitions

```xml
<transmission name="h1_left_hip_yaw_trans">
  <type>transmission_interface/SimpleTransmission</type>
  <joint name="h1_left_hip_yaw_joint">
    <hardwareInterface>hardware_interface/EffortJointInterface</hardwareInterface>
  </joint>
  <actuator name="h1_left_hip_yaw_motor">
    <hardwareInterface>hardware_interface/EffortJointInterface</hardwareInterface>
    <mechanicalReduction>1</mechanicalReduction>
  </actuator>
</transmission>
```

## Validation and Testing

### URDF Validation

```bash
# Check for URDF errors
check_urdf /path/to/h1.urdf

# Visualize the robot structure
urdf_to_graphiz /path/to/h1.urdf
```

### Kinematic Validation

- **Forward Kinematics**: Verify end-effector positions
- **Inverse Kinematics**: Test reachability of target poses
- **Jacobian Computation**: Validate velocity relationships

## Tools and Workflows

### Xacro for Complex Models

Xacro (XML Macros) simplifies complex URDF models:

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="h1">

  <xacro:property name="M_PI" value="3.1415926535897931" />

  <xacro:macro name="h1_leg" params="side reflect">
    <link name="h1_${side}_hip_yaw_link">
      <!-- Leg definition using parameters -->
    </link>
    <!-- Additional leg links and joints -->
  </xacro:macro>

  <xacro:h1_leg side="left" reflect="1"/>
  <xacro:h1_leg side="right" reflect="-1"/>

</robot>
```

### CAD Integration

- **SolidWorks to URDF**: Direct export plugins
- **Fusion 360**: Export to STEP, then convert to URDF
- **Blender**: Import/export URDF functionality

## Best Practices

### File Organization

```
h1_description/
├── urdf/
│   ├── h1.urdf.xacro
│   ├── h1.gazebo.xacro
│   └── components/
│       ├── leg.urdf.xacro
│       ├── arm.urdf.xacro
│       └── torso.urdf.xacro
├── meshes/
│   ├── visual/
│   └── collision/
└── launch/
    └── display.launch.py
```

### Performance Considerations

- **Mesh Simplification**: Use simpler meshes for collision detection
- **Inertial Approximation**: Balance accuracy with computational cost
- **Joint Limit Validation**: Ensure limits match physical constraints

## Troubleshooting Common Issues

### Kinematic Issues
- **Self-Collision**: Check joint limits and collision meshes
- **Singularity**: Avoid configurations where Jacobian becomes singular
- **Assembly Errors**: Verify all joints have proper parent-child relationships

### Simulation Issues
- **Jittering**: Increase solver iterations or adjust physics parameters
- **Drifting**: Check mass properties and joint constraints
- **Performance**: Simplify collision meshes if needed

## Summary

URDF modeling is fundamental to humanoid robotics, providing the geometric and kinematic description needed for simulation, control, and visualization. For complex robots like the Unitree H1, careful attention to inertial properties, joint limits, and sensor integration ensures accurate simulation and safe operation. Proper use of Xacro and modular design principles makes URDF models maintainable and reusable.