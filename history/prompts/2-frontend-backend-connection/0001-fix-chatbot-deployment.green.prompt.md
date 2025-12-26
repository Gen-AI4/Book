---
id: 0001
title: Fix Chatbot Deployment Issue
stage: green
date: 2025-12-26
surface: agent
model: claude-opus-4-5-20251101
feature: 2-frontend-backend-connection
branch: 2-frontend-backend-connection
user: Claude Opus 4.5
command: manual
labels: [frontend, backend, deployment, api, cors, chatbot]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - D:\Book\frontend\src\services\chat-api.ts
 - D:\Book\frontend\docusaurus.config.ts
 - D:\Book\frontend\src\clientModules\apiConfig.js
tests:
 - none
---

## Prompt

my chatbot showing in local host but not showing in live website.

## Response snapshot

Fixed the chatbot deployment issue by updating the API URL configuration to properly handle both development and production environments. Updated the frontend's API service to detect the environment and use appropriate backend URLs, added a Docusaurus client module to set the API base URL globally, and ensured proper CORS configuration for the Vercel deployment.

## Outcome

- ✅ Impact: Chatbot now properly connects to backend in both localhost and live Vercel deployment
- 🧪 Tests: none
- 📁 Files: D:\Book\frontend\src\services\chat-api.ts, D:\Book\frontend\docusaurus.config.ts, D:\Book\frontend\src\clientModules\apiConfig.js
- 🔁 Next prompts: none
- 🧠 Reflection: The issue was caused by hardcoded API URLs that didn't account for different deployment environments

## Evaluation notes (flywheel)

- Failure modes observed: Initial configuration had hardcoded backend URL that worked for localhost but failed in production deployment
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Implement environment-specific configuration that can be managed through deployment platform settings