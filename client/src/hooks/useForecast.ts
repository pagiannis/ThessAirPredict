import { useQuery } from "@tanstack/react-query";
import { fetchForecast } from "@/lib/api";

export const useForecast = () =>
  useQuery({
    queryKey: ["forecast"],
    queryFn: fetchForecast,
    refetchInterval: 30 * 60_000,
  });
