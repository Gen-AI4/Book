---
description: "Task list for Docusaurus Textbook Frontend implementation"
---

# Tasks: Docusaurus Textbook Frontend

**Input**: Design documents from `/specs/1-docusaurus-textbook-init/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: No explicit test requirements in the specification, so test tasks are not included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/` for Docusaurus site

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan in frontend/
- [ ] T002 Initialize Docusaurus project with dependencies in frontend/
- [ ] T003 [P] Configure linting and formatting tools for JavaScript/Markdown

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Install required plugins: npm install remark-math rehype-katex @docusaurus/theme-mermaid in frontend/
- [ ] T005 Create context7.json in project root pointing to frontend/docs/ for indexing
- [ ] T006 Update docusaurus.config.js with mathematical rendering and diagram support
- [ ] T007 Create basic documentation directory structure with 6 modules in frontend/docs/
- [ ] T008 Create custom CSS file for hardware admonition styling in frontend/src/css/custom.css
- [ ] T009 Create homepage component in frontend/src/pages/index.js

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Textbook Navigation (Priority: P1) 🎯 MVP

**Goal**: Enable students to access a well-organized textbook interface with clear navigation to efficiently find and read curriculum content on ROS 2, Gazebo, NVIDIA Isaac, and VLA topics.

**Independent Test**: Can be fully tested by navigating through different curriculum modules and verifying that content is properly organized and accessible from the main interface.

### Implementation for User Story 1

- [ ] T010 [P] [US1] Create 01-intro module directory in frontend/docs/01-intro/
- [ ] T011 [P] [US1] Create Foundations chapter in frontend/docs/01-intro/01-foundations.md
- [ ] T012 [P] [US1] Create Embodied Intelligence chapter in frontend/docs/01-intro/02-embodied-intelligence.md
- [ ] T013 [P] [US1] Create Hardware Lab chapter in frontend/docs/01-intro/03-hardware-lab.md
- [ ] T014 [P] [US1] Create Course Roadmap chapter in frontend/docs/01-intro/04-course-roadmap.md
- [ ] T015 [P] [US1] Create 02-module-1-ros2 module directory in frontend/docs/02-module-1-ros2/
- [ ] T016 [P] [US1] Create Architecture chapter in frontend/docs/02-module-1-ros2/01-architecture.md
- [ ] T017 [P] [US1] Create Python Agents chapter in frontend/docs/02-module-1-ros2/02-python-agents.md
- [ ] T018 [P] [US1] Create URDF Modeling chapter in frontend/docs/02-module-1-ros2/03-urdf-modeling.md
- [ ] T019 [P] [US1] Create Launch Systems chapter in frontend/docs/02-module-1-ros2/04-launch-systems.md
- [ ] T020 [US1] Update sidebar configuration in frontend/sidebars.js to include intro and ROS2 modules
- [ ] T021 [US1] Add navigation links between related content in different modules

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Interactive Learning Experience (Priority: P2)

**Goal**: Enable students to interact with the textbook through a chatbot assistant and mathematical equation rendering to get context-aware help and properly understand complex formulas.

**Independent Test**: Can be tested by verifying that mathematical equations render correctly and that chatbot integration is available.

### Implementation for User Story 2

- [ ] T022 [P] [US2] Create Gazebo Physics chapter in frontend/docs/02-module-2-digital-twin/01-gazebo-physics.md
- [ ] T023 [P] [US2] Create Unity Rendering chapter in frontend/docs/02-module-2-digital-twin/02-unity-rendering.md
- [ ] T024 [P] [US2] Create Sensor Sim chapter in frontend/docs/02-module-2-digital-twin/03-sensor-sim.md
- [ ] T025 [P] [US2] Create URDF to Sim chapter in frontend/docs/02-module-2-digital-twin/04-urdf-to-sim.md
- [ ] T026 [P] [US2] Create Isaac Sim Setup chapter in frontend/docs/04-module-3-isaac/01-isaac-sim-setup.md
- [ ] T027 [P] [US2] Create Isaac ROS Bridge chapter in frontend/docs/04-module-3-isaac/02-isaac-ros-bridge.md
- [ ] T028 [P] [US2] Create Visual SLAM chapter in frontend/docs/04-module-3-isaac/03-visual-slam.md
- [ ] T029 [P] [US2] Create Nav2 Planning chapter in frontend/docs/04-module-3-isaac/04-nav2-planning.md
- [ ] T030 [US2] Update docusaurus.config.js to include mathematical equation rendering (remark-math, rehype-katex)
- [ ] T031 [US2] Add mathematical formulas to relevant chapters in all modules
- [ ] T032 [US2] Update sidebar configuration in frontend/sidebars.js to include digital twin and Isaac modules

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Hardware-Aware Learning (Priority: P3)

**Goal**: Ensure students are clearly informed about hardware requirements and constraints throughout the curriculum so they can properly set up their development environment and understand practical implementation limitations.

**Independent Test**: Can be tested by reviewing content pages to verify that hardware-specific constraints and requirements are clearly highlighted.

### Implementation for User Story 3

- [ ] T033 [P] [US3] Create Voice Interface chapter in frontend/docs/05-module-4-vla/01-voice-interface.md
- [ ] T034 [P] [US3] Create LLM Planner chapter in frontend/docs/05-module-4-vla/02-llm-planner.md
- [ ] T035 [P] [US3] Create VLA Models chapter in frontend/docs/05-module-4-vla/03-vla-models.md
- [ ] T036 [P] [US3] Create Action Decoding chapter in frontend/docs/05-module-4-vla/04-action-decoding.md
- [ ] T037 [P] [US3] Create Project Specs chapter in frontend/docs/06-capstone/01-project-specs.md
- [ ] T038 [P] [US3] Create Design Doc chapter in frontend/docs/06-capstone/02-design-doc.md
- [ ] T039 [P] [US3] Create Integration chapter in frontend/docs/06-capstone/03-integration.md
- [ ] T040 [P] [US3] Create Final Demo chapter in frontend/docs/06-capstone/04-final-demo.md
- [ ] T041 [US3] Add hardware admonition styling to custom.css in frontend/src/css/custom.css
- [ ] T042 [US3] Add hardware constraint markers to relevant chapters throughout all modules
- [ ] T043 [US3] Update sidebar configuration in frontend/sidebars.js to include VLA and capstone modules
- [ ] T044 [US3] Ensure dark mode is set as default theme in docusaurus.config.js

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T045 [P] Documentation updates and consistency checks across all chapters
- [ ] T046 Code cleanup and refactoring of CSS and configuration files
- [ ] T047 Performance optimization of the Docusaurus site
- [ ] T048 [P] Review and finalize all chapter frontmatter (sidebar_position, title, id)
- [ ] T049 Security review of all content and configurations
- [ ] T050 Run build process to validate site generation in frontend/

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

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All content creation tasks within each user story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all content creation for User Story 1 together:
Task: "Create Foundations chapter in frontend/docs/01-intro/01-foundations.md"
Task: "Create Embodied Intelligence chapter in frontend/docs/01-intro/02-embodied-intelligence.md"
Task: "Create Hardware Lab chapter in frontend/docs/01-intro/03-hardware-lab.md"
Task: "Create Course Roadmap chapter in frontend/docs/01-intro/04-course-roadmap.md"
Task: "Create Architecture chapter in frontend/docs/02-module-1-ros2/01-architecture.md"
```

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
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence