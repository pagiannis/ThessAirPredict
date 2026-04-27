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
  lat: number;
  lon: number;
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
