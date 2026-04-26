# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

No test runner is configured.

## Architecture

**ThessAirPredict** is a React 19 + TypeScript SPA for air quality monitoring and forecasting in Thessaloniki. Built with Vite, styled with Tailwind CSS 4 and shadcn/ui (radix-nova style).
It is a project with concept: AI-based air quality forecasting

### Routing

Two pages under a shared `Layout`:

```
/ (Layout.tsx)
  ├── Dashboard (index)   — live AQI overview
  └── /forecast           — 48-hour forecast chart
```

`App.tsx` → `RouterProvider` → `routes.tsx` defines the route tree.
`Layout.tsx` wraps pages with `Header` + `HeroSection` (dynamic per route) + `<Outlet>`.

### Component hierarchy

- **Dashboard.tsx** — assembles the main page: `AqiOverview` (left column, 2-row span), six `PollutantCard`s (PM2.5, PM10, NO₂, O₃, CO, SO₂) in a 3-col grid, then `StationMap`.
- **Forecast.tsx** — renders `ForecastChart` (Recharts area chart, 48-hour AQI).
- **HeroSection.tsx** — background image + gradient overlay, content varies by active route.
- All data is currently static/mock — no API integration yet.

### Styling conventions

- Tailwind CSS 4 via `@tailwindcss/vite` plugin (no `tailwind.config.js` — config lives inside CSS).
- Design tokens are CSS custom properties declared in `src/index.css`: colors (background, foreground, primary `#17a697`, AQI bands good/moderate/unhealthy), font families (Space Grotesk display, Inter body).
- Use `cn()` from `src/lib/utils.ts` (clsx + tailwind-merge) for conditional class composition.
- shadcn components live in `src/components/ui/`; use Class Variance Authority for variant props.
- Framer Motion is available for animations.

### Path alias

`@/` resolves to `./src/` — use it for all internal imports.

### Adding shadcn components

Components are configured via `components.json` (style: radix-nova, base color: neutral). Add new primitives with the shadcn CLI and place them in `src/components/ui/`.
