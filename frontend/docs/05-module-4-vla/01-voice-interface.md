---
id: voice-interface
title: Voice Interface
sidebar_position: 1
---

# Voice Interface

Voice interfaces enable natural human-robot interaction, allowing users to communicate with humanoid robots using spoken language. This chapter explores the implementation of voice interfaces for humanoid robots like the Unitree H1, covering speech recognition, natural language processing, and multimodal interaction.

## Voice Interface Fundamentals

### Speech Recognition Pipeline

The voice interface for humanoid robots involves multiple components working together:

- **Audio Capture**: Microphones positioned on the robot
- **Speech Recognition**: Converting speech to text
- **Natural Language Understanding**: Interpreting user intent
- **Response Generation**: Creating appropriate responses
- **Speech Synthesis**: Converting text to speech

### Humanoid-Specific Considerations

When implementing voice interfaces for humanoid robots:

- **Microphone Array**: Multiple microphones for noise cancellation and directionality
- **Real-time Processing**: Low-latency processing for natural interaction
- **Environmental Noise**: Handling background noise in real-world environments
- **Social Interaction**: Natural turn-taking and conversational flow

## Audio Processing and Capture

### Microphone Configuration

Setting up audio capture for humanoid robots:

```python
import pyaudio
import numpy as np
import webrtcvad
from scipy import signal
import threading

class HumanoidAudioCapture:
    def __init__(self, sample_rate=16000, channels=4, chunk_size=1024):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.audio = pyaudio.PyAudio()

        # Voice Activity Detection
        self.vad = webrtcvad.Vad(2)  # Aggressiveness mode 2

        # Audio stream
        self.stream = None
        self.is_listening = False
        self.audio_buffer = []

        # Direction of arrival estimation
        self.doa_estimator = DoAEstimator(sample_rate, channels)

    def setup_microphone_array(self):
        """Setup microphone array for humanoid robot"""
        # Configure audio stream with multiple channels
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=self.audio_callback
        )

        return self.stream

    def audio_callback(self, in_data, frame_count, time_info, status):
        """Process incoming audio data"""
        # Convert to numpy array
        audio_data = np.frombuffer(in_data, dtype=np.int16)

        # Reshape for multi-channel
        if self.channels > 1:
            audio_data = audio_data.reshape(-1, self.channels)

        # Perform voice activity detection
        if self.is_speech_detected(audio_data):
            self.audio_buffer.append(audio_data)

        return (in_data, pyaudio.paContinue)

    def is_speech_detected(self, audio_data):
        """Detect if speech is present in audio data"""
        # Convert to 16kHz mono for VAD
        if self.channels > 1:
            mono_audio = np.mean(audio_data, axis=1)
        else:
            mono_audio = audio_data

        # Convert to bytes for VAD
        audio_bytes = (mono_audio.astype(np.int16)).tobytes()

        # Check for voice activity (frame size must be 10, 20, or 30 ms)
        frame_size = int(self.sample_rate * 0.02)  # 20ms
        frames = [audio_bytes[i:i+frame_size*2] for i in range(0, len(audio_bytes), frame_size*2)]

        speech_frames = 0
        total_frames = 0

        for frame in frames:
            if len(frame) == frame_size * 2:
                if self.vad.is_speech(frame, self.sample_rate):
                    speech_frames += 1
                total_frames += 1

        # Consider speech if >30% of frames have speech
        speech_ratio = speech_frames / max(total_frames, 1)
        return speech_ratio > 0.3

    def estimate_direction_of_arrival(self, audio_data):
        """Estimate direction of arrival for speech source"""
        if self.channels > 1:
            doa = self.doa_estimator.estimate_doa(audio_data)
            return doa
        return 0  # Default to front for single channel

    def start_listening(self):
        """Start audio capture"""
        self.is_listening = True
        if self.stream is None:
            self.setup_microphone_array()
        self.stream.start_stream()

    def stop_listening(self):
        """Stop audio capture"""
        self.is_listening = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

    def get_audio_chunk(self):
        """Get accumulated audio data"""
        if self.audio_buffer:
            chunk = np.concatenate(self.audio_buffer)
            self.audio_buffer = []
            return chunk
        return None
```

### Noise Reduction and Beamforming

Implementing noise reduction for humanoid applications:

```python
import sounddevice as sd
from scipy import signal
import pyroomacoustics as pra

class AudioProcessor:
    def __init__(self, sample_rate=16000, channels=4):
        self.sample_rate = sample_rate
        self.channels = channels

        # Initialize beamforming
        self.beamformer = self.initialize_beamformer()

        # Initialize noise reduction
        self.noise_estimator = NoiseEstimator(sample_rate)

        # Initialize acoustic echo cancellation
        self.aec = AcousticEchoCanceler(sample_rate)

    def initialize_beamformer(self):
        """Initialize beamforming for directional audio"""
        # Microphone array configuration for humanoid
        # Assume 4 microphones arranged in a square
        mic_array = np.array([
            [0.05, 0.05, 0.1],   # Top-right
            [0.05, -0.05, 0.1],  # Bottom-right
            [-0.05, -0.05, 0.1], # Bottom-left
            [-0.05, 0.05, 0.1]   # Top-left
        ])

        # Create beamformer (delay-and-sum)
        return pra.Beamformer(mic_array.T, self.sample_rate)

    def apply_beamforming(self, audio_data):
        """Apply beamforming to focus on speaker direction"""
        # Estimate direction of arrival
        doa = self.estimate_doa(audio_data)

        # Steer beam towards speaker
        beamformed = self.beamformer.process(audio_data, direction=doa)
        return beamformed

    def reduce_noise(self, audio_data):
        """Apply noise reduction to audio"""
        # Estimate noise profile
        noise_profile = self.noise_estimator.estimate_noise(audio_data)

        # Apply noise reduction
        clean_audio = self.apply_spectral_subtraction(audio_data, noise_profile)
        return clean_audio

    def apply_spectral_subtraction(self, audio_data, noise_profile):
        """Apply spectral subtraction noise reduction"""
        # Convert to frequency domain
        fft_data = np.fft.fft(audio_data)
        magnitude = np.abs(fft_data)
        phase = np.angle(fft_data)

        # Subtract noise estimate
        enhanced_magnitude = np.maximum(magnitude - noise_profile, 0)

        # Convert back to time domain
        enhanced_fft = enhanced_magnitude * np.exp(1j * phase)
        enhanced_audio = np.real(np.fft.ifft(enhanced_fft))

        return enhanced_audio.astype(np.int16)

    def estimate_doa(self, audio_data):
        """Estimate direction of arrival"""
        # Simple GCC-PHAT implementation
        reference_channel = audio_data[:, 0]
        for i in range(1, self.channels):
            delay = self.estimate_delay(reference_channel, audio_data[:, i])
            # Convert delay to angle based on microphone geometry
            pass
        return 0  # Placeholder
```

## Speech Recognition Systems

### Integration with ASR Models

Implementing speech recognition for humanoid robots:

```python
import speech_recognition as sr
import torch
import whisper
from transformers import AutoProcessor, AutoModel
import asyncio

class HumanoidSpeechRecognizer:
    def __init__(self, model_name="base"):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Initialize Whisper model for speech recognition
        self.whisper_model = whisper.load_model(model_name)

        # Initialize VAD
        self.vad_threshold = 0.3

        # Initialize wake word detection
        self.wake_word_detector = WakeWordDetector()

        # Configuration for humanoid-specific recognition
        self.setup_humanoid_config()

    def setup_humanoid_config(self):
        """Setup configuration for humanoid speech recognition"""
        # Adjust for humanoid's microphone position and environment
        self.recognizer.energy_threshold = 4000  # Adjust based on microphone sensitivity
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8  # Shorter pause for natural conversation

    def listen_for_speech(self, timeout=5.0, phrase_time_limit=10.0):
        """Listen for speech with humanoid-specific parameters"""
        try:
            with self.microphone as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1.0)

                # Listen for audio
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )

                return audio
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None

    def transcribe_audio(self, audio_data):
        """Transcribe audio using Whisper model"""
        try:
            # Convert audio to appropriate format for Whisper
            audio_np = self.audio_to_numpy(audio_data)

            # Transcribe with Whisper
            result = self.whisper_model.transcribe(
                audio_np,
                language="en",
                task="transcribe"
            )

            return result["text"]
        except Exception as e:
            print(f"Transcription error: {e}")
            return ""

    def audio_to_numpy(self, audio_data):
        """Convert audio data to numpy array for Whisper"""
        # Convert audio data to raw format
        raw_data = audio_data.get_raw_data()

        # Convert to numpy array
        import struct
        samples = struct.unpack(f"{len(raw_data)//2}h", raw_data)
        audio_np = np.array(samples, dtype=np.float32) / 32768.0  # Normalize

        return audio_np

    def continuous_listening(self, callback_func):
        """Continuously listen for speech and process"""
        def audio_callback(recognizer, audio):
            try:
                # Transcribe the audio
                text = self.transcribe_audio(audio)

                if text.strip():
                    # Process the recognized text
                    callback_func(text)
            except Exception as e:
                print(f"Error processing audio: {e}")

        # Start continuous listening
        stop_listening = self.recognizer.listen_in_background(
            self.microphone,
            audio_callback
        )

        return stop_listening

    def detect_wake_word(self, audio_data):
        """Detect wake word to activate robot attention"""
        return self.wake_word_detector.detect(audio_data)
```

> [!hardware]
> **Hardware Note**: The Unitree H1 humanoid robot includes an array of microphones positioned to capture speech from various directions while filtering out motor and environmental noise. The voice interface system must account for the robot's own mechanical sounds and the acoustics of the humanoid form factor.

## Natural Language Understanding

### Intent Recognition for Humanoid Robots

Processing natural language commands for humanoid robots:

```python
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import re

class HumanoidNLU:
    def __init__(self):
        # Initialize intent classification pipeline
        self.intent_classifier = pipeline(
            "text-classification",
            model="microsoft/DialoGPT-medium"  # Or custom trained model
        )

        # Initialize entity extraction
        self.entity_extractor = self.setup_entity_extraction()

        # Define humanoid-specific intents
        self.intent_patterns = {
            "move_forward": [
                r"walk forward", r"go forward", r"move ahead", r"step forward"
            ],
            "turn_left": [
                r"turn left", r"rotate left", r"pivot left", r"spin left"
            ],
            "turn_right": [
                r"turn right", r"rotate right", r"pivot right", r"spin right"
            ],
            "stop": [
                r"stop", r"halt", r"freeze", r"stand still"
            ],
            "greet": [
                r"hello", r"hi", r"greetings", r"good morning", r"good afternoon"
            ],
            "navigation": [
                r"go to", r"navigate to", r"walk to", r"move to", r"find"
            ]
        }

    def setup_entity_extraction(self):
        """Setup entity extraction for navigation and object references"""
        # This could use spaCy, NLTK, or custom NER model
        import spacy
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Download model if not available
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            nlp = spacy.load("en_core_web_sm")

        return nlp

    def classify_intent(self, text):
        """Classify the intent of the user's speech"""
        text_lower = text.lower().strip()

        # Check against predefined patterns
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return intent, 1.0  # Intent and confidence

        # If no pattern matches, use ML classification
        return self.ml_classify_intent(text)

    def ml_classify_intent(self, text):
        """Use machine learning to classify intent"""
        # This is a simplified approach - in practice, you'd train a custom model
        # based on your humanoid's specific command vocabulary

        # For demonstration, return a generic intent
        return "unknown", 0.0

    def extract_entities(self, text):
        """Extract entities like locations, objects, and people from text"""
        doc = self.entity_extractor(text)

        entities = {
            "locations": [],
            "objects": [],
            "people": [],
            "quantities": []
        }

        for ent in doc.ents:
            if ent.label_ in ["GPE", "LOC", "FAC"]:  # Geographic, Location, Facility
                entities["locations"].append(ent.text)
            elif ent.label_ in ["OBJECT", "PRODUCT"]:  # Custom labels
                entities["objects"].append(ent.text)
            elif ent.label_ in ["PERSON", "NORP"]:  # Person, Nationalities
                entities["people"].append(ent.text)
            elif ent.label_ in ["MONEY", "QUANTITY", "CARDINAL"]:
                entities["quantities"].append(ent.text)

        return entities

    def parse_navigation_command(self, text):
        """Parse navigation-related commands"""
        # Look for navigation patterns
        nav_match = re.search(r"go to|navigate to|walk to|move to\s+(.+?)(?:\s|$)", text.lower())
        if nav_match:
            destination = nav_match.group(1).strip()
            return {
                "intent": "navigate",
                "destination": destination,
                "confidence": 0.9
            }

        # Look for directional commands
        direction_match = re.search(r"(forward|backward|left|right|ahead|back)", text.lower())
        if direction_match:
            direction = direction_match.group(1)
            return {
                "intent": f"move_{direction}",
                "direction": direction,
                "confidence": 0.8
            }

        return None

    def process_command(self, text):
        """Process a complete command from speech"""
        # First, try navigation parsing (more specific)
        nav_result = self.parse_navigation_command(text)
        if nav_result:
            return nav_result

        # Then, try general intent classification
        intent, confidence = self.classify_intent(text)
        entities = self.extract_entities(text)

        return {
            "intent": intent,
            "confidence": confidence,
            "entities": entities,
            "original_text": text
        }
```

## Text-to-Speech and Voice Synthesis

### Humanoid Voice Synthesis

Implementing natural voice synthesis for humanoid robots:

```python
import pyttsx3
import torch
from transformers import VitsModel, AutoTokenizer
import numpy as np
import sounddevice as sd

class HumanoidTextToSpeech:
    def __init__(self):
        # Initialize multiple TTS engines for different scenarios
        self.pyttsx3_engine = pyttsx3.init()
        self.setup_pyttsx3()

        # Initialize neural TTS model
        self.neural_tts = self.initialize_neural_tts()

        # Voice characteristics for humanoid
        self.voice_pitch = 1.0
        self.voice_speed = 200  # words per minute
        self.voice_volume = 0.8

    def setup_pyttsx3(self):
        """Setup pyttsx3 TTS engine"""
        # Get available voices
        voices = self.pyttsx3_engine.getProperty('voices')

        # Select a suitable voice (preferably one that sounds natural)
        for voice in voices:
            if "sapi5" in voice.id.lower():
                self.pyttsx3_engine.setProperty('voice', voice.id)
                break

        # Set properties
        self.pyttsx3_engine.setProperty('rate', self.voice_speed)
        self.pyttsx3_engine.setProperty('volume', self.voice_volume)

    def initialize_neural_tts(self):
        """Initialize neural text-to-speech model"""
        try:
            # Use a pre-trained VITS model or similar
            model = VitsModel.from_pretrained("facebook/mms-tts-eng")
            tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")
            return {"model": model, "tokenizer": tokenizer}
        except:
            # Fallback to simpler approach
            return None

    def speak_text(self, text, method="neural", blocking=True):
        """Speak the given text using selected method"""
        if method == "neural" and self.neural_tts:
            self.speak_neural(text, blocking)
        else:
            self.speak_pyttsx3(text, blocking)

    def speak_neural(self, text, blocking=True):
        """Speak using neural TTS model"""
        if self.neural_tts is None:
            # Fallback to pyttsx3
            self.speak_pyttsx3(text, blocking)
            return

        try:
            inputs = self.neural_tts["tokenizer"](text, return_tensors="pt")

            with torch.no_grad():
                output = self.neural_tts["model"](**inputs).waveform

            # Play the audio
            audio_np = output.numpy().squeeze()
            sd.play(audio_np, samplerate=16000)

            if blocking:
                sd.wait()  # Wait until audio finishes playing

        except Exception as e:
            print(f"Neural TTS error: {e}")
            # Fallback to pyttsx3
            self.speak_pyttsx3(text, blocking)

    def speak_pyttsx3(self, text, blocking=True):
        """Speak using pyttsx3 engine"""
        if blocking:
            self.pyttsx3_engine.say(text)
            self.pyttsx3_engine.runAndWait()
        else:
            # Non-blocking version
            self.pyttsx3_engine.say(text)
            # Note: pyttsx3 doesn't have a clean non-blocking way
            # This would require threading in a real implementation

    def set_voice_characteristics(self, pitch=1.0, speed=200, volume=0.8):
        """Set voice characteristics"""
        self.voice_pitch = pitch
        self.voice_speed = speed
        self.voice_volume = volume

        self.pyttsx3_engine.setProperty('rate', speed)
        self.pyttsx3_engine.setProperty('volume', volume)

    def speak_with_emotion(self, text, emotion="neutral"):
        """Speak with emotional intonation"""
        # In a real implementation, this would use emotional TTS models
        # For now, adjust pitch and speed based on emotion
        original_speed = self.voice_speed
        original_pitch = self.voice_pitch

        if emotion == "happy":
            self.set_voice_characteristics(
                pitch=min(1.3, self.voice_pitch * 1.2),
                speed=min(250, self.voice_speed * 1.1)
            )
        elif emotion == "sad":
            self.set_voice_characteristics(
                pitch=max(0.8, self.voice_pitch * 0.9),
                speed=max(150, self.voice_speed * 0.9)
            )
        elif emotion == "excited":
            self.set_voice_characteristics(
                pitch=min(1.5, self.voice_pitch * 1.3),
                speed=min(300, self.voice_speed * 1.2)
            )

        self.speak_text(text)

        # Restore original settings
        self.set_voice_characteristics(original_speed, original_pitch, self.voice_volume)

    def generate_response(self, intent, entities):
        """Generate appropriate verbal response based on intent"""
        responses = {
            "greet": ["Hello! How can I assist you today?",
                     "Greetings! What can I do for you?",
                     "Hi there! Ready to help!"],
            "navigation": [f"Okay, I will navigate to {entities.get('locations', ['the location'])[0]}.",
                          f"Setting course for {entities.get('locations', ['destination'])[0]}.",
                          f"On my way to {entities.get('locations', ['there'])[0]}."],
            "move_forward": ["Moving forward as requested.",
                           "Stepping forward.",
                           "Advancing forward."],
            "turn_left": ["Turning left.",
                         "Rotating left as instructed.",
                         "Pivoting left."],
            "unknown": ["I'm sorry, I didn't understand that command.",
                       "Could you please repeat that?",
                       "I'm not sure I understood correctly."]
        }

        import random
        response_list = responses.get(intent, responses["unknown"])
        return random.choice(response_list)
```

## Multimodal Voice Interface

### Integration with Other Modalities

Creating a multimodal voice interface for humanoid robots:

```python
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class MultimodalVoiceInterface:
    def __init__(self, nlu_system, tts_system, vision_system):
        self.nlu = nlu_system
        self.tts = tts_system
        self.vision = vision_system
        self.cv_bridge = CvBridge()

        # Context management
        self.conversation_context = {}
        self.attention_target = None

        # Gesture coordination
        self.gesture_controller = GestureController()

    def process_multimodal_command(self, speech_text, visual_context=None):
        """Process command using both speech and visual context"""
        # Parse the speech command
        command_result = self.nlu.process_command(speech_text)

        # If visual context is available, enhance understanding
        if visual_context:
            command_result = self.enhance_with_vision(
                command_result, visual_context
            )

        # Execute the command
        execution_result = self.execute_command(command_result)

        # Generate response
        response = self.generate_response(command_result, execution_result)

        # Speak the response
        self.tts.speak_text(response)

        # Perform coordinating gestures
        self.perform_coordinating_gestures(command_result["intent"])

        return execution_result

    def enhance_with_vision(self, command_result, visual_context):
        """Enhance command understanding with visual context"""
        intent = command_result["intent"]

        if intent == "find" or "navigate" in intent:
            # Use visual context to disambiguate
            if "object" in command_result["entities"]:
                target_object = command_result["entities"]["object"]

                # Look for the object in visual context
                detected_objects = self.vision.detect_objects(visual_context)

                if target_object in detected_objects:
                    # Update command with visual confirmation
                    command_result["visual_confirmation"] = True
                    command_result["object_location"] = detected_objects[target_object]["position"]

        elif intent == "greet":
            # Detect people in visual field to personalize greeting
            people = self.vision.detect_people(visual_context)
            if people:
                command_result["target_person"] = people[0]  # Greet the first person seen

        return command_result

    def execute_command(self, command_result):
        """Execute the parsed command"""
        intent = command_result["intent"]

        if intent == "greet":
            return self.execute_greeting(command_result)
        elif intent == "navigate":
            return self.execute_navigation(command_result)
        elif intent.startswith("move_"):
            return self.execute_movement(intent.replace("move_", ""))
        elif intent in ["turn_left", "turn_right"]:
            return self.execute_rotation(intent)
        else:
            return {"status": "unknown_command", "details": f"Unknown intent: {intent}"}

    def execute_greeting(self, command_result):
        """Execute greeting command"""
        target_person = command_result.get("target_person")

        if target_person:
            # Turn to face the person
            self.face_person(target_person)

        # Perform greeting gesture
        self.gesture_controller.perform_gesture("wave")

        return {"status": "success", "action": "greeted_person"}

    def execute_navigation(self, command_result):
        """Execute navigation command"""
        destination = command_result.get("destination", "unknown location")

        # Use navigation system to go to destination
        nav_result = self.navigation_system.go_to(destination)

        return {
            "status": nav_result["status"],
            "destination": destination,
            "details": nav_result.get("details", "")
        }

    def execute_movement(self, direction):
        """Execute movement command"""
        # Send movement command to robot base
        movement_result = self.robot_base.move_in_direction(direction)

        return {
            "status": "success" if movement_result else "failed",
            "direction": direction,
            "details": f"Attempted to move {direction}"
        }

    def execute_rotation(self, rotation_type):
        """Execute rotation command"""
        if rotation_type == "turn_left":
            angle = -90  # degrees
        elif rotation_type == "turn_right":
            angle = 90
        else:
            angle = 0

        # Rotate the robot
        rotation_result = self.robot_base.rotate(angle)

        return {
            "status": "success" if rotation_result else "failed",
            "angle": angle,
            "details": f"Attempted to rotate {angle} degrees"
        }

    def generate_response(self, command_result, execution_result):
        """Generate verbal response based on command and execution"""
        intent = command_result["intent"]

        if execution_result["status"] == "success":
            if intent == "greet":
                return "Hello! Nice to meet you."
            elif "navigate" in intent:
                return f"I'm on my way to {command_result.get('destination', 'the location')}."
            elif intent.startswith("move_"):
                return f"Moving {intent.replace('move_', '')} as requested."
            else:
                return "Command executed successfully."
        else:
            return "I'm sorry, I couldn't complete that command."

    def perform_coordinating_gestures(self, intent):
        """Perform gestures that coordinate with speech"""
        gesture_map = {
            "greet": "wave",
            "navigate": "point_forward",
            "move_forward": "step_forward_gesture",
            "turn_left": "point_left",
            "turn_right": "point_right"
        }

        gesture = gesture_map.get(intent)
        if gesture:
            self.gesture_controller.perform_gesture(gesture)

    def face_person(self, person_info):
        """Turn robot to face a detected person"""
        # Calculate direction to person
        person_position = person_info["position"]

        # Turn robot base to face person
        self.robot_base.turn_to_face(person_position)
```

## Voice Interface Optimization

### Performance and Quality Improvements

Optimizing voice interface for humanoid robot applications:

```python
import queue
import threading
import time

class OptimizedVoiceInterface:
    def __init__(self):
        self.audio_queue = queue.Queue(maxsize=10)
        self.command_queue = queue.Queue(maxsize=5)
        self.processing_thread = None
        self.is_running = False

        # Performance metrics
        self.metrics = {
            "latency": [],
            "accuracy": [],
            "throughput": []
        }

    def start_processing_pipeline(self):
        """Start the voice processing pipeline"""
        self.is_running = True
        self.processing_thread = threading.Thread(target=self.processing_loop)
        self.processing_thread.start()

    def processing_loop(self):
        """Main processing loop for voice interface"""
        while self.is_running:
            try:
                # Get audio from queue
                if not self.audio_queue.empty():
                    audio_data = self.audio_queue.get(timeout=0.1)

                    # Process audio
                    start_time = time.time()
                    text = self.process_audio_chunk(audio_data)

                    if text.strip():
                        # Add to command queue
                        self.command_queue.put({
                            "text": text,
                            "timestamp": time.time(),
                            "processing_time": time.time() - start_time
                        })

                time.sleep(0.01)  # Small delay to prevent busy waiting

            except queue.Empty:
                continue
            except Exception as e:
                print(f"Processing error: {e}")

    def process_audio_chunk(self, audio_data):
        """Process a chunk of audio data"""
        # Apply noise reduction
        clean_audio = self.apply_noise_reduction(audio_data)

        # Perform speech recognition
        text = self.speech_recognizer.transcribe_audio(clean_audio)

        return text

    def apply_noise_reduction(self, audio_data):
        """Apply optimized noise reduction"""
        # Use fast Fourier transform for real-time noise reduction
        # This is a simplified version
        return audio_data  # Placeholder

    def get_performance_metrics(self):
        """Get performance metrics for the voice interface"""
        if not self.metrics["latency"]:
            return {"status": "no_data"}

        return {
            "avg_latency": sum(self.metrics["latency"]) / len(self.metrics["latency"]),
            "avg_accuracy": sum(self.metrics["accuracy"]) / len(self.metrics["accuracy"]) if self.metrics["accuracy"] else 0,
            "avg_throughput": sum(self.metrics["throughput"]) / len(self.metrics["throughput"]) if self.metrics["throughput"] else 0,
            "total_commands_processed": len(self.metrics["latency"])
        }

    def stop_processing_pipeline(self):
        """Stop the voice processing pipeline"""
        self.is_running = False
        if self.processing_thread:
            self.processing_thread.join()

def voice_interface_best_practices():
    """Best practices for humanoid voice interfaces"""

    practices = [
        "Implement wake word detection to activate attention",
        "Use beamforming to focus on speaker direction",
        "Apply noise reduction for better recognition in real environments",
        "Maintain conversation context for natural interaction",
        "Provide verbal feedback for all commands",
        "Implement timeout mechanisms to prevent hanging",
        "Use multimodal input (speech + vision) for better understanding",
        "Optimize for real-time performance with low latency",
        "Test in various acoustic environments",
        "Provide fallback mechanisms when recognition fails"
    ]

    for i, practice in enumerate(practices, 1):
        print(f"{i}. {practice}")

## Summary

Voice interfaces provide natural and intuitive interaction with humanoid robots, enabling users to communicate using spoken language. The implementation involves audio processing, speech recognition, natural language understanding, and text-to-speech synthesis. For humanoid robots like the Unitree H1, special consideration must be given to microphone placement, noise cancellation, and multimodal integration to create a seamless and natural interaction experience.