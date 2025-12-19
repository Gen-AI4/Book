---
id: 1
title: Create robotics textbook constitution
stage: constitution
date: 2025-12-19
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: master
user: User
command: /sp.constitution
labels: ["constitution", "robotics", "textbook", "education"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

## ROLE & OBJECTIVE
You are an expert Robotics Educator and Full-Stack Engineer acting as the architect for the project "Textbook for Teaching Physical AI & Humanoid Robotics." Your goal is to build a unified, interactive Docusaurus-based textbook that bridges the gap between digital AI and embodied physical intelligence.

## CORE DELIVERABLES
1. **The Textbook:** A comprehensive Docusaurus site hosted on GitHub Pages, covering ROS 2, Gazebo, NVIDIA Isaac, and VLA (Vision-Language-Action).
2. **The RAG Chatbot:** An embedded AI assistant capable of answering context-aware questions based on the book's content and user text selection.

## TECH STACK & ARCHITECTURE
- **Documentation/Frontend:** Docusaurus (React/MDX).
- **Chatbot Backend:** Python, FastAPI, OpenAI Agents/ChatKit SDK.
- **Database:** Neon (Serverless Postgres) for transactional data.
- **Vector Search:** Qdrant Cloud (Free Tier) for RAG implementation.
- **Development Tools:** Claude Code, Spec-Kit Plus.

## CURRICULUM FRAMEWORK (Content Roadmap)
You will structure the content into four distinct technical modules:
1.  **Module 1: The Robotic Nervous System (ROS 2):** Middleware, Nodes, Topics, rclpy, and URDF.
2.  **Module 2: The Digital Twin (Gazebo & Unity):** Physics simulation, sensor modeling (LiDAR/Depth), and environment building.
3.  **Module 3: The AI-Robot Brain (NVIDIA Isaac):** Isaac Sim, Isaac ROS, VSLAM, and Nav2 path planning.
4.  **Module 4: Vision-Language-Action (VLA):** Integrating LLMs, OpenAI Whisper, and cognitive planning for humanoid control.

## HARDWARE CONTEXT
All technical instructions must respect the course hardware constraints:
- **Workstations:** NVIDIA RTX 40-Series (High VRAM) required for Isaac Sim.
- **Edge:** NVIDIA Jetson Orin Nano/NX for deployment.
- **Robots:** Unitree Go2/G1 or generic manipulators.

## EDITORIAL GUIDELINES
- Tone: Academic yet practical, focused on "Sim-to-Real" transfer.
- Code style: Python-centric (ROS 2 Humble/Iron standards).
- Ensure specific emphasis on hardware limitations (latency, VRAM bottlenecks) in all tutorials.

## Response snapshot

# Textbook for Teaching Physical AI & Humanoid Robotics Constitution

## Core Principles

### Sim-to-Real Transfer Focus
Every tutorial and concept must bridge digital AI and embodied physical intelligence; All examples should demonstrate practical application on target hardware platforms (Unitree robots, NVIDIA Jetson); Hardware limitations (VRAM, latency) must be explicitly addressed in all implementations

### Multi-Modal Learning Approach
Content integrates ROS 2, Gazebo, NVIDIA Isaac, and VLA technologies; Each module builds upon previous concepts while maintaining standalone accessibility; Practical code examples accompany theoretical explanations

### Test-First for Educational Content (NON-NEGOTIABLE)
Every tutorial includes runnable code examples; Tests written → Content validated → Examples work → Then publish; All code snippets must be verified in both simulated and real environments

### Hardware-Aware Implementation
All code examples consider target hardware constraints (RTX 40-series, Jetson Orin, Unitree platforms); Resource optimization is prioritized; Performance benchmarks are included for each major implementation

### Interactive Learning Experience
Docusaurus-based textbook includes embedded RAG chatbot for context-aware Q&A; Code examples are interactive and copy-paste runnable; Real-world robotics applications are emphasized over theoretical concepts

### Modular Curriculum Design
Four distinct technical modules (ROS 2, Gazebo, NVIDIA Isaac, VLA) that can be taught independently; Cross-module dependencies are clearly documented; Each module has specific learning outcomes and assessment criteria

## Technology Stack Requirements
Frontend: Docusaurus (React/MDX); Backend: Python, FastAPI; Database: Neon (Serverless Postgres); Vector Search: Qdrant Cloud; AI Integration: OpenAI Agents/ChatKit SDK; Simulation: ROS 2, Gazebo, Isaac Sim

## Development Workflow
Content development follows Spec-Driven Development; All code examples tested on target hardware configurations; Documentation and code maintained in parallel; Peer review required for all curriculum additions

## Governance
All curriculum content must comply with hardware constraints and technology stack; Changes to core modules require architectural review; Educational effectiveness measured through student feedback and practical outcomes

**Version**: 1.0.0 | **Ratified**: 2025-12-19 | **Last Amended**: 2025-12-19

## Outcome

- ✅ Impact: Created foundational constitution for robotics textbook project that establishes core principles for sim-to-real transfer, multi-modal learning, hardware-aware implementation, and interactive learning experience
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md updated with project-specific principles and governance
- 🔁 Next prompts: Plan and develop specific curriculum modules based on this constitution
- 🧠 Reflection: The constitution successfully captures the essential requirements for a robotics textbook project, emphasizing the unique aspects of physical AI and humanoid robotics education

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin developing curriculum modules based on the established principles