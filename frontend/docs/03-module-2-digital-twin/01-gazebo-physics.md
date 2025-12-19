---
id: gazebo-physics
title: Gazebo Physics
sidebar_position: 1
---

# Gazebo Physics

Gazebo provides realistic physics simulation for humanoid robots, enabling safe testing and development before deployment on physical hardware. Understanding Gazebo's physics engine is crucial for effective simulation of complex robots like the Unitree H1.

## Physics Engine Fundamentals

### Open Dynamics Engine (ODE)

Gazebo uses ODE as its primary physics engine, providing:

- **Rigid Body Dynamics**: Accurate simulation of rigid body motion
- **Collision Detection**: Fast and reliable collision detection
- **Joint Constraints**: Various joint types with limits and dynamics
- **Contact Modeling**: Realistic contact forces and friction

### Physics Parameters

The physics engine is configured through parameters that affect simulation accuracy and performance:

```xml
<!-- Gazebo physics configuration -->
<physics type="ode">
  <max_step_size>0.001</max_step_size>  <!-- Time step for physics updates -->
  <real_time_factor>1.0</real_time_factor>  <!-- Simulation speed relative to real time -->
  <real_time_update_rate>1000.0</real_time_update_rate>  <!-- Physics updates per second -->
  <gravity>0 0 -9.8</gravity>  <!-- Gravity vector -->
  <ode>
    <solver>
      <type>quick</type>  <!-- Solver type: quick, world, dantzig, pgs -->
      <iters>100</iters>  <!-- Maximum solver iterations -->
      <sor>1.3</sor>  <!-- Successive over-relaxation parameter -->
    </solver>
    <constraints>
      <cfm>0.0</cfm>  <!-- Constraint force mixing parameter -->
      <erp>0.2</erp>  <!-- Error reduction parameter -->
      <contact_max_correcting_vel>100.0</contact_max_correcting_vel>
      <contact_surface_layer>0.001</contact_surface_layer>
    </constraints>
  </ode>
</physics>
```

## Humanoid Robot Simulation Challenges

### Balance and Stability

Humanoid robots present unique challenges for physics simulation:

- **High Degrees of Freedom**: 25+ joints require careful tuning
- **Dynamic Balance**: Maintaining balance during locomotion
- **Contact Transitions**: Accurate simulation of foot-ground contact
- **Whole-Body Control**: Coordinated control of all limbs

### Simulation Fidelity vs. Performance

Trade-offs between accuracy and computational efficiency:

- **Time Step**: Smaller steps improve accuracy but increase computation
- **Solver Iterations**: More iterations improve stability but reduce performance
- **Collision Meshes**: Complex meshes improve accuracy but slow simulation

## Gazebo World Design

### World Configuration

A typical humanoid robot simulation world includes:

```xml
<sdf version="1.7">
  <world name="h1_world">
    <!-- Physics engine configuration -->
    <physics name="ode" type="ode">
      <!-- Physics parameters -->
    </physics>

    <!-- Lighting -->
    <light name="sun" type="directional">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <attenuation>
        <range>1000</range>
      </attenuation>
      <direction>-0.4 0.2 -0.9</direction>
    </light>

    <!-- Ground plane -->
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
          <surface>
            <friction>
              <ode>
                <mu>1.0</mu>
                <mu2>1.0</mu2>
              </ode>
            </friction>
          </surface>
        </collision>
        <visual name="visual">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
          <material>
            <ambient>0.7 0.7 0.7 1</ambient>
            <diffuse>0.7 0.7 0.7 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

    <!-- Include the H1 robot -->
    <include>
      <uri>model://h1_description</uri>
      <pose>0 0 0.85 0 0 0</pose>
    </include>
  </world>
</sdf>
```

### Terrain and Environment

Realistic environments for humanoid testing:

- **Flat Ground**: For basic locomotion testing
- **Rough Terrain**: For robustness testing
- **Obstacles**: For navigation and path planning
- **Stairs**: For complex locomotion challenges

## Sensor Simulation

### IMU Simulation

Accurate IMU simulation for balance control:

```xml
<sensor name="h1_imu" type="imu">
  <always_on>true</always_on>
  <update_rate>100</update_rate>
  <imu>
    <angular_velocity>
      <x>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>2e-4</stddev>
          <bias_mean>0.0000075</bias_mean>
          <bias_stddev>0.0000008</bias_stddev>
        </noise>
      </x>
      <y>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>2e-4</stddev>
          <bias_mean>0.0000075</bias_mean>
          <bias_stddev>0.0000008</bias_stddev>
        </noise>
      </y>
      <z>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>2e-4</stddev>
          <bias_mean>0.0000075</bias_mean>
          <bias_stddev>0.0000008</bias_stddev>
        </noise>
      </z>
    </angular_velocity>
    <linear_acceleration>
      <x>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>1.7e-2</stddev>
          <bias_mean>0.1</bias_mean>
          <bias_stddev>0.001</bias_stddev>
        </noise>
      </x>
      <y>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>1.7e-2</stddev>
          <bias_mean>0.1</bias_mean>
          <bias_stddev>0.001</bias_stddev>
        </noise>
      </y>
      <z>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>1.7e-2</stddev>
          <bias_mean>0.1</bias_mean>
          <bias_stddev>0.001</bias_stddev>
        </noise>
      </z>
    </linear_acceleration>
  </imu>
</sensor>
```

### Force/Torque Sensors

Simulation of force/torque sensors in joints:

```xml
<sensor name="h1_left_foot_ft" type="force_torque">
  <always_on>true</always_on>
  <update_rate>500</update_rate>
  <force_torque>
    <frame>child</frame>
    <measure_direction>child_to_parent</measure_direction>
  </force_torque>
</sensor>
```

> [!hardware]
> **Hardware Note**: The Unitree H1 includes force/torque sensors in the feet. Gazebo simulation should include these sensors with realistic noise characteristics to properly test balance control algorithms.

## Physics Tuning for Humanoid Robots

### Contact Parameters

Tuning contact parameters for stable humanoid simulation:

```xml
<!-- In URDF/Gazebo integration -->
<gazebo reference="h1_left_foot_link">
  <collision>
    <surface>
      <contact>
        <ode>
          <kp>100000000</kp>  <!-- Contact stiffness -->
          <kd>1000</kd>       <!-- Damping coefficient -->
          <max_vel>100.0</max_vel>        <!-- Maximum contact correction velocity -->
          <min_depth>0.001</min_depth>    <!-- Penetration depth before applying force -->
        </ode>
      </contact>
      <friction>
        <ode>
          <mu>0.8</mu>    <!-- Primary friction coefficient -->
          <mu2>0.8</mu2>  <!-- Secondary friction coefficient -->
        </ode>
      </friction>
    </surface>
  </collision>
</gazebo>
```

### Joint Dynamics

Proper joint dynamics for realistic movement:

```xml
<!-- In URDF -->
<joint name="h1_left_knee_joint" type="revolute">
  <parent link="h1_left_hip_pitch_link"/>
  <child link="h1_left_knee_link"/>
  <axis xyz="0 1 0"/>
  <limit lower="0.0" upper="2.4" effort="400" velocity="4.0"/>
  <dynamics damping="2.0" friction="0.5"/>  <!-- Joint dynamics -->
</joint>

<!-- Gazebo-specific joint properties -->
<gazebo reference="h1_left_knee_joint">
  <implicitSpringDamper>1</implicitSpringDamper>
</gazebo>
```

## Simulation Performance Optimization

### Multi-Threaded Physics

Gazebo supports multi-threaded physics for better performance:

```xml
<physics name="ode" type="ode">
  <max_step_size>0.001</max_step_size>
  <real_time_factor>1.0</real_time_factor>
  <real_time_update_rate>1000.0</real_time_update_rate>
  <threads>4</threads>  <!-- Use multiple threads for physics -->
  <ode>
    <solver>
      <type>quick</type>
      <iters>100</iters>
      <sor>1.3</sor>
    </solver>
  </ode>
</physics>
```

### Contact Reduction

Optimize for humanoid robots with many potential contacts:

- **Contact Merging**: Combine nearby contacts
- **Contact Culling**: Remove distant contacts
- **Collision Filtering**: Skip unnecessary collision checks

## Simulation-to-Reality Transfer

### Domain Randomization

Techniques to improve sim-to-real transfer:

- **Parameter Randomization**: Randomize physics parameters during training
- **Visual Randomization**: Randomize lighting and textures
- **Actuator Randomization**: Add variability to actuator responses

### System Identification

Methods to match simulation to real robot:

- **Inertial Parameter Tuning**: Adjust masses and inertias
- **Friction Coefficient Tuning**: Match contact behavior
- **Actuator Model Tuning**: Match motor dynamics

## Debugging Simulation Issues

### Common Problems

- **Jittering**: Increase solver iterations or adjust ERP/CFM
- **Exploding Simulation**: Check for unstable parameters
- **Penetration**: Increase contact stiffness or reduce time step
- **Balance Issues**: Verify IMU noise and contact parameters

### Diagnostic Tools

```bash
# Run Gazebo with verbose output
gzserver --verbose world_file.world

# Check contact information
gz topic -e /gazebo/default/h1/left_foot/contacts

# Monitor physics performance
gz stats
```

## Advanced Features

### Joint Feedback Control

Integration with ROS 2 controllers:

```xml
<gazebo>
  <plugin name="gazebo_ros_control" filename="libgazebo_ros_control.so">
    <robotNamespace>/h1</robotNamespace>
    <robotSimType>gazebo_ros_control/DefaultRobotHWSim</robotSimType>
  </plugin>
</gazebo>
```

### Custom Physics Plugins

For specialized behaviors:

```cpp
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>

class H1BalancePlugin : public gazebo::ModelPlugin
{
public:
  void Load(gazebo::physics::ModelPtr _model, sdf::ElementPtr _sdf)
  {
    // Custom balance control for H1 robot
    this->model = _model;
    this->world = _model->GetWorld();
    this->updateConnection = gazebo::event::Events::ConnectWorldUpdateBegin(
        std::bind(&H1BalancePlugin::OnUpdate, this));
  }

  void OnUpdate()
  {
    // Custom physics update logic
  }

private:
  gazebo::physics::ModelPtr model;
  gazebo::physics::WorldPtr world;
  gazebo::event::ConnectionPtr updateConnection;
};

GZ_REGISTER_MODEL_PLUGIN(H1BalancePlugin)
```

## Best Practices

### Physics Parameter Tuning

- **Start Conservative**: Begin with stable parameters and gradually improve
- **Iterative Testing**: Test simple behaviors before complex ones
- **Hardware Validation**: Compare simulation results with real robot when possible

### Simulation Validation

- **Unit Testing**: Validate individual components in isolation
- **Integration Testing**: Test complete robot behaviors
- **Performance Monitoring**: Track simulation real-time factor

## Summary

Gazebo physics simulation provides the foundation for safe and efficient humanoid robot development. Proper configuration of physics parameters, contact properties, and sensor models is essential for achieving realistic simulation that can effectively support robot development and testing. The balance between simulation accuracy and computational performance requires careful tuning based on specific application requirements.