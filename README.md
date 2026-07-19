# ERP Copilot

A modern ERP web application with an AI-powered Copilot chat interface.

## Project structure

- `backend/` - FastAPI backend, database models, business services, and API routers.
- `frontend/` - React + TypeScript Vite frontend with Tailwind CSS and AI chat support.
- `vercel.json` - Vercel deployment configuration for the frontend.

## Features

- ERP dashboard, finance, HR, inventory, manufacturing, CRM, and sales modules
- AI Copilot chat interface with voice input and text-to-speech support
- Responsive layout with reusable UI components
- Frontend deployed on Vercel

## Local setup

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open the frontend in your browser at `http://localhost:5173`.

## Production build

From the `frontend/` directory:

```bash
npm run build
```

## Deployment

This repository currently deploys the frontend static site to Vercel. The Vercel project is configured to build and serve `frontend/dist`.

Deploy with:

```bash
cd /path/to/erp-copilot
npx vercel --prod --yes
```

### Deployed frontend URL

- `https://erp-copilot-nine.vercel.app`

### Important note

The current Vercel deployment serves only the frontend app. The backend API is not deployed as part of this same Vercel project, so the AI chat and ERP data API features require a separate backend deployment or backend host.

## Full-stack deployment guidance

To make the app fully functional in production, you should deploy the backend separately and configure the frontend to call that backend API.

Possible options:

- Deploy the backend using a separate Vercel Serverless or Cloud Function project
- Deploy the backend on another host (Heroku, Render, Railway, Fly, etc.)
- Update the frontend API base URL in `frontend/src/lib/api.ts` if the backend runs on a different origin

## Notes

- The backend uses FastAPI and SQLAlchemy.
- The frontend is built with React 19, Vite, and Tailwind CSS.
- Environment variables should be managed securely and are not checked into git.
