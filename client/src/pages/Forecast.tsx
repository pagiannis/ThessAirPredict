import ForecastChart from "../components/ForecastChart";
import { Skeleton } from "@/components/ui/skeleton";
import { useForecast } from "@/hooks/useForecast";

const ForecastSkeleton = () => (
  <div className="bg-card p-6 rounded-xl border border-border flex flex-col gap-4">
    <Skeleton className="h-4 w-36" />
    <Skeleton className="h-3 w-52" />
    {/* Chart area */}
    <div className="flex items-end gap-1 h-48 pt-4">
      {Array.from({ length: 16 }).map((_, i) => (
        <Skeleton
          key={i}
          className="flex-1 rounded-sm"
          style={{ height: `${35 + Math.sin(i * 0.7) * 25 + 20}%` }}
        />
      ))}
    </div>
    {/* X-axis labels */}
    <div className="flex justify-between">
      {Array.from({ length: 5 }).map((_, i) => (
        <Skeleton key={i} className="h-3 w-10" />
      ))}
    </div>
  </div>
);

const Forecast = () => {
  const { data, isLoading, isError } = useForecast();

  if (isLoading) return <div className="space-y-6"><ForecastSkeleton /></div>;

  return (
    <div className="space-y-6">
      <div className="bg-card p-6 rounded-xl border border-border">
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
