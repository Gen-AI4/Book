---
id: ros2-architecture
title: ROS 2 Architecture
sidebar_position: 1
---

# ROS 2 Architecture

The Robot Operating System 2 (ROS 2) provides the communication framework for humanoid robotics applications. Understanding its architecture is essential for building robust robotic systems.

## Core Architecture Concepts

ROS 2 follows a distributed computing model where multiple processes communicate over a middleware layer. This architecture enables:

- **Process Isolation**: Individual nodes can fail without affecting the entire system
- **Language Agnostic**: Support for multiple programming languages (C++, Python, etc.)
- **Platform Independence**: Runs on various operating systems and hardware platforms
- **Real-time Capabilities**: With proper configuration, supports real-time execution

### DDS Middleware

ROS 2 uses Data Distribution Service (DDS) as its underlying communication middleware:

- **Data-Centric**: Communication is based on data topics rather than connections
- **Publisher-Subscriber Model**: Nodes publish data to topics, other nodes subscribe
- **Service-Client Model**: Request-response communication for synchronous operations
- **Parameter Server**: Centralized parameter management across nodes

```python
# Example ROS 2 publisher
import rclpy
from std_msgs.msg import String

def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('h1_sensor_publisher')

    publisher = node.create_publisher(String, 'sensor_data', 10)
    timer = node.create_timer(0.1, lambda: publisher.publish(String(data='sensor reading')))

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

## Node Architecture

### Node Lifecycle

ROS 2 nodes follow a well-defined lifecycle:

- **Unconfigured**: Node created but not configured
- **Inactive**: Configuration applied but not active
- **Active**: Node is running and participating in communication
- **Finalized**: Node is shutting down

> [!hardware]
> **Hardware Integration**: On the Unitree H1 humanoid, each major subsystem (legs, arms, sensors) typically runs as a separate ROS 2 node to ensure fault isolation and maintainability.

### Communication Patterns

#### Topics (Publish-Subscribe)
- **Asynchronous**: Publishers and subscribers don't need to run simultaneously
- **Many-to-Many**: Multiple publishers and subscribers can connect to the same topic
- **Real-time**: Low-latency communication suitable for sensor and control data

#### Services (Request-Response)
- **Synchronous**: Client waits for response from service server
- **One-to-One**: Each request goes to a specific service server
- **Reliable**: Ensures delivery of request and response

#### Actions
- **Long-running**: For operations that take significant time
- **Goal-State-Result**: Three-part communication pattern
- **Feedback**: Continuous updates during execution

## Quality of Service (QoS) Settings

QoS profiles control how messages are delivered:

- **Reliability**: Best effort vs. reliable delivery
- **Durability**: Volatile vs. transient local
- **History**: Keep last N messages vs. keep all
- **Deadline**: Maximum time between messages

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

# For critical control commands
control_qos = QoSProfile(
    depth=1,
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.VOLATILE
)

# For sensor data where some loss is acceptable
sensor_qos = QoSProfile(
    depth=10,
    reliability=ReliabilityPolicy.BEST_EFFORT,
    durability=DurabilityPolicy.VOLATILE
)
```

## Launch System

ROS 2 launch files coordinate the startup of multiple nodes:

```python
# launch/h1_system.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='h1_control',
            executable='h1_controller',
            name='h1_controller'
        ),
        Node(
            package='h1_sensors',
            executable='imu_bridge',
            name='imu_bridge'
        )
    ])
```

## Parameter Management

ROS 2 provides centralized parameter management:

- **Node Parameters**: Each node can declare and manage its own parameters
- **Parameter Files**: YAML files for configuration
- **Dynamic Parameters**: Parameters can be changed at runtime
- **Parameter Validation**: Type checking and validation rules

## Security Architecture

ROS 2 includes security features for production environments:

- **Authentication**: Verify node identity
- **Authorization**: Control node permissions
- **Encryption**: Encrypt communication between nodes

## Performance Considerations

### Real-time Requirements

For humanoid robotics, ROS 2 must meet strict timing requirements:

- **Control Loop**: 100Hz to 1kHz for whole-body control
- **Perception**: 30Hz to 60Hz for visual processing
- **Planning**: 10Hz to 50Hz for motion planning

### Memory Management

- **Zero-Copy**: DDS can avoid unnecessary memory copies
- **Preallocation**: Reduce dynamic memory allocation during runtime
- **Message Pooling**: Reuse message objects to reduce allocation overhead

## Hardware Integration Patterns

### Sensor Integration
- **Bridge Nodes**: Convert hardware protocols to ROS 2 messages
- **Hardware Abstraction**: Same interface regardless of specific hardware
- **Calibration**: ROS 2 parameter system for calibration data

### Actuator Control
- **Low-level Controllers**: Handle hardware-specific control algorithms
- **High-level Interfaces**: Abstract actuator control for applications
- **Safety Monitoring**: Continuous monitoring of actuator states

## Debugging and Monitoring

### Tools
- **ros2 topic**: Monitor topic data
- **ros2 service**: Call services and check status
- **rqt**: Graphical tools for monitoring and debugging
- **ros2 bag**: Record and playback data

### Best Practices
- **Comprehensive Logging**: Use ROS 2 logging system
- **Health Monitoring**: Publish system health status
- **Performance Profiling**: Monitor node performance

## Summary

ROS 2 architecture provides the foundation for complex humanoid robotics applications. Its distributed nature, quality of service controls, and comprehensive tooling make it well-suited for safety-critical robotic systems. Understanding these architectural concepts is essential for building robust, maintainable humanoid robot applications.