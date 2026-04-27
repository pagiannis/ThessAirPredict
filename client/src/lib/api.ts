import apiClient from "./axios";
import type { AirQualityResponse, ForecastResponse } from "@/types/api";

export async function fetchAirQuality(): Promise<AirQualityResponse> {
  const { data } = await apiClient.get<AirQualityResponse>("/api/air-quality");
  return data;
}

export async function fetchForecast(): Promise<ForecastResponse> {
  const { data } = await apiClient.get<ForecastResponse>("/api/forecast");
  return data;
}
