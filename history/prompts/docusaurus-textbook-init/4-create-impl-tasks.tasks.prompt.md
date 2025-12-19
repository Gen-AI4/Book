---
id: 4
title: Create impl tasks
stage: tasks
date: 2025-12-19
surface: agent
model: claude-opus-4-5-20251101
feature: docusaurus-textbook-init
branch: 1-docusaurus-textbook-init
user: User
command: /sp.tasks
labels: ["tasks", "docusaurus", "textbook", "frontend", "backend"]
links:
  spec: specs/1-docusaurus-textbook-init/spec.md
  plan: specs/1-docusaurus-textbook-init/plan.md
  adr: null
  pr: null
files:
 - specs/1-docusaurus-textbook-init/tasks.md
tests:
 - none
---

## Prompt

 # TASKS

## 1. FRONTEND CONFIGURATION (Priority)
- [ ] **Install Plugins:** Run `npm install remark-math rehype-katex @docusaurus/theme-mermaid` inside the `frontend/` directory.
- [ ] **Update Config:** Modify `frontend/docusaurus.config.js`:
  - Add `remark-math` and `rehype-katex` to the `docs` plugin options.
  - Add `mermaid` to the markdown config.
  - Set `title` to "Physical AI & Humanoid Robotics".
- [ ] **Custom Styling:** Add a `.admonition-hardware` class in `frontend/src/css/custom.css` (use yellow/orange colors for hardware warnings).
- [ ] **Landing Page:** Update `frontend/src/pages/index.js` with the course title, subtitle, and CTA buttons.

## 2. CONTENT SCAFFOLDING
- [ ] **Clean Up:** Remove the default Docusaurus `tutorial` folders and files.
- [ ] **Create Structure:** Generate the following folders in `frontend/docs/`:
  - `01-intro`
  - `02-module-1-ros2`
  - `03-module-2-digital-twin`
  - `04-module-3-isaac`
  - `05-module-4-vla`
- [ ] **Generate Stubs:** Create an `index.md` in each folder containing the correct Module Title, "Learning Outcomes," and "Hardware Requirements" sections.

## 3. BACKEND SETUP
- [ ] **Init Backend:** Create a `backend/` directory (sibling to `frontend/`).
- [ ] **Dependencies:** Create `backend/requirements.txt` listing: `fastapi`, `uvicorn`, `qdrant-client`, `openai`, `python-dotenv`, `psycopg2-binary`.
- [ ] **API Skeleton:** Create `backend/main.py` with a basic `FastAPI` app instance and a root GET endpoint (health check).

## 4. RAG IMPLEMENTATION
- [ ] **Ingestion Script:** Create `backend/ingest.py` to parse Markdown files from `frontend/docs/`, strip frontmatter, and index them into Qdrant.
- [ ] **Chat Endpoint:** Implement `POST /chat` in `backend/main.py` (Search Qdrant -> Prompt OpenAI -> Return Response).
- [ ] **Frontend Widget:** Create `frontend/src/components/ChatWidget.jsx` (Floating button + Chat window) and connect it to the backend API.

## Response snapshot

---
description: "Task list for Docusaurus Textbook Frontend implementation"
---

# Tasks: Docusaurus Textbook Frontend

**Input**: Design documents from `/specs/1-docusaurus-textbook-init/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume web app structure - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project root directory structure with frontend/ and backend/ directories
- [ ] T002 Initialize Docusaurus project in frontend/ directory with classic template
- [ ] T003 [P] Initialize Python project in backend/ directory with requirements.txt

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Install required Docusaurus plugins: npm install remark-math rehype-katex @docusaurus/theme-mermaid in frontend/
- [ ] T005 [P] Install required Python packages: fastapi uvicorn qdrant-client openai python-dotenv in backend/
- [ ] T006 Configure docusaurus.config.js with math and mermaid support
- [ ] T007 Create basic FastAPI application structure in backend/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---
## Phase 3: User Story 1 - Textbook Navigation (Priority: P1) 🎯 MVP

**Goal**: Provide a well-organized textbook interface with clear navigation for accessing curriculum content on ROS 2, Gazebo, NVIDIA Isaac, and VLA topics

**Independent Test**: Can be fully tested by navigating through different curriculum modules and verifying that content is properly organized and accessible from the main interface

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T008 [P] [US1] Contract test for navigation endpoints in backend/tests/test_navigation.py
- [ ] T009 [P] [US1] Integration test for curriculum module navigation in backend/tests/test_modules.py

### Implementation for User Story 1

- [ ] T010 [P] [US1] Create curriculum module structure in frontend/docs/ with 6 directories (01-intro, 02-module-1-ros2, 03-module-2-digital-twin, 04-module-3-isaac, 05-module-4-vla, 06-capstone)
- [ ] T011 [P] [US1] Create index.md stub files in each module directory with Module Title, Learning Outcomes, and Hardware Requirements sections
- [ ] T012 [US1] Update docusaurus.config.js to define the sidebar navigation for all 6 modules
- [ ] T013 [US1] Create landing page at frontend/src/pages/index.js with course title, subtitle, and CTA buttons
- [ ] T014 [US1] Implement dark mode as default theme in docusaurus.config.js
- [ ] T015 [US1] Add custom CSS for basic styling in frontend/src/css/custom.css

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---
## Phase 4: User Story 2 - Interactive Learning Experience (Priority: P2)

**Goal**: Provide interaction with the textbook through a chatbot assistant and mathematical equation rendering for context-aware help and proper understanding of complex formulas

**Independent Test**: Can be tested by using the chatbot feature to ask questions about textbook content and verifying that mathematical equations render correctly

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T016 [P] [US2] Contract test for chat completions endpoint in backend/tests/test_chat.py
- [ ] T017 [P] [US2] Integration test for equation rendering in frontend/tests/test_math.js

### Implementation for User Story 2

- [ ] T018 [P] [US2] Implement math and diagram rendering configuration in docusaurus.config.js with remark-math and rehype-katex
- [ ] T019 [P] [US2] Create backend API endpoints for health check and chat completions in backend/main.py
- [ ] T020 [P] [US2] Create ingestion script to process Markdown files from frontend/docs/ in backend/ingest.py
- [ ] T021 [US2] Create ChatWidget React component in frontend/src/components/ChatWidget.jsx
- [ ] T022 [US2] Integrate ChatWidget with backend API for chat functionality
- [ ] T023 [US2] Test mathematical equation rendering with LaTeX examples in sample docs

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---
## Phase 5: User Story 3 - Hardware-Aware Learning (Priority: P3)

**Goal**: Clearly inform students about hardware requirements and constraints throughout the curriculum so they can properly set up their development environment and understand practical implementation limitations

**Independent Test**: Can be tested by reviewing content pages to verify that hardware-specific constraints and requirements are clearly highlighted

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T024 [P] [US3] Contract test for hardware requirement display in frontend/tests/test_hardware_admonitions.js

### Implementation for User Story 3

- [ ] T025 [P] [US3] Create custom CSS class .admonition-hardware in frontend/src/css/custom.css with yellow/orange styling for hardware warnings
- [ ] T026 [P] [US3] Update docusaurus.config.js to support custom admonitions
- [ ] T027 [US3] Add hardware requirement markers to all relevant content pages in frontend/docs/
- [ ] T028 [US3] Create example hardware admonitions in sample module content
- [ ] T029 [US3] Verify hardware markers display correctly in the UI

**Checkpoint**: All user stories should now be independently functional

---
## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T030 [P] Documentation updates in docs/
- [ ] T031 Code cleanup and refactoring
- [ ] T032 Performance optimization across all stories
- [ ] T033 [P] Additional unit tests (if requested) in tests/unit/
- [ ] T034 Security hardening
- [ ] T035 Run quickstart.md validation

---
## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---
## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---
## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

## Outcome

- ✅ Impact: Created comprehensive task list organized by user stories with proper dependencies and parallel execution opportunities
- 🧪 Tests: none
- 📁 Files: specs/1-docusaurus-textbook-init/tasks.md created
- 🔁 Next prompts: Begin implementation of tasks for Docusaurus textbook frontend
- 🧠 Reflection: Tasks organized by user story priority with clear dependencies and independent test criteria

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All tasks properly formatted with IDs, story labels, and file paths
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Start with T001-T003 setup tasks