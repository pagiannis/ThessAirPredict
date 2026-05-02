import ForecastChart from "../components/ForecastChart";
import ForecastSkeleton from "@/components/ForecastSkeleton";
import { useForecast } from "@/hooks/useForecast";

const Forecast = () => {
  const { data, isLoading, isError } = useForecast();

  if (isLoading)
    return (
      <div className="space-y-6">
        <ForecastSkeleton />
      </div>
    );

  return (
    <div className="space-y-6">
      <div className="bg-card p-2 sm:p-6 rounded-xl border border-border">
        {isError && (
          <p className="text-aqi-unhealthy text-sm">
            Failed to load forecast data.
          </p>
        )}
        {data && <ForecastChart data={data.forecast} />}
      </div>
    </div>
  );
};

export default Forecast;
