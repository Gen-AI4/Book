---
id: llm-planner
title: LLM Planner
sidebar_position: 2
---

# LLM Planner

Large Language Model (LLM) planners provide high-level reasoning and task decomposition capabilities for humanoid robots, enabling complex goal-directed behavior through natural language interaction. This chapter explores the integration of LLMs with humanoid robot control systems for intelligent planning and execution.

## LLM Planner Architecture

### Core Components

An LLM planner for humanoid robots consists of several key components:

- **Language Interface**: Natural language understanding and generation
- **Task Decomposition**: Breaking complex goals into executable actions
- **Knowledge Integration**: Incorporating world knowledge and robot capabilities
- **Action Mapping**: Converting LLM outputs to robot commands
- **Execution Monitoring**: Tracking plan execution and handling failures

### Integration with Robot Systems

```python
import openai
import json
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class RobotCapability:
    name: str
    description: str
    parameters: Dict[str, str]
    preconditions: List[str]
    effects: List[str]

@dataclass
class PlanStep:
    action: str
    parameters: Dict[str, Any]
    description: str
    priority: int = 0

class LLMPlanner:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        openai.api_key = api_key

        # Robot capabilities database
        self.capabilities = self.initialize_robot_capabilities()

        # Context and memory
        self.conversation_history = []
        self.current_plan = []
        self.executed_steps = []

    def initialize_robot_capabilities(self) -> Dict[str, RobotCapability]:
        """Initialize the robot's known capabilities"""
        return {
            "move_to": RobotCapability(
                name="move_to",
                description="Move the robot to a specific location",
                parameters={"location": "str", "speed": "float"},
                preconditions=["robot_is_active", "location_is_safe"],
                effects=["robot_position_changes"]
            ),
            "grasp_object": RobotCapability(
                name="grasp_object",
                description="Grasp an object with the robot's hand",
                parameters={"object_id": "str", "hand": "str"},
                preconditions=["object_is_reachable", "hand_is_free"],
                effects=["object_is_grasped"]
            ),
            "release_object": RobotCapability(
                name="release_object",
                description="Release a currently grasped object",
                parameters={"hand": "str"},
                preconditions=["object_is_grasped"],
                effects=["object_is_released"]
            ),
            "detect_object": RobotCapability(
                name="detect_object",
                description="Detect and identify objects in the environment",
                parameters={"object_type": "str", "search_area": "str"},
                preconditions=["camera_is_active"],
                effects=["object_location_known"]
            ),
            "navigate_to_object": RobotCapability(
                name="navigate_to_object",
                description="Navigate to a specific object",
                parameters={"object_id": "str"},
                preconditions=["object_is_detected"],
                effects=["robot_is_near_object"]
            ),
            "speak": RobotCapability(
                name="speak",
                description="Speak a text message",
                parameters={"message": "str", "emotion": "str"},
                preconditions=["tts_system_active"],
                effects=["message_spoken"]
            ),
            "greet_person": RobotCapability(
                name="greet_person",
                description="Greet a person in the environment",
                parameters={"person_id": "str", "greeting_type": "str"},
                preconditions=["person_is_detected"],
                effects=["person_acknowledged"]
            )
        }

    def plan_from_natural_language(self, goal: str, context: Dict[str, Any] = None) -> List[PlanStep]:
        """Generate a plan from natural language goal with context"""
        # Prepare the prompt for the LLM
        prompt = self.create_planning_prompt(goal, context)

        # Call the LLM
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )

        # Parse the response
        plan_json = response.choices[0].message.content.strip()

        try:
            plan_data = json.loads(plan_json)
            plan_steps = self.parse_plan_steps(plan_data)
            return plan_steps
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract steps from text
            return self.extract_steps_from_text(plan_json)

    def create_planning_prompt(self, goal: str, context: Dict[str, Any] = None) -> str:
        """Create the prompt for the LLM planner"""
        capabilities_str = self.format_capabilities()

        context_str = ""
        if context:
            context_str = f"Additional context:\n{json.dumps(context, indent=2)}\n\n"

        prompt = f"""You are an intelligent planner for a humanoid robot. Your task is to decompose high-level goals into a sequence of executable actions.

Robot capabilities:
{capabilities_str}

Goal: {goal}

{context_str}
Provide the plan as a JSON array of steps. Each step should have:
- action: the capability name
- parameters: required parameters as key-value pairs
- description: brief description of the step

Example format:
[
    {{
        "action": "detect_object",
        "parameters": {{"object_type": "cup", "search_area": "kitchen_table"}},
        "description": "Look for a cup on the kitchen table"
    }},
    {{
        "action": "navigate_to_object",
        "parameters": {{"object_id": "cup_123"}},
        "description": "Move to the location of the cup"
    }}
]

Plan:"""

        return prompt

    def format_capabilities(self) -> str:
        """Format robot capabilities for the LLM"""
        formatted = []
        for name, capability in self.capabilities.items():
            formatted.append(
                f"- {name}: {capability.description}\n"
                f"  Parameters: {capability.parameters}\n"
                f"  Preconditions: {capability.preconditions}\n"
                f"  Effects: {capability.effects}\n"
            )
        return "\n".join(formatted)

    def get_system_prompt(self) -> str:
        """Get the system prompt for the LLM"""
        return """You are an intelligent task planner for a humanoid robot. Generate step-by-step plans to accomplish user goals using the robot's capabilities. Consider:
1. Physical constraints and safety
2. Logical sequence of operations
3. Precondition satisfaction
4. Efficient execution
5. Natural human-robot interaction

Always respond with valid JSON or plain text that can be parsed."""
```

## Task Decomposition and Reasoning

### Hierarchical Task Planning

Implementing hierarchical planning for complex humanoid tasks:

```python
from enum import Enum
from typing import Union

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Task:
    id: str
    name: str
    description: str
    steps: List[PlanStep]
    dependencies: List[str]
    status: TaskStatus = TaskStatus.PENDING
    priority: int = 0

class HierarchicalPlanner:
    def __init__(self, llm_planner: LLMPlanner):
        self.llm_planner = llm_planner
        self.tasks = {}
        self.task_queue = []
        self.active_tasks = []

    def decompose_high_level_task(self, goal: str, context: Dict[str, Any] = None) -> Task:
        """Decompose a high-level task into subtasks"""
        # First, get a detailed plan from LLM
        plan_steps = self.llm_planner.plan_from_natural_language(goal, context)

        # Group steps into logical subtasks
        subtasks = self.group_steps_into_subtasks(plan_steps)

        # Create main task
        main_task = Task(
            id=f"task_{len(self.tasks)}",
            name=goal,
            description=f"High-level task: {goal}",
            steps=[],
            dependencies=[]
        )

        # Add subtasks
        for i, subtask_steps in enumerate(subtasks):
            subtask = Task(
                id=f"{main_task.id}_subtask_{i}",
                name=f"Subtask {i+1}",
                description=f"Subtask for: {goal}",
                steps=subtask_steps,
                dependencies=[],
                priority=i
            )
            self.tasks[subtask.id] = subtask

            # Add dependency on previous subtask
            if i > 0:
                subtask.dependencies.append(f"{main_task.id}_subtask_{i-1}")

        main_task.steps = plan_steps
        self.tasks[main_task.id] = main_task

        return main_task

    def group_steps_into_subtasks(self, steps: List[PlanStep]) -> List[List[PlanStep]]:
        """Group plan steps into logical subtasks"""
        subtasks = []
        current_subtask = []

        for step in steps:
            # Group related actions together
            if current_subtask and self.are_steps_related(current_subtask[-1], step):
                current_subtask.append(step)
            else:
                if current_subtask:
                    subtasks.append(current_subtask)
                current_subtask = [step]

        if current_subtask:
            subtasks.append(current_subtask)

        return subtasks

    def are_steps_related(self, step1: PlanStep, step2: PlanStep) -> bool:
        """Determine if two steps are related and should be grouped"""
        # Same action type
        if step1.action == step2.action:
            return True

        # Sequential navigation steps
        navigation_actions = ["move_to", "navigate_to_object"]
        if step1.action in navigation_actions and step2.action in navigation_actions:
            return True

        # Perception followed by action
        perception_actions = ["detect_object"]
        if step1.action in perception_actions and step2.action not in perception_actions:
            return True

        return False

    def execute_task(self, task_id: str) -> bool:
        """Execute a task and its subtasks"""
        task = self.tasks.get(task_id)
        if not task:
            return False

        task.status = TaskStatus.IN_PROGRESS
        self.active_tasks.append(task_id)

        success = True
        for step in task.steps:
            step_success = self.execute_plan_step(step)
            if not step_success:
                success = False
                task.status = TaskStatus.FAILED
                break

        if success:
            task.status = TaskStatus.COMPLETED

        self.active_tasks.remove(task_id)
        return success

    def execute_plan_step(self, step: PlanStep) -> bool:
        """Execute a single plan step"""
        # This would interface with the actual robot execution system
        print(f"Executing: {step.description}")
        print(f"Action: {step.action}")
        print(f"Parameters: {step.parameters}")

        # In a real implementation, this would call the robot's action system
        # For simulation, we'll return success
        return True
```

> [!hardware]
> **Hardware Note**: The LLM planner for the Unitree H1 humanoid robot must account for the robot's physical constraints, including balance requirements, joint limits, and the time needed for bipedal locomotion. The planner should generate plans that are physically realizable and maintain the robot's stability throughout execution.

## Context and Memory Management

### World Model and Context Tracking

Maintaining context for intelligent planning:

```python
from datetime import datetime
import copy

class WorldModel:
    def __init__(self):
        self.objects = {}
        self.locations = {}
        self.robot_state = {}
        self.human_interactions = []
        self.update_history = []

    def update_object(self, obj_id: str, properties: Dict[str, Any]):
        """Update information about an object"""
        if obj_id not in self.objects:
            self.objects[obj_id] = {"id": obj_id, "first_seen": datetime.now()}

        self.objects[obj_id].update(properties)
        self.objects[obj_id]["last_updated"] = datetime.now()

        self.update_history.append({
            "type": "object_update",
            "object_id": obj_id,
            "properties": properties,
            "timestamp": datetime.now()
        })

    def update_location(self, location_id: str, properties: Dict[str, Any]):
        """Update information about a location"""
        if location_id not in self.locations:
            self.locations[location_id] = {"id": location_id}

        self.locations[location_id].update(properties)

    def update_robot_state(self, state: Dict[str, Any]):
        """Update robot state information"""
        self.robot_state.update(state)
        self.update_history.append({
            "type": "robot_state_update",
            "state": state,
            "timestamp": datetime.now()
        })

    def get_context_for_planning(self) -> Dict[str, Any]:
        """Get current context for planning"""
        return {
            "current_time": datetime.now().isoformat(),
            "robot_position": self.robot_state.get("position"),
            "robot_battery": self.robot_state.get("battery_level"),
            "detected_objects": list(self.objects.values()),
            "known_locations": list(self.locations.values()),
            "recent_interactions": self.human_interactions[-5:] if self.human_interactions else []
        }

    def predict_outcome(self, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Predict the outcome of an action"""
        # This would use a physics simulator or learned models
        # For now, return a simple prediction
        predicted_state = copy.deepcopy(self.robot_state)

        if action == "move_to":
            predicted_state["position"] = parameters.get("location")
        elif action == "grasp_object":
            obj_id = parameters.get("object_id")
            if obj_id in self.objects:
                self.objects[obj_id]["grasped"] = True
                predicted_state["held_object"] = obj_id

        return {
            "predicted_state": predicted_state,
            "predicted_effects": [f"robot_moved_to_{parameters.get('location')}"] if action == "move_to" else []
        }

class ContextualPlanner:
    def __init__(self, llm_planner: LLMPlanner):
        self.llm_planner = llm_planner
        self.world_model = WorldModel()
        self.conversation_context = []

    def plan_with_context(self, goal: str) -> List[PlanStep]:
        """Plan with current world context"""
        # Get current context
        context = self.world_model.get_context_for_planning()

        # Add recent conversation history
        context["conversation_history"] = self.conversation_context[-3:]

        # Generate plan with context
        plan = self.llm_planner.plan_from_natural_language(goal, context)

        # Validate plan against current state
        validated_plan = self.validate_plan(plan)

        return validated_plan

    def validate_plan(self, plan: List[PlanStep]) -> List[PlanStep]:
        """Validate plan against current world state"""
        validated_plan = []

        for step in plan:
            if self.is_step_feasible(step):
                validated_plan.append(step)
            else:
                # Try to adapt the step or find an alternative
                adapted_step = self.adapt_step(step)
                if adapted_step:
                    validated_plan.append(adapted_step)

        return validated_plan

    def is_step_feasible(self, step: PlanStep) -> bool:
        """Check if a step is feasible given current state"""
        capability = self.llm_planner.capabilities.get(step.action)
        if not capability:
            return False

        # Check preconditions
        for precondition in capability.preconditions:
            if not self.check_precondition(precondition, step.parameters):
                return False

        return True

    def check_precondition(self, precondition: str, parameters: Dict[str, Any]) -> bool:
        """Check if a precondition is satisfied"""
        if precondition == "robot_is_active":
            return self.world_model.robot_state.get("active", False)
        elif precondition == "location_is_safe":
            location = parameters.get("location")
            if location:
                location_info = self.world_model.locations.get(location, {})
                return location_info.get("safe", True)
        elif precondition == "object_is_reachable":
            obj_id = parameters.get("object_id")
            if obj_id in self.world_model.objects:
                obj_info = self.world_model.objects[obj_id]
                return obj_info.get("reachable", True)
        elif precondition == "hand_is_free":
            hand = parameters.get("hand", "right")
            return not bool(self.world_model.robot_state.get(f"{hand}_hand_holds_object"))

        return True

    def adapt_step(self, step: PlanStep) -> Optional[PlanStep]:
        """Adapt a step to make it feasible"""
        # Try to find an alternative approach
        if step.action == "move_to":
            # Check if there's an alternative route
            return self.find_alternative_route(step)
        elif step.action == "grasp_object":
            # Check if there's an alternative object
            return self.find_alternative_object(step)

        return None

    def find_alternative_route(self, step: PlanStep) -> Optional[PlanStep]:
        """Find an alternative route to the destination"""
        # This would interface with navigation system
        # For now, return the original step
        return step

    def find_alternative_object(self, step: PlanStep) -> Optional[PlanStep]:
        """Find an alternative object to grasp"""
        # Look for similar objects
        target_type = step.parameters.get("object_type")
        if target_type:
            for obj_id, obj_info in self.world_model.objects.items():
                if obj_info.get("type") == target_type and not obj_info.get("grasped"):
                    new_step = copy.deepcopy(step)
                    new_step.parameters["object_id"] = obj_id
                    return new_step

        return None

    def update_context_after_execution(self, step: PlanStep, success: bool):
        """Update context based on step execution result"""
        if success:
            # Update world model with effects of the action
            capability = self.llm_planner.capabilities.get(step.action)
            if capability:
                for effect in capability.effects:
                    self.apply_effect(effect, step.parameters)

    def apply_effect(self, effect: str, parameters: Dict[str, Any]):
        """Apply the effect of an action to the world model"""
        if effect == "robot_position_changes":
            new_pos = parameters.get("location")
            if new_pos:
                self.world_model.update_robot_state({"position": new_pos})
        elif effect == "object_is_grasped":
            obj_id = parameters.get("object_id")
            if obj_id:
                self.world_model.update_object(obj_id, {"grasped": True})
                hand = parameters.get("hand", "right")
                self.world_model.update_robot_state({f"{hand}_hand_holds_object": obj_id})
```

## Planning with Uncertainty

### Robust Planning Under Uncertainty

Handling uncertainty in LLM-based planning:

```python
import random
from typing import Tuple

class UncertaintyAwarePlanner:
    def __init__(self, contextual_planner: ContextualPlanner):
        self.contextual_planner = contextual_planner
        self.uncertainty_models = self.initialize_uncertainty_models()

    def initialize_uncertainty_models(self):
        """Initialize models for different types of uncertainty"""
        return {
            "action_success": {
                "move_to": 0.95,  # 95% success rate
                "grasp_object": 0.85,  # 85% success rate
                "detect_object": 0.90,  # 90% success rate
            },
            "object_location": {
                "precision": 0.1,  # meters uncertainty
                "drift_rate": 0.01  # meters per minute
            },
            "human_behavior": {
                "cooperation_probability": 0.8,
                "response_time_mean": 5.0,  # seconds
                "response_time_std": 2.0
            }
        }

    def plan_with_uncertainty(self, goal: str, risk_tolerance: float = 0.1) -> List[PlanStep]:
        """Plan while considering uncertainty"""
        # Generate initial plan
        plan = self.contextual_planner.plan_with_context(goal)

        # Evaluate plan robustness
        robust_plan = self.make_plan_robust(plan, risk_tolerance)

        return robust_plan

    def make_plan_robust(self, plan: List[PlanStep], risk_tolerance: float) -> List[PlanStep]:
        """Make the plan more robust to uncertainties"""
        robust_plan = []

        for step in plan:
            # Calculate success probability
            success_prob = self.estimate_step_success_probability(step)

            if success_prob < (1 - risk_tolerance):
                # Add recovery actions
                robust_plan.extend(self.add_recovery_actions(step))
            else:
                robust_plan.append(step)

        return robust_plan

    def estimate_step_success_probability(self, step: PlanStep) -> float:
        """Estimate the probability of step success"""
        base_prob = self.uncertainty_models["action_success"].get(step.action, 0.9)

        # Adjust for specific parameters
        if step.action == "move_to":
            # Longer distances might have lower success
            distance = self.estimate_travel_distance(step.parameters.get("location"))
            if distance and distance > 5.0:  # More than 5 meters
                base_prob *= 0.9  # Reduce success probability

        elif step.action == "grasp_object":
            # Fragile objects might have lower success
            obj_id = step.parameters.get("object_id")
            if obj_id in self.contextual_planner.world_model.objects:
                obj = self.contextual_planner.world_model.objects[obj_id]
                fragility = obj.get("fragility", 0.5)
                base_prob *= (1 - fragility * 0.3)  # Reduce for fragile objects

        return base_prob

    def estimate_travel_distance(self, location: str) -> Optional[float]:
        """Estimate travel distance to a location"""
        # This would use the robot's map
        # For now, return a placeholder
        return random.uniform(1.0, 10.0)

    def add_recovery_actions(self, original_step: PlanStep) -> List[PlanStep]:
        """Add recovery actions for a potentially failed step"""
        recovery_steps = [original_step]

        if original_step.action == "move_to":
            # Add verification step
            verify_step = PlanStep(
                action="detect_object",
                parameters={"object_type": "landmark", "search_area": "current_position"},
                description="Verify current position after movement"
            )
            recovery_steps.append(verify_step)

            # Add repositioning if needed
            reposition_step = PlanStep(
                action="move_to",
                parameters=original_step.parameters,
                description="Reposition if initial movement was inaccurate"
            )
            recovery_steps.append(reposition_step)

        elif original_step.action == "grasp_object":
            # Add retry mechanism
            retry_step = PlanStep(
                action="grasp_object",
                parameters=original_step.parameters,
                description="Retry grasp if first attempt failed"
            )
            recovery_steps.append(retry_step)

            # Add alternative grasp
            alt_grasp_step = PlanStep(
                action="grasp_object",
                parameters={**original_step.parameters, "grasp_type": "power"},
                description="Use power grasp if precision grasp failed"
            )
            recovery_steps.append(alt_grasp_step)

        return recovery_steps

    def handle_execution_uncertainty(self, step: PlanStep) -> Tuple[bool, Dict[str, Any]]:
        """Handle uncertainty during execution"""
        success_prob = self.estimate_step_success_probability(step)

        # Simulate success/failure based on probability
        success = random.random() < success_prob

        execution_info = {
            "success_probability": success_prob,
            "actual_success": success,
            "execution_time": random.uniform(1.0, 5.0),  # Simulated execution time
            "recovery_needed": not success
        }

        return success, execution_info

    def replan_on_failure(self, failed_step: PlanStep, failure_reason: str) -> Optional[List[PlanStep]]:
        """Generate an alternative plan when a step fails"""
        # Create context about the failure
        failure_context = {
            "failed_step": failed_step,
            "failure_reason": failure_reason,
            "current_state": self.contextual_planner.world_model.get_context_for_planning()
        }

        # Generate alternative approach
        alternative_prompt = f"""
        The previous step failed: {failed_step.description}
        Failure reason: {failure_reason}

        Generate an alternative approach to achieve the same goal.
        Consider the failure and propose a different strategy.
        """

        # This would call the LLM again with failure context
        # For now, return a simple alternative
        if failed_step.action == "move_to":
            return [PlanStep(
                action="navigate_to_object",
                parameters={"object_id": "waypoint_123"},
                description="Use waypoint navigation as alternative"
            )]

        return None
```

## Multi-Agent Coordination

### Coordinating with Other Systems

Integrating LLM planning with other robot systems:

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class MultiAgentPlanner:
    def __init__(self, llm_planner: LLMPlanner, uncertainty_planner: UncertaintyAwarePlanner):
        self.llm_planner = llm_planner
        self.uncertainty_planner = uncertainty_planner
        self.executor = ThreadPoolExecutor(max_workers=4)

        # Integration with other systems
        self.navigation_system = None
        self.manipulation_system = None
        self.perception_system = None
        self.speech_system = None

    def set_robot_systems(
        self,
        navigation_system,
        manipulation_system,
        perception_system,
        speech_system
    ):
        """Set references to other robot systems"""
        self.navigation_system = navigation_system
        self.manipulation_system = manipulation_system
        self.perception_system = perception_system
        self.speech_system = speech_system

    async def execute_plan_async(self, plan: List[PlanStep]) -> Dict[str, Any]:
        """Execute a plan asynchronously with system coordination"""
        results = {
            "steps_executed": 0,
            "steps_successful": 0,
            "steps_failed": 0,
            "total_time": 0,
            "details": []
        }

        start_time = asyncio.get_event_loop().time()

        for i, step in enumerate(plan):
            print(f"Executing step {i+1}/{len(plan)}: {step.description}")

            # Check for system availability
            if not await self.check_system_availability(step):
                results["steps_failed"] += 1
                results["details"].append({
                    "step": step,
                    "status": "failed",
                    "reason": "system_unavailable"
                })
                continue

            # Execute the step with appropriate system
            success, execution_time = await self.execute_step_with_system(step)

            if success:
                results["steps_successful"] += 1
                status = "success"
            else:
                results["steps_failed"] += 1
                status = "failed"

            results["details"].append({
                "step": step,
                "status": status,
                "execution_time": execution_time
            })

            results["steps_executed"] += 1

        results["total_time"] = asyncio.get_event_loop().time() - start_time
        return results

    async def check_system_availability(self, step: PlanStep) -> bool:
        """Check if required systems are available for step execution"""
        if step.action in ["move_to", "navigate_to_object"]:
            return self.navigation_system is not None and self.navigation_system.is_available()
        elif step.action in ["grasp_object", "release_object"]:
            return self.manipulation_system is not None and self.manipulation_system.is_available()
        elif step.action in ["detect_object"]:
            return self.perception_system is not None and self.perception_system.is_available()
        elif step.action in ["speak", "greet_person"]:
            return self.speech_system is not None and self.speech_system.is_available()

        return True  # Assume available for other actions

    async def execute_step_with_system(self, step: PlanStep) -> Tuple[bool, float]:
        """Execute a step using the appropriate robot system"""
        start_time = asyncio.get_event_loop().time()

        if step.action in ["move_to", "navigate_to_object"]:
            success = await self.execute_navigation_step(step)
        elif step.action in ["grasp_object", "release_object"]:
            success = await self.execute_manipulation_step(step)
        elif step.action in ["detect_object"]:
            success = await self.execute_perception_step(step)
        elif step.action in ["speak", "greet_person"]:
            success = await self.execute_speech_step(step)
        else:
            # For other actions, use generic execution
            success = await self.execute_generic_step(step)

        execution_time = asyncio.get_event_loop().time() - start_time
        return success, execution_time

    async def execute_navigation_step(self, step: PlanStep) -> bool:
        """Execute navigation-related steps"""
        loop = asyncio.get_event_loop()
        try:
            # Call navigation system
            future = loop.run_in_executor(
                self.executor,
                self.navigation_system.navigate_to,
                step.parameters
            )
            result = await asyncio.wait_for(future, timeout=30.0)
            return result.get("success", False)
        except asyncio.TimeoutError:
            print(f"Navigation step timed out: {step.description}")
            return False
        except Exception as e:
            print(f"Navigation step failed: {e}")
            return False

    async def execute_manipulation_step(self, step: PlanStep) -> bool:
        """Execute manipulation-related steps"""
        loop = asyncio.get_event_loop()
        try:
            future = loop.run_in_executor(
                self.executor,
                self.manipulation_system.execute_grasp,
                step.parameters
            )
            result = await asyncio.wait_for(future, timeout=15.0)
            return result.get("success", False)
        except asyncio.TimeoutError:
            print(f"Manipulation step timed out: {step.description}")
            return False
        except Exception as e:
            print(f"Manipulation step failed: {e}")
            return False

    async def execute_perception_step(self, step: PlanStep) -> bool:
        """Execute perception-related steps"""
        loop = asyncio.get_event_loop()
        try:
            future = loop.run_in_executor(
                self.executor,
                self.perception_system.detect_objects,
                step.parameters
            )
            result = await asyncio.wait_for(future, timeout=10.0)
            return result.get("success", False)
        except asyncio.TimeoutError:
            print(f"Perception step timed out: {step.description}")
            return False
        except Exception as e:
            print(f"Perception step failed: {e}")
            return False

    async def execute_speech_step(self, step: PlanStep) -> bool:
        """Execute speech-related steps"""
        loop = asyncio.get_event_loop()
        try:
            future = loop.run_in_executor(
                self.executor,
                self.speech_system.speak,
                step.parameters.get("message", "")
            )
            result = await asyncio.wait_for(future, timeout=5.0)
            return result.get("success", False)
        except asyncio.TimeoutError:
            print(f"Speech step timed out: {step.description}")
            return False
        except Exception as e:
            print(f"Speech step failed: {e}")
            return False

    async def execute_generic_step(self, step: PlanStep) -> bool:
        """Execute generic steps"""
        # For now, assume generic steps succeed
        # In a real system, this would interface with other components
        return True

    def generate_explanation(self, plan: List[PlanStep], results: Dict[str, Any]) -> str:
        """Generate a natural language explanation of plan execution"""
        success_rate = results["steps_successful"] / max(results["steps_executed"], 1)

        explanation = f"I executed a plan with {len(plan)} steps. "
        explanation += f"Successfully completed {results['steps_successful']} out of {results['steps_executed']} steps "
        explanation += f"(success rate: {success_rate:.1%}). "

        if results["steps_failed"] > 0:
            explanation += "Some steps failed, but I handled them appropriately. "

        explanation += "The entire plan took {:.1f} seconds to execute.".format(results["total_time"])

        return explanation
```

## Planning Optimization

### Performance and Efficiency Improvements

Optimizing LLM planning for real-time humanoid applications:

```python
import time
import functools
from typing import Callable

class OptimizedLLMPlanner:
    def __init__(self, llm_planner: LLMPlanner):
        self.llm_planner = llm_planner
        self.cache = {}
        self.metrics = {
            "api_calls": 0,
            "cache_hits": 0,
            "average_response_time": 0,
            "total_planning_time": 0
        }

    def cache_plans(func):
        """Decorator to cache planning results"""
        @functools.wraps(func)
        def wrapper(self, goal: str, context: Dict[str, Any] = None, use_cache: bool = True):
            # Create cache key
            cache_key = self.create_cache_key(goal, context)

            if use_cache and cache_key in self.cache:
                self.metrics["cache_hits"] += 1
                return self.cache[cache_key]

            start_time = time.time()
            result = func(self, goal, context, use_cache)
            planning_time = time.time() - start_time

            self.metrics["total_planning_time"] += planning_time

            if use_cache:
                self.cache[cache_key] = result

            return result
        return wrapper

    def create_cache_key(self, goal: str, context: Dict[str, Any]) -> str:
        """Create a cache key for the planning request"""
        import hashlib
        import json

        cache_input = {
            "goal": goal,
            "context_keys": sorted(context.keys()) if context else []
        }

        cache_str = json.dumps(cache_input, sort_keys=True)
        return hashlib.md5(cache_str.encode()).hexdigest()

    @cache_plans
    def plan_from_natural_language(self, goal: str, context: Dict[str, Any] = None, use_cache: bool = True) -> List[PlanStep]:
        """Optimized planning with caching"""
        self.metrics["api_calls"] += 1

        # Use the original LLM planner
        return self.llm_planner.plan_from_natural_language(goal, context)

    def precompute_common_plans(self):
        """Precompute plans for common tasks"""
        common_goals = [
            "greet a person",
            "move to the kitchen",
            "pick up a red cup",
            "bring me water",
            "find my keys"
        ]

        for goal in common_goals:
            # Precompute with empty context
            self.plan_from_natural_language(goal, {}, use_cache=True)

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for the planner"""
        total_calls = self.metrics["api_calls"]
        cache_hit_rate = self.metrics["cache_hits"] / total_calls if total_calls > 0 else 0

        return {
            "api_calls_made": self.metrics["api_calls"],
            "cache_hit_rate": f"{cache_hit_rate:.1%}",
            "cache_size": len(self.cache),
            "total_planning_time": f"{self.metrics['total_planning_time']:.2f}s",
            "average_planning_time": f"{self.metrics['total_planning_time'] / max(total_calls, 1):.2f}s per call"
        }

    def optimize_for_frequency(self, goal: str, frequency: str = "high") -> List[PlanStep]:
        """Optimize plan for frequency of execution"""
        if frequency == "high":
            # For frequently executed goals, use more deterministic approaches
            return self.get_optimized_plan_for_frequent_goal(goal)
        else:
            # For rare goals, use full LLM planning
            return self.plan_from_natural_language(goal)

    def get_optimized_plan_for_frequent_goal(self, goal: str) -> List[PlanStep]:
        """Get optimized plan for frequently executed goals"""
        # Use template-based planning for common goals
        templates = {
            "greet": [
                PlanStep("detect_object", {"object_type": "person"}, "Detect person to greet"),
                PlanStep("speak", {"message": "Hello! Nice to meet you."}, "Greet the person")
            ],
            "move_to": [
                PlanStep("navigate_to_object", {"object_id": "destination"}, "Navigate to destination")
            ],
            "pick_up": [
                PlanStep("detect_object", {"object_type": "item"}, "Find the item"),
                PlanStep("navigate_to_object", {"object_id": "item"}, "Move to item location"),
                PlanStep("grasp_object", {"object_id": "item"}, "Grasp the item")
            ]
        }

        # Simple keyword matching for template selection
        goal_lower = goal.lower()
        if "greet" in goal_lower or "hello" in goal_lower:
            return templates["greet"]
        elif "move" in goal_lower or "go to" in goal_lower:
            return templates["move_to"]
        elif "pick up" in goal_lower or "grasp" in goal_lower:
            return templates["pick_up"]

        # Fall back to LLM planning
        return self.plan_from_natural_language(goal)

def llm_planner_best_practices():
    """Best practices for LLM-based planning"""

    practices = [
        "Use context-aware planning that considers current robot state",
        "Implement caching for common planning requests",
        "Handle uncertainty with probabilistic reasoning",
        "Validate plans against physical constraints",
        "Provide fallback mechanisms for failed steps",
        "Maintain conversation context for natural interaction",
        "Optimize for real-time performance with precomputed templates",
        "Monitor and log planning performance metrics",
        "Use hierarchical planning for complex tasks",
        "Integrate with other robot systems for coordinated execution"
    ]

    for i, practice in enumerate(practices, 1):
        print(f"{i}. {practice}")

## Summary

LLM planners provide powerful high-level reasoning capabilities for humanoid robots, enabling complex goal-directed behavior through natural language interaction. By combining LLMs with robot capabilities, world modeling, and uncertainty handling, these systems can generate sophisticated plans that adapt to changing conditions and handle failures gracefully. Proper optimization and integration with other robot systems ensure efficient and reliable execution of LLM-generated plans.