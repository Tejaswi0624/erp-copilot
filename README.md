# ERP Copilot

A modern ERP web application with an AI-powered Copilot chat interface.

## Repository links

- GitHub: https://github.com/Tejaswi0624/erp-copilot
- Vercel frontend demo: https://erp-copilot-nine.vercel.app

## Project structure

- `backend/` — FastAPI backend with SQLAlchemy models, auth, business services, and API routers
- `frontend/` — React + TypeScript Vite frontend with Tailwind CSS, routing, and voice-enabled AI chat
- `vercel.json` — Vercel configuration for the frontend static deployment
# ERP Copilot

A modern, production-oriented ERP web application with an AI Copilot assistant for business insights.

<!-- Project badges -->

[![Build Frontend](https://img.shields.io/badge/build-frontend-brightgreen)](https://erp-copilot-nine.vercel.app)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

Overview
--------
ERP Copilot is a full-stack example ERP with modules for Finance, HR, Inventory, Sales, CRM and Manufacturing, plus an AI-driven Copilot chat that summarizes data and answers operational questions.

## Repository

- GitHub: https://github.com/Tejaswi0624/erp-copilot
- Live frontend demo: https://erp-copilot-nine.vercel.app

## Project structure

- `backend/` — FastAPI backend with SQLAlchemy models, auth, business services, and API routers
- `frontend/` — React + TypeScript Vite frontend with Tailwind CSS, routing, and voice-enabled AI chat
- `vercel.json` — Vercel configuration for the frontend static deployment

## Current status

- Frontend: production build verified and deployed to Vercel (static hosting).
- Backend: FastAPI app included in repo; not deployed by the Vercel frontend project by default. To enable full end-to-end behavior deploy the backend separately or configure API hosting.

## Quickstart (developer)

1) Prepare backend

```bash
cd backend
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend default: http://127.0.0.1:8000

2) Prepare frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend default: http://localhost:5173

3) Recommended run order

- Start the backend first, then the frontend. The frontend expects the API under `/api`.

## AI backend configuration

The Copilot chat uses a local Ollama instance by default or OpenAI as a fallback. Configure `backend/.env`:

- `USE_OLLAMA=true` to call local Ollama (must be running at `OLLAMA_BASE_URL`).
- If `USE_OLLAMA=false`, set `OPENAI_API_KEY` and `OPENAI_MODEL`.

See `backend/.env.example` for supported variables.

## Production build

Build the frontend for production:

```bash
cd frontend
npm run build
```

## Deployment notes

- The repo includes `vercel.json` configured to build and publish the static frontend to Vercel.
- To run the full product in production you should deploy the backend to a server/host (e.g., Render, Railway, Fly, a Vercel Serverless project, or a container service) and point the frontend API base URL to that host.

Example quick deploy (frontend only):

```bash
cd /path/to/erp-copilot
npx vercel --prod --yes
```

## For reviewers

Checklist:

1. Clone repository and inspect `backend/` and `frontend/` code.
2. Run backend and confirm `GET /api/health` returns `{"status":"healthy"}`.
3. Run frontend and confirm pages load and API calls target `/api/`.
4. Open `/copilot` and test the chat UI; note AI replies depend on the AI backend configuration.

If you want a single-click preview for reviewers, consider deploying the backend to a short-lived preview URL and updating `frontend/src/lib/api.ts` to point there.

---

If you'd like, I can also add a short `CONTRIBUTING.md` and an `MIT` license file — tell me and I will add them and push a single commit.

- GitHub source: https://github.com/Tejaswi0624/erp-copilot
- Live frontend demo: https://erp-copilot-nine.vercel.app
