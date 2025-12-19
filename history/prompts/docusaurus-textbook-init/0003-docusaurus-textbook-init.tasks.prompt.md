---
id: 3
title: docusaurus-textbook-init
stage: tasks
date: 2025-12-19
surface: agent
model: claude-opus-4-5-20251101
feature: docusaurus-textbook-init
branch: 1-docusaurus-textbook-init
user: Adi
command: /sp.tasks
labels: ["docusaurus", "textbook", "frontend", "tasks", "implementation"]
links:
  spec: specs/1-docusaurus-textbook-init/spec.md
  plan: specs/1-docusaurus-textbook-init/plan.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-docusaurus-textbook-init/tasks.md
 - history/prompts/docusaurus-textbook-init/0003-docusaurus-textbook-init.tasks.prompt.md
tests:
 - none
---

## Prompt

 # TASKS

## 1. CONFIGURATION & TOOLS
- [ ] **Install Plugins:** Run `npm install remark-math rehype-katex @docusaurus/theme-mermaid` in `frontend/`.
- [ ] **Context7 Init:** Create `context7.json` in the project root pointing to `frontend/docs/` for indexing.
- [ ] **Update Config:** Modify `docusaurus.config.js`:
  - Add `remark-math`/`rehype-katex` to `presets`.
  - Enable `mermaid` in markdown config.
  - Set title to "Physical AI & Humanoid Robotics".

## 2. CONTENT GENERATION (The 24 Chapters)
- [ ] **01-Intro:** Create chapters: `Foundations`, `Embodied Intelligence`, `Hardware Lab`, `Course Roadmap`.
- [ ] **02-Module-1 (ROS2):** Create chapters: `Architecture`, `Python Agents`, `URDF Modeling`, `Launch Systems`.
- [ ] **03-Module-2 (Sim):** Create chapters: `Gazebo Physics`, `Unity Rendering`, `Sensor Sim`, `URDF to Sim`.
- [ ] **04-Module-3 (Isaac):** Create chapters: `Isaac Sim Setup`, `Isaac ROS Bridge`, `Visual SLAM`, `Nav2 Planning`.
- [ ] **05-Module-4 (VLA):** Create chapters: `Voice Interface`, `LLM Planner`, `VLA Models`, `Action Decoding`.
- [ ] **06-Capstone:** Create chapters: `Project Specs`, `Design Doc`, `Integration`, `Final Demo`.

## 3. UI IMPLEMENTATION
- [ ] **Admonition:** Add `.admonition-hardware` to `src/css/custom.css` (Yellow/Orange styling).
- [ ] **Homepage:** Replace `src/pages/index.js` content with the Course Title, Subtitle, and "Start Reading" button.

## Response snapshot

Generated comprehensive tasks.md file for the Docusaurus textbook frontend implementation. The file contains 50 specific tasks organized across 6 phases: Setup, Foundational, and 3 user stories (Textbook Navigation, Interactive Learning Experience, Hardware-Aware Learning) plus a Polish phase. Tasks are properly formatted with IDs, story labels where appropriate, and exact file paths.

## Outcome

- ✅ Impact: Complete task breakdown created for Docusaurus textbook implementation
- 🧪 Tests: none
- 📁 Files: 2 files created/updated (tasks.md and PHR)
- 🔁 Next prompts: Ready for implementation phase
- 🧠 Reflection: Tasks organized by user stories to enable independent implementation and testing

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - all required tasks generated with proper format
- Prompt variant (if applicable): Tasks organized by user stories for independent implementation
- Next experiment (smallest change to try): Begin implementation with Phase 1 setup tasks