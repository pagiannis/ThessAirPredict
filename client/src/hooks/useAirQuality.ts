import { useQuery } from "@tanstack/react-query";
import { fetchAirQuality } from "@/lib/api";

export const useAirQuality = () =>
  useQuery({
    queryKey: ["air-quality"],
    queryFn: fetchAirQuality,
    refetchInterval: 60_000,
  });
