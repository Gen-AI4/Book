---
id: unity-rendering
title: Unity Rendering
sidebar_position: 2
---

# Unity Rendering

Unity provides high-fidelity visual rendering for humanoid robot simulation, offering photorealistic environments and advanced graphics capabilities that complement physics simulation. This chapter explores Unity's integration with robotics simulation, particularly for humanoid robots like the Unitree H1.

## Unity Robotics Overview

### Unity Robotics Package

Unity provides specialized packages for robotics simulation:

- **Unity Robotics Hub**: Centralized access to robotics tools
- **Unity Simulation**: High-fidelity physics and rendering
- **ML-Agents**: Machine learning for robotics
- **ROS-TCP-Connector**: Bridge between Unity and ROS 2

### Installation and Setup

Setting up Unity for robotics simulation:

1. Install Unity Hub and Unity 2021.3 LTS or newer
2. Install Robotics packages via Unity Package Manager
3. Configure ROS-TCP-Connector for communication
4. Import robot models and environments

## Scene Architecture for Humanoid Simulation

### Environment Design

Creating realistic environments for humanoid robots:

```csharp
using UnityEngine;

public class HumanoidEnvironment : MonoBehaviour
{
    [Header("Environment Settings")]
    public float terrainScale = 100f;
    public int terrainResolution = 257;
    public AnimationCurve terrainHeightCurve;

    [Header("Lighting")]
    public Light sunLight;
    public float dayNightCycleSpeed = 1f;

    void Start()
    {
        GenerateTerrain();
        SetupLighting();
    }

    void GenerateTerrain()
    {
        // Create terrain with realistic features for humanoid navigation
        Terrain terrain = GetComponent<Terrain>();
        terrain.terrainData.size = new Vector3(terrainScale, 20, terrainScale);

        // Generate heightmap based on terrain curve
        float[,] heights = new float[terrainResolution, terrainResolution];
        for (int x = 0; x < terrainResolution; x++)
        {
            for (int y = 0; y < terrainResolution; y++)
            {
                float xNorm = (float)x / (terrainResolution - 1);
                float yNorm = (float)y / (terrainResolution - 1);

                // Add realistic terrain features
                float height = terrainHeightCurve.Evaluate(xNorm) *
                              Mathf.PerlinNoise(xNorm * 5f, yNorm * 5f);
                heights[x, y] = height;
            }
        }

        terrain.terrainData.SetHeights(0, 0, heights);
    }

    void SetupLighting()
    {
        // Configure realistic lighting for humanoid vision systems
        RenderSettings.ambientLight = new Color(0.4f, 0.4f, 0.4f);
        sunLight.intensity = 1.0f;
        sunLight.shadows = LightShadows.Soft;
    }
}
```

### Robot Integration

Importing and configuring humanoid robot models:

- **URDF Import**: Convert URDF models to Unity format
- **Joint Configuration**: Map physical joints to Unity constraints
- **Actuator Simulation**: Simulate motor dynamics
- **Sensor Placement**: Position cameras, IMUs, and other sensors

## High-Fidelity Rendering

### Physically-Based Rendering (PBR)

Unity's PBR system creates realistic materials:

```csharp
using UnityEngine;

[CreateAssetMenu(fileName = "RobotMaterial", menuName = "Robot/Material")]
public class RobotMaterial : ScriptableObject
{
    [Header("Base Properties")]
    public Color baseColor = Color.gray;
    public Texture2D albedoMap;

    [Header("Metallic Properties")]
    public float metallic = 0.5f;
    public Texture2D metallicMap;

    [Header("Normal Mapping")]
    public Texture2D normalMap;
    public float normalScale = 1f;

    [Header("Surface Details")]
    public Texture2D occlusionMap;
    public Texture2D emissionMap;

    public Material CreateMaterial()
    {
        Material material = new Material(Shader.Find("Standard"));
        material.SetColor("_Color", baseColor);
        material.SetTexture("_MainTex", albedoMap);
        material.SetFloat("_Metallic", metallic);
        material.SetTexture("_MetallicGlossMap", metallicMap);
        material.SetTexture("_BumpMap", normalMap);
        material.SetFloat("_BumpScale", normalScale);
        material.SetTexture("_OcclusionMap", occlusionMap);
        material.SetTexture("_EmissionMap", emissionMap);

        return material;
    }
}
```

### Realistic Lighting

Advanced lighting for photorealistic humanoid simulation:

- **Global Illumination**: Indirect lighting simulation
- **Light Probes**: Capture lighting information for moving objects
- **Reflection Probes**: Realistic reflections on robot surfaces
- **HDR Rendering**: High dynamic range for realistic lighting

## Sensor Simulation

### Camera Simulation

High-fidelity camera simulation for humanoid vision:

```csharp
using UnityEngine;

public class RobotCamera : MonoBehaviour
{
    [Header("Camera Settings")]
    public int resolutionWidth = 640;
    public int resolutionHeight = 480;
    public float fieldOfView = 60f;

    [Header("Noise Parameters")]
    public float noiseIntensity = 0.01f;
    public float blurAmount = 0.1f;

    private Camera cam;
    private RenderTexture renderTexture;

    void Start()
    {
        cam = GetComponent<Camera>();
        SetupCamera();
        SetupRenderTexture();
    }

    void SetupCamera()
    {
        cam.fieldOfView = fieldOfView;
        cam.allowMSAA = false; // Disable for performance
        cam.allowDynamicResolution = true;
    }

    void SetupRenderTexture()
    {
        renderTexture = new RenderTexture(resolutionWidth, resolutionHeight, 24);
        renderTexture.format = RenderTextureFormat.ARGB32;
        cam.targetTexture = renderTexture;
    }

    // Add noise to simulate real camera sensors
    void AddSensorNoise(RenderTexture source, RenderTexture destination)
    {
        // Apply noise and distortion effects
        // This would be implemented with a custom shader
        Graphics.Blit(source, destination);
    }
}
```

### LiDAR Simulation

Simulating LiDAR sensors for humanoid navigation:

```csharp
using UnityEngine;
using System.Collections.Generic;

public class RobotLidar : MonoBehaviour
{
    [Header("LiDAR Settings")]
    public int horizontalRays = 360;
    public int verticalRays = 16;
    public float minRange = 0.1f;
    public float maxRange = 25.0f;
    public float fovHorizontal = 360f;
    public float fovVertical = 30f;

    [Header("Noise Settings")]
    public float distanceNoise = 0.01f;
    public float angularNoise = 0.001f;

    private List<float> ranges;
    private RaycastHit[] hits;

    void Start()
    {
        ranges = new List<float>(horizontalRays * verticalRays);
        hits = new RaycastHit[horizontalRays * verticalRays];
    }

    public void Scan()
    {
        ranges.Clear();

        float hStep = fovHorizontal / horizontalRays;
        float vStep = fovVertical / verticalRays;

        for (int h = 0; h < horizontalRays; h++)
        {
            for (int v = 0; v < verticalRays; v++)
            {
                float hAngle = (h * hStep - fovHorizontal / 2) * Mathf.Deg2Rad;
                float vAngle = (v * vStep - fovVertical / 2) * Mathf.Deg2Rad;

                Vector3 direction = new Vector3(
                    Mathf.Cos(vAngle) * Mathf.Sin(hAngle),
                    Mathf.Sin(vAngle),
                    Mathf.Cos(vAngle) * Mathf.Cos(hAngle)
                );

                direction = transform.TransformDirection(direction);

                if (Physics.Raycast(transform.position, direction, out RaycastHit hit, maxRange))
                {
                    float range = hit.distance;
                    // Add noise to simulate real sensor
                    range += Random.Range(-distanceNoise, distanceNoise) * range;
                    ranges.Add(range);
                }
                else
                {
                    ranges.Add(maxRange);
                }
            }
        }
    }
}
```

> [!hardware]
> **Hardware Note**: Unity simulation of the Unitree H1 includes realistic rendering of its distinctive design elements, including LED indicators, joint actuators, and sensor housings. The visual fidelity helps train computer vision algorithms that will run on the physical robot's Jetson Orin computer.

## Physics Integration

### NVIDIA PhysX

Unity's PhysX engine for realistic humanoid physics:

```csharp
using UnityEngine;

public class HumanoidPhysics : MonoBehaviour
{
    [Header("Balance Parameters")]
    public float balanceThreshold = 0.1f;
    public float recoveryForce = 100f;

    [Header("Contact Detection")]
    public LayerMask groundLayer;
    public Transform leftFoot;
    public Transform rightFoot;

    private Rigidbody rb;
    private bool isLeftFootContact = false;
    private bool isRightFootContact = false;

    void Start()
    {
        rb = GetComponent<Rigidbody>();
    }

    void FixedUpdate()
    {
        UpdateContactStates();
        ApplyBalanceForces();
    }

    void UpdateContactStates()
    {
        // Check if feet are in contact with ground
        isLeftFootContact = Physics.CheckSphere(leftFoot.position, 0.05f, groundLayer);
        isRightFootContact = Physics.CheckSphere(rightFoot.position, 0.05f, groundLayer);
    }

    void ApplyBalanceForces()
    {
        // Apply balance correction forces based on COM position
        Vector3 comOffset = CalculateCenterOfMassOffset();
        if (comOffset.magnitude > balanceThreshold)
        {
            Vector3 correctionForce = -comOffset.normalized * recoveryForce * Time.fixedDeltaTime;
            rb.AddForceAtPosition(correctionForce, transform.position);
        }
    }

    Vector3 CalculateCenterOfMassOffset()
    {
        // Calculate offset from desired balance point
        Vector3 groundProjection = new Vector3(transform.position.x, 0, transform.position.z);
        Vector3 com = rb.worldCenterOfMass;
        return new Vector3(com.x - groundProjection.x, 0, com.z - groundProjection.z);
    }
}
```

### Joint Constraints

Simulating humanoid joint limitations:

- **Hinge Joints**: For single-axis rotation joints
- **Configurable Joints**: For complex multi-axis joints
- **Spring Constraints**: For compliant joint behavior
- **Motor Simulation**: For actuator dynamics

## Performance Optimization

### Level of Detail (LOD)

Managing performance with complex humanoid models:

```csharp
using UnityEngine;

public class HumanoidLOD : MonoBehaviour
{
    [System.Serializable]
    public class LODLevel
    {
        public string name;
        public float distance;
        public GameObject[] objects;
        public Material[] materials;
    }

    public LODLevel[] lodLevels;
    public Transform referenceTransform;

    private int currentLOD = 0;

    void Start()
    {
        UpdateLOD();
    }

    void Update()
    {
        float distance = Vector3.Distance(transform.position, referenceTransform.position);

        int newLOD = 0;
        for (int i = 0; i < lodLevels.Length; i++)
        {
            if (distance > lodLevels[i].distance)
            {
                newLOD = i;
            }
        }

        if (newLOD != currentLOD)
        {
            currentLOD = newLOD;
            UpdateLOD();
        }
    }

    void UpdateLOD()
    {
        for (int i = 0; i < lodLevels.Length; i++)
        {
            bool active = (i == currentLOD);
            foreach (GameObject obj in lodLevels[i].objects)
            {
                obj.SetActive(active);
            }
        }
    }
}
```

### Occlusion Culling

Optimizing rendering for large environments:

- **Occlusion Areas**: Define areas where objects can be culled
- **Occluder Static**: Mark large objects as occluders
- **Camera Frustum Culling**: Automatic culling outside camera view

## ROS 2 Integration

### ROS-TCP-Connector

Connecting Unity to ROS 2:

```csharp
using System.Collections;
using Unity.Robotics.ROSTCPConnector;
using UnityEngine;

public class H1ROSConnector : MonoBehaviour
{
    [Header("ROS Connection")]
    public string rosIP = "127.0.0.1";
    public int rosPort = 10000;

    [Header("Robot Topics")]
    public string jointStateTopic = "/h1/joint_states";
    public string sensorTopic = "/h1/sensors";

    private ROSConnection ros;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();
        ros.Initialize(rosIP, rosPort);
    }

    public void PublishJointStates(float[] positions, float[] velocities, float[] efforts)
    {
        // Publish joint state message to ROS
        var jointStateMsg = new sensor_msgs.JointState();
        jointStateMsg.name = GetJointNames(); // Array of joint names
        jointStateMsg.position = positions;
        jointStateMsg.velocity = velocities;
        jointStateMsg.effort = efforts;

        ros.Publish(jointStateTopic, jointStateMsg);
    }

    public void SubscribeToCommands()
    {
        ros.Subscribe<trajectory_msgs.JointTrajectory>(
            "/h1/joint_trajectory",
            OnJointTrajectoryReceived
        );
    }

    void OnJointTrajectoryReceived(trajectory_msgs.JointTrajectory trajectory)
    {
        // Process incoming trajectory commands
        ApplyTrajectoryToRobot(trajectory);
    }

    void ApplyTrajectoryToRobot(trajectory_msgs.JointTrajectory trajectory)
    {
        // Apply trajectory to Unity humanoid model
        // This would involve updating joint positions over time
    }
}
```

## Machine Learning Integration

### ML-Agents for Humanoid Control

Training humanoid locomotion with ML-Agents:

```csharp
using Unity.MLAgents;
using Unity.MLAgents.Sensors;
using Unity.MLAgents.Actuators;
using UnityEngine;

public class H1Agent : Agent
{
    [Header("Agent Configuration")]
    public Transform target;
    public float moveSpeed = 2f;

    [Header("Sensors")]
    public RayPerceptionSensor3D raySensor;

    private Rigidbody rb;
    private H1RobotController robotController;

    public override void Initialize()
    {
        rb = GetComponent<Rigidbody>();
        robotController = GetComponent<H1RobotController>();
    }

    public override void OnEpisodeBegin()
    {
        // Reset agent position and target
        transform.position = new Vector3(0, 1.0f, 0);
        target.position = new Vector3(Random.Range(-10f, 10f), 0, Random.Range(-10f, 10f));
    }

    public override void CollectObservations(VectorSensor sensor)
    {
        // Collect observations for the neural network
        sensor.AddObservation(transform.position);
        sensor.AddObservation(transform.rotation);
        sensor.AddObservation(rb.velocity);
        sensor.AddObservation(GetJointStates());
        sensor.AddObservation(Vector3.Distance(transform.position, target.position));
    }

    public override void OnActionReceived(ActionBuffers actions)
    {
        // Apply actions to control the humanoid
        float[] continuousActions = actions.ContinuousActions.Array;

        // Interpret actions as joint torques or positions
        ApplyControlActions(continuousActions);

        // Calculate reward
        float distanceToTarget = Vector3.Distance(transform.position, target.position);
        SetReward(-distanceToTarget * 0.01f); // Negative reward for distance

        // Check if episode should end
        if (distanceToTarget < 1.0f)
        {
            SetReward(10.0f); // Positive reward for reaching target
            EndEpisode();
        }
        else if (transform.position.y < 0.5f) // Fallen
        {
            SetReward(-5.0f); // Negative reward for falling
            EndEpisode();
        }
    }

    void ApplyControlActions(float[] actions)
    {
        // Map neural network outputs to robot control
        robotController.ApplyActions(actions);
    }

    float[] GetJointStates()
    {
        // Return current joint positions, velocities, etc.
        return robotController.GetJointStates();
    }
}
```

## Advanced Rendering Features

### Shader Development

Custom shaders for realistic robot appearance:

```hlsl
// RobotMetallic.shader
Shader "Robot/Metallic"
{
    Properties
    {
        _Color ("Color", Color) = (0.8, 0.8, 0.8, 1)
        _Metallic ("Metallic", Range(0, 1)) = 0.7
        _Smoothness ("Smoothness", Range(0, 1)) = 0.5
        _BumpMap ("Normal Map", 2D) = "bump" {}
        _BumpScale ("Normal Scale", Float) = 1.0
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 200

        CGPROGRAM
        #pragma surface surf Standard fullforwardshadows
        #pragma target 3.0

        sampler2D _BumpMap;
        fixed4 _Color;
        half _Metallic;
        half _Smoothness;
        float _BumpScale;

        struct Input
        {
            float2 uv_BumpMap;
        };

        void surf (Input IN, inout SurfaceOutputStandard o)
        {
            o.Albedo = _Color.rgb;
            o.Metallic = _Metallic;
            o.Smoothness = _Smoothness;
            o.Normal = UnpackScaleNormal(tex2D(_BumpMap, IN.uv_BumpMap), _BumpScale);
            o.Alpha = _Color.a;
        }
        ENDCG
    }
    Fallback "Diffuse"
}
```

### Post-Processing Effects

Realistic camera effects for humanoid vision:

- **Lens Distortion**: Simulate real camera lens effects
- **Chromatic Aberration**: Realistic color fringing
- **Motion Blur**: For fast-moving humanoid robots
- **Depth of Field**: Focus effects for vision systems

## Debugging and Visualization

### Physics Debugging

Visualizing physics for debugging humanoid simulation:

```csharp
using UnityEngine;

public class PhysicsDebugger : MonoBehaviour
{
    [Header("Debug Settings")]
    public bool showCOM = true;
    public bool showContacts = true;
    public bool showForces = true;

    private Rigidbody rb;

    void Start()
    {
        rb = GetComponent<Rigidbody>();
    }

    void OnDrawGizmos()
    {
        if (!enabled) return;

        if (showCOM)
        {
            // Draw center of mass
            Gizmos.color = Color.red;
            Gizmos.DrawSphere(rb.worldCenterOfMass, 0.05f);
        }

        if (showContacts)
        {
            // Draw contact points
            ContactPoint[] contacts = new ContactPoint[4];
            int contactCount = rb.GetContacts(contacts);

            for (int i = 0; i < contactCount; i++)
            {
                Gizmos.color = Color.green;
                Gizmos.DrawSphere(contacts[i].point, 0.02f);
            }
        }

        if (showForces)
        {
            // Draw force vectors
            Gizmos.color = Color.blue;
            Gizmos.DrawRay(transform.position, rb.velocity * 0.1f);
        }
    }
}
```

## Best Practices

### Performance Guidelines

- **LOD Management**: Use multiple detail levels for complex robots
- **Occlusion Culling**: Cull objects not visible to cameras
- **Texture Compression**: Use appropriate compression for mobile deployment
- **Batching**: Combine similar objects for rendering efficiency

### Quality Assurance

- **Validation**: Compare Unity results with real robot data
- **Calibration**: Ensure visual properties match physical robot
- **Testing**: Validate sensor simulation accuracy
- **Documentation**: Maintain clear documentation of simulation parameters

## Summary

Unity rendering provides the high-fidelity visualization needed for advanced humanoid robotics simulation. Combined with realistic physics, accurate sensor simulation, and ROS 2 integration, Unity enables comprehensive testing and development of humanoid robot systems. The photorealistic rendering capabilities are particularly valuable for training computer vision systems and validating perception algorithms before deployment on physical hardware.