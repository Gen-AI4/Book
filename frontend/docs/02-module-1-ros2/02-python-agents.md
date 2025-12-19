---
id: python-agents
title: Python Agents
sidebar_position: 2
---

# Python Agents

Python agents form the backbone of many humanoid robotics applications, providing high-level control, planning, and decision-making capabilities. This chapter explores the development of sophisticated Python-based agents for humanoid robots.

## Agent Architecture

### Behavior Trees

Behavior trees provide a structured approach to complex robot behaviors:

```python
import py_trees
import rclpy
from rclpy.node import Node

class H1BehaviorAgent(Node):
    def __init__(self):
        super().__init__('h1_behavior_agent')

        # Create behavior tree
        self.root = self.setup_behavior_tree()
        self.tree = py_trees.trees.BehaviourTree(self.root)

    def setup_behavior_tree(self):
        # Root selector
        root = py_trees.composites.Selector(name="H1 Main Behaviors")

        # Safety behavior (highest priority)
        safety_behavior = SafetyCheck(self)

        # Navigation behavior
        navigation_behavior = NavigationTask(self)

        # Manipulation behavior
        manipulation_behavior = ManipulationTask(self)

        root.add_children([safety_behavior, navigation_behavior, manipulation_behavior])
        return root
```

### State Machines

For simpler behaviors, state machines provide a clear execution flow:

- **Idle State**: Robot waiting for commands
- **Walking State**: Executing locomotion
- **Manipulation State**: Performing object interaction
- **Emergency State**: Safety procedures

## Control Agents

### Joint Space Control

Python agents can control individual joints for precise manipulation:

```python
import rclpy
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

class JointController:
    def __init__(self, node):
        self.publisher = node.create_publisher(
            JointTrajectory,
            '/h1/joint_trajectory_controller/joint_trajectory',
            10
        )

    def move_to_position(self, joint_names, positions, duration=2.0):
        msg = JointTrajectory()
        msg.joint_names = joint_names

        point = JointTrajectoryPoint()
        point.positions = positions
        point.time_from_start = Duration(sec=int(duration), nanosec=0)

        msg.points = [point]
        self.publisher.publish(msg)
```

### Operational Space Control

For end-effector control, operational space control provides intuitive Cartesian control:

- **Position Control**: Control end-effector position
- **Orientation Control**: Control end-effector orientation
- **Impedance Control**: Control interaction forces

## Perception Agents

### Sensor Data Processing

Python agents process sensor data for environment understanding:

```python
from sensor_msgs.msg import JointState, Imu, Image
import numpy as np

class PerceptionAgent:
    def __init__(self, node):
        self.joint_state = None
        self.imu_data = None

        node.create_subscription(JointState, '/h1/joint_states', self.joint_callback, 10)
        node.create_subscription(Imu, '/h1/imu', self.imu_callback, 10)

    def joint_callback(self, msg):
        self.joint_state = msg

    def imu_callback(self, msg):
        self.imu_data = msg
        self.process_balance_data()

    def process_balance_data(self):
        if self.imu_data:
            # Process orientation and angular velocity for balance control
            orientation = self.imu_data.orientation
            angular_velocity = self.imu_data.angular_velocity
            # Implement balance algorithms
```

### Vision Processing

Computer vision agents process camera data:

- **Object Detection**: Identify objects in the environment
- **Pose Estimation**: Determine object poses for manipulation
- **SLAM Integration**: Combine vision with other sensors for localization

## Planning Agents

### Motion Planning

Motion planning agents generate collision-free trajectories:

```python
import moveit_commander
import geometry_msgs.msg

class MotionPlanner:
    def __init__(self):
        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface()
        self.arm_group = moveit_commander.MoveGroupCommander("h1_right_arm")

    def plan_to_pose(self, target_pose):
        self.arm_group.set_pose_target(target_pose)
        plan = self.arm_group.plan()
        return plan

    def execute_plan(self, plan):
        return self.arm_group.execute(plan, wait=True)
```

### Task Planning

High-level task planning coordinates complex behaviors:

- **PDDL Integration**: Use classical planning formalisms
- **Temporal Planning**: Account for time constraints
- **Resource Management**: Coordinate multiple robot resources

## Learning Agents

### Reinforcement Learning Integration

Python agents can interface with reinforcement learning systems:

```python
import torch
import numpy as np

class RLLearningAgent:
    def __init__(self, model_path):
        self.policy = torch.load(model_path)
        self.policy.eval()

    def get_action(self, observation):
        with torch.no_grad():
            action = self.policy(torch.tensor(observation).float())
        return action.numpy()

    def update_policy(self, experience_batch):
        # Update the policy based on new experience
        pass
```

### Imitation Learning

Agents can learn from demonstrations:

- **Behavior Cloning**: Learn from expert demonstrations
- **DAGGER**: Interactive learning approach
- **GAIL**: Generative adversarial imitation learning

## Communication Patterns

### Action Servers

For long-running tasks, action servers provide progress feedback:

```python
from rclpy.action import ActionServer
from h1_msgs.action import WalkToGoal

class NavigationAgent:
    def __init__(self, node):
        self.node = node
        self.action_server = ActionServer(
            node,
            WalkToGoal,
            'walk_to_goal',
            self.execute_callback
        )

    def execute_callback(self, goal_handle):
        feedback_msg = WalkToGoal.Feedback()

        while not self.reached_goal():
            # Update feedback
            feedback_msg.distance_remaining = self.get_distance_to_goal()
            goal_handle.publish_feedback(feedback_msg)

            # Check for cancellation
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return WalkToGoal.Result()

        goal_handle.succeed()
        return WalkToGoal.Result()
```

### Parameter Management

Dynamic parameter systems allow runtime configuration:

```python
from rclpy.parameter import Parameter

class AdaptiveAgent:
    def __init__(self, node):
        self.node = node
        self.declare_parameters(
            [('walking_speed', 0.5),
             ('step_height', 0.1),
             ('stance_width', 0.3)]
        )

        self.node.add_on_set_parameters_callback(self.parameter_callback)

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'walking_speed':
                self.update_walking_controller(param.value)
        return SetParametersResult(successful=True)
```

> [!hardware]
> **Hardware Note**: On the Unitree H1, Python agents typically run on the onboard Jetson Orin computer, with critical control loops running at higher priorities to ensure real-time performance.

## Safety Considerations

### Emergency Procedures

Python agents must implement comprehensive safety systems:

- **Emergency Stop**: Immediate halt of all motion
- **Joint Limit Checking**: Prevent dangerous joint configurations
- **Balance Recovery**: Restore balance when lost
- **Fall Prevention**: Avoid configurations that could cause falls

### Fault Detection

Agents should monitor system health:

```python
def check_system_health(self):
    # Check joint temperature limits
    for joint in self.joint_states:
        if joint.temperature > MAX_TEMP:
            self.trigger_safety_procedure("Joint overheating")

    # Check actuator status
    for actuator in self.actuator_status:
        if actuator.error:
            self.trigger_safety_procedure(f"Actuator error: {actuator.name}")
```

## Performance Optimization

### Threading and Concurrency

Python agents should use appropriate concurrency models:

- **AsyncIO**: For I/O-bound operations
- **Threading**: For blocking operations
- **Multiprocessing**: For CPU-intensive tasks

### Memory Management

- **Object Pooling**: Reuse objects to reduce allocation
- **Garbage Collection**: Tune for real-time performance
- **Memory Profiling**: Monitor and optimize memory usage

## Debugging and Testing

### Unit Testing

Python agents should be thoroughly tested:

```python
import unittest
from unittest.mock import Mock, patch

class TestH1Agent(unittest.TestCase):
    def setUp(self):
        self.agent = H1BehaviorAgent()

    def test_walk_behavior(self):
        # Test walking behavior with mocked sensors
        with patch('sensor_subscriber') as mock_sensor:
            mock_sensor.return_value = Mock()
            result = self.agent.execute_walk()
            self.assertTrue(result.success)
```

### Integration Testing

Test agent behavior in complete system scenarios:

- **Simulation Testing**: Test in Gazebo or Isaac Sim
- **Hardware-in-Loop**: Test with real sensors
- **Performance Testing**: Validate timing requirements

## Best Practices

### Code Organization

- **Modular Design**: Separate concerns into distinct modules
- **Configuration Management**: Use parameter files for configuration
- **Error Handling**: Comprehensive error handling and recovery

### Documentation

- **Type Hints**: Use Python type hints for clarity
- **Docstrings**: Document all public interfaces
- **Examples**: Provide usage examples

## Summary

Python agents provide the high-level intelligence for humanoid robots, handling perception, planning, learning, and control. By following established patterns and best practices, developers can create robust, maintainable agents that safely control complex humanoid systems. The combination of ROS 2 communication, Python's flexibility, and proper safety systems enables sophisticated robotic behaviors.