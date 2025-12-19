---
id: sensor-sim
title: Sensor Simulation
sidebar_position: 3
---

# Sensor Simulation

Sensor simulation is critical for humanoid robot development, providing realistic sensor data for testing perception algorithms, control systems, and AI models before deployment on physical hardware. This chapter covers comprehensive simulation of sensors commonly found on humanoid robots like the Unitree H1.

## Sensor Simulation Fundamentals

### Physics-Based vs. Ray-Based Simulation

Sensor simulation approaches in robotics:

- **Physics-Based**: Simulates physical processes for maximum accuracy
- **Ray-Based**: Uses ray tracing for performance with acceptable accuracy
- **Hybrid Approaches**: Combines both for optimal results

### Noise Modeling

Realistic sensor noise is essential for robust algorithm development:

```python
import numpy as np

class SensorNoiseModel:
    def __init__(self, noise_params):
        self.params = noise_params

    def add_gaussian_noise(self, signal, std_dev):
        """Add Gaussian noise to sensor signal"""
        noise = np.random.normal(0, std_dev, signal.shape)
        return signal + noise

    def add_bias_drift(self, signal, drift_rate, dt):
        """Simulate bias drift over time"""
        drift = np.cumsum(np.random.normal(0, drift_rate * dt, signal.shape))
        return signal + drift

    def add_quantization_noise(self, signal, resolution):
        """Simulate quantization effects"""
        quantized = np.round(signal / resolution) * resolution
        return quantized

    def add_delay(self, signal, delay_samples):
        """Add delay to simulate sensor processing time"""
        delayed_signal = np.zeros_like(signal)
        delayed_signal[delay_samples:] = signal[:-delay_samples]
        return delayed_signal
```

## IMU Simulation

### Accelerometer and Gyroscope Modeling

IMU sensors are critical for humanoid balance and control:

```python
class IMUSimulator:
    def __init__(self, sample_rate=100):
        self.sample_rate = sample_rate
        self.dt = 1.0 / sample_rate

        # IMU parameters (typical for humanoid robot)
        self.accel_noise_density = 80e-6  # m/s^2/sqrt(Hz)
        self.accel_bias_instability = 2e-4  # m/s^2
        self.gyro_noise_density = 3.5e-5  # rad/s/sqrt(Hz)
        self.gyro_bias_instability = 1e-5  # rad/s

        # Bias random walk
        self.accel_bias_walk = 0.0
        self.gyro_bias_walk = 0.0

    def simulate_imu(self, true_accel, true_gyro, time):
        """Simulate IMU measurements with realistic noise"""
        # Convert noise density to discrete noise
        accel_noise_std = self.accel_noise_density * np.sqrt(self.sample_rate / 2)
        gyro_noise_std = self.gyro_noise_density * np.sqrt(self.sample_rate / 2)

        # Add noise to true measurements
        accel_meas = self.add_noise(true_accel, accel_noise_std)
        gyro_meas = self.add_noise(true_gyro, gyro_noise_std)

        # Add bias and drift
        accel_meas = self.add_bias_drift(accel_meas, self.accel_bias_instability, time)
        gyro_meas = self.add_bias_drift(gyro_meas, self.gyro_bias_instability, time)

        return accel_meas, gyro_meas

    def add_noise(self, signal, noise_std):
        """Add white Gaussian noise"""
        noise = np.random.normal(0, noise_std, signal.shape)
        return signal + noise

    def add_bias_drift(self, signal, bias_std, time):
        """Add bias drift using random walk model"""
        # Update bias walk
        self.accel_bias_walk += np.random.normal(0, bias_std * np.sqrt(self.dt))
        return signal + self.accel_bias_walk
```

### Magnetometer Simulation

For heading estimation in humanoid navigation:

```python
class MagnetometerSimulator:
    def __init__(self):
        self.earth_field = np.array([22000, 0, -44000])  # nT, typical for mid-latitudes
        self.noise_std = 100  # nT
        self.bias = np.random.normal(0, 500, 3)  # Initial bias

    def simulate_magnetometer(self, orientation):
        """Simulate magnetometer readings with orientation"""
        # Apply orientation to Earth's magnetic field
        R = self.orientation_to_rotation_matrix(orientation)
        field_world = R @ self.earth_field

        # Add noise and bias
        noise = np.random.normal(0, self.noise_std, 3)
        measurement = field_world + self.bias + noise

        return measurement

    def orientation_to_rotation_matrix(self, orientation):
        """Convert quaternion to rotation matrix"""
        # Implementation for quaternion to rotation matrix
        pass
```

> [!hardware]
> **Hardware Note**: The Unitree H1 includes high-precision IMUs for balance control. Simulation must accurately model the specific noise characteristics and update rates of these sensors to ensure effective sim-to-real transfer of balance control algorithms.

## Camera Simulation

### RGB Camera Modeling

Realistic RGB camera simulation for computer vision:

```python
import cv2
import numpy as np

class RGBCameraSimulator:
    def __init__(self, width=640, height=480, fov=60):
        self.width = width
        self.height = height
        self.fov = fov

        # Camera intrinsic parameters
        self.fx = (width / 2) / np.tan(np.radians(fov / 2))
        self.fy = (height / 2) / np.tan(np.radians(fov / 2))
        self.cx = width / 2
        self.cy = height / 2

        # Distortion parameters
        self.k1 = -0.1  # Radial distortion
        self.k2 = 0.05
        self.p1 = 0.0   # Tangential distortion
        self.p2 = 0.0

        # Noise parameters
        self.noise_std = 10  # Pixel noise standard deviation
        self.dropout_rate = 0.001  # Dead pixel rate

    def simulate_camera_image(self, scene_depth, scene_normals, camera_pose):
        """Simulate camera image from scene data"""
        # Project 3D points to 2D image coordinates
        image_coords = self.project_to_image(scene_depth, camera_pose)

        # Apply lens distortion
        distorted_coords = self.apply_distortion(image_coords)

        # Add noise
        noisy_image = self.add_noise_to_image(scene_depth, distorted_coords)

        # Simulate motion blur
        motion_blur_image = self.apply_motion_blur(noisy_image, camera_pose)

        return motion_blur_image

    def apply_distortion(self, points):
        """Apply camera lens distortion"""
        x, y = points[:, 0], points[:, 1]

        # Normalize coordinates
        x_norm = (x - self.cx) / self.fx
        y_norm = (y - self.cy) / self.fy

        # Calculate distortion
        r2 = x_norm**2 + y_norm**2
        r4 = r2**2

        # Apply distortion
        x_distorted = x_norm * (1 + self.k1 * r2 + self.k2 * r4) + \
                     2 * self.p1 * x_norm * y_norm + self.p2 * (r2 + 2 * x_norm**2)
        y_distorted = y_norm * (1 + self.k1 * r2 + self.k2 * r4) + \
                     self.p1 * (r2 + 2 * y_norm**2) + 2 * self.p2 * x_norm * y_norm

        # Convert back to pixel coordinates
        x_distorted = x_distorted * self.fx + self.cx
        y_distorted = y_distorted * self.fy + self.cy

        return np.stack([x_distorted, y_distorted], axis=1)

    def add_noise_to_image(self, image, coords):
        """Add realistic noise to image"""
        # Add Gaussian noise
        noise = np.random.normal(0, self.noise_std, image.shape)
        noisy_image = image + noise

        # Add random pixel dropout (dead pixels)
        dropout_mask = np.random.random(image.shape[:2]) < self.dropout_rate
        noisy_image[dropout_mask] = 0  # Black pixels

        return np.clip(noisy_image, 0, 255).astype(np.uint8)
```

### Depth Camera Simulation

For 3D perception and navigation:

```python
class DepthCameraSimulator:
    def __init__(self, width=640, height=480, fov=60):
        self.width = width
        self.height = height
        self.fov = fov
        self.max_range = 10.0  # meters

        # Depth sensor parameters
        self.depth_noise_factor = 0.001  # Proportional to depth
        self.depth_bias = 0.01  # Fixed bias in meters
        self.depth_dropout_rate = 0.02  # Percentage of invalid readings

    def simulate_depth_image(self, true_depth):
        """Simulate depth camera measurements"""
        # Add proportional noise
        noise = np.random.normal(0, self.depth_noise_factor * true_depth, true_depth.shape)

        # Add fixed bias
        depth_with_bias = true_depth + self.depth_bias

        # Add noise
        noisy_depth = depth_with_bias + noise

        # Simulate invalid readings (dropout)
        dropout_mask = np.random.random(true_depth.shape) < self.depth_dropout_rate
        noisy_depth[dropout_mask] = 0  # Invalid readings

        # Clamp to valid range
        noisy_depth = np.clip(noisy_depth, 0, self.max_range)

        return noisy_depth
```

## LiDAR Simulation

### 3D LiDAR Modeling

For navigation and mapping in humanoid robots:

```python
class LiDARSimulator:
    def __init__(self, horizontal_beams=360, vertical_beams=16,
                 fov_horizontal=360, fov_vertical=30, max_range=25.0):
        self.horizontal_beams = horizontal_beams
        self.vertical_beams = vertical_beams
        self.fov_horizontal = np.radians(fov_horizontal)
        self.fov_vertical = np.radians(fov_vertical)
        self.max_range = max_range

        # LiDAR parameters
        self.range_noise_std = 0.02  # meters
        self.ang_resolution = self.fov_horizontal / horizontal_beams
        self.intensity_range = (0.1, 1.0)  # Reflectance values

    def simulate_lidar_scan(self, scene_points, robot_pose):
        """Simulate LiDAR point cloud from scene"""
        # Transform scene points to robot frame
        robot_frame_points = self.transform_to_robot_frame(scene_points, robot_pose)

        # Calculate spherical coordinates
        ranges, angles_h, angles_v = self.cartesian_to_spherical(robot_frame_points)

        # Quantize to LiDAR beam pattern
        quantized_ranges = self.quantize_to_beams(ranges, angles_h, angles_v)

        # Add noise to range measurements
        noisy_ranges = self.add_range_noise(quantized_ranges)

        # Generate point cloud in robot frame
        point_cloud = self.generate_point_cloud(noisy_ranges)

        return point_cloud

    def add_range_noise(self, ranges):
        """Add realistic range noise to LiDAR measurements"""
        # Add Gaussian noise proportional to range
        noise = np.random.normal(0, self.range_noise_std, ranges.shape)

        # Add some systematic bias
        bias = np.random.normal(0, 0.005, ranges.shape)

        noisy_ranges = ranges + noise + bias

        # Ensure valid range
        noisy_ranges = np.clip(noisy_ranges, 0, self.max_range)

        return noisy_ranges

    def generate_intensity(self, point_cloud):
        """Simulate intensity values based on surface properties"""
        # Calculate surface normals
        normals = self.estimate_normals(point_cloud)

        # Simulate intensity based on angle of incidence
        intensity = np.abs(np.sum(normals * np.array([0, 0, 1]), axis=1))
        intensity = np.clip(intensity, self.intensity_range[0], self.intensity_range[1])

        return intensity
```

## Force/Torque Sensor Simulation

### Six-Axis Force/Torque Sensors

For humanoid manipulation and balance:

```python
class ForceTorqueSimulator:
    def __init__(self, sensor_location):
        self.location = sensor_location
        self.sample_rate = 500  # Hz

        # Sensor parameters
        self.force_noise_std = [0.1, 0.1, 0.15]  # [Fx, Fy, Fz] in Newtons
        self.torque_noise_std = [0.01, 0.01, 0.015]  # [Tx, Ty, Tz] in Nm

        # Bias and drift parameters
        self.force_bias = np.random.normal(0, 0.05, 3)
        self.torque_bias = np.random.normal(0, 0.005, 3)

    def simulate_force_torque(self, true_force, true_torque, contact_state):
        """Simulate force/torque measurements"""
        # Add noise to true values
        force_noise = np.random.normal(0, self.force_noise_std)
        torque_noise = np.random.normal(0, self.torque_noise_std)

        measured_force = true_force + force_noise + self.force_bias
        measured_torque = true_torque + torque_noise + self.torque_bias

        # Add contact-dependent effects
        if contact_state:
            # Add contact dynamics and micro-vibrations
            contact_effects = self.add_contact_effects()
            measured_force += contact_effects[:3]
            measured_torque += contact_effects[3:]

        return measured_force, measured_torque

    def add_contact_effects(self):
        """Add contact-specific effects to measurements"""
        # Simulate contact dynamics
        contact_force = np.random.normal(0, 0.05, 6)  # Small random forces/torques
        return contact_force
```

## Sensor Fusion and Integration

### Multi-Sensor Data Integration

Combining data from multiple sensors:

```python
class SensorFusion:
    def __init__(self):
        self.imu_data = None
        self.camera_data = None
        self.lidar_data = None
        self.ekf = self.initialize_ekf()  # Extended Kalman Filter

    def initialize_ekf(self):
        """Initialize Extended Kalman Filter for sensor fusion"""
        # State: [position, orientation, velocity, angular_velocity, bias]
        # Implementation would include state transition and measurement models
        pass

    def process_sensor_data(self, imu_reading, camera_reading, lidar_reading):
        """Process and fuse sensor data"""
        # Predict step using IMU data
        self.ekf.predict(imu_reading)

        # Update step using camera data (if available)
        if camera_reading is not None:
            self.ekf.update_camera(camera_reading)

        # Update step using LiDAR data (if available)
        if lidar_reading is not None:
            self.ekf.update_lidar(lidar_reading)

        return self.ekf.get_state_estimate()

    def handle_sensor_failures(self):
        """Handle sensor failures gracefully"""
        # Implement sensor failure detection and recovery
        pass
```

## Realistic Sensor Scenarios

### Environmental Effects

Simulating environmental conditions affecting sensors:

```python
class EnvironmentalEffects:
    def __init__(self):
        self.weather_effects = {
            'clear': {'visibility': 1.0, 'lighting': 1.0},
            'fog': {'visibility': 0.3, 'lighting': 0.8},
            'rain': {'visibility': 0.7, 'lighting': 0.6},
            'snow': {'visibility': 0.5, 'lighting': 0.7}
        }

    def apply_weather_effects(self, sensor_data, weather_condition):
        """Apply weather effects to sensor data"""
        effects = self.weather_effects.get(weather_condition, self.weather_effects['clear'])

        # Reduce visibility for depth sensors
        if 'depth' in sensor_data:
            sensor_data['depth'] *= effects['visibility']

        # Add weather-specific noise
        if weather_condition == 'rain':
            # Add raindrop artifacts to camera images
            sensor_data['camera'] = self.add_rain_effects(sensor_data['camera'])
        elif weather_condition == 'fog':
            # Add fog to depth measurements
            sensor_data['depth'] = self.add_fog_effects(sensor_data['depth'])

        return sensor_data

    def add_rain_effects(self, image):
        """Add raindrop artifacts to camera images"""
        # Add random raindrop patterns
        raindrops = np.random.random(image.shape[:2]) < 0.01
        image[raindrops] = [0, 0, 0]  # Black raindrops
        return image

    def add_fog_effects(self, depth):
        """Add fog effects to depth measurements"""
        # Reduce effective range in fog
        fog_factor = 0.3
        depth[depth > 2.0] *= fog_factor  # Reduce distant measurements
        return depth
```

## Simulation Validation

### Ground Truth Comparison

Validating sensor simulation accuracy:

```python
class SensorValidation:
    def __init__(self):
        self.ground_truth = None
        self.simulated_data = None

    def validate_imu_simulation(self, true_accel, true_gyro, measured_accel, measured_gyro):
        """Validate IMU simulation against ground truth"""
        # Calculate error statistics
        accel_error = measured_accel - true_accel
        gyro_error = measured_gyro - true_gyro

        # Calculate RMS error
        accel_rms = np.sqrt(np.mean(accel_error**2))
        gyro_rms = np.sqrt(np.mean(gyro_error**2))

        # Validate noise characteristics
        accel_std = np.std(accel_error)
        gyro_std = np.std(gyro_error)

        print(f"IMU Validation - Accel RMS: {accel_rms:.6f}, Gyro RMS: {gyro_rms:.6f}")
        print(f"IMU Noise - Accel Std: {accel_std:.6f}, Gyro Std: {gyro_std:.6f}")

        return {
            'accel_rms': accel_rms,
            'gyro_rms': gyro_rms,
            'accel_std': accel_std,
            'gyro_std': gyro_std
        }
```

## Performance Optimization

### Efficient Sensor Simulation

Optimizing sensor simulation for real-time performance:

```python
class EfficientSensorSimulator:
    def __init__(self):
        # Pre-allocate arrays to avoid memory allocation during simulation
        self.buffer_size = 1000
        self.time_buffer = np.zeros(self.buffer_size)
        self.data_buffer = np.zeros((self.buffer_size, 6))  # Example 6D sensor
        self.buffer_index = 0

    def simulate_batch(self, num_samples):
        """Simulate multiple sensor readings efficiently"""
        # Pre-generate random numbers in batches
        noise_batch = np.random.normal(0, 1, (num_samples, 6))

        # Apply transformations efficiently using vectorized operations
        simulated_data = self.apply_sensor_model(noise_batch)

        return simulated_data

    def apply_sensor_model(self, noise_batch):
        """Apply sensor model to noise batch efficiently"""
        # Vectorized sensor model application
        return noise_batch * 0.01 + 0.1  # Example: scale and bias
```

## Best Practices

### Sensor Simulation Guidelines

- **Realistic Noise Models**: Use noise parameters from real sensors
- **Temporal Consistency**: Maintain proper timing relationships
- **Physical Plausibility**: Ensure measurements are physically possible
- **Validation**: Compare simulation results with real sensor data
- **Modularity**: Design simulators that can be easily modified
- **Performance**: Optimize for real-time simulation when needed

## Debugging Sensor Issues

### Common Problems and Solutions

- **Drifting Measurements**: Check bias models and drift parameters
- **Excessive Noise**: Verify noise standard deviations
- **Temporal Artifacts**: Ensure proper sampling rates
- **Coordinate Frame Issues**: Validate transform chains
- **Performance Problems**: Profile and optimize critical paths

## Summary

Sensor simulation is fundamental to humanoid robot development, providing safe and cost-effective testing of perception and control algorithms. Realistic modeling of sensor noise, dynamics, and environmental effects ensures effective sim-to-real transfer of algorithms. Proper validation against real sensor data and performance optimization enable efficient development workflows for complex humanoid robots like the Unitree H1.