# Implementation Plan: Docusaurus Textbook Frontend

**Branch**: `1-docusaurus-textbook-init` | **Date**: 2025-12-19 | **Spec**: [link]
**Input**: Feature specification from `/specs/1-docusaurus-textbook-init/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This implementation will create a Docusaurus-based textbook for teaching Physical AI & Humanoid Robotics. The solution consists of a frontend Docusaurus site with curriculum content organized in 6 modules (Intro, ROS 2, Digital Twin, Isaac, VLA, Capstone), mathematical equation rendering, custom hardware-aware admonitions, and a RAG chatbot integrated as a React component. The backend will be implemented in Python with FastAPI to handle chatbot interactions, connecting to Qdrant Cloud for vector storage and Neon Postgres for transactional data.

## Technical Context

**Language/Version**: Node.js 18.0+ for Docusaurus, Python 3.9+ for backend
**Primary Dependencies**: Docusaurus 3.x, React, Node.js, npm; Python 3.9+ for backend
**Storage**: Qdrant Cloud (vector database) and Neon Serverless Postgres (transactional data)
**Testing**: Jest and React Testing Library for frontend; Pytest for backend
**Target Platform**: Web-based textbook accessible via GitHub Pages
**Project Type**: Web application with separate frontend (Docusaurus) and backend (FastAPI)
**Performance Goals**: Page load times under 3 seconds, chatbot response times under 5 seconds
**Constraints**: Development environment should have sufficient VRAM for Isaac Sim (RTX 40-series recommended), but frontend deployment is hardware-agnostic via GitHub Pages
**Scale/Scope**: Educational textbook for robotics curriculum with interactive chatbot

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Sim-to-Real Transfer Focus: Content bridges digital AI and physical intelligence through curriculum modules covering ROS 2, Gazebo, Isaac, and VLA
- ✅ Multi-Modal Learning Approach: Integration of ROS 2, Gazebo, NVIDIA Isaac, and VLA technologies in curriculum structure
- ✅ Test-First for Educational Content: All code examples will be verified in simulated and real environments as per development workflow
- ✅ Hardware-Aware Implementation: Consideration of RTX 40-series, Jetson Orin, Unitree platform constraints in curriculum and deployment
- ✅ Interactive Learning Experience: Includes RAG chatbot for context-aware Q&A as specified
- ✅ Modular Curriculum Design: Six distinct modules (Intro, ROS 2, Digital Twin, Isaac, VLA, Capstone) that can be taught independently

## Project Structure

### Documentation (this feature)

```text
specs/1-docusaurus-textbook-init/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── docs/
│   ├── 01-intro/
│   ├── 02-module-1-ros2/
│   ├── 03-module-2-digital-twin/
│   ├── 04-module-3-isaac/
│   ├── 05-module-4-vla/
│   └── 06-capstone/
├── src/
│   ├── components/
│   │   └── ChatWidget/
│   ├── pages/
│   ├── css/
│   └── theme/
├── docusaurus.config.js
├── package.json
└── static/

backend/
├── main.py
├── ingest.py
├── requirements.txt
└── config/
    ├── qdrant_client.py
    └── neon_client.py
```

**Structure Decision**: Web application with separate frontend (Docusaurus) and backend (FastAPI) to maintain clear separation of concerns between static content delivery and dynamic AI services.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |