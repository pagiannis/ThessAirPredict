from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import air_quality, forecast
from config import settings

app = FastAPI(title="ThessAirPredict API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(air_quality.router, prefix="/api")
app.include_router(forecast.router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok"}
