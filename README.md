# ERP Copilot

A modern ERP web application with an AI-powered Copilot chat interface.

## Repository links

- GitHub: https://github.com/Tejaswi0624/erp-copilot
- Vercel frontend demo: https://erp-copilot-nine.vercel.app

## Project structure

- `backend/` — FastAPI backend with SQLAlchemy models, auth, business services, and API routers
- `frontend/` — React + TypeScript Vite frontend with Tailwind CSS, routing, and voice-enabled AI chat
- `vercel.json` — Vercel configuration for the frontend static deployment

## Verified status

- ✅ Frontend production build succeeds
- ✅ Backend Python files compile cleanly
- ⚠️ Current Vercel deployment includes only the frontend app. The backend API is not deployed as part of this same Vercel project.

## Getting started locally

### 1. Backend setup

```bash
cd backend
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Then start the backend:

```bash
uvicorn app.main:app --reload
```

The backend will run at `http://127.0.0.1:8000`.

### 2. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Open the frontend in your browser at `http://localhost:5173`.

### 3. Run order

1. Start the backend first
2. Then start the frontend
3. Visit `http://localhost:5173`

This ensures the frontend can reach the backend API at `/api`.

## AI backend configuration

The backend can use either local Ollama or OpenAI:

- `USE_OLLAMA=true` uses the local Ollama server
- `OPENAI_API_KEY` is required if `USE_OLLAMA=false`

Default values are provided in `backend/.env.example`.

## Production build

Build the frontend for production:

```bash
cd frontend
npm run build
```

## Deployment

Current Vercel deployment is configured for frontend hosting only.

Deploy with:

```bash
cd /path/to/erp-copilot
npx vercel --prod --yes
```

When deploying the backend for a full-stack app, use a separate backend host and update `frontend/src/lib/api.ts` if needed.

## Notes for reviewers

- The frontend is a complete React/Vite app with module routing and an AI chat page
- The backend is a FastAPI app with seeded demo data and JWT auth
- To run the full app locally, both backend and frontend must be running
- `backend/.env.example` is provided for easy setup

## Helpful links

- GitHub source: https://github.com/Tejaswi0624/erp-copilot
- Live frontend demo: https://erp-copilot-nine.vercel.app
