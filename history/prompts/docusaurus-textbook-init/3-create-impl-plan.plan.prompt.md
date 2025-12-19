---
id: 3
title: Create impl plan
stage: plan
date: 2025-12-19
surface: agent
model: claude-opus-4-5-20251101
feature: docusaurus-textbook-init
branch: 1-docusaurus-textbook-init
user: User
command: /sp.plan
labels: ["plan", "docusaurus", "textbook", "frontend", "backend"]
links:
  spec: specs/1-docusaurus-textbook-init/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-docusaurus-textbook-init/plan.md
 - specs/1-docusaurus-textbook-init/research.md
 - specs/1-docusaurus-textbook-init/data-model.md
 - specs/1-docusaurus-textbook-init/quickstart.md
 - specs/1-docusaurus-textbook-init/contracts/chat-api.yaml
 - specs/1-docusaurus-textbook-init/contracts/
tests:
 - none
---

## Prompt

## PHASE 1: FRONTEND CONFIGURATION (Existing Project)
- [ ] **Project Audit:** Confirm existence of `frontend/` directory and `docusaurus.config.js`.
- [ ] **Dependencies:** Inside `frontend/`, install required packages:
    - `npm install remark-math rehype-katex` (for Equations)
    - `npm install @docusaurus/theme-mermaid` (for Diagrams)
- [ ] **Config Update:** Modify `frontend/docusaurus.config.js`:
    - Enable `remark-math` and `rehype-katex` in the presets.
    - Add `mermaid` to the markdown config.
    - Set the site title to "Textbook for Physical AI".
- [ ] **Custom UI:**
    - Create `frontend/src/css/custom.css` styles for the `:::hardware` admonition.
    - Update `frontend/src/pages/index.js` with the course landing page copy.

## PHASE 2: CONTENT SKELETON
- [ ] **Directory Setup:** Clear default docs and create the following structure in `frontend/docs/`:
    - `01-intro/`
    - `02-module-1-ros2/`
    - `03-module-2-digital-twin/`
    - `04-module-3-isaac/`
    - `05-module-4-vla/`
- [ ] **Stub Files:** Generate `index.md` in each folder containing the Module Title, Learning Outcomes, and Hardware Requirements headers.

## PHASE 3: RAG BACKEND (THE BRAIN)
- [ ] **Setup:** Create a new root directory `backend/` (sibling to `frontend/`).
- [ ] **Environment:** Initialize Python environment in `backend/` and install `fastapi`, `uvicorn`, `qdrant-client`, `openai`.
- [ ] **Database:**
    - Connect to Qdrant Cloud (Free Tier).
    - Connect to Neon (Serverless Postgres).
- [ ] **API:** Create `backend/main.py` with a basic health check endpoint.

## PHASE 4: INTELLIGENCE & INTEGRATION
- [ ] **Ingestion:** Write `backend/ingest.py` to crawl `frontend/docs/`, strip Markdown, and push embeddings to Qdrant.
- [ ] **Chat Widget:** Create `frontend/src/components/ChatWidget.jsx` (React) to fetch data from the FastAPI backend.
- [ ] **Wiring:** Register the Chat Widget in the Docusaurus `Root` or `Layout` so it appears on every page.

## PHASE 5: DEPLOYMENT
- [ ] **Build:** Run `npm run build` in `frontend/`.
- [ ] **Verification:** Test local serving of docs + chatbot interaction.

## Response snapshot

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

# Research: Docusaurus Textbook Frontend Implementation

## Node.js Version for Docusaurus

**Decision**: Use Node.js version 18.0 or higher as specified in the original requirements
**Rationale**: Docusaurus 3.x requires Node.js 18.0 or higher for optimal performance and compatibility
**Alternatives considered**: Node.js 16 was considered but is not supported by Docusaurus 3.x

## Qdrant Cloud and Neon Postgres Setup Details

**Decision**: Use Qdrant Cloud free tier for vector storage and Neon Serverless Postgres for transactional data
**Rationale**: These technologies were specified in the original requirements and provide the necessary functionality for the RAG chatbot system
**Alternatives considered**:
- Pinecone, Weaviate for vector storage
- Traditional PostgreSQL, MySQL for transactional data
- Self-hosted solutions

## Testing Framework for Docusaurus/React Application

**Decision**: Use Jest and React Testing Library for frontend testing
**Rationale**: These are standard tools in the React/Docusaurus ecosystem and provide comprehensive testing capabilities
**Alternatives considered**:
- Cypress for end-to-end testing
- Vitest as a faster alternative to Jest
- Enzyme (now deprecated in favor of React Testing Library)

## Performance Requirements

**Decision**:
- Page load times: Under 3 seconds as specified in the success criteria
- Chatbot response times: Under 5 seconds for acceptable user experience
**Rationale**: These metrics align with web performance best practices and the success criteria in the specification
**Alternatives considered**: More aggressive performance targets were considered but would require additional optimization work

## Hardware Constraints for Deployment

**Decision**: The frontend will be built as static assets for GitHub Pages deployment, so hardware constraints primarily apply to the development environment and backend processing
**Rationale**: GitHub Pages hosting eliminates most hardware constraints for end users, while the backend will run on cloud infrastructure
**Alternatives considered**: Self-hosted solutions that would require more hardware consideration

# Data Model: Docusaurus Textbook Frontend

## Entities

### Curriculum Module
- **id**: String (unique identifier)
- **title**: String (module title)
- **description**: String (module description)
- **order**: Integer (sequence in curriculum)
- **learningOutcomes**: Array<String> (what students will learn)
- **hardwareRequirements**: Array<String> (specific hardware needed)
- **relatedModules**: Array<String> (links to other modules)

### Textbook Page
- **id**: String (unique identifier)
- **title**: String (page title)
- **content**: String (markdown content)
- **module**: String (parent module id)
- **order**: Integer (sequence in module)
- **codeExamples**: Array<CodeExample> (code snippets in the page)
- **mathFormulas**: Array<String> (LaTeX formulas)
- **diagrams**: Array<String> (Mermaid diagrams)

### Code Example
- **id**: String (unique identifier)
- **language**: String (python, c++, etc.)
- **code**: String (the actual code)
- **description**: String (what the code demonstrates)
- **hardwareConstraints**: Array<String> (specific hardware notes)

### User Interaction
- **id**: String (unique identifier)
- **userId**: String (user identifier)
- **sessionId**: String (session identifier)
- **actionType**: String (navigation, chat, etc.)
- **timestamp**: DateTime (when action occurred)
- **pageId**: String (which page the action occurred on)
- **details**: Object (specific action details)

### Chat Message
- **id**: String (unique identifier)
- **sessionId**: String (chat session identifier)
- **sender**: String (user or bot)
- **content**: String (message content)
- **timestamp**: DateTime (when message was sent)
- **context**: String (text selection or page context)
- **sourceDocuments**: Array<String> (documents referenced in response)

# Quickstart: Docusaurus Textbook Frontend

## Prerequisites
- Node.js 18.0 or higher
- Python 3.9 or higher
- npm package manager
- Access to Qdrant Cloud (for vector database)
- Access to Neon Postgres (for transactional data)

## Setup Instructions

### 1. Clone and Initialize the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Set up the Frontend (Docusaurus)
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Install required packages for math and diagrams
npm install remark-math rehype-katex
npm install @docusaurus/theme-mermaid

# Start development server
npm start
```

### 3. Set up the Backend (FastAPI)
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn qdrant-client openai python-dotenv

# Set up environment variables
cp .env.example .env
# Edit .env with your Qdrant and Neon credentials

# Start the backend server
uvicorn main:app --reload
```

### 4. Initialize the Knowledge Base
```bash
# From the backend directory
python ingest.py
```

### 5. Build and Deploy
```bash
# From the frontend directory
npm run build

# The built static files will be in the build/ directory
# Deploy these to GitHub Pages or your preferred static hosting
```

## Environment Variables
Create a `.env` file in the backend directory with the following variables:
```
QDRANT_URL=<your-qdrant-url>
QDRANT_API_KEY=<your-qdrant-api-key>
NEON_DATABASE_URL=<your-neon-database-url>
OPENAI_API_KEY=<your-openai-api-key>
```

## Running Tests
```bash
# Frontend tests
npm test

# Backend tests
cd backend
python -m pytest
```

## Development Workflow
1. Make changes to the documentation in `frontend/docs/`
2. Update the knowledge base by running `python backend/ingest.py`
3. Test the chatbot functionality
4. Run the build process to generate static files
5. Deploy to GitHub Pages

# API Contract: Chatbot API

openapi: 3.0.0
info:
  title: Textbook Chatbot API
  description: API for the RAG chatbot functionality in the Physical AI & Humanoid Robotics textbook
  version: 1.0.0
servers:
  - url: http://localhost:8000
    description: Development server
  - url: https://your-deployment-url.com
    description: Production server

paths:
  /health:
    get:
      summary: Health check endpoint
      responses:
        '200':
          description: Server is running
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: "healthy"
                  timestamp:
                    type: string
                    format: date-time
                    example: "2025-12-19T10:00:00Z"

  /chat/completions:
    post:
      summary: Get chat completions from the textbook knowledge base
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - message
                - context
              properties:
                message:
                  type: string
                  description: The user's message or question
                  example: "Explain how ROS 2 nodes communicate with each other"
                context:
                  type: string
                  description: The current page or selected text context
                  example: "Currently reading about ROS 2 communication patterns"
                sessionId:
                  type: string
                  description: Unique session identifier for conversation history
                  example: "session-12345"
      responses:
        '200':
          description: Successful response from the chatbot
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: string
                    example: "response-67890"
                  message:
                    type: string
                    description: The chatbot's response
                    example: "ROS 2 nodes communicate through a publish-subscribe pattern..."
                  sources:
                    type: array
                    items:
                      type: string
                    description: List of source documents used to generate the response
                    example: ["/docs/02-module-1-ros2/communication-patterns.md"]
                  timestamp:
                    type: string
                    format: date-time
                    example: "2025-12-19T10:05:00Z"
        '400':
          description: Bad request - missing required fields
        '500':
          description: Internal server error

  /ingest:
    post:
      summary: Ingest textbook content into the knowledge base
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - source_path
              properties:
                source_path:
                  type: string
                  description: Path to the documentation to be ingested
                  example: "/frontend/docs"
                force_update:
                  type: boolean
                  description: Whether to force re-processing of existing content
                  example: false
      responses:
        '200':
          description: Content successfully ingested
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: "success"
                  documents_processed:
                    type: integer
                    example: 24
                  timestamp:
                    type: string
                    format: date-time
                    example: "2025-12-19T10:10:00Z"
        '500':
          description: Internal server error

## Outcome

- ✅ Impact: Created comprehensive implementation plan with research, data models, quickstart guide, and API contracts for the Docusaurus textbook frontend
- 🧪 Tests: none
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, and chat-api.yaml
- 🔁 Next prompts: Generate tasks for implementation of the Docusaurus textbook frontend
- 🧠 Reflection: Planning phase complete with all required artifacts generated according to the specification

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All planning artifacts successfully created
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin task generation for implementation