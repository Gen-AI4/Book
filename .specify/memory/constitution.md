<!-- SYNC IMPACT REPORT:
Version change: N/A -> 1.0.0
Added sections: All principles and sections as per project requirements
Removed sections: Template placeholders
Modified principles: N/A (new constitution)
Templates requiring updates: N/A (new project)
Follow-up TODOs: None
-->
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