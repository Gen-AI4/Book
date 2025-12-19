---
id: action-decoding
title: Action Decoding
sidebar_position: 4
---

# Action Decoding

Action decoding is the critical process of converting high-level outputs from Vision-Language-Action (VLA) models into executable robot commands. This chapter explores the techniques, challenges, and best practices for effectively decoding model outputs into safe, feasible, and meaningful robot actions.

## Action Decoding Fundamentals

### The Decoding Pipeline

The action decoding process involves several key stages:

- **Model Output Interpretation**: Understanding what the VLA model is suggesting
- **Constraint Validation**: Ensuring actions are physically and logically feasible
- **Trajectory Generation**: Creating smooth, executable trajectories
- **Safety Filtering**: Preventing dangerous or inappropriate actions
- **Execution Planning**: Coordinating with robot systems for execution

### Action Space Representation

Different approaches to representing and decoding actions:

```python
import numpy as np
import torch
import torch.nn.functional as F
from enum import Enum
from typing import Dict, List, Tuple, Optional, Any

class ActionType(Enum):
    NAVIGATION = "navigation"
    MANIPULATION = "manipulation"
    SPEECH = "speech"
    GESTURE = "gesture"
    BALANCE = "balance"

class ActionSpace:
    def __init__(self, robot_config):
        self.robot_config = robot_config
        self.action_bounds = self.define_action_bounds()
        self.action_names = self.define_action_names()

    def define_action_bounds(self) -> Dict[str, Tuple[float, float]]:
        """Define bounds for different action types"""
        return {
            # Navigation: [linear_x, linear_y, angular_z, speed_limit]
            "nav_linear_x": (-0.5, 0.5),      # m/s
            "nav_linear_y": (-0.3, 0.3),      # m/s (lateral movement)
            "nav_angular_z": (-0.5, 0.5),     # rad/s
            "nav_speed_limit": (0.0, 0.5),    # m/s max speed

            # Manipulation: [pos_x, pos_y, pos_z, rot_x, rot_y, rot_z, grasp]
            "manip_pos_x": (-1.0, 1.0),       # m from robot center
            "manip_pos_y": (-0.8, 0.8),
            "manip_pos_z": (0.2, 1.5),        # Constrained by robot height
            "manip_rot_x": (-1.57, 1.57),     # rad
            "manip_rot_y": (-1.57, 1.57),
            "manip_rot_z": (-3.14, 3.14),
            "manip_grasp": (0.0, 1.0),        # 0=open, 1=closed

            # Speech: [text_id, volume, speed, emotion]
            "speech_text_id": (0, 1000),      # Vocabulary index
            "speech_volume": (0.0, 1.0),
            "speech_speed": (0.5, 2.0),       # Words per minute multiplier
            "speech_emotion": (0, 4),         # 0=neutral, 1=happy, 2=sad, 3=excited
        }

    def define_action_names(self) -> List[str]:
        """Define names for action dimensions"""
        return [
            "nav_linear_x", "nav_linear_y", "nav_angular_z", "nav_speed_limit",
            "manip_pos_x", "manip_pos_y", "manip_pos_z",
            "manip_rot_x", "manip_rot_y", "manip_rot_z", "manip_grasp",
            "speech_text_id", "speech_volume", "speech_speed", "speech_emotion"
        ]

class ActionDecoder:
    def __init__(self, action_space: ActionSpace):
        self.action_space = action_space
        self.action_dim = len(action_space.action_names)

    def decode_raw_output(self, raw_output: torch.Tensor) -> Dict[str, Any]:
        """Decode raw model output into structured action"""
        # Ensure output is the right shape
        if raw_output.shape[-1] != self.action_dim:
            # If dimensions don't match, use a projection layer
            raw_output = self.project_to_action_space(raw_output)

        # Apply activation functions and constraints
        actions = self.apply_constraints(raw_output)

        # Structure the output
        structured_action = self.structure_output(actions)

        return structured_action

    def project_to_action_space(self, raw_output: torch.Tensor) -> torch.Tensor:
        """Project raw output to action space dimensions"""
        # This would typically be a learned projection
        if raw_output.shape[-1] < self.action_dim:
            # Pad with zeros
            padding = torch.zeros(*raw_output.shape[:-1],
                                self.action_dim - raw_output.shape[-1])
            return torch.cat([raw_output, padding], dim=-1)
        elif raw_output.shape[-1] > self.action_dim:
            # Project down
            projection = torch.nn.Linear(raw_output.shape[-1], self.action_dim)
            return projection(raw_output)
        else:
            return raw_output

    def apply_constraints(self, actions: torch.Tensor) -> torch.Tensor:
        """Apply action space constraints"""
        constrained_actions = actions.clone()

        for i, action_name in enumerate(self.action_space.action_names):
            if action_name in self.action_space.action_bounds:
                lower_bound, upper_bound = self.action_space.action_bounds[action_name]

                # Apply different activation functions based on action type
                if "nav" in action_name:
                    # Use tanh for navigation (smooth, bounded)
                    constrained_actions[..., i] = torch.tanh(actions[..., i]) * (upper_bound - lower_bound) / 2
                    constrained_actions[..., i] += (upper_bound + lower_bound) / 2
                elif "manip" in action_name and "grasp" not in action_name:
                    # Use tanh for manipulation positions
                    constrained_actions[..., i] = torch.tanh(actions[..., i]) * (upper_bound - lower_bound) / 2
                    constrained_actions[..., i] += (upper_bound + lower_bound) / 2
                elif "grasp" in action_name:
                    # Use sigmoid for grasp (binary-like)
                    constrained_actions[..., i] = torch.sigmoid(actions[..., i]) * (upper_bound - lower_bound) + lower_bound
                elif "speech" in action_name and "text_id" in action_name:
                    # Use softmax for text selection
                    # This is handled separately as discrete action
                    pass
                else:
                    # Clamp for other actions
                    constrained_actions[..., i] = torch.clamp(
                        actions[..., i], lower_bound, upper_bound
                    )

        return constrained_actions

    def structure_output(self, actions: torch.Tensor) -> Dict[str, Any]:
        """Structure the output into meaningful action components"""
        batch_size = actions.shape[0] if len(actions.shape) > 1 else 1

        structured = {
            "navigation": {},
            "manipulation": {},
            "speech": {},
            "confidence": 0.0  # Placeholder for confidence
        }

        # Extract navigation actions
        nav_indices = [i for i, name in enumerate(self.action_space.action_names) if name.startswith("nav_")]
        if nav_indices:
            nav_actions = actions[..., nav_indices] if len(actions.shape) > 1 else actions[nav_indices]
            structured["navigation"] = {
                "linear_x": float(nav_actions[..., 0]) if actions.shape[-1] > 0 else 0.0,
                "linear_y": float(nav_actions[..., 1]) if actions.shape[-1] > 1 else 0.0,
                "angular_z": float(nav_actions[..., 2]) if actions.shape[-1] > 2 else 0.0,
                "speed_limit": float(nav_actions[..., 3]) if actions.shape[-1] > 3 else 0.2
            }

        # Extract manipulation actions
        manip_indices = [i for i, name in enumerate(self.action_space.action_names) if name.startswith("manip_")]
        if manip_indices:
            manip_actions = actions[..., manip_indices] if len(actions.shape) > 1 else actions[manip_indices]
            structured["manipulation"] = {
                "position": [
                    float(manip_actions[..., 0]) if actions.shape[-1] > 4 else 0.0,  # pos_x
                    float(manip_actions[..., 1]) if actions.shape[-1] > 5 else 0.0,  # pos_y
                    float(manip_actions[..., 2]) if actions.shape[-1] > 6 else 0.0   # pos_z
                ],
                "orientation": [
                    float(manip_actions[..., 3]) if actions.shape[-1] > 7 else 0.0,  # rot_x
                    float(manip_actions[..., 4]) if actions.shape[-1] > 8 else 0.0,  # rot_y
                    float(manip_actions[..., 5]) if actions.shape[-1] > 9 else 0.0   # rot_z
                ],
                "grasp": float(manip_actions[..., 6]) if actions.shape[-1] > 10 else 0.0
            }

        # Extract speech actions
        speech_indices = [i for i, name in enumerate(self.action_space.action_names) if name.startswith("speech_")]
        if speech_indices:
            speech_actions = actions[..., speech_indices] if len(actions.shape) > 1 else actions[speech_indices]
            structured["speech"] = {
                "text_id": int(speech_actions[..., 0]) if actions.shape[-1] > 11 else 0,
                "volume": float(speech_actions[..., 1]) if actions.shape[-1] > 12 else 0.8,
                "speed": float(speech_actions[..., 2]) if actions.shape[-1] > 13 else 1.0,
                "emotion": int(speech_actions[..., 3]) if actions.shape[-1] > 14 else 0
            }

        return structured
```

## Safety and Constraint Validation

### Physical Constraint Checking

Ensuring decoded actions are physically feasible:

```python
class SafetyValidator:
    def __init__(self, robot_config):
        self.robot_config = robot_config
        self.kinematic_chain = self.build_kinematic_chain()
        self.workspace_limits = self.define_workspace()

    def build_kinematic_chain(self):
        """Define robot kinematic chain for constraint checking"""
        # This would typically interface with robot URDF or kinematic model
        return {
            "arm_dh_params": [  # Denavit-Hartenberg parameters
                {"a": 0.1, "alpha": 0, "d": 0.2, "theta_range": (-1.57, 1.57)},
                {"a": 0.15, "alpha": 0, "d": 0, "theta_range": (-2.0, 2.0)},
                # ... more joints
            ],
            "joint_limits": {
                "shoulder_pitch": (-2.0, 2.0),
                "shoulder_roll": (-1.57, 1.57),
                "elbow": (-2.5, 0.5),
                # ... more joint limits
            }
        }

    def define_workspace(self):
        """Define workspace limits for the robot"""
        return {
            "reachable_volume": {
                "min": [-0.8, -0.6, 0.1],  # x, y, z min
                "max": [0.8, 0.6, 1.5]     # x, y, z max
            },
            "obstacle_buffer": 0.1  # meters
        }

    def validate_navigation_action(self, action: Dict[str, float]) -> Tuple[bool, str]:
        """Validate navigation action for safety"""
        # Check speed limits
        linear_speed = np.sqrt(action["linear_x"]**2 + action["linear_y"]**2)
        if linear_speed > self.robot_config.get("max_linear_speed", 0.5):
            return False, f"Linear speed {linear_speed:.2f} exceeds limit"

        # Check angular velocity limits
        if abs(action["angular_z"]) > self.robot_config.get("max_angular_speed", 0.5):
            return False, f"Angular velocity {action['angular_z']:.2f} exceeds limit"

        # Check for balance considerations
        if abs(action["angular_z"]) > 0.3 and abs(action["linear_x"]) > 0.2:
            # Combining rotation and translation might affect balance
            return False, "Combining fast translation and rotation may affect balance"

        return True, "Valid navigation action"

    def validate_manipulation_action(self, action: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate manipulation action for safety"""
        position = action["position"]

        # Check workspace limits
        workspace_min = self.workspace_limits["reachable_volume"]["min"]
        workspace_max = self.workspace_limits["reachable_volume"]["max"]

        for i, (pos, min_val, max_val) in enumerate(zip(position, workspace_min, workspace_max)):
            if not (min_val <= pos <= max_val):
                return False, f"Position component {i} ({pos:.2f}) outside workspace limits [{min_val}, {max_val}]"

        # Check joint limit feasibility through inverse kinematics
        try:
            joint_angles = self.inverse_kinematics(position, action["orientation"])
            if joint_angles is None:
                return False, "No valid inverse kinematics solution for target pose"

            # Check individual joint limits
            for joint_name, angle in joint_angles.items():
                if joint_name in self.kinematic_chain["joint_limits"]:
                    min_limit, max_limit = self.kinematic_chain["joint_limits"][joint_name]
                    if not (min_limit <= angle <= max_limit):
                        return False, f"Joint {joint_name} angle {angle:.2f} exceeds limits [{min_limit}, {max_limit}]"
        except Exception as e:
            return False, f"Inverse kinematics error: {str(e)}"

        # Check for self-collision
        if self.check_self_collision(joint_angles):
            return False, "Action would cause self-collision"

        # Check grasp command validity
        if not (0.0 <= action["grasp"] <= 1.0):
            return False, f"Invalid grasp value: {action['grasp']} (should be 0.0-1.0)"

        return True, "Valid manipulation action"

    def inverse_kinematics(self, position: List[float], orientation: List[float]) -> Optional[Dict[str, float]]:
        """Calculate inverse kinematics (simplified implementation)"""
        # This would use a proper IK solver in practice
        # For demonstration, return a simple approximation
        try:
            # Simplified analytical IK for a 3-DOF arm
            x, y, z = position
            r, p, yaw = orientation

            # Calculate joint angles (this is highly simplified)
            joint_angles = {
                "shoulder_pitch": np.arctan2(z - self.robot_config.get("arm_base_height", 0.5), np.sqrt(x**2 + y**2)),
                "elbow": -np.pi/4,  # Fixed for simplicity
                "wrist_yaw": yaw
            }

            return joint_angles
        except:
            return None

    def check_self_collision(self, joint_angles: Dict[str, float]) -> bool:
        """Check for self-collision given joint angles"""
        # This would use a proper collision detection system
        # For now, use simple checks
        shoulder_pitch = joint_angles.get("shoulder_pitch", 0)
        elbow = joint_angles.get("elbow", 0)

        # Check for extreme configurations that might cause self-collision
        if shoulder_pitch > 1.5 and elbow < -1.0:
            return True  # Potential self-collision

        return False

    def validate_speech_action(self, action: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate speech action"""
        # Check volume bounds
        if not (0.0 <= action["volume"] <= 1.0):
            return False, f"Invalid volume: {action['volume']} (should be 0.0-1.0)"

        # Check speed bounds
        if not (0.5 <= action["speed"] <= 2.0):
            return False, f"Invalid speed: {action['speed']} (should be 0.5-2.0)"

        # Check emotion index bounds
        if not (0 <= action["emotion"] <= 4):
            return False, f"Invalid emotion: {action['emotion']} (should be 0-4)"

        # Check if text ID is valid
        if action["text_id"] < 0 or action["text_id"] > 1000:  # Assuming vocab size
            return False, f"Invalid text ID: {action['text_id']}"

        return True, "Valid speech action"

    def validate_action_sequence(self, actions: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """Validate a sequence of actions for consistency and safety"""
        for i, action in enumerate(actions):
            # Validate individual action
            is_valid, msg = self.validate_single_action(action)
            if not is_valid:
                return False, f"Action {i}: {msg}"

            # Check for continuity between actions (if applicable)
            if i > 0:
                prev_action = actions[i-1]
                continuity_ok, continuity_msg = self.check_action_continuity(prev_action, action)
                if not continuity_ok:
                    return False, f"Action continuity error between {i-1} and {i}: {continuity_msg}"

        return True, "Valid action sequence"

    def validate_single_action(self, action: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate a single action based on its type"""
        if "navigation" in action:
            return self.validate_navigation_action(action["navigation"])
        elif "manipulation" in action:
            return self.validate_manipulation_action(action["manipulation"])
        elif "speech" in action:
            return self.validate_speech_action(action["speech"])
        else:
            return False, "Unknown action type"

    def check_action_continuity(self, prev_action: Dict[str, Any], curr_action: Dict[str, Any]) -> Tuple[bool, str]:
        """Check if the transition between two actions is smooth and safe"""
        # Check for sudden changes that might be unsafe
        if "navigation" in prev_action and "navigation" in curr_action:
            prev_nav = prev_action["navigation"]
            curr_nav = curr_action["navigation"]

            # Check for sudden velocity changes
            prev_speed = np.sqrt(prev_nav["linear_x"]**2 + prev_nav["linear_y"]**2)
            curr_speed = np.sqrt(curr_nav["linear_x"]**2 + curr_nav["linear_y"]**2)

            if abs(curr_speed - prev_speed) > 0.3:  # Threshold for smoothness
                return False, f"Sudden speed change from {prev_speed:.2f} to {curr_speed:.2f}"

            # Check for sudden direction changes
            if abs(curr_nav["angular_z"] - prev_nav["angular_z"]) > 0.5:  # 0.5 rad threshold
                return False, "Sudden angular velocity change"

        return True, "Actions are continuous"
```

> [!hardware]
> **Hardware Note**: The Unitree H1 humanoid robot requires special attention during action decoding to ensure balance and stability. Actions must be validated against the robot's dynamic constraints, including zero moment point (ZMP) stability during locomotion and joint torque limits during manipulation tasks.

## Trajectory Generation and Smoothing

### Converting Actions to Executable Trajectories

Creating smooth, executable trajectories from decoded actions:

```python
from scipy import interpolate
from scipy.spatial.transform import Rotation as R

class TrajectoryGenerator:
    def __init__(self, robot_config):
        self.robot_config = robot_config
        self.sampling_rate = robot_config.get("control_frequency", 50)  # Hz

    def generate_navigation_trajectory(self, action: Dict[str, float], duration: float = 2.0) -> List[Dict[str, float]]:
        """Generate navigation trajectory from action"""
        # Calculate target displacement
        linear_speed = np.sqrt(action["linear_x"]**2 + action["linear_y"]**2)
        if linear_speed == 0:
            # Only rotation
            angular_steps = int(duration * self.sampling_rate)
            angular_vel = action["angular_z"]
            angular_disp = angular_vel * duration

            trajectory = []
            for i in range(angular_steps):
                t = i / self.sampling_rate
                step = {
                    "linear_x": 0.0,
                    "linear_y": 0.0,
                    "angular_z": angular_vel,
                    "timestamp": t
                }
                trajectory.append(step)
        else:
            # Translation with possible rotation
            steps = int(duration * self.sampling_rate)
            trajectory = []

            for i in range(steps):
                t = i / self.sampling_rate
                progress = t / duration

                # Linear interpolation for smooth motion
                step = {
                    "linear_x": action["linear_x"] * progress,
                    "linear_y": action["linear_y"] * progress,
                    "angular_z": action["angular_z"],
                    "timestamp": t
                }
                trajectory.append(step)

        return trajectory

    def generate_manipulation_trajectory(self, action: Dict[str, Any], duration: float = 3.0) -> List[Dict[str, Any]]:
        """Generate manipulation trajectory from action"""
        current_position = self.get_current_end_effector_position()
        target_position = action["position"]
        target_orientation = action["orientation"]

        # Use cubic spline interpolation for smooth motion
        steps = int(duration * self.sampling_rate)
        trajectory = []

        # Time vector
        t = np.linspace(0, 1, steps)

        # Cubic spline coefficients for smooth interpolation
        # Position trajectory
        pos_start = np.array(current_position)
        pos_end = np.array(target_position)

        # Generate smooth trajectory using cubic interpolation
        for i in range(steps):
            progress = t[i]
            # Cubic interpolation: s(t) = a*t³ + b*t² + c*t + d
            # For smooth start/stop: s(0)=0, s(1)=1, s'(0)=0, s'(1)=0
            smooth_progress = 3*progress**2 - 2*progress**3

            current_pos = pos_start + smooth_progress * (pos_end - pos_start)

            # Interpolate orientation (slerp for quaternions, but we'll use linear for Euler)
            current_orient = [
                current_position[0] + smooth_progress * (target_orientation[0] - current_position[0]),
                current_position[1] + smooth_progress * (target_orientation[1] - current_position[1]),
                current_position[2] + smooth_progress * (target_orientation[2] - current_position[2])
            ]

            # Grasp interpolation
            current_grasp = action["grasp"] * smooth_progress

            step = {
                "position": current_pos.tolist(),
                "orientation": current_orient,
                "grasp": current_grasp,
                "timestamp": i / self.sampling_rate
            }
            trajectory.append(step)

        return trajectory

    def generate_speech_trajectory(self, action: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate speech trajectory (mostly immediate execution)"""
        # Speech is typically executed immediately
        return [{
            "text_id": action["text_id"],
            "volume": action["volume"],
            "speed": action["speed"],
            "emotion": action["emotion"],
            "timestamp": 0.0
        }]

    def get_current_end_effector_position(self) -> List[float]:
        """Get current end-effector position from robot state"""
        # This would interface with the robot's state
        # For simulation, return a default position
        return [0.3, 0.0, 0.8]  # Default position in front of robot

    def smooth_trajectory(self, trajectory: List[Dict[str, Any]], action_type: str) -> List[Dict[str, Any]]:
        """Apply smoothing to trajectory"""
        if len(trajectory) < 3:
            return trajectory

        if action_type == "navigation":
            return self.smooth_navigation_trajectory(trajectory)
        elif action_type == "manipulation":
            return self.smooth_manipulation_trajectory(trajectory)
        else:
            return trajectory  # Speech doesn't need smoothing

    def smooth_navigation_trajectory(self, trajectory: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply smoothing to navigation trajectory"""
        if len(trajectory) < 3:
            return trajectory

        # Extract x, y, theta components
        x_vals = [step["linear_x"] for step in trajectory]
        y_vals = [step["linear_y"] for step in trajectory]
        theta_vals = [step["angular_z"] for step in trajectory]

        # Apply smoothing (simple moving average)
        window_size = 3
        smoothed_trajectory = []

        for i in range(len(trajectory)):
            start_idx = max(0, i - window_size//2)
            end_idx = min(len(trajectory), i + window_size//2 + 1)

            avg_x = sum(x_vals[start_idx:end_idx]) / (end_idx - start_idx)
            avg_y = sum(y_vals[start_idx:end_idx]) / (end_idx - start_idx)
            avg_theta = sum(theta_vals[start_idx:end_idx]) / (end_idx - start_idx)

            smoothed_step = trajectory[i].copy()
            smoothed_step.update({
                "linear_x": avg_x,
                "linear_y": avg_y,
                "angular_z": avg_theta
            })
            smoothed_trajectory.append(smoothed_step)

        return smoothed_trajectory

    def smooth_manipulation_trajectory(self, trajectory: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply smoothing to manipulation trajectory"""
        if len(trajectory) < 3:
            return trajectory

        # Extract position and orientation components
        pos_x = [step["position"][0] for step in trajectory]
        pos_y = [step["position"][1] for step in trajectory]
        pos_z = [step["position"][2] for step in trajectory]

        # Apply smoothing to each component
        window_size = 3
        smoothed_trajectory = []

        for i in range(len(trajectory)):
            start_idx = max(0, i - window_size//2)
            end_idx = min(len(trajectory), i + window_size//2 + 1)

            avg_pos_x = sum(pos_x[start_idx:end_idx]) / (end_idx - start_idx)
            avg_pos_y = sum(pos_y[start_idx:end_idx]) / (end_idx - start_idx)
            avg_pos_z = sum(pos_z[start_idx:end_idx]) / (end_idx - start_idx)

            smoothed_step = trajectory[i].copy()
            smoothed_step["position"] = [avg_pos_x, avg_pos_y, avg_pos_z]
            smoothed_trajectory.append(smoothed_step)

        return smoothed_trajectory
```

## Confidence-Based Action Selection

### Handling Uncertainty in Action Decoding

Managing confidence levels and uncertainty in decoded actions:

```python
class ConfidenceBasedDecoder:
    def __init__(self, base_decoder: ActionDecoder, safety_validator: SafetyValidator):
        self.base_decoder = base_decoder
        self.safety_validator = safety_validator
        self.confidence_threshold = 0.7  # Minimum confidence for execution

    def decode_with_confidence(self, raw_output: torch.Tensor,
                             temperature: float = 1.0) -> Tuple[Dict[str, Any], float]:
        """Decode output with confidence estimation"""
        # Apply temperature scaling for confidence estimation
        scaled_output = raw_output / temperature

        # Get base decoding
        decoded_action = self.base_decoder.decode_raw_output(scaled_output)

        # Estimate confidence
        confidence = self.estimate_action_confidence(scaled_output, decoded_action)

        # Add confidence to decoded action
        decoded_action["confidence"] = confidence

        return decoded_action, confidence

    def estimate_action_confidence(self, raw_output: torch.Tensor,
                                 decoded_action: Dict[str, Any]) -> float:
        """Estimate confidence in the decoded action"""
        # Method 1: Entropy-based confidence (lower entropy = higher confidence)
        entropy = self.calculate_output_entropy(raw_output)
        confidence_from_entropy = 1.0 - entropy  # Invert entropy

        # Method 2: Distance from action boundaries (farther from boundaries = higher confidence)
        boundary_confidence = self.calculate_boundary_confidence(decoded_action)

        # Method 3: Constraint satisfaction (more constraints satisfied = higher confidence)
        constraint_confidence = self.calculate_constraint_confidence(decoded_action)

        # Combine confidences (weighted average)
        combined_confidence = (
            0.4 * confidence_from_entropy +
            0.3 * boundary_confidence +
            0.3 * constraint_confidence
        )

        return max(0.0, min(1.0, combined_confidence))  # Clamp to [0, 1]

    def calculate_output_entropy(self, raw_output: torch.Tensor) -> float:
        """Calculate entropy of the raw output as inverse confidence measure"""
        # Apply softmax to get probabilities
        probs = F.softmax(raw_output, dim=-1)

        # Calculate entropy: -sum(p * log(p))
        entropy = -(probs * torch.log(probs + 1e-8)).sum(dim=-1).mean().item()

        # Normalize entropy (max entropy for uniform distribution)
        max_entropy = np.log(raw_output.shape[-1])
        normalized_entropy = entropy / max_entropy

        return normalized_entropy

    def calculate_boundary_confidence(self, decoded_action: Dict[str, Any]) -> float:
        """Calculate confidence based on distance from action boundaries"""
        min_distance = float('inf')

        # Check navigation actions
        if "navigation" in decoded_action:
            nav = decoded_action["navigation"]
            # Calculate distance from boundaries
            linear_speed = np.sqrt(nav["linear_x"]**2 + nav["linear_y"]**2)
            speed_ratio = linear_speed / 0.5  # Assuming 0.5 is max speed
            angular_ratio = abs(nav["angular_z"]) / 0.5  # Assuming 0.5 is max angular
            min_distance = min(min_distance, 1 - max(speed_ratio, angular_ratio))

        # Check manipulation actions
        if "manipulation" in decoded_action:
            manip = decoded_action["manipulation"]
            # Check if position is near workspace boundaries
            workspace_center = [0, 0, 0.8]  # Approximate center
            pos = manip["position"]
            distance_from_center = np.linalg.norm(np.array(pos) - np.array(workspace_center))
            workspace_radius = 0.8  # Approximate workspace radius
            center_ratio = distance_from_center / workspace_radius
            min_distance = min(min_distance, 1 - center_ratio)

        return max(0.0, min_distance)  # Clamp to [0, 1]

    def calculate_constraint_confidence(self, decoded_action: Dict[str, Any]) -> float:
        """Calculate confidence based on constraint satisfaction"""
        is_valid, _ = self.safety_validator.validate_single_action(decoded_action)
        return 1.0 if is_valid else 0.0

    def safe_decode(self, raw_output: torch.Tensor,
                   fallback_action: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Decode with safety fallbacks"""
        decoded_action, confidence = self.decode_with_confidence(raw_output)

        if confidence < self.confidence_threshold:
            if fallback_action:
                return fallback_action
            else:
                # Return a safe default action (stop, neutral pose, etc.)
                return self.get_safe_default_action()

        # Validate the action is safe
        is_safe, reason = self.safety_validator.validate_single_action(decoded_action)
        if not is_safe:
            if fallback_action:
                return fallback_action
            else:
                return self.get_safe_default_action()

        return decoded_action

    def get_safe_default_action(self) -> Dict[str, Any]:
        """Return a safe default action"""
        return {
            "navigation": {"linear_x": 0.0, "linear_y": 0.0, "angular_z": 0.0, "speed_limit": 0.0},
            "manipulation": {"position": [0.3, 0.0, 0.8], "orientation": [0, 0, 0], "grasp": 0.0},
            "speech": {"text_id": 0, "volume": 0.5, "speed": 1.0, "emotion": 0},
            "confidence": 0.0
        }

    def multi_hypothesis_decode(self, raw_output: torch.Tensor,
                              num_hypotheses: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """Generate multiple action hypotheses with different temperature settings"""
        hypotheses = []

        temperatures = np.linspace(0.5, 2.0, num_hypotheses)

        for temp in temperatures:
            decoded_action, confidence = self.decode_with_confidence(raw_output, temp)

            # Only include actions that pass basic safety checks
            is_safe, _ = self.safety_validator.validate_single_action(decoded_action)
            if is_safe:
                hypotheses.append((decoded_action, confidence))

        # Sort by confidence
        hypotheses.sort(key=lambda x: x[1], reverse=True)

        return hypotheses

    def select_best_action(self, hypotheses: List[Tuple[Dict[str, Any], float]],
                          context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Select the best action from multiple hypotheses based on context"""
        if not hypotheses:
            return self.get_safe_default_action()

        if not context:
            # If no context, return highest confidence
            return hypotheses[0][0]

        # Score hypotheses based on context
        scored_hypotheses = []
        for action, confidence in hypotheses:
            score = self.score_action_context_fit(action, context, confidence)
            scored_hypotheses.append((action, score))

        # Return action with highest score
        best_action, _ = max(scored_hypotheses, key=lambda x: x[1])
        return best_action

    def score_action_context_fit(self, action: Dict[str, Any],
                               context: Dict[str, Any], base_confidence: float) -> float:
        """Score how well an action fits the current context"""
        score = base_confidence

        # Context-based adjustments
        if "task_type" in context:
            task_type = context["task_type"]

            # Penalize actions that don't match task type
            if task_type == "navigation" and "navigation" not in action:
                score *= 0.5
            elif task_type == "manipulation" and "manipulation" not in action:
                score *= 0.5

        # Consider environmental context
        if "obstacles_nearby" in context and context["obstacles_nearby"]:
            # Prefer actions with lower speeds for safety
            if "navigation" in action:
                nav_speed = np.sqrt(action["navigation"]["linear_x"]**2 +
                                  action["navigation"]["linear_y"]**2)
                if nav_speed > 0.2:  # High speed with obstacles
                    score *= 0.7

        # Consider robot state
        if "robot_stability" in context and context["robot_stability"] < 0.5:
            # Robot is less stable, prefer conservative actions
            if "navigation" in action:
                nav_speed = np.sqrt(action["navigation"]["linear_x"]**2 +
                                  action["navigation"]["linear_y"]**2)
                if nav_speed > 0.1:  # Reduce speed when unstable
                    score *= 0.8

        return max(0.0, min(1.0, score))
```

## Real-time Action Decoding

### Optimized Decoding for Real-time Applications

Implementing efficient action decoding for real-time humanoid robot control:

```python
import time
from collections import deque
import threading

class RealTimeActionDecoder:
    def __init__(self, confidence_decoder: ConfidenceBasedDecoder,
                 trajectory_generator: TrajectoryGenerator):
        self.confidence_decoder = confidence_decoder
        self.trajectory_generator = trajectory_generator
        self.safety_validator = confidence_decoder.safety_validator

        # Real-time performance tracking
        self.decoding_times = deque(maxlen=100)
        self.target_decode_time = 0.05  # 50ms target

        # Action buffering for smooth execution
        self.action_buffer = deque(maxlen=10)
        self.current_trajectory = []
        self.trajectory_index = 0

        # Threading for non-blocking operations
        self.processing_thread = None
        self.input_queue = deque(maxlen=5)
        self.output_queue = deque(maxlen=5)
        self.is_running = False

    def start_processing_pipeline(self):
        """Start the real-time processing pipeline"""
        self.is_running = True
        self.processing_thread = threading.Thread(target=self.processing_loop)
        self.processing_thread.start()

    def processing_loop(self):
        """Main processing loop for real-time action decoding"""
        while self.is_running:
            start_time = time.time()

            if self.input_queue:
                # Process input
                raw_output = self.input_queue.popleft()

                # Decode action with confidence
                decoded_action = self.confidence_decoder.safe_decode(raw_output)

                # Generate trajectory
                trajectory = self.generate_and_validate_trajectory(decoded_action)

                # Add to output queue
                if trajectory:
                    self.output_queue.append(trajectory)

            # Maintain target timing
            processing_time = time.time() - start_time
            sleep_time = max(0, self.target_decode_time - processing_time)

            if sleep_time > 0:
                time.sleep(sleep_time)

            # Track performance
            self.decoding_times.append(processing_time)

    def decode_action_realtime(self, raw_output: torch.Tensor) -> Optional[List[Dict[str, Any]]]:
        """Decode action with real-time constraints"""
        start_time = time.time()

        try:
            # Quick safety check on raw output
            if not self.is_output_valid(raw_output):
                return None

            # Decode with confidence
            decoded_action = self.confidence_decoder.safe_decode(raw_output)

            # Validate action
            is_valid, reason = self.safety_validator.validate_single_action(decoded_action)
            if not is_valid:
                return None

            # Generate trajectory
            trajectory = self.generate_and_validate_trajectory(decoded_action)

            # Track performance
            decode_time = time.time() - start_time
            self.decoding_times.append(decode_time)

            return trajectory

        except Exception as e:
            print(f"Real-time decoding error: {e}")
            return None

    def is_output_valid(self, raw_output: torch.Tensor) -> bool:
        """Quick validation of raw output"""
        # Check for NaN or extreme values
        if torch.isnan(raw_output).any() or torch.isinf(raw_output).any():
            return False

        # Check output magnitude (shouldn't be extremely large)
        if torch.max(torch.abs(raw_output)) > 1000:
            return False

        return True

    def generate_and_validate_trajectory(self, decoded_action: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """Generate trajectory and validate it"""
        try:
            # Determine action type and generate appropriate trajectory
            if "navigation" in decoded_action:
                trajectory = self.trajectory_generator.generate_navigation_trajectory(
                    decoded_action["navigation"]
                )
                action_type = "navigation"
            elif "manipulation" in decoded_action:
                trajectory = self.trajectory_generator.generate_manipulation_trajectory(
                    decoded_action["manipulation"]
                )
                action_type = "manipulation"
            elif "speech" in decoded_action:
                trajectory = self.trajectory_generator.generate_speech_trajectory(
                    decoded_action["speech"]
                )
                action_type = "speech"
            else:
                return None

            # Validate trajectory
            is_valid, reason = self.safety_validator.validate_action_sequence(trajectory)
            if not is_valid:
                return None

            # Smooth trajectory
            smoothed_trajectory = self.trajectory_generator.smooth_trajectory(
                trajectory, action_type
            )

            return smoothed_trajectory

        except Exception as e:
            print(f"Trajectory generation error: {e}")
            return None

    def get_performance_metrics(self) -> Dict[str, float]:
        """Get real-time performance metrics"""
        if not self.decoding_times:
            return {"avg_decode_time": 0.0, "decode_rate": 0.0}

        avg_time = sum(self.decoding_times) / len(self.decoding_times)
        decode_rate = len(self.decoding_times) / min(len(self.decoding_times), 10) * 10  # Approximate rate

        return {
            "avg_decode_time": avg_time,
            "decode_rate": decode_rate,
            "target_decode_time": self.target_decode_time,
            "buffer_size": len(self.action_buffer)
        }

    def adaptive_decode(self, raw_output: torch.Tensor,
                       current_robot_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Adaptive decoding based on robot state"""
        # Adjust decoding based on robot state
        state_factor = self.calculate_state_factor(current_robot_state)

        # Modify confidence threshold based on state
        original_threshold = self.confidence_decoder.confidence_threshold
        adaptive_threshold = max(0.5, original_threshold * state_factor)

        # Temporarily adjust threshold
        self.confidence_decoder.confidence_threshold = adaptive_threshold

        try:
            action = self.confidence_decoder.safe_decode(raw_output)
        finally:
            # Restore original threshold
            self.confidence_decoder.confidence_threshold = original_threshold

        return action

    def calculate_state_factor(self, robot_state: Dict[str, Any]) -> float:
        """Calculate factor based on robot state for adaptive decoding"""
        factor = 1.0

        # Reduce confidence requirement when robot is in safe state
        if robot_state.get("balance_confidence", 1.0) > 0.8:
            factor *= 1.2  # More confident when balanced
        elif robot_state.get("balance_confidence", 1.0) < 0.3:
            factor *= 0.7  # Less confident when unbalanced

        # Adjust based on battery level
        battery_level = robot_state.get("battery_level", 1.0)
        if battery_level < 0.2:
            factor *= 0.8  # Be more conservative with low battery

        # Adjust based on environment complexity
        env_complexity = robot_state.get("environment_complexity", 0.5)
        if env_complexity > 0.7:
            factor *= 0.9  # Be more conservative in complex environments

        return max(0.5, min(1.5, factor))

def action_decoding_best_practices():
    """Best practices for action decoding"""

    practices = [
        "Always validate decoded actions against physical constraints",
        "Implement confidence-based decision making with appropriate thresholds",
        "Use trajectory smoothing for natural, safe robot motion",
        "Consider robot state and environment when decoding actions",
        "Implement safety fallbacks for uncertain situations",
        "Optimize for real-time performance with target timing constraints",
        "Validate action sequences for continuity and safety",
        "Use multi-hypothesis decoding for better decision making",
        "Monitor and adapt to changing robot conditions",
        "Implement proper error handling and recovery mechanisms"
    ]

    for i, practice in enumerate(practices, 1):
        print(f"{i}. {practice}")

## Summary

Action decoding is a critical component in VLA systems for humanoid robots, bridging the gap between high-level model outputs and safe, executable robot commands. The process involves careful validation against physical constraints, trajectory generation for smooth execution, and confidence-based decision making to handle uncertainty. Proper implementation ensures that humanoid robots can safely and effectively execute complex vision-language-action tasks while maintaining stability and avoiding dangerous situations.