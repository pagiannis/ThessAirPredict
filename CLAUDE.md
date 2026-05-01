# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

No test runner is configured.

## Project Overview
AI-based air quality forecasting for Thessaloniki.
- **Frontend:** React 19, TypeScript, Vite, Tailwind 4, shadcn/ui.
- **Backend:** FastAPI (Python 3.11+), OpenAQ v3 API.
- **ML:** scikit-learn RandomForest trained on EEA historical data, served by the backend.


### ML retraining (`ml/` with its own venv)
```bash
python preprocessing.py   # fetch + process EEA data → features CSV
python train_model.py     # train RandomForest → model.pkl
# Then manually copy: cp ml/model.pkl server/model/model.pkl
```

## Environment Variables
- `client/.env`: `VITE_API_URL=http://localhost:8000` (consumed via `import.meta.env.VITE_API_URL` in `lib/axios.ts`)
- `server/.env`: `OPENAQ_API_KEY=<key>` and optionally `CORS_ORIGINS=["..."]`

## Architecture

### Request Flow
```
Browser → React Query hook → lib/api.ts → axios (baseURL=VITE_API_URL)
       → FastAPI route → service → OpenAQ v3 / open-meteo
```

Two API endpoints, both under `/api`:
- `GET /api/air-quality` → `services/openaq.py::fetch_air_quality()` — live readings, 5-min in-memory cache
- `GET /api/forecast` → `services/prediction.py::generate_forecast()` — calls `fetch_air_quality()` then runs the RandomForest

### ML Inference Pipeline
`generate_forecast()` in `services/prediction.py`:
1. Extracts NO₂, O₃, CO, SO₂ concentrations from the cached air quality data.
2. Fetches current weather from open-meteo (temperature, humidity, precipitation, wind speed); falls back to hardcoded defaults if unavailable.
3. Runs the RandomForest for each forecast horizon (0 h to 48 h, step 3 h). The "Now" point uses the live AQI directly.
4. Feature column order is fixed: `[hour, day_of_week, month, hours_ahead, no2_conc, o3_conc, co_conc, so2_conc, temperature, humidity, precipitation, wind_speed]` — must match `ml/preprocessing.py::FEATURE_COLS` exactly or predictions will be silently wrong.

### Critical Sync Points
- **AQI breakpoints** — EPA piecewise breakpoints for NO₂, O₃, SO₂ are duplicated in `server/services/openaq.py` and `ml/preprocessing.py`. Both files must stay identical.
- **Schema contract** — `server/models/schemas.py` (Pydantic) and `client/src/types/api.ts` (TypeScript) must stay in sync. `AqiLabel` and `Trend` are `Literal`/union types in both.
- **Model file** — `server/model/model.pkl` is loaded lazily on the first `/api/forecast` request. After retraining, copy the new pkl manually (no automated step exists).

## Strategic Guidelines
- **Modern React:** Functional components with hooks. Prefer `const Component = () => ...`.
- **Typing:** Strict TypeScript (`strict: true`, `noUnusedLocals`, `noUnusedParameters`). Prefer `interface` for API responses and component props.
- **Styling:** Tailwind 4 utility classes. Use `cn()` from `lib/utils.ts` for all conditional classes. AQI colour tokens (`aqi-good`, `aqi-moderate`, `aqi-unhealthy`, `aqi-very-unhealthy`, `aqi-hazardous`) are defined as CSS custom properties in `index.css` and exposed as Tailwind theme tokens.
- **Data fetching:** All fetch logic goes through `lib/api.ts` → `lib/axios.ts`. Use React Query hooks (`useAirQuality`, `useForecast`) — do not fetch directly in components.

## Routing & Component Structure
- Routes defined in `src/routes.tsx` using React Router v7 data router (`createBrowserRouter`). Layout wraps both pages; `errorElement` handles navigation errors.
- `HeroSection` content switches based on `useLocation()` — no props needed.
- `src/components/ui/`: shadcn primitives only. `src/components/`: feature components. `src/pages/`: page-level components and `Layout`.
- Path alias: `@/*` → `./src/*`

## Adding shadcn Components
```bash
cd client && npx shadcn@latest add [component]
```
