---
id: integration
title: Integration
sidebar_position: 3
---

# Integration

System integration is the critical phase where all individual components of the humanoid robot system are combined and validated as a cohesive whole. This chapter details the integration process, addressing challenges, methodologies, and best practices for achieving successful system integration.

## Integration Strategy

### Modular Integration Approach

The integration follows a modular, bottom-up approach where components are integrated incrementally:

1. **Component Level**: Individual modules are validated independently
2. **Subsystem Level**: Related components are integrated and tested
3. **System Level**: All subsystems are integrated and validated
4. **Deployment Level**: System is validated in operational environment

### Integration Timeline

```
Week 1-2: Component Integration
├── Vision system integration
├── Audio system integration
├── Navigation system integration
└── Manipulation system integration

Week 3-4: Subsystem Integration
├── Perception subsystem
├── Cognition subsystem
├── Action subsystem
└── Safety subsystem

Week 5-6: System Integration
├── End-to-end workflow integration
├── Safety system validation
├── Performance optimization
└── Bug fixing and refinement

Week 7-8: Deployment Integration
├── Hardware-software integration
├── Real-world testing
├── Performance validation
└── Final system validation
```

## Component Integration

### Vision System Integration

Integrating the perception components into a cohesive vision pipeline:

```python
# vision_integration.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from vision_msgs.msg import Detection2DArray
from std_msgs.msg import String
import cv2
from cv_bridge import CvBridge
import threading
import queue

class VisionSystemIntegration(Node):
    def __init__(self):
        super().__init__('vision_system_integration')

        # Initialize components
        self.cv_bridge = CvBridge()
        self.object_detector = ObjectDetector(self)
        self.depth_processor = DepthProcessor(self)
        self.tracker = ObjectTracker(self)

        # Initialize queues for component communication
        self.image_queue = queue.Queue(maxsize=5)
        self.detection_queue = queue.Queue(maxsize=5)

        # Publishers and subscribers
        self.image_sub = self.create_subscription(
            Image, '/h1/camera/rgb/image_raw', self.image_callback, 10
        )
        self.depth_sub = self.create_subscription(
            Image, '/h1/camera/depth/image_raw', self.depth_callback, 10
        )
        self.detection_pub = self.create_publisher(
            Detection2DArray, '/h1/vision/detections', 10
        )
        self.tracking_pub = self.create_publisher(
            String, '/h1/vision/tracking', 10
        )

        # Start processing threads
        self.processing_thread = threading.Thread(target=self.processing_loop)
        self.processing_thread.daemon = True
        self.processing_thread.start()

    def image_callback(self, msg):
        """Receive and queue image for processing"""
        try:
            if not self.image_queue.full():
                self.image_queue.put(msg)
        except queue.Full:
            self.get_logger().warn('Image queue is full, dropping frame')

    def depth_callback(self, msg):
        """Receive depth image"""
        self.latest_depth = msg

    def processing_loop(self):
        """Main processing loop for vision pipeline"""
        while rclpy.ok():
            try:
                # Get image from queue
                if not self.image_queue.empty():
                    image_msg = self.image_queue.get(timeout=0.1)

                    # Process with all vision components
                    cv_image = self.cv_bridge.imgmsg_to_cv2(image_msg, desired_encoding='bgr8')

                    # 1. Object detection
                    detections = self.object_detector.detect(cv_image)

                    # 2. Depth processing for 3D positions
                    if hasattr(self, 'latest_depth'):
                        detections_3d = self.depth_processor.process_3d_positions(
                            detections, self.latest_depth
                        )
                    else:
                        detections_3d = detections

                    # 3. Object tracking
                    tracked_objects = self.tracker.update_tracking(detections_3d)

                    # 4. Publish results
                    self.publish_detections(tracked_objects, image_msg.header)
                    self.publish_tracking_info(tracked_objects)

            except queue.Empty:
                continue
            except Exception as e:
                self.get_logger().error(f'Processing error: {e}')

    def publish_detections(self, detections, header):
        """Publish detection results"""
        detection_msg = Detection2DArray()
        detection_msg.header = header

        for detection in detections:
            detection_2d = Detection2D()
            detection_2d.bbox.size_x = detection['bbox'][2] - detection['bbox'][0]
            detection_2d.bbox.size_y = detection['bbox'][3] - detection['bbox'][1]
            detection_2d.bbox.center.x = (detection['bbox'][0] + detection['bbox'][2]) / 2
            detection_2d.bbox.center.y = (detection['bbox'][1] + detection['bbox'][3]) / 2

            hypothesis = ObjectHypothesisWithPose()
            hypothesis.hypothesis.object_name = detection['label']
            hypothesis.hypothesis.score = detection['confidence']
            detection_2d.results.append(hypothesis)

            detection_msg.detections.append(detection_2d)

        self.detection_pub.publish(detection_msg)

    def publish_tracking_info(self, tracked_objects):
        """Publish tracking information"""
        tracking_msg = String()
        tracking_data = {
            'timestamp': self.get_clock().now().to_msg(),
            'objects': [
                {
                    'id': obj['id'],
                    'label': obj['label'],
                    'position': obj['position_3d'],
                    'velocity': obj['velocity'] if 'velocity' in obj else [0, 0, 0]
                } for obj in tracked_objects
            ]
        }
        tracking_msg.data = json.dumps(tracking_data)
        self.tracking_pub.publish(tracking_msg)

class ObjectDetector:
    def __init__(self, node):
        self.node = node
        self.model = self.load_model()

    def load_model(self):
        """Load object detection model"""
        import ultralytics
        return ultralytics.YOLO('yolov8x-seg.pt')

    def detect(self, image):
        """Run object detection on image"""
        results = self.model(image, conf=0.5)
        detections = []

        for result in results:
            for box in result.boxes:
                detections.append({
                    'bbox': [int(box.xyxy[0][0]), int(box.xyxy[0][1]),
                            int(box.xyxy[0][2]), int(box.xyxy[0][3])],
                    'label': result.names[int(box.cls)],
                    'confidence': float(box.conf),
                    'mask': result.masks[int(box.id)] if result.masks is not None else None
                })

        return detections

class DepthProcessor:
    def __init__(self, node):
        self.node = node
        self.camera_info = None

    def process_3d_positions(self, detections, depth_msg):
        """Convert 2D detections to 3D positions using depth"""
        if depth_msg is None:
            return detections

        # Convert depth image to numpy array
        depth_image = self.node.cv_bridge.imgmsg_to_cv2(depth_msg, desired_encoding='32FC1')

        detections_3d = []
        for detection in detections:
            bbox = detection['bbox']
            center_x = int((bbox[0] + bbox[2]) / 2)
            center_y = int((bbox[1] + bbox[3]) / 2)

            # Get depth at center of bounding box
            depth = depth_image[center_y, center_x] if depth_image is not None else 0.0

            # Convert pixel coordinates to 3D world coordinates
            world_pos = self.pixel_to_world(center_x, center_y, depth, self.camera_info)

            detection_3d = detection.copy()
            detection_3d['position_3d'] = world_pos
            detections_3d.append(detection_3d)

        return detections_3d

    def pixel_to_world(self, u, v, depth, camera_info):
        """Convert pixel coordinates to world coordinates"""
        if camera_info is None:
            # Default camera parameters
            fx, fy = 616.171, 616.44
            cx, cy = 310.095, 236.027
        else:
            fx = camera_info.k[0]  # fx
            fy = camera_info.k[4]  # fy
            cx = camera_info.k[2]  # cx
            cy = camera_info.k[5]  # cy

        x = (u - cx) * depth / fx
        y = (v - cy) * depth / fy
        z = depth

        return [x, y, z]

class ObjectTracker:
    def __init__(self, node):
        self.node = node
        self.trackers = {}  # Trackers for each object
        self.next_id = 0

    def update_tracking(self, detections):
        """Update object tracking with new detections"""
        # This is a simplified tracking implementation
        # In practice, use SORT, DeepSORT, or similar tracking algorithm
        for detection in detections:
            if 'id' not in detection:
                detection['id'] = self.next_id
                self.next_id += 1

        return detections
```

> [!hardware]
> **Hardware Note**: When integrating the vision system with the Unitree H1, special attention must be paid to the synchronization between RGB and depth cameras, as well as the calibration of the stereo vision system. The integration must account for the robot's mechanical vibrations which can affect image quality and depth measurements.

### Audio System Integration

Integrating audio processing components for robust speech interaction:

```python
# audio_integration.py
import pyaudio
import numpy as np
import webrtcvad
import threading
import queue
from scipy import signal
from std_msgs.msg import String
from audio_common_msgs.msg import AudioData

class AudioSystemIntegration(Node):
    def __init__(self):
        super().__init__('audio_system_integration')

        # Initialize audio components
        self.vad = webrtcvad.Vad(2)  # Voice activity detector
        self.noise_reducer = NoiseReducer()
        self.speech_recognizer = SpeechRecognizer(self)
        self.text_to_speech = TextToSpeech(self)

        # Audio processing queues
        self.audio_queue = queue.Queue(maxsize=10)
        self.speech_queue = queue.Queue(maxsize=5)

        # Publishers and subscribers
        self.audio_sub = self.create_subscription(
            AudioData, '/h1/audio/raw', self.audio_callback, 10
        )
        self.speech_pub = self.create_publisher(
            String, '/h1/audio/speech_recognition', 10
        )
        self.tts_sub = self.create_subscription(
            String, '/h1/audio/tts_request', self.tts_callback, 10
        )

        # Start audio processing thread
        self.processing_thread = threading.Thread(target=self.processing_loop)
        self.processing_thread.daemon = True
        self.processing_thread.start()

    def audio_callback(self, msg):
        """Receive audio data and queue for processing"""
        try:
            if not self.audio_queue.full():
                self.audio_queue.put(msg)
        except queue.Full:
            self.get_logger().warn('Audio queue is full, dropping samples')

    def processing_loop(self):
        """Main audio processing loop"""
        while rclpy.ok():
            try:
                if not self.audio_queue.empty():
                    audio_msg = self.audio_queue.get(timeout=0.1)

                    # Convert to numpy array
                    audio_data = np.frombuffer(audio_msg.data, dtype=np.int16)

                    # 1. Apply noise reduction
                    clean_audio = self.noise_reducer.reduce_noise(audio_data)

                    # 2. Detect voice activity
                    if self.is_speech_present(clean_audio):
                        # 3. Perform speech recognition
                        text = self.speech_recognizer.recognize(clean_audio)

                        if text.strip():
                            # 4. Publish recognized text
                            text_msg = String()
                            text_msg.data = text
                            self.speech_pub.publish(text_msg)

            except queue.Empty:
                continue
            except Exception as e:
                self.get_logger().error(f'Audio processing error: {e}')

    def is_speech_present(self, audio_data):
        """Detect if speech is present in audio data"""
        # Convert to 16kHz mono for VAD (assuming original is 16kHz)
        if len(audio_data.shape) > 1:  # Multi-channel
            mono_audio = np.mean(audio_data, axis=1)
        else:
            mono_audio = audio_data

        # Check voice activity in 20ms frames
        frame_size = int(16000 * 0.02)  # 20ms at 16kHz
        frames = [mono_audio[i:i+frame_size] for i in range(0, len(mono_audio), frame_size)]

        speech_frames = sum(1 for frame in frames if len(frame) == frame_size and
                          self.vad.is_speech(frame.astype(np.int16).tobytes(), 16000))

        # Consider speech if >20% of frames have voice activity
        return speech_frames / max(len(frames), 1) > 0.2

    def tts_callback(self, msg):
        """Handle text-to-speech request"""
        text = msg.data
        self.text_to_speech.speak(text)

class NoiseReducer:
    def __init__(self):
        # Initialize noise reduction parameters
        self.noise_profile = None
        self.alpha = 0.9  # Smoothing factor

    def reduce_noise(self, audio_data):
        """Apply noise reduction to audio data"""
        # This is a simplified spectral subtraction approach
        if self.noise_profile is None:
            # Estimate initial noise profile from beginning of audio
            self.estimate_noise_profile(audio_data[:48000])  # First 3 seconds at 16kHz

        # Convert to frequency domain
        fft_data = np.fft.fft(audio_data.astype(np.float32))
        magnitude = np.abs(fft_data)
        phase = np.angle(fft_data)

        # Apply noise reduction
        enhanced_magnitude = np.maximum(magnitude - self.noise_profile * 0.5, 0)

        # Convert back to time domain
        enhanced_fft = enhanced_magnitude * np.exp(1j * phase)
        enhanced_audio = np.real(np.fft.ifft(enhanced_fft)).astype(np.int16)

        return enhanced_audio

    def estimate_noise_profile(self, audio_segment):
        """Estimate noise profile from audio segment"""
        fft_segment = np.fft.fft(audio_segment.astype(np.float32))
        magnitude = np.abs(fft_segment)
        self.noise_profile = magnitude

class SpeechRecognizer:
    def __init__(self, node):
        self.node = node
        self.model = self.load_model()

    def load_model(self):
        """Load speech recognition model"""
        import whisper
        return whisper.load_model("base")

    def recognize(self, audio_data):
        """Perform speech recognition on audio data"""
        try:
            # Convert to float32 and normalize
            audio_float = audio_data.astype(np.float32) / 32768.0

            # Perform transcription
            result = self.model.transcribe(audio_float, language="en")
            return result["text"]
        except Exception as e:
            self.node.get_logger().error(f'Speech recognition error: {e}')
            return ""

class TextToSpeech:
    def __init__(self, node):
        self.node = node
        self.engine = pyttsx3.init()

    def speak(self, text):
        """Convert text to speech and play"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            self.node.get_logger().error(f'TTS error: {e}')
```

## Subsystem Integration

### Perception Subsystem Integration

Combining vision, audio, and sensor systems into a unified perception module:

```python
# perception_subsystem.py
from sensor_msgs.msg import Image, CameraInfo, Imu, LaserScan
from std_msgs.msg import String
from geometry_msgs.msg import PointStamped
import threading
import time

class PerceptionSubsystem(Node):
    def __init__(self):
        super().__init__('perception_subsystem')

        # Initialize all perception components
        self.vision_system = VisionSystemIntegration(self)
        self.audio_system = AudioSystemIntegration(self)
        self.sensor_fusion = SensorFusion(self)

        # Publishers for fused perception data
        self.perception_pub = self.create_publisher(
            String, '/h1/perception/fused_data', 10
        )

        # Subscribers for all sensor data
        self.imu_sub = self.create_subscription(
            Imu, '/h1/imu/data', self.imu_callback, 10
        )
        self.laser_sub = self.create_subscription(
            LaserScan, '/h1/laser_scan', self.laser_callback, 10
        )

        # Initialize sensor data storage
        self.imu_data = None
        self.laser_data = None
        self.vision_data = None
        self.audio_data = None

        # Data synchronization
        self.data_lock = threading.Lock()
        self.last_update_time = time.time()

    def imu_callback(self, msg):
        """Process IMU data"""
        with self.data_lock:
            self.imu_data = {
                'orientation': [msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w],
                'angular_velocity': [msg.angular_velocity.x, msg.angular_velocity.y, msg.angular_velocity.z],
                'linear_acceleration': [msg.linear_acceleration.x, msg.linear_acceleration.y, msg.linear_acceleration.z],
                'timestamp': msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
            }

    def laser_callback(self, msg):
        """Process laser scan data"""
        with self.data_lock:
            self.laser_data = {
                'ranges': list(msg.ranges),
                'intensities': list(msg.intensities),
                'angle_min': msg.angle_min,
                'angle_max': msg.angle_max,
                'angle_increment': msg.angle_increment,
                'time_increment': msg.time_increment,
                'scan_time': msg.scan_time,
                'range_min': msg.range_min,
                'range_max': msg.range_max,
                'timestamp': msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
            }

    def update_vision_data(self, vision_msg):
        """Update vision data from vision system"""
        with self.data_lock:
            self.vision_data = vision_msg

    def update_audio_data(self, audio_msg):
        """Update audio data from audio system"""
        with self.data_lock:
            self.audio_data = audio_msg

    def fuse_sensor_data(self):
        """Fuse data from all sensors"""
        with self.data_lock:
            # Check if we have recent data from all sensors
            current_time = time.time()
            if current_time - self.last_update_time > 1.0:  # 1 second timeout
                return None

            fused_data = {
                'timestamp': current_time,
                'vision': self.vision_data,
                'audio': self.audio_data,
                'imu': self.imu_data,
                'laser': self.laser_data
            }

            # Apply sensor fusion algorithms
            fused_data = self.apply_fusion_algorithms(fused_data)

            self.last_update_time = current_time
            return fused_data

    def apply_fusion_algorithms(self, data):
        """Apply sensor fusion algorithms"""
        # 1. Object localization using vision + IMU
        if data['vision'] and data['imu']:
            data['fused_objects'] = self.localize_objects_with_imu(
                data['vision'], data['imu']
            )

        # 2. Sound source localization using audio + IMU
        if data['audio'] and data['imu']:
            data['sound_sources'] = self.localize_sound_sources(
                data['audio'], data['imu']
            )

        # 3. Environment mapping using laser + vision
        if data['laser'] and data['vision']:
            data['environment_map'] = self.create_environment_map(
                data['laser'], data['vision']
            )

        return data

    def localize_objects_with_imu(self, vision_data, imu_data):
        """Improve object localization using IMU data"""
        # Compensate for robot orientation when calculating object positions
        if not vision_data or not imu_data:
            return []

        objects = []
        robot_orientation = imu_data['orientation']  # quaternion

        for obj in vision_data.get('objects', []):
            # Transform object position based on robot orientation
            world_position = self.transform_to_world_frame(
                obj['position_3d'], robot_orientation
            )
            obj['world_position'] = world_position
            objects.append(obj)

        return objects

    def transform_to_world_frame(self, position, orientation):
        """Transform position from robot frame to world frame"""
        import tf_transformations
        rotation_matrix = tf_transformations.quaternion_matrix(orientation)[:3, :3]
        world_position = rotation_matrix @ np.array(position)
        return world_position.tolist()

    def create_environment_map(self, laser_data, vision_data):
        """Create environment map combining laser and vision data"""
        # Combine laser range data with visual features
        environment_map = {
            'obstacles': self.extract_obstacles_from_laser(laser_data),
            'landmarks': self.extract_landmarks_from_vision(vision_data),
            'free_space': self.calculate_free_space(laser_data)
        }
        return environment_map

    def extract_obstacles_from_laser(self, laser_data):
        """Extract obstacles from laser scan"""
        if not laser_data:
            return []

        obstacles = []
        for i, range_val in enumerate(laser_data['ranges']):
            if range_val < laser_data['range_max'] and range_val > laser_data['range_min']:
                angle = laser_data['angle_min'] + i * laser_data['angle_increment']
                x = range_val * np.cos(angle)
                y = range_val * np.sin(angle)
                obstacles.append({'x': x, 'y': y, 'range': range_val})

        return obstacles

    def extract_landmarks_from_vision(self, vision_data):
        """Extract landmarks from vision data"""
        if not vision_data:
            return []

        landmarks = []
        for detection in vision_data.get('detections', []):
            if detection['confidence'] > 0.7:  # Confidence threshold
                landmarks.append({
                    'label': detection['label'],
                    'position': detection.get('position_3d', [0, 0, 0]),
                    'confidence': detection['confidence']
                })

        return landmarks

    def publish_fused_data(self):
        """Publish fused perception data"""
        fused_data = self.fuse_sensor_data()
        if fused_data:
            msg = String()
            msg.data = json.dumps(fused_data)
            self.perception_pub.publish(msg)
```

### Cognition Subsystem Integration

Integrating LLM, planning, and decision-making components:

```python
# cognition_subsystem.py
from std_msgs.msg import String
from geometry_msgs.msg import Pose
import json
import asyncio

class CognitionSubsystem(Node):
    def __init__(self):
        super().__init__('cognition_subsystem')

        # Initialize cognition components
        self.llm_interface = LLMIntegration(self)
        self.task_planner = TaskPlanner(self)
        self.memory_system = MemorySystem(self)
        self.decision_maker = DecisionMaker(self)

        # Publishers and subscribers
        self.command_sub = self.create_subscription(
            String, '/h1/cognition/command', self.command_callback, 10
        )
        self.perception_sub = self.create_subscription(
            String, '/h1/perception/fused_data', self.perception_callback, 10
        )
        self.plan_pub = self.create_publisher(
            String, '/h1/cognition/plan', 10
        )

        # Initialize context
        self.current_context = {}
        self.perception_data = None

    def command_callback(self, msg):
        """Process high-level command"""
        command = msg.data

        # Update memory with current context
        self.memory_system.update_context(command, self.current_context)

        # Generate plan using LLM
        plan = self.llm_interface.generate_plan(command, self.current_context)

        # Refine plan with task planner
        refined_plan = self.task_planner.refine_plan(plan)

        # Publish refined plan
        plan_msg = String()
        plan_msg.data = json.dumps(refined_plan)
        self.plan_pub.publish(plan_msg)

    def perception_callback(self, msg):
        """Update with perception data"""
        try:
            self.perception_data = json.loads(msg.data)
            self.update_context_with_perception()
        except json.JSONDecodeError:
            self.get_logger().error('Failed to decode perception data')

    def update_context_with_perception(self):
        """Update context with latest perception data"""
        if not self.perception_data:
            return

        # Extract relevant information from perception data
        context_update = {
            'objects': self.perception_data.get('fused_objects', []),
            'environment': self.perception_data.get('environment_map', {}),
            'sound_sources': self.perception_data.get('sound_sources', []),
            'timestamp': self.perception_data.get('timestamp')
        }

        self.current_context.update(context_update)

class MemorySystem:
    def __init__(self, node):
        self.node = node
        self.episodic_memory = []  # Recent experiences
        self.semantic_memory = {}  # General knowledge
        self.procedural_memory = {}  # How-to knowledge

    def update_context(self, command, context):
        """Update context with new information"""
        # Store the command and context for future reference
        episode = {
            'command': command,
            'context': context.copy(),
            'timestamp': self.node.get_clock().now().to_msg(),
            'episode_id': len(self.episodic_memory)
        }
        self.episodic_memory.append(episode)

        # Keep only recent episodes (last 100)
        if len(self.episodic_memory) > 100:
            self.episodic_memory = self.episodic_memory[-100:]

    def retrieve_relevant_memory(self, query):
        """Retrieve relevant memories for a query"""
        # Simple keyword-based retrieval
        relevant_episodes = []
        for episode in self.episodic_memory[-20:]:  # Check last 20 episodes
            if query.lower() in episode['command'].lower():
                relevant_episodes.append(episode)

        return relevant_episodes

class DecisionMaker:
    def __init__(self, node):
        self.node = node
        self.safety_thresholds = self.load_safety_thresholds()

    def load_safety_thresholds(self):
        """Load safety thresholds for decision making"""
        return {
            'collision_probability': 0.1,
            'balance_confidence': 0.3,
            'task_success_probability': 0.6
        }

    def make_decision(self, options, context):
        """Make decision among options considering safety and context"""
        best_option = None
        best_score = float('-inf')

        for option in options:
            score = self.evaluate_option(option, context)
            if score > best_score:
                best_score = score
                best_option = option

        return best_option

    def evaluate_option(self, option, context):
        """Evaluate an option based on multiple criteria"""
        # Safety evaluation
        safety_score = self.evaluate_safety(option, context)
        if safety_score < self.safety_thresholds['collision_probability']:
            return float('-inf')  # Unsafe option

        # Success probability
        success_score = self.estimate_success_probability(option, context)

        # Efficiency
        efficiency_score = self.estimate_efficiency(option, context)

        # Weighted combination
        total_score = (
            0.4 * safety_score +
            0.4 * success_score +
            0.2 * efficiency_score
        )

        return total_score

    def evaluate_safety(self, option, context):
        """Evaluate safety of an option"""
        # Check for potential collisions, balance issues, etc.
        # This would interface with safety monitoring system
        return 0.9  # Placeholder

    def estimate_success_probability(self, option, context):
        """Estimate probability of success for an option"""
        # Based on past experiences and current context
        return 0.8  # Placeholder

    def estimate_efficiency(self, option, context):
        """Estimate efficiency of an option"""
        # Time, energy, resource usage considerations
        return 0.7  # Placeholder
```

## System-Level Integration

### Main Integration Node

The central node that coordinates all subsystems:

```python
# main_integration.py
from std_msgs.msg import String, Bool
from geometry_msgs.msg import PoseStamped
from action_msgs.msg import GoalStatus
import threading

class MainIntegrationNode(Node):
    def __init__(self):
        super().__init__('main_integration')

        # Initialize all subsystems
        self.perception_system = PerceptionSubsystem(self)
        self.cognition_system = CognitionSubsystem(self)
        self.action_system = ActionSystem(self)
        self.safety_system = SafetyMonitor(self)

        # System state management
        self.system_state = 'idle'  # idle, executing, paused, emergency
        self.current_task = None
        self.system_status = {
            'perception_ok': True,
            'cognition_ok': True,
            'action_ok': True,
            'safety_ok': True
        }

        # Publishers and subscribers
        self.system_status_pub = self.create_publisher(
            String, '/h1/system/status', 10
        )
        self.emergency_stop_sub = self.create_subscription(
            Bool, '/h1/emergency_stop', self.emergency_stop_callback, 10
        )
        self.command_sub = self.create_subscription(
            String, '/h1/command', self.command_callback, 10
        )

        # Start system monitoring
        self.status_timer = self.create_timer(1.0, self.publish_system_status)
        self.monitoring_thread = threading.Thread(target=self.system_monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()

    def command_callback(self, msg):
        """Process system commands"""
        command = json.loads(msg.data)
        cmd_type = command.get('type')

        if cmd_type == 'execute_task':
            self.execute_task(command['task'])
        elif cmd_type == 'pause':
            self.pause_system()
        elif cmd_type == 'resume':
            self.resume_system()
        elif cmd_type == 'shutdown':
            self.shutdown_system()

    def execute_task(self, task):
        """Execute a high-level task"""
        if not self.safety_system.is_safe():
            self.get_logger().error('Safety check failed, cannot execute task')
            return False

        self.system_state = 'executing'
        self.current_task = task

        # Route task to appropriate subsystem
        if task['type'] == 'navigation':
            return self.action_system.execute_navigation_task(task)
        elif task['type'] == 'manipulation':
            return self.action_system.execute_manipulation_task(task)
        elif task['type'] == 'interaction':
            return self.cognition_system.process_interaction_task(task)

        return False

    def emergency_stop_callback(self, msg):
        """Handle emergency stop signal"""
        if msg.data:
            self.trigger_emergency_stop()

    def trigger_emergency_stop(self):
        """Trigger emergency stop across all systems"""
        self.system_state = 'emergency'
        self.current_task = None

        # Stop all motion
        self.action_system.emergency_stop()

        # Log emergency event
        self.get_logger().fatal('EMERGENCY STOP ACTIVATED')

    def pause_system(self):
        """Pause system operation"""
        self.system_state = 'paused'
        self.action_system.pause_execution()

    def resume_system(self):
        """Resume system operation"""
        if self.safety_system.is_safe():
            self.system_state = 'idle'
            self.action_system.resume_execution()
        else:
            self.get_logger().error('Cannot resume, safety check failed')

    def shutdown_system(self):
        """Graceful system shutdown"""
        self.system_state = 'shutdown'
        self.action_system.emergency_stop()

        # Perform cleanup
        self.cleanup_resources()

    def system_monitoring_loop(self):
        """Continuous monitoring of system health"""
        while rclpy.ok():
            # Check all subsystems
            self.system_status['perception_ok'] = self.check_perception_health()
            self.system_status['cognition_ok'] = self.check_cognition_health()
            self.system_status['action_ok'] = self.check_action_health()
            self.system_status['safety_ok'] = self.safety_system.is_safe()

            # Check for system anomalies
            self.detect_system_anomalies()

            time.sleep(0.1)  # 100Hz monitoring

    def check_perception_health(self):
        """Check perception system health"""
        # This would check for sensor data freshness, processing errors, etc.
        return True

    def check_cognition_health(self):
        """Check cognition system health"""
        # This would check for LLM connectivity, memory usage, etc.
        return True

    def check_action_health(self):
        """Check action system health"""
        # This would check for actuator status, communication, etc.
        return True

    def detect_system_anomalies(self):
        """Detect potential system anomalies"""
        # Check for unusual patterns in system behavior
        pass

    def publish_system_status(self):
        """Publish system status"""
        status_msg = {
            'state': self.system_state,
            'current_task': self.current_task,
            'subsystem_status': self.system_status,
            'timestamp': self.get_clock().now().to_msg()
        }

        msg = String()
        msg.data = json.dumps(status_msg)
        self.system_status_pub.publish(msg)

    def cleanup_resources(self):
        """Clean up system resources"""
        # Close all threads, connections, etc.
        pass
```

## Integration Testing and Validation

### Comprehensive Integration Test Suite

```python
# integration_tests.py
import unittest
from unittest.mock import Mock, patch
import rclpy
from std_msgs.msg import String, Bool
from geometry_msgs.msg import Twist

class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.node = MainIntegrationNode()

    def test_perception_pipeline(self):
        """Test complete perception pipeline"""
        # Simulate sensor data input
        image_msg = self.create_test_image()
        self.node.perception_system.image_callback(image_msg)

        # Verify processing pipeline works
        self.assertIsNotNone(self.node.perception_system.vision_data)

    def test_cognition_workflow(self):
        """Test cognition workflow from command to plan"""
        command_msg = String()
        command_msg.data = "Go to the kitchen and bring me a cup"

        # Process command through cognition system
        self.node.cognition_system.command_callback(command_msg)

        # Verify plan was generated
        self.assertIsNotNone(self.node.cognition_system.current_plan)

    def test_action_execution(self):
        """Test action execution with safety monitoring"""
        # Create a simple navigation task
        task = {
            'type': 'navigation',
            'destination': [1.0, 1.0, 0.0]
        }

        # Execute task
        result = self.node.execute_task(task)

        # Verify execution started
        self.assertTrue(result)

    def test_safety_integration(self):
        """Test safety system integration"""
        # Verify safety system is active
        self.assertTrue(self.node.safety_system.is_safe())

        # Simulate emergency condition
        emergency_msg = Bool()
        emergency_msg.data = True
        self.node.emergency_stop_callback(emergency_msg)

        # Verify emergency stop was triggered
        self.assertEqual(self.node.system_state, 'emergency')

    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        # 1. Send command
        command_msg = String()
        command_msg.data = "Navigate to location (2,2)"
        self.node.command_callback(command_msg)

        # 2. Simulate perception data
        perception_data = {
            'objects': [],
            'environment': {'obstacles': [], 'free_space': []}
        }
        perception_msg = String()
        perception_msg.data = json.dumps(perception_data)
        self.node.perception_system.perception_callback(perception_msg)

        # 3. Verify plan generation and execution
        self.assertIsNotNone(self.node.current_task)
        self.assertEqual(self.node.system_state, 'executing')

    def create_test_image(self):
        """Create test image message"""
        import numpy as np
        import cv2
        from cv_bridge import CvBridge

        # Create a simple test image
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.rectangle(img, (100, 100), (200, 200), (255, 0, 0), -1)

        bridge = CvBridge()
        return bridge.cv2_to_imgmsg(img, encoding="bgr8")

def run_integration_tests():
    """Run all integration tests"""
    unittest.main(argv=[''], exit=False, verbosity=2)

if __name__ == '__main__':
    rclpy.init()
    run_integration_tests()
    rclpy.shutdown()
```

## Performance Optimization

### Real-time Performance Tuning

```python
# performance_optimizer.py
import psutil
import time
from collections import deque

class PerformanceOptimizer:
    def __init__(self, node):
        self.node = node
        self.metrics = {
            'cpu_usage': deque(maxlen=100),
            'memory_usage': deque(maxlen=100),
            'processing_times': deque(maxlen=100),
            'throughput': deque(maxlen=100)
        }
        self.optimization_thresholds = {
            'cpu_max': 80.0,
            'memory_max': 80.0,
            'processing_max': 0.1  # 100ms per operation
        }

    def monitor_performance(self):
        """Monitor system performance metrics"""
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent

        self.metrics['cpu_usage'].append(cpu_percent)
        self.metrics['memory_usage'].append(memory_percent)

        # Calculate averages
        avg_cpu = sum(self.metrics['cpu_usage']) / len(self.metrics['cpu_usage'])
        avg_memory = sum(self.metrics['memory_usage']) / len(self.metrics['memory_usage'])

        # Check if optimization is needed
        if avg_cpu > self.optimization_thresholds['cpu_max']:
            self.optimize_cpu_usage()
        if avg_memory > self.optimization_thresholds['memory_max']:
            self.optimize_memory_usage()

    def optimize_cpu_usage(self):
        """Optimize CPU usage"""
        self.node.get_logger().info('Optimizing CPU usage...')
        # Reduce processing frequency for non-critical tasks
        # Use more efficient algorithms where possible
        # Consider offloading to GPU for intensive tasks

    def optimize_memory_usage(self):
        """Optimize memory usage"""
        self.node.get_logger().info('Optimizing memory usage...')
        # Clear unused data
        # Use more memory-efficient data structures
        # Implement proper garbage collection

    def adaptive_processing_rate(self, component_name, processing_time):
        """Adjust processing rate based on performance"""
        self.metrics['processing_times'].append(processing_time)

        if len(self.metrics['processing_times']) >= 10:
            avg_time = sum(self.metrics['processing_times']) / len(self.metrics['processing_times'])

            if avg_time > self.optimization_thresholds['processing_max']:
                # Reduce processing rate
                self.node.get_logger().warn(f'Reducing processing rate for {component_name}')
                return max(1, int(1.0 / avg_time * 0.8))  # 80% of calculated rate
            else:
                # Can potentially increase rate
                return min(30, int(1.0 / avg_time * 1.2))  # 120% of calculated rate

        return 10  # Default rate
```

## Troubleshooting and Debugging

### Integration Debugging Tools

```python
# integration_debugger.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
import time

class IntegrationDebugger(Node):
    def __init__(self):
        super().__init__('integration_debugger')

        # Debug publishers and subscribers
        self.debug_sub = self.create_subscription(
            String, '/h1/debug', self.debug_callback, 10
        )
        self.log_pub = self.create_publisher(
            String, '/h1/debug/log', 10
        )

        # Component status tracking
        self.component_status = {}
        self.message_flow = []

    def debug_callback(self, msg):
        """Handle debug messages"""
        try:
            debug_info = json.loads(msg.data)
            self.log_debug_info(debug_info)
            self.check_component_status(debug_info)
        except json.JSONDecodeError:
            self.get_logger().error(f'Invalid debug message: {msg.data}')

    def log_debug_info(self, debug_info):
        """Log debug information"""
        timestamp = time.time()
        log_entry = {
            'timestamp': timestamp,
            'component': debug_info.get('component'),
            'status': debug_info.get('status'),
            'message': debug_info.get('message'),
            'data': debug_info.get('data', {})
        }
        self.message_flow.append(log_entry)

        # Keep only recent entries
        if len(self.message_flow) > 1000:
            self.message_flow = self.message_flow[-1000:]

    def check_component_status(self, debug_info):
        """Check and update component status"""
        component = debug_info.get('component')
        if component:
            self.component_status[component] = {
                'status': debug_info.get('status'),
                'last_update': time.time(),
                'message': debug_info.get('message')
            }

    def generate_system_health_report(self):
        """Generate comprehensive system health report"""
        report = {
            'timestamp': time.time(),
            'component_status': self.component_status.copy(),
            'recent_messages': self.message_flow[-10:],  # Last 10 messages
            'total_messages': len(self.message_flow),
            'system_uptime': self.get_clock().now().seconds_nanoseconds()
        }

        return report

    def identify_integration_issues(self):
        """Identify potential integration issues"""
        issues = []

        # Check for components that haven't updated recently
        current_time = time.time()
        for component, status in self.component_status.items():
            time_since_update = current_time - status['last_update']
            if time_since_update > 5.0:  # 5 seconds
                issues.append(f'Component {component} not updating (last update: {time_since_update:.1f}s ago)')

        # Check for error statuses
        for component, status in self.component_status.items():
            if status['status'] == 'error':
                issues.append(f'Component {component} reporting error: {status["message"]}')

        return issues
```

## Conclusion

System integration is a complex but critical phase that determines the success of the humanoid robot project. The modular integration approach, comprehensive testing, and continuous monitoring ensure that all components work together harmoniously. Proper performance optimization and debugging capabilities are essential for maintaining system reliability in real-world operation. The integration process should be iterative, with continuous validation and refinement throughout development.