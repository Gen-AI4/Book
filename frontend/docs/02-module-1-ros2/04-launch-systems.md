---
id: launch-systems
title: Launch Systems
sidebar_position: 4
---

# Launch Systems

ROS 2 launch systems provide the infrastructure to start and coordinate multiple nodes for humanoid robot operation. Proper launch configuration is essential for reliable system startup and operation.

## Launch Architecture

### Python Launch Files

ROS 2 uses Python-based launch files for maximum flexibility:

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

def generate_launch_description():
    # Declare launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    robot_model = LaunchConfiguration('robot_model', default='h1')

    # Launch the robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': Command(['xacro ', FindFile('h1_description', 'urdf/h1.urdf.xacro')]),
            'use_sim_time': use_sim_time
        }],
        remappings=[
            ('/tf', 'tf'),
            ('/tf_static', 'tf_static')
        ]
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false', description='Use simulation time'),
        DeclareLaunchArgument('robot_model', default_value='h1', description='Robot model to use'),
        robot_state_publisher,
    ])
```

### Launch Arguments

Launch arguments provide runtime configuration:

- **use_sim_time**: Switch between real and simulation time
- **robot_model**: Select between different robot variants
- **config_file**: Load different parameter configurations
- **debug**: Enable debugging features

## Humanoid Robot Launch Patterns

### Hierarchical Launch Structure

For complex robots like the Unitree H1, use a hierarchical launch structure:

```
h1_bringup/
├── launch/
│   ├── h1_system.launch.py      # Main system launch
│   ├── h1_control.launch.py     # Control system only
│   ├── h1_perception.launch.py  # Perception system only
│   ├── h1_simulation.launch.py  # Simulation-specific launch
│   └── h1_hardware.launch.py    # Hardware-specific launch
```

### Control System Launch

```python
# h1_control.launch.py
from launch import LaunchDescription
from launch.actions import TimerAction
from launch_ros.actions import Node

def generate_launch_description():
    # Joint trajectory controller
    joint_trajectory_controller = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[
            {'robot_description': Command(['xacro ', FindFile('h1_description', 'urdf/h1.urdf.xacro')])},
            PathJoinSubstitution([FindPackageShare('h1_control'), 'config', 'h1_controllers.yaml'])
        ],
        output='screen'
    )

    # Balance controller
    balance_controller = Node(
        package='h1_balance_controller',
        executable='balance_controller_node',
        parameters=[
            PathJoinSubstitution([FindPackageShare('h1_control'), 'config', 'balance_params.yaml'])
        ],
        output='screen'
    )

    # Walk controller
    walk_controller = Node(
        package='h1_walk_controller',
        executable='walk_controller_node',
        parameters=[
            PathJoinSubstitution([FindPackageShare('h1_control'), 'config', 'walk_params.yaml'])
        ],
        output='screen'
    )

    return LaunchDescription([
        joint_trajectory_controller,
        TimerAction(
            period=2.0,
            actions=[balance_controller]
        ),
        TimerAction(
            period=3.0,
            actions=[walk_controller]
        )
    ])
```

## Parameter Management

### YAML Configuration Files

Launch files integrate with YAML parameter files:

```yaml
# config/h1_controllers.yaml
controller_manager:
  ros__parameters:
    update_rate: 500  # Hz

    joint_trajectory_controller:
      type: joint_trajectory_controller/JointTrajectoryController

    joint_state_broadcaster:
      type: joint_state_broadcaster/JointStateBroadcaster

joint_trajectory_controller:
  ros__parameters:
    joints:
      - h1_left_hip_yaw_joint
      - h1_left_hip_roll_joint
      - h1_left_hip_pitch_joint
      # ... all other joints
    command_interfaces:
      - position
    state_interfaces:
      - position
      - velocity
```

### Dynamic Parameter Loading

```python
# Load parameters from file
parameter_file = PathJoinSubstitution([
    FindPackageShare('h1_bringup'),
    'config',
    [robot_model, '_params.yaml']
])

node_with_params = Node(
    package='h1_controller',
    executable='controller_node',
    parameters=[parameter_file],
    output='screen'
)
```

## Hardware vs Simulation Launch

### Simulation Launch

```python
# h1_simulation.launch.py
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Launch Gazebo simulation
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            get_package_share_directory('gazebo_ros'),
            '/launch/gazebo.launch.py'
        ])
    )

    # Launch robot in simulation
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'h1',
            '-x', '0', '-y', '0', '-z', '1.0'
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        spawn_entity,
    ])
```

> [!hardware]
> **Hardware Note**: When launching on the physical H1 robot, additional safety checks and hardware interface configurations are required. The launch system should verify hardware availability before starting controllers.

### Hardware Launch

```python
# h1_hardware.launch.py
from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable
from launch_ros.actions import Node

def generate_launch_description():
    # Set environment for hardware
    set_env = SetEnvironmentVariable('RCUTILS_LOGGING_USE_STDOUT', '1')

    # Hardware interface node
    hardware_interface = Node(
        package='h1_hardware_interface',
        executable='h1_hardware_node',
        parameters=[
            PathJoinSubstitution([FindPackageShare('h1_hardware_interface'), 'config', 'h1_hardware.yaml'])
        ],
        output='screen'
    )

    # Safety monitor
    safety_monitor = Node(
        package='h1_safety',
        executable='safety_monitor_node',
        parameters=[
            PathJoinSubstitution([FindPackageShare('h1_safety'), 'config', 'safety_params.yaml'])
        ],
        output='screen'
    )

    return LaunchDescription([
        set_env,
        safety_monitor,
        hardware_interface,
    ])
```

## Event Handling and Coordination

### Startup Sequences

Control the order of node startup to ensure proper initialization:

```python
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessStart, OnProcessExit

def generate_launch_description():
    # Start safety monitor first
    safety_monitor = Node(
        package='h1_safety',
        executable='safety_monitor_node',
        name='safety_monitor'
    )

    # Start controller only after safety monitor is running
    controller = Node(
        package='h1_controller',
        executable='controller_node',
        name='controller'
    )

    delayed_controller = RegisterEventHandler(
        OnProcessStart(
            target_action=safety_monitor,
            on_start=[controller]
        )
    )

    return LaunchDescription([
        safety_monitor,
        delayed_controller
    ])
```

### Shutdown Procedures

Ensure proper cleanup on system shutdown:

```python
from launch.actions import Shutdown

def create_shutdown_handler():
    # Create a service or action that can trigger shutdown
    shutdown_node = Node(
        package='h1_bringup',
        executable='shutdown_handler_node',
        on_exit=Shutdown()
    )
    return shutdown_node
```

## Composable Nodes

For performance-critical applications, use composable nodes in containers:

```python
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

def generate_launch_description():
    # Create a container for high-frequency nodes
    perception_container = ComposableNodeContainer(
        name='perception_container',
        namespace='',
        package='rclcpp_components',
        executable='component_container',
        composable_node_descriptions=[
            ComposableNode(
                package='h1_perception',
                plugin='h1_perception::ImageProcessor',
                name='image_processor',
                parameters=[
                    PathJoinSubstitution([FindPackageShare('h1_perception'), 'config', 'image_params.yaml'])
                ]
            ),
            ComposableNode(
                package='h1_perception',
                plugin='h1_perception::PointCloudProcessor',
                name='pointcloud_processor',
                parameters=[
                    PathJoinSubstitution([FindPackageShare('h1_perception'), 'config', 'pc_params.yaml'])
                ]
            )
        ],
        output='screen'
    )

    return LaunchDescription([perception_container])
```

## Launch Testing

### Launch Testing Framework

ROS 2 provides tools for testing launch files:

```python
# test/test_h1_launch.py
import unittest
import launch
from launch import LaunchDescription
from launch_ros.actions import Node
import launch_testing.actions
import pytest

@pytest.mark.launch_test
def generate_test_description():
    h1_node = Node(
        package='h1_system',
        executable='h1_node',
        name='h1_test_node'
    )

    return LaunchDescription([
        h1_node,
        launch_testing.actions.ReadyToTest()
    ])

def test_node_running(output_file):
    # Test that the node starts successfully
    assert True
```

## Debugging Launch Issues

### Common Problems

- **Node Startup Failures**: Check parameter files and dependencies
- **Timing Issues**: Use TimerAction for proper startup sequences
- **Resource Conflicts**: Ensure unique node names and namespaces
- **Permission Issues**: Verify hardware access permissions

### Diagnostic Tools

```bash
# Check launch file syntax
ros2 launch --dry-run package_name launch_file.py

# Monitor launch process
ros2 launch package_name launch_file.py --log-level debug

# List active nodes
ros2 node list
```

## Performance Optimization

### Resource Management

- **Process Grouping**: Group related nodes for better resource management
- **Priority Settings**: Set appropriate process priorities for real-time performance
- **Memory Management**: Configure memory limits for containers

### Monitoring

```python
# Launch system monitoring
system_monitor = Node(
    package='h1_monitoring',
    executable='system_monitor_node',
    parameters=[
        PathJoinSubstitution([FindPackageShare('h1_monitoring'), 'config', 'monitoring.yaml'])
    ],
    output='screen'
)
```

## Safety Integration

### Emergency Procedures

Launch files should include safety systems:

```python
# Safety systems launch first
safety_system = Node(
    package='h1_safety',
    executable='emergency_stop_node',
    parameters=[
        PathJoinSubstitution([FindPackageShare('h1_safety'), 'config', 'emergency_params.yaml'])
    ],
    respawn=True,  # Restart if it crashes
    respawn_delay=1  # Wait 1 second before restart
)
```

## Best Practices

### Modularity

- **Separate Concerns**: Split launch files by function (control, perception, etc.)
- **Reusable Components**: Create parameterized launch files
- **Configuration Variants**: Support different robot configurations

### Documentation

- **Comment Launch Files**: Explain the purpose of each node
- **Parameter Descriptions**: Document all launch arguments
- **Startup Sequences**: Clarify dependencies between nodes

## Summary

Launch systems are critical for humanoid robot operation, coordinating the startup and configuration of multiple nodes. Proper launch design ensures reliable system startup, appropriate node ordering, and safe operation. For complex robots like the Unitree H1, hierarchical launch structures with proper safety integration provide the foundation for successful robotic applications.