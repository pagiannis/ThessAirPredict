import { useQuery } from "@tanstack/react-query";
import { fetchForecast } from "@/lib/api";

export const useForecast = () =>
  useQuery({
    queryKey: ["forecast"],
    queryFn: fetchForecast,
    refetchInterval: 300_000,
  });
