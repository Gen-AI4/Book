---
id: 1
title: docusaurus-textbook-init
stage: spec
date: 2025-12-19
surface: agent
model: claude-opus-4-5-20251101
feature: docusaurus-textbook-init
branch: 1-docusaurus-textbook-init
user: Adi
command: /sp.specify
labels: ["docusaurus", "textbook", "frontend", "specification"]
links:
  spec: specs/1-docusaurus-textbook-init/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-docusaurus-textbook-init/spec.md
 - specs/1-docusaurus-textbook-init/checklists/requirements.md
 - history/prompts/docusaurus-textbook-init/0001-docusaurus-textbook-init.spec.prompt.md
tests:
 - none
---

## Prompt

# COMPONENT: FRONTEND (Textbook UI)

## OBJECTIVE
Initialize and configure the Docusaurus instance that serves as the "Physical AI & Humanoid Robotics" textbook. This interface must be optimized for reading technical documentation, displaying code snippets (Python/C++), and hosting the RAG Chatbot UI. Additionally, integrate **Context7 MCP Server** to enhance documentation context capabilities.

## TECH STACK
- **Framework:** Docusaurus 3.x (React-based static site generator).
- **Styling:** CSS Modules / Infima (Docusaurus default).
- **Deployment Target:** GitHub Pages.
- **Node Version:** >= 18.0.
- **Documentation Context:** Context7 MCP Server.

## FUNCTIONAL REQUIREMENTS

### 1. Project Initialization
- Initialize a new Docusaurus site named `physical-ai-textbook` (or verify existing `frontend` directory).
- Use the **classic** preset (Docs, Blog, Pages).
- Configure `docusaurus.config.js` for GitHub Pages deployment:
  - `organizationName`: [GIAIC]
  - `projectName`: [The-Book]
  - `deploymentBranch`: `gh-pages`

### 2. Information Architecture (Mandatory 4 Chapters Per Module)
Create the following folder hierarchy in `/docs` with exactly **4 sub-chapters** (Markdown files) per module to ensure comprehensive coverage:

- **`01-intro/`**
  1. `01-foundations.md`: What is Physical AI?
  2. `02-embodied-intelligence.md`: Digital Brain vs. Physical Body.
  3. `03-hardware-lab.md`: Workstations, Edge Kits, and Robots.
  4. `04-course-roadmap.md`: Weekly Schedule and Assessments.

- **`02-module-1-ros2/` (The Nervous System)**
  1. `01-architecture.md`: Nodes, Topics, and Services.
  2. `02-python-agents.md`: Writing `rclpy` scripts.
  3. `03-urdf-modeling.md`: Building the Robot Description.
  4. `04-launch-systems.md`: Parameter Management & Launch Files.

- **`03-module-2-digital-twin/` (Simulation)**
  1. `01-gazebo-physics.md`: World Building & Gravity.
  2. `02-unity-rendering.md`: High-Fidelity Visualization.
  3. `03-sensor-sim.md`: LiDAR, Depth Cameras, IMU.
  4. `04-urdf-to-sim.md`: Spawning Robots in Simulation.

- **`04-module-3-isaac/` (The Brain)**
  1. `01-isaac-sim-setup.md`: RTX Rendering & USD Assets.
  2. `02-isaac-ros-bridge.md`: Connecting Sim to ROS 2.
  3. `03-visual-slam.md`: Mapping & Localization.
  4. `04-nav2-planning.md`: Path Planning for Humanoids.

- **`05-module-4-vla/` (Vision-Language-Action)**
  1. `01-voice-interface.md`: OpenAI Whisper Integration.
  2. `02-llm-planner.md`: Cognitive Logic with GPT-4o.
  3. `03-vla-models.md`: Vision-Language-Action Transformers.
  4. `04-action-decoding.md`: Translating Text to ROS Actions.

- **`06-capstone/`**
  1. `01-project-specs.md`: The "Autonomous Humanoid" Challenge.
  2. `02-design-doc.md`: Architecture & Node Graph.
  3. `03-integration.md`: Combining Vision, Voice, and Motion.
  4. `04-final-demo.md`: Submission & Presentation Guide.

### 3. Context7 MCP Server Integration
- **Objective:** Enable Model Context Protocol (MCP) support for the documentation.
- **Configuration:**
  - Create a `context7.json` (or relevant config file) in the root.
  - Define the `docs` directory as the primary context source.
  - Ensure the MCP server can index the Docusaurus Markdown files to provide context-aware answers during development.

### 4. UI/UX Customization
- **Theme:** Enable Dark Mode by default.
- **Custom Admonitions:** Create `:::hardware` (Yellow/Orange icon) for hardware constraints.
- **Landing Page (`src/pages/index.js`):**
  - **Hero Title:** "Physical AI & Humanoid Robotics"
  - **Subtitle:** "Bridging the Digital Brain and the Physical Body"
  - **CTA Buttons:** "Start Reading" and "Hardware Setup".

### 5. Mathematical & Diagram Support
- **LaTeX:** Install `remark-math` and `rehype-katex`. Configure in `docusaurus.config.js`.
- **Diagrams:** Install `@docusaurus/theme-mermaid`. Enable Mermaid blocks in markdown.

## Response snapshot

Created a comprehensive specification for the Docusaurus-based textbook frontend for Physical AI & Humanoid Robotics. The specification includes user scenarios, functional requirements, and success criteria for a documentation platform optimized for technical learning with mathematical support and hardware-aware content markers.

## Outcome

- ✅ Impact: Complete specification created for Docusaurus textbook platform with all required modules and features
- 🧪 Tests: none
- 📁 Files: 2 files created/modified (spec and checklist)
- 🔁 Next prompts: Ready for planning phase with /sp.plan
- 🧠 Reflection: Structured documentation platform with MCP integration will provide context-aware learning experience

## Evaluation notes (flywheel)

- Failure modes observed: Script .specify/scripts/bash/create-phr.sh did not exist, required manual PHR creation
- Graders run and results (PASS/FAIL): PASS - all required information captured in PHR
- Prompt variant (if applicable): Manual fallback process used when automation script unavailable
- Next experiment (smallest change to try): Ensure PHR creation scripts are properly configured in project setup