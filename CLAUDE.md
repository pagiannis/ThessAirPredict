# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

No test runner is configured.

## Project Overview
AI-based air quality forecasting for Thessaloniki.
- **Frontend:** React 19, TypeScript, Vite, Tailwind 4, shadcn/ui.
- **Backend:** FastAPI (Python 3.11+), OpenAQ v3 API.

## Strategic Guidelines
- **Modern React:** Use Functional Components with Hooks. Prefer `const Component = () => ...`.
- **Typing:** Strict TypeScript. Prefer `interface` for API responses and component props.
- **Styling:** Use Tailwind 4 utility classes. Use the `cn()` utility for all conditional classes.
- **State/Data:** Use `src/lib/api.ts` for all fetch logic. Use React Query and axios for data fetching from the backned.

## Architecture & Routing
- **Routes:** Defined in `src/routes.tsx`. Layout-based structure.
- **Hero Section:** The `HeroSection` content is determined by the `useLocation()` hook within the component.

## Component Hierarchy
- `src/components/ui/`: Low-level shadcn primitives.
- `src/components/`: Other components.
- `src/pages/`: Layout, Home Page, Forecast Page.

## Backend (FastAPI)
- **Caching:** 5-minute in-memory cache in `openaq.py`.
- **Forecast Logic:** `forecaster.py` uses a sinusoidal model (peaks at 08:00 and 18:00).
- **Validation:** Pydantic models in `server/models/schemas.py` must sync with `client/src/types/api.ts`.

## Development Workflow
### Setup
1. Client: `cd client && npm install`
2. Server: `cd server && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`

### Common Commands
- `npm run dev`: Start Vite dev server.
- `python server/main.py`: Start FastAPI (or use uvicorn).
- `npx shadcn@latest add [component]`: Add new UI primitives.

## Path Aliases
- `@/*` -> `./src/*`