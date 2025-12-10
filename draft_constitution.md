<!-- SYNC IMPACT REPORT: 
Version change: none → 1.0.0
Added sections: All sections as this is the initial constitution
Removed sections: none
Templates requiring updates: none (initial creation)
Follow-up TODOs: RATIFICATION_DATE still needs to be set to actual ratification date
-->

# AI-Native Textbook for Physical AI & Humanoid Robotics Constitution

## Core Principles

### Simplicity First
Keep frontend extremely simple and readable, avoid complexity and heavy dependencies.

### Modular Architecture
Keep backend modular (FastAPI + services + routes), use clean folder structure with `/backend`, `/website`, `/rag`, `/agents`.

### User-Centric Design (NON-NEGOTIABLE)
Clean UI, fast loading, mobile-friendly, support low-end devices (users reading on phones). All features must be tested for usability on mobile devices.

### AI-First Integration
All features should leverage AI capabilities (RAG, personalization, translation). Every component must incorporate AI where beneficial rather than relying solely on traditional programming techniques.

### Performance & Scalability
Must work on free tiers (Qdrant + Neon), must deploy within 90 seconds demo recording, optimized for performance. Code must be efficient enough to run on low-end devices.

### Quality & Accuracy
RAG answers accurate, cited, and grounded, high-quality Urdu translation for every chapter. All AI-generated content must undergo verification for factual accuracy.

## Technical Constraints

All data must be stored cleanly in Neon + Qdrant. Use the following technology stack:
- Frontend: Docusaurus-based interactive textbook
- Backend: FastAPI with modular service architecture
- Authentication: Better-Auth
- Vector Storage: Qdrant
- Database: Neon
- Deployment: Frontend → Vercel, Backend → Railway

## Development Workflow

Development must follow iterative phases with emphasis on reusable agent skills for bonus scoring. The textbook should comprise 10-12 short, clean, modern chapters that can be read in under 60 minutes total. Each feature must be built in phases to manage token usage and ensure steady progress toward the final deliverables:
1. Functional Docusaurus-based textbook
2. Fully operational RAG chatbot
3. User authentication and personalization
4. Translation and auxiliary features
5. Summaries, quizzes, and learning boosters

## Governance

This constitution supersedes all other development practices for this project. All pull requests and reviews must verify compliance with these principles. All features must be testable and demonstrable. The project must result in a 90-second demo recording showing all functionality working together.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): Original adoption date unknown | **Last Amended**: 2025-01-09