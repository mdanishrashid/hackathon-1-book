---
id: 1
title: AI Native Textbook Constitution
stage: constitution
date: 2025-01-09
surface: agent
model: gpt-4
feature: none
branch: main
user: Administrator
command: /sp.constitution
labels: [constitution,ai,textbook,physical-ai,humanoid-robotics]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - null
---

## Prompt

/sp.constitution # Project Constitution: AI-Native Textbook for Physical AI & Humanoid Robotics
## 1. Mission
Build a fully AI-native, interactive, intelligent textbook that teaches the Physical The product must be fast, simple, beautiful, and feel like a REAL AI-powered educat:
## 2. Core Deliverables
1. A Docusaurus-based interactive textbook with 10-12 short, clean, modern chapters. 2. A fully functional RAG chatbot answering questions ONLY from the book.
3. User authentication (signup/login) using Better-Auth.
4. Personalized chapter content based on user background.
5. One-click Urdu translation for every chapter.
6. Auto-generated summaries, quizzes, and learning boosters.
## 3. Success Criteria
- Clean UI, fast loading, mobile-friendly.
- Book readable in < 60 minutes total.
- RAG answers accurate, cited, and grounded.
- Personalization visibly improves text.
- Urdu translation high-quality and fast. 
Fully deployed:
Frontend → Vercel  
Backend → Railway  
Vectors → Qdrant 
Database Neon
## 4. Non-Goals
- No extra animations beyond minimal useful motion. 
- No overly long chapters (short + clear only).
- No complex robotics code 
-only education content.
## 5. Architecture Principles
- Keep frontend extremely simple, readable.
- Keep backend modular (FastAPI + services + routes).
- All data must be stored cleanly in Neon + Qdrant.
- Use clean folder structure:
- `/backend `/website /rag` `/agents`
Use reusable agent skills for bonus scoring.
## 6. User Stories (Prioritized)
1. As a learner, I want to read the textbook smoothly.
2. As a learner, I want to ask the chatbot questions.
3. As a learner, I want personalized content based on my background.
4. As a learner, I want Urdu translation.
5. As a learner, I want summaries + quizzes.
6. As an admin, I want clean architecture and deployment.
## 7. Constraints
- Must work on free tiers (Qdrant + Neon).
- Must deploy within 90 seconds demo recording.
- Must support low-end devices (users reading on phones). 
- Must avoid complexity and heavy dependencies.
## 8. Risks & Mitigation
**RAG low accuracy** → use chunking + MiniLM embeddings. 
**Token usage high** → implement in phases.
**User confusion** → keep UI minimal and clean. 
**Backend errors** add health checks + logging.
## 9. Definition of Done
All chapters visible and readable.
Chatbot fully functional with grounded answers. 
Auth + personalization + translation working. 
Quizzes + summaries per chapter generated. 
Fully deployed URLS live and stable.
90-second demo recorded.

## Response snapshot

I have successfully updated the project constitution based on your requirements for the AI-Native Textbook for Physical AI & Humanoid Robotics. Here's a summary of what was done:

## Summary of Changes

- **New Version**: 1.0.0 (initial version)
- **Constitution Created**: Complete constitution document with 6 core principles specific to your project
- **Files Updated**: `.specify/memory/constitution.md` has been filled with project-specific principles

## Core Principles Implemented

1. **Simplicity First** - Keep frontend extremely simple and readable
2. **Modular Architecture** - Keep backend modular with clean folder structure
3. **User-Centric Design** - Clean UI, mobile-friendly, supports low-end devices
4. **AI-First Integration** - Leverage AI capabilities throughout all features
5. **Performance & Scalability** - Works on free tiers and optimized for performance
6. **Quality & Accuracy** - Ensure RAG answers are accurate and translations are high-quality

## Technical Constraints & Workflow Defined

- Technology stack: Docusaurus, FastAPI, Better-Auth, Qdrant, Neon DB
- Deployment: Vercel (frontend), Railway (backend)
- Development workflow: Iterative phases with 10-12 chapters in under 60 min total read time

## Next Steps

- Set an actual ratification date to replace the `TODO(RATIFICATION_DATE)` placeholder
- All future development should follow these principles
- The constitution will guide architectural decisions throughout the project

The suggested commit message would be: `docs: create project constitution for AI-native textbook v1.0.0`

## Outcome

- ✅ Impact: Created project constitution with 6 core principles
- 🧪 Tests: No tests required for this change
- 📁 Files: Updated .specify/memory/constitution.md with project-specific values
- 🔁 Next prompts: Ready to implement features following the constitution
- 🧠 Reflection: The constitution properly captures the project's core principles

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementing specific features according to the new constitution