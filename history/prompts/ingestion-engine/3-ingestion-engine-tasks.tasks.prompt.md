---
id: 3
title: "ingestion-engine-tasks"
stage: "tasks"
date: "2025-12-20"
surface: "agent"
model: "claude-opus-4-5-20251101"
feature: "ingestion-engine"
branch: "2-ingestion-engine"
user: "user"
command: "/sp.tasks"
labels: ["tasks", "ingestion", "implementation"]
links:
  spec: "specs/2-ingestion-engine/spec.md"
  plan: "specs/2-ingestion-engine/plan.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "specs/2-ingestion-engine/tasks.md"
tests: []
---

# PHR: ingestion-engine-tasks

## Input Prompt

```
# TASKS (Spec 1)

## 1. SETUP & CONFIG
- [ ] **Dependencies:** Create `backend/requirements.txt` with: `cohere`, `qdrant-client`, `python-dotenv`, `langchain-text-splitters` (optional but recommended for chunking).
- [ ] **Env Variables:** Update `backend/.env` with `COHERE_API_KEY`, `QDRANT_URL`, and `QDRANT_API_KEY`.

## 2. DATABASE INIT
- [ ] **Schema Script:** Create `backend/init_db.py`.
- [ ] **Collection Logic:** Implement logic to check if collection `physical_ai_textbook` exists; if not, create it with `vector_size: 1024` (for Cohere `embed-english-v3.0`) and `distance: Cosine`.

## 3. INGESTION LOGIC
- [ ] **Parser:** Implement function in `backend/ingest.py` to walk through `frontend/docs/` and strip Markdown frontmatter.
- [ ] **Chunker:** Implement text splitting (overlap: 50 tokens, chunk_size: 500 tokens).
- [ ] **Embedding Loop:** Implement batch processing (send chunks to Cohere API).
- [ ] **Upsert:** Write logic to push vectors + metadata (filename, content preview) to Qdrant.
```

## Response Summary

Created a comprehensive task breakdown for the ingestion engine backend feature with 28 specific tasks organized across 7 phases:

1. **Phase 1: Setup** - Project structure and dependencies
2. **Phase 2: Foundational** - Database initialization
3. **Phase 3: User Story 1** - Textbook content ingestion (P1 priority)
4. **Phase 4: User Story 2** - Vector embedding generation (P2 priority)
5. **Phase 5: User Story 3** - Vector storage management (P3 priority)
6. **Phase 6: Integration and Testing** - Complete pipeline integration
7. **Phase 7: Polish & Cross-Cutting Concerns** - Edge cases and finishing touches

The tasks follow the required checklist format with proper IDs, parallelization markers, and user story labels. Each task is specific enough to be executed independently and includes file paths. The implementation follows the single-file design with specific functions as requested (`get_all_urls`, `extract_text_from_url`, `chunk_text`, `embed`, `create_collection`, `save_chunk_to_qdrant`, and `main`).

## Outcome

Task breakdown is complete with 28 specific, actionable tasks that follow the checklist format. The tasks are organized by user story priority and include proper dependencies and parallel execution opportunities. Ready for implementation.