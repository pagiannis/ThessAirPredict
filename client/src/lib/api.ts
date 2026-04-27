export type AqiLabel =
  | "Good"
  | "Moderate"
  | "Unhealthy"
  | "Very Unhealthy"
  | "Hazardous";

export type Trend = "up" | "down" | "stable";

export interface PollutantReading {
  name: string;
  value: number;
  unit: string;
  trend: Trend;
}

export interface StationReading {
  name: string;
  x: number;
  y: number;
  aqi: number;
}

export interface AirQualityResponse {
  aqi: number;
  aqi_label: AqiLabel;
  updated_at: string;
  pollutants: PollutantReading[];
  stations: StationReading[];
}

export interface ForecastPoint {
  time: string;
  aqi: number;
}

export interface ForecastResponse {
  forecast: ForecastPoint[];
}

const API_URL = import.meta.env.VITE_API_URL;

const _mockAirQuality: AirQualityResponse = {
  aqi: 72,
  aqi_label: "Moderate",
  updated_at: new Date().toISOString(),
  pollutants: [
    { name: "PM2.5", value: 28, unit: "μg/m³", trend: "up" },
    { name: "PM10", value: 42, unit: "μg/m³", trend: "stable" },
    { name: "NO₂", value: 35, unit: "μg/m³", trend: "down" },
    { name: "O₃", value: 48, unit: "μg/m³", trend: "up" },
    { name: "SO₂", value: 8, unit: "μg/m³", trend: "down" },
    { name: "CO", value: 0.6, unit: "mg/m³", trend: "stable" },
  ],
  stations: [
    { name: "Kordelio", x: 25, y: 40, aqi: 85 },
    { name: "Sindos", x: 15, y: 30, aqi: 92 },
    { name: "Agia Sofia", x: 55, y: 55, aqi: 62 },
    { name: "Panorama", x: 75, y: 35, aqi: 45 },
    { name: "Kalamaria", x: 65, y: 70, aqi: 58 },
  ],
};

const _mockForecast: ForecastResponse = {
  forecast: [
    { time: "Now", aqi: 72 },
    { time: "+3h", aqi: 68 },
    { time: "+6h", aqi: 65 },
    { time: "+12h", aqi: 58 },
    { time: "+24h", aqi: 52 },
    { time: "+36h", aqi: 61 },
    { time: "+48h", aqi: 70 },
  ],
};

export async function fetchAirQuality(): Promise<AirQualityResponse> {
  if (!API_URL) return _mockAirQuality;
  const res = await fetch(`${API_URL}/api/air-quality`);
  if (!res.ok) throw new Error("Failed to fetch air quality data");
  return res.json();
}

export async function fetchForecast(): Promise<ForecastResponse> {
  if (!API_URL) return _mockForecast;
  const res = await fetch(`${API_URL}/api/forecast`);
  if (!res.ok) throw new Error("Failed to fetch forecast data");
  return res.json();
}
