---
id: nav2-planning
title: Nav2 Planning
sidebar_position: 4
---

# Nav2 Planning

Navigation 2 (Nav2) is the state-of-the-art navigation framework for ROS 2, providing advanced path planning and navigation capabilities for mobile robots. This chapter explores the implementation of Nav2 for humanoid robots, addressing the unique challenges of bipedal navigation and human-aware path planning.

## Nav2 Architecture Overview

### Core Components

Nav2 is built around a behavior tree architecture that provides flexibility and modularity:

- **Navigation Stack**: Complete navigation system with localization, mapping, and path planning
- **Behavior Trees**: Modular execution of navigation behaviors
- **Planners**: Global and local path planning algorithms
- **Controllers**: Trajectory following and obstacle avoidance
- **Sensors**: Integration with various sensor modalities

### Humanoid-Specific Considerations

When adapting Nav2 for humanoid robots like the Unitree H1, several factors must be considered:

- **Bipedal Kinematics**: Different from wheeled robots
- **Balance Constraints**: Must maintain stability during navigation
- **Step Planning**: Requires discrete footstep planning
- **Terrain Adaptation**: Handle various ground types and obstacles

```yaml
# Nav2 configuration for humanoid robot
bt_navigator:
  ros__parameters:
    use_sim_time: True
    global_frame: map
    robot_base_frame: h1/base_link
    odom_topic: /h1/odometry
    bt_loop_duration: 10
    default_server_timeout: 20
    enable_groot_monitoring: True
    groot_zmq_publisher_port: 1666
    groot_zmq_server_port: 1667
    # Behavior tree for humanoid navigation
    default_nav_to_pose_bt_xml: /opt/nav2/share/nav2_bt_navigator/behavior_trees/humanoid_nav_to_pose_w_replanning_and_recovery.xml
    default_nav_through_poses_bt_xml: /opt/nav2/share/nav2_bt_navigator/behavior_trees/humanoid_nav_through_poses_w_replanning_and_recovery.xml

planner_server:
  ros__parameters:
    use_sim_time: True
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_navfn_planner/NavfnPlanner"
      tolerance: 0.5
      use_astar: false
      allow_unknown: true

controller_server:
  ros__parameters:
    use_sim_time: True
    controller_frequency: 20.0
    min_x_velocity_threshold: 0.001
    min_y_velocity_threshold: 0.5
    min_theta_velocity_threshold: 0.001
    failure_tolerance: 0.3
    progress_checker_plugin: "progress_checker"
    goal_checker_plugin: "goal_checker"
    controller_plugins: ["FollowPath"]

    # Humanoid-specific controller
    FollowPath:
      plugin: "nav2_humanoid_controller/HumanoidController"
      speed_limit_scale: 0.7  # Humanoid robots move slower than wheeled robots
      max_linear_speed: 0.5   # m/s for humanoid walking
      max_angular_speed: 0.5  # rad/s
```

## Global Path Planning

### Humanoid-Aware Global Planner

The global planner must account for humanoid-specific constraints:

```python
from nav2_core.global_planner import GlobalPlanner
from nav2_core.types import Costmap, Pose
from geometry_msgs.msg import PoseStamped, Point
from nav_msgs.msg import Path
from builtin_interfaces.msg import Duration
import numpy as np
import heapq

class HumanoidGlobalPlanner(GlobalPlanner):
    def __init__(self):
        super().__init__()
        self.costmap = None
        self.planner_name = "HumanoidGlobalPlanner"

    def configure(self, tf_buffer, costmap_ros, lifecycle_node, name):
        """Configure the planner with costmap and other parameters"""
        self.costmap = costmap_ros
        self.tf_buffer = tf_buffer
        self.lifecycle_node = lifecycle_node
        self.planner_name = name

    def cleanup(self):
        """Clean up resources"""
        pass

    def set_costmap(self, costmap):
        """Set the costmap for planning"""
        self.costmap = costmap

    def create_plan(self, start, goal):
        """Create a global plan from start to goal"""
        # Convert start and goal to costmap coordinates
        start_costmap = self.world_to_costmap(start.pose.position)
        goal_costmap = self.world_to_costmap(goal.pose.position)

        # Check if start and goal are valid
        if not self.is_valid_cell(start_costmap) or not self.is_valid_cell(goal_costmap):
            self.lifecycle_node.get_logger().warn("Start or goal is in invalid cell")
            return Path()

        # Plan using A* with humanoid-specific costs
        path_indices = self.humanoid_astar(start_costmap, goal_costmap)

        if not path_indices:
            self.lifecycle_node.get_logger().warn("No path found")
            return Path()

        # Convert path indices back to world coordinates
        world_path = self.indices_to_world_path(path_indices)

        # Smooth the path for humanoid locomotion
        smoothed_path = self.smooth_humanoid_path(world_path)

        return smoothed_path

    def humanoid_astar(self, start, goal):
        """A* algorithm with humanoid-specific cost function"""
        # Get costmap dimensions
        width = self.costmap.get_size_x()
        height = self.costmap.get_size_y()

        # Initialize open set with start position
        open_set = [(0, start)]
        heapq.heapify(open_set)

        # Initialize cost dictionaries
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        came_from = {}

        # Directions for 8-connected grid (including diagonal moves)
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

        while open_set:
            current_cost, current = heapq.heappop(open_set)

            if current == goal:
                # Reconstruct path
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path

            for dx, dy in directions:
                neighbor = (current[0] + dx, current[1] + dy)

                # Check bounds
                if not (0 <= neighbor[0] < width and 0 <= neighbor[1] < height):
                    continue

                # Check if neighbor is valid (not in obstacle)
                if not self.is_valid_cell(neighbor):
                    continue

                # Calculate movement cost (diagonal moves cost more for humanoid)
                if dx != 0 and dy != 0:  # Diagonal move
                    movement_cost = 1.414  # sqrt(2)
                else:  # Horizontal/vertical move
                    movement_cost = 1.0

                # Add humanoid-specific costs (e.g., terrain difficulty)
                humanoid_cost = self.calculate_humanoid_cost(neighbor)
                tentative_g_score = g_score[current] + movement_cost + humanoid_cost

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []  # No path found

    def calculate_humanoid_cost(self, cell):
        """Calculate additional cost for humanoid-specific factors"""
        # Get costmap value
        costmap_cost = self.costmap.get_cost(cell[0], cell[1])

        # Additional costs for humanoid:
        # - Rough terrain cost
        # - Stairs/slopes cost
        # - Narrow passages cost (for balance)
        terrain_cost = 0.0

        # Example: increase cost for potentially unstable terrain
        if costmap_cost > 100:  # Lethal obstacle
            return float('inf')
        elif costmap_cost > 50:  # Inscribed obstacle
            terrain_cost = 2.0
        else:
            terrain_cost = 0.1

        return terrain_cost

    def heuristic(self, a, b):
        """Heuristic function for A* (Euclidean distance)"""
        return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    def is_valid_cell(self, cell):
        """Check if a cell is valid for humanoid navigation"""
        cost = self.costmap.get_cost(cell[0], cell[1])
        return cost < 253  # Not lethal obstacle

    def world_to_costmap(self, world_point):
        """Convert world coordinates to costmap indices"""
        resolution = self.costmap.get_resolution()
        origin = self.costmap.get_origin()

        x = int((world_point.x - origin.position.x) / resolution)
        y = int((world_point.y - origin.position.y) / resolution)

        return (x, y)

    def indices_to_world_path(self, indices):
        """Convert costmap indices to world path"""
        path = Path()
        path.header.frame_id = "map"
        path.header.stamp = self.lifecycle_node.get_clock().now().to_msg()

        resolution = self.costmap.get_resolution()
        origin = self.costmap.get_origin()

        for idx in indices:
            world_x = idx[0] * resolution + origin.position.x
            world_y = idx[1] * resolution + origin.position.y

            pose_stamped = PoseStamped()
            pose_stamped.header.frame_id = "map"
            pose_stamped.header.stamp = path.header.stamp
            pose_stamped.pose.position.x = world_x
            pose_stamped.pose.position.y = world_y
            pose_stamped.pose.position.z = 0.0  # Assume flat terrain for now
            pose_stamped.pose.orientation.w = 1.0  # No rotation initially

            path.poses.append(pose_stamped)

        return path

    def smooth_humanoid_path(self, path):
        """Smooth path for humanoid locomotion"""
        # Apply path smoothing algorithm suitable for humanoid robots
        # This could be a spline-based smoother or other humanoid-aware algorithm
        return self.spline_smoothing(path)

    def spline_smoothing(self, path):
        """Apply spline-based smoothing to the path"""
        if len(path.poses) < 3:
            return path

        # Convert poses to numpy arrays for processing
        points = np.array([[p.pose.position.x, p.pose.position.y] for p in path.poses])

        # Apply spline smoothing (simplified version)
        smoothed_points = self.apply_cubic_spline(points)

        # Create new smoothed path
        smoothed_path = Path()
        smoothed_path.header = path.header

        for point in smoothed_points:
            pose_stamped = PoseStamped()
            pose_stamped.header = path.header
            pose_stamped.pose.position.x = point[0]
            pose_stamped.pose.position.y = point[1]
            pose_stamped.pose.position.z = 0.0
            pose_stamped.pose.orientation.w = 1.0
            smoothed_path.poses.append(pose_stamped)

        return smoothed_path

    def apply_cubic_spline(self, points):
        """Apply cubic spline smoothing to path points"""
        # Simplified cubic spline implementation
        # In practice, you'd use scipy or other libraries
        if len(points) < 2:
            return points

        # For demonstration, use simple averaging
        smoothed = []
        for i in range(len(points)):
            if i == 0 or i == len(points) - 1:
                # Keep start and end points
                smoothed.append(points[i])
            else:
                # Average with neighbors
                avg_point = (points[i-1] + points[i] + points[i+1]) / 3
                smoothed.append(avg_point)

        return np.array(smoothed)
```

> [!hardware]
> **Hardware Note**: The Unitree H1 humanoid robot requires specialized path planning that considers its bipedal locomotion capabilities. Unlike wheeled robots, the H1 must plan discrete footsteps and maintain balance throughout navigation, requiring path planning algorithms that account for the robot's dynamic stability constraints.

## Local Path Planning and Control

### Humanoid Local Planner

The local planner handles real-time obstacle avoidance and trajectory following:

```python
from nav2_core.local_planner import LocalPlanner
from geometry_msgs.msg import Twist, PoseStamped
from sensor_msgs.msg import LaserScan, PointCloud2
from nav_msgs.msg import Path
import math

class HumanoidLocalPlanner(LocalPlanner):
    def __init__(self):
        super().__init__()
        self.current_path = None
        self.current_pose = None
        self.linear_vel = 0.0
        self.angular_vel = 0.0
        self.humanoid_controller = HumanoidWalkController()

    def configure(self, tf_buffer, costmap_ros, lifecycle_node, name):
        """Configure the local planner"""
        self.tf_buffer = tf_buffer
        self.costmap = costmap_ros
        self.lifecycle_node = lifecycle_node
        self.planner_name = name

    def setPlan(self, path):
        """Set the global plan for local planning"""
        self.current_path = path
        self.lifecycle_node.get_logger().info(f"Received path with {len(path.poses)} waypoints")

    def computeVelocityCommands(self, pose, velocity):
        """Compute velocity commands for humanoid robot"""
        self.current_pose = pose

        if not self.current_path or len(self.current_path.poses) == 0:
            # No path, stop the robot
            return self.create_twist(0.0, 0.0), Duration()

        # Calculate next velocity command based on path following
        cmd_vel = self.calculate_humanoid_cmd_vel(pose, self.current_path)

        # Check for local obstacles
        if self.detect_local_obstacles():
            # Implement obstacle avoidance for humanoid
            cmd_vel = self.humanoid_obstacle_avoidance(cmd_vel)

        # Validate command for humanoid constraints
        cmd_vel = self.validate_humanoid_command(cmd_vel)

        return cmd_vel, Duration()

    def calculate_humanoid_cmd_vel(self, current_pose, path):
        """Calculate velocity commands for humanoid path following"""
        # Find closest point on path
        closest_idx = self.find_closest_waypoint(current_pose, path)

        if closest_idx is None:
            return self.create_twist(0.0, 0.0)

        # Determine target point ahead on the path
        target_idx = min(closest_idx + 5, len(path.poses) - 1)  # Look 5 waypoints ahead
        target_pose = path.poses[target_idx]

        # Calculate desired direction and distance
        dx = target_pose.pose.position.x - current_pose.pose.position.x
        dy = target_pose.pose.position.y - current_pose.pose.position.y
        distance = math.sqrt(dx*dx + dy*dy)

        # Calculate desired heading
        desired_yaw = math.atan2(dy, dx)
        current_yaw = self.quaternion_to_yaw(current_pose.pose.orientation)

        # Calculate angular error
        angle_error = self.normalize_angle(desired_yaw - current_yaw)

        # Calculate velocity based on distance and angle error
        linear_vel = min(0.5, max(0.1, distance * 0.5))  # Scale with distance, max 0.5 m/s
        angular_vel = angle_error * 0.8  # PID-like angular control

        # Apply humanoid-specific constraints
        linear_vel = min(linear_vel, 0.5)  # Max humanoid walking speed
        angular_vel = max(min(angular_vel, 0.5), -0.5)  # Limit angular velocity

        return self.create_twist(linear_vel, angular_vel)

    def detect_local_obstacles(self):
        """Detect obstacles in local area"""
        # This would interface with local costmap or sensor data
        # Return True if obstacles are detected that require avoidance
        local_costmap = self.costmap.get_costmap()
        robot_x, robot_y = self.get_robot_position()

        # Check immediate vicinity for obstacles
        robot_costmap_x = int((robot_x - local_costmap.getOriginX()) / local_costmap.getResolution())
        robot_costmap_y = int((robot_y - local_costmap.getOriginY()) / local_costmap.getResolution())

        # Check 3x3 area around robot
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                check_x = robot_costmap_x + dx
                check_y = robot_costmap_y + dy

                if (0 <= check_x < local_costmap.getSizeInCellsX() and
                    0 <= check_y < local_costmap.getSizeInCellsY()):
                    cost = local_costmap.getCost(check_x, check_y)
                    if cost > 200:  # Consider as obstacle
                        return True

        return False

    def humanoid_obstacle_avoidance(self, original_cmd_vel):
        """Implement humanoid-specific obstacle avoidance"""
        # For humanoid robots, obstacle avoidance might involve:
        # - Sidestepping instead of turning
        # - Stopping to assess situation
        # - Requesting alternative path from global planner

        # Simple implementation: reduce speed and potentially turn
        cmd_vel = Twist()
        cmd_vel.linear.x = max(0.0, original_cmd_vel.linear.x * 0.3)  # Reduce speed to 30%
        cmd_vel.angular.z = original_cmd_vel.angular.z * 0.7  # Reduce angular speed too

        # If obstacle is very close, consider stopping
        if self.is_obstacle_very_close():
            cmd_vel.linear.x = 0.0
            cmd_vel.angular.z = 0.0
            # Could trigger replanning here

        return cmd_vel

    def validate_humanoid_command(self, cmd_vel):
        """Validate and limit commands for humanoid robot"""
        # Apply humanoid-specific limits
        max_linear = 0.5  # m/s
        max_angular = 0.5  # rad/s

        # Limit linear velocity
        cmd_vel.linear.x = max(min(cmd_vel.linear.x, max_linear), -max_linear)
        cmd_vel.linear.y = max(min(cmd_vel.linear.y, max_linear * 0.5), -max_linear * 0.5)  # Lateral movement is slower

        # Limit angular velocity
        cmd_vel.angular.z = max(min(cmd_vel.angular.z, max_angular), -max_angular)

        return cmd_vel

    def find_closest_waypoint(self, current_pose, path):
        """Find the closest waypoint on the path"""
        if not path.poses:
            return None

        min_dist = float('inf')
        closest_idx = 0

        for i, pose in enumerate(path.poses):
            dist = math.sqrt(
                (current_pose.pose.position.x - pose.pose.position.x)**2 +
                (current_pose.pose.position.y - pose.pose.position.y)**2
            )
            if dist < min_dist:
                min_dist = dist
                closest_idx = i

        return closest_idx

    def quaternion_to_yaw(self, orientation):
        """Convert quaternion to yaw angle"""
        siny_cosp = 2 * (orientation.w * orientation.z + orientation.x * orientation.y)
        cosy_cosp = 1 - 2 * (orientation.y * orientation.y + orientation.z * orientation.z)
        return math.atan2(siny_cosp, cosy_cosp)

    def normalize_angle(self, angle):
        """Normalize angle to [-pi, pi] range"""
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle

    def get_robot_position(self):
        """Get current robot position"""
        if self.current_pose:
            return (self.current_pose.pose.position.x, self.current_pose.pose.position.y)
        return (0.0, 0.0)

    def is_obstacle_very_close(self):
        """Check if obstacle is very close to robot"""
        # This would check local costmap or sensor data for immediate obstacles
        return False

    def create_twist(self, linear_x, angular_z):
        """Create Twist message with given velocities"""
        twist = Twist()
        twist.linear.x = linear_x
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = angular_z
        return twist
```

## Footstep Planning Integration

### Humanoid Footstep Planner

For bipedal robots, path planning must include discrete footstep planning:

```python
import numpy as np
from geometry_msgs.msg import Point

class HumanoidFootstepPlanner:
    def __init__(self):
        self.step_width = 0.2  # Distance between feet
        self.step_length = 0.3  # Max step length forward
        self.step_height = 0.05  # Step height for clearance

    def plan_footsteps(self, path, start_pose):
        """Plan discrete footsteps based on continuous path"""
        footsteps = []

        # Initialize with current foot positions
        left_foot = self.calculate_initial_foot_position(start_pose, "left")
        right_foot = self.calculate_initial_foot_position(start_pose, "right")

        current_left = left_foot
        current_right = right_foot
        support_foot = "left"  # Start with left foot as support

        # Process path in segments
        for i in range(1, len(path.poses)):
            target_pose = path.poses[i]

            # Calculate next foot position based on path direction
            next_left, next_right = self.calculate_next_foot_positions(
                current_left, current_right, target_pose, support_foot
            )

            # Validate step feasibility
            if self.is_step_feasible(current_left if support_foot == "right" else current_right,
                                   next_left if support_foot == "left" else next_right):

                # Add step to sequence
                if support_foot == "left":
                    footsteps.append(("right", next_right))
                    current_right = next_right
                else:
                    footsteps.append(("left", next_left))
                    current_left = next_left

                # Switch support foot
                support_foot = "right" if support_foot == "left" else "left"
            else:
                # If step not feasible, try to replan or wait
                continue

        return footsteps

    def calculate_initial_foot_position(self, pose, foot_type):
        """Calculate initial foot position based on robot pose"""
        # Position feet relative to robot center
        offset_x = 0.0
        offset_y = self.step_width / 2 if foot_type == "left" else -self.step_width / 2

        # Transform offset to world frame
        cos_yaw = np.cos(self.quaternion_to_yaw(pose.pose.orientation))
        sin_yaw = np.sin(self.quaternion_to_yaw(pose.pose.orientation))

        world_x = pose.pose.position.x + offset_x * cos_yaw - offset_y * sin_yaw
        world_y = pose.pose.position.y + offset_x * sin_yaw + offset_y * cos_yaw

        return Point(x=world_x, y=world_y, z=0.0)

    def calculate_next_foot_positions(self, left_pos, right_pos, target_pose, support_foot):
        """Calculate next foot positions based on target"""
        # Calculate desired next position along path
        target_x = target_pose.pose.position.x
        target_y = target_pose.pose.position.y

        # Calculate direction of movement
        dx = target_x - (left_pos.x + right_pos.x) / 2  # Robot center
        dy = target_y - (left_pos.y + right_pos.y) / 2
        distance = np.sqrt(dx*dx + dy*dy)

        if distance > 0:
            # Normalize direction
            dx_norm = dx / distance
            dy_norm = dy / distance

            # Calculate step distance (limited by max step length)
            step_dist = min(distance, self.step_length)

            # Calculate new foot positions
            if support_foot == "left":
                # Move right foot toward target
                new_right_x = right_pos.x + dx_norm * step_dist
                new_right_y = right_pos.y + dy_norm * step_dist
                return left_pos, Point(x=new_right_x, y=new_right_y, z=0.0)
            else:
                # Move left foot toward target
                new_left_x = left_pos.x + dx_norm * step_dist
                new_left_y = left_pos.y + dy_norm * step_dist
                return Point(x=new_left_x, y=new_left_y, z=0.0), right_pos
        else:
            return left_pos, right_pos

    def is_step_feasible(self, current_pos, next_pos):
        """Check if a step is kinematically and environmentally feasible"""
        # Check step length constraint
        step_dist = np.sqrt((next_pos.x - current_pos.x)**2 + (next_pos.y - current_pos.y)**2)
        if step_dist > self.step_length * 1.5:  # Allow some flexibility
            return False

        # Check for obstacles in step path (would check costmap)
        # This is a simplified check
        return True

    def quaternion_to_yaw(self, orientation):
        """Convert quaternion to yaw angle"""
        siny_cosp = 2 * (orientation.w * orientation.z + orientation.x * orientation.y)
        cosy_cosp = 1 - 2 * (orientation.y * orientation.y + orientation.z * orientation.z)
        return np.arctan2(siny_cosp, cosy_cosp)
```

## Behavior Trees for Humanoid Navigation

### Custom Behavior Tree Nodes

Creating behavior tree nodes for humanoid-specific navigation:

```xml
<!-- humanoid_nav_to_pose_w_replanning_and_recovery.xml -->
<root main_tree_to_execute="MainTree">
    <BehaviorTree ID="MainTree">
        <Sequence name="NavigateWithReplanning">
            <PipelineSequence name="global_plan">
                <RateController hz="0.1">
                    <RecoveryNode number_of_retries="1" name="ComputePathToPose">
                        <ComputePathToPose goal="{goal}" path="{path}" planner_id="GridBased"/>
                        <ReactiveFailure name="PathUpdated"/>
                    </RecoveryNode>
                </RateController>
            </PipelineSequence>

            <PipelineSequence name="local_plan">
                <RateController hz="20">
                    <RecoveryNode number_of_retries="3" name="FollowPath">
                        <FollowPath path="{path}" controller_id="FollowPath"/>
                        <ReactiveFailure name="FollowPathRecovery"/>
                    </RecoveryNode>
                </RateController>
            </PipelineSequence>

            <ReactiveSequence name="achieve_goal">
                <GoalReached goal="{goal}" tolerance="0.25"/>
            </ReactiveSequence>
        </Sequence>
    </BehaviorTree>
</root>
```

### Humanoid-Specific Recovery Behaviors

```python
from py_trees import Status, Behaviour
import py_trees

class HumanoidSpinRecovery(Behaviour):
    def __init__(self, name="HumanoidSpinRecovery"):
        super(HumanoidSpinRecovery, self).__init__(name)
        self.command_publisher = None
        self.timeout = 10.0  # seconds
        self.start_time = None

    def setup(self, **kwargs):
        """Setup the recovery behavior"""
        try:
            self.command_publisher = kwargs['node'].create_publisher(
                Twist, '/h1/cmd_vel', 10
            )
        except Exception as e:
            self.logger.error(f"Failed to create publisher: {e}")

    def initialise(self):
        """Initialize the recovery behavior"""
        self.start_time = self.node.get_clock().now().nanoseconds / 1e9
        self.publish_spin_command()

    def update(self):
        """Update the recovery behavior"""
        current_time = self.node.get_clock().now().nanoseconds / 1e9

        if current_time - self.start_time > self.timeout:
            self.publish_stop_command()
            return Status.SUCCESS

        # Continue spinning
        self.publish_spin_command()
        return Status.RUNNING

    def terminate(self, new_status):
        """Clean up when behavior terminates"""
        self.publish_stop_command()

    def publish_spin_command(self):
        """Publish spin command for humanoid"""
        if self.command_publisher:
            twist = Twist()
            twist.linear.x = 0.0
            twist.angular.z = 0.5  # Gentle spin for humanoid
            self.command_publisher.publish(twist)

    def publish_stop_command(self):
        """Stop the robot"""
        if self.command_publisher:
            twist = Twist()
            self.command_publisher.publish(twist)

class HumanoidWaitRecovery(Behaviour):
    def __init__(self, name="HumanoidWaitRecovery", wait_time=5.0):
        super(HumanoidWaitRecovery, self).__init__(name)
        self.wait_time = wait_time
        self.start_time = None

    def initialise(self):
        """Initialize the wait behavior"""
        self.start_time = self.node.get_clock().now().nanoseconds / 1e9

    def update(self):
        """Update the wait behavior"""
        current_time = self.node.get_clock().now().nanoseconds / 1e9

        if current_time - self.start_time > self.wait_time:
            return Status.SUCCESS

        # While waiting, the humanoid might perform balancing
        self.perform_balance_check()
        return Status.RUNNING

    def perform_balance_check(self):
        """Perform balance check while waiting"""
        # Check if humanoid is still balanced
        # This would interface with balance control system
        pass
```

## Integration with Isaac Sim

### Isaac Sim Navigation Testing

Testing navigation algorithms in Isaac Sim:

```python
from omni.isaac.core import World
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.robots import Robot
from omni.isaac.core.utils.viewports import set_viewport_camera
import numpy as np

class IsaacSimNavigationTest:
    def __init__(self):
        self.world = World(stage_units_in_meters=1.0)
        self.navigation_node = None
        self.humanoid_robot = None

    def setup_navigation_environment(self):
        """Setup Isaac Sim environment for navigation testing"""
        # Add humanoid robot
        self.humanoid_robot = self.world.scene.add(
            Robot(
                prim_path="/World/H1",
                name="h1_robot",
                usd_path="path/to/h1_model.usd",
                position=np.array([0, 0, 0.85]),
                orientation=np.array([0, 0, 0, 1])
            )
        )

        # Create navigation test environment
        self.create_navigation_course()

        # Setup ROS bridge for navigation
        self.setup_ros_bridge()

    def create_navigation_course(self):
        """Create a navigation course with obstacles"""
        # Create start and goal markers
        self.create_navigation_waypoints()

        # Add obstacles
        self.add_navigation_obstacles()

        # Add dynamic obstacles that move during navigation
        self.add_dynamic_obstacles()

    def create_navigation_waypoints(self):
        """Create navigation waypoints for testing"""
        # Start position
        start_marker = VisualCuboid(
            prim_path="/World/StartMarker",
            name="start_marker",
            position=np.array([0, 0, 0.1]),
            size=0.2,
            color=np.array([0, 1, 0])  # Green for start
        )

        # Goal position
        goal_marker = VisualCuboid(
            prim_path="/World/GoalMarker",
            name="goal_marker",
            position=np.array([5, 5, 0.1]),
            size=0.2,
            color=np.array([1, 0, 0])  # Red for goal
        )

    def add_navigation_obstacles(self):
        """Add static obstacles for navigation testing"""
        obstacle_positions = [
            [1, 1, 0.5], [2, 2, 0.5], [3, 1, 0.5],
            [4, 3, 0.5], [1, 4, 0.5], [2, 4, 0.5]
        ]

        for i, pos in enumerate(obstacle_positions):
            obstacle = DynamicCuboid(
                prim_path=f"/World/Obstacle_{i}",
                name=f"obstacle_{i}",
                position=np.array(pos),
                size=0.5,
                mass=1.0
            )

    def run_navigation_test(self, start_pose, goal_pose):
        """Run navigation test in Isaac Sim"""
        # Reset robot to start position
        self.humanoid_robot.set_world_pose(position=start_pose[:3], orientation=start_pose[3:])

        # Send navigation goal
        if self.navigation_node:
            self.navigation_node.send_goal(goal_pose)

        # Run simulation and monitor progress
        success = self.monitor_navigation_progress(goal_pose)

        return success

    def monitor_navigation_progress(self, goal_pose):
        """Monitor navigation progress and success"""
        import time

        start_time = time.time()
        max_time = 60  # Maximum navigation time

        while time.time() - start_time < max_time:
            # Get current robot position
            current_pos, _ = self.humanoid_robot.get_world_pose()

            # Check if reached goal
            goal_pos = goal_pose[:3]
            distance = np.linalg.norm(np.array(current_pos) - np.array(goal_pos))

            if distance < 0.5:  # Within 0.5m of goal
                print("Navigation successful!")
                return True

            # Step simulation
            self.world.step(render=True)

        print("Navigation timeout!")
        return False
```

## Performance Optimization

### Navigation Performance Tuning

Optimizing Nav2 for humanoid robot performance:

```python
class HumanoidNavPerformanceOptimizer:
    def __init__(self, nav_node):
        self.nav_node = nav_node
        self.performance_metrics = {
            'planning_time': [],
            'execution_time': [],
            'success_rate': 0,
            'average_speed': 0
        }

    def optimize_planning_frequency(self):
        """Optimize planning frequency based on environment complexity"""
        # In complex environments, plan less frequently to save computation
        # In simple environments, plan more frequently for better responsiveness
        pass

    def dynamic_footstep_parameters(self):
        """Adjust footstep parameters based on terrain"""
        # Adjust step length, width, height based on terrain roughness
        # Use sensor data to detect terrain type and adjust accordingly
        pass

    def balance_computation_load(self):
        """Balance navigation computation with balance control"""
        # Ensure navigation doesn't interfere with critical balance control
        # Use separate threads or priority levels for balance vs navigation
        pass

    def adaptive_path_smoothing(self):
        """Adjust path smoothing based on robot capabilities"""
        # For humanoid robots, too much smoothing might make path unrealistic
        # Adjust smoothing parameters based on robot's turning capabilities
        pass
```

## Troubleshooting and Best Practices

### Common Navigation Issues

Addressing common Nav2 issues with humanoid robots:

```python
def troubleshoot_humanoid_navigation():
    """Common troubleshooting for humanoid navigation"""

    issues = {
        "Oscillation": {
            "problem": "Robot oscillates around path",
            "solution": "Increase minimum distance to path, adjust PID parameters"
        },
        "Getting Stuck": {
            "problem": "Robot gets stuck in local minima",
            "solution": "Improve global planner, add random walk recovery"
        },
        "Balance Loss": {
            "problem": "Navigation commands cause balance loss",
            "solution": "Implement balance-aware velocity limiting"
        },
        "Step Planning Failure": {
            "problem": "Footstep planner fails in complex terrain",
            "solution": "Use terrain classification, adjust step parameters"
        }
    }

    for issue, details in issues.items():
        print(f"{issue}: {details['problem']}")
        print(f"  Solution: {details['solution']}\n")

def humanoid_navigation_best_practices():
    """Best practices for humanoid navigation"""

    practices = [
        "Use balance-aware velocity commands that consider humanoid stability",
        "Implement proper footstep planning integrated with path planning",
        "Validate navigation commands with balance control system",
        "Use appropriate costmaps that consider humanoid-specific constraints",
        "Test navigation thoroughly in simulation before real-world deployment",
        "Implement robust recovery behaviors for humanoid-specific failures",
        "Consider the robot's height changes during walking in sensor processing"
    ]

    for i, practice in enumerate(practices, 1):
        print(f"{i}. {practice}")
```

## Summary

Nav2 planning for humanoid robots requires specialized considerations that account for bipedal locomotion, balance constraints, and discrete footstep planning. The integration of traditional path planning with humanoid-specific controllers and footstep planners enables effective navigation for robots like the Unitree H1. Proper configuration of costmaps, velocity limits, and recovery behaviors ensures safe and efficient navigation in complex environments while maintaining the robot's dynamic stability.