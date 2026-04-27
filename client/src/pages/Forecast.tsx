import ForecastChart from "../components/ForecastChart";
import { useForecast } from "@/hooks/useForecast";

const Forecast = () => {
  const { data, isLoading, isError } = useForecast();

  return (
    <div className="space-y-6">
      <div>
        <p className="text-muted-foreground">
          AI-driven predictions for the next 7 days based on local sensor data.
        </p>
      </div>

      <div className="bg-card p-6 rounded-xl border border-border">
        {isLoading && (
          <p className="text-muted-foreground text-sm">Loading forecast…</p>
        )}
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
