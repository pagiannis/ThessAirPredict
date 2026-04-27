import { Atom, Cigarette, Cloud, Droplets, Flame, Wind } from "lucide-react";
import type { LucideIcon } from "lucide-react";
import AqiOverview from "../components/AqiOverview";
import PollutantCard from "../components/PollutantCard";
import StationMap from "../components/StationMap";
import { Skeleton } from "@/components/ui/skeleton";
import { useAirQuality } from "@/hooks/useAirQuality";

const POLLUTANT_ICONS: Record<string, LucideIcon> = {
  "PM2.5": Cloud,
  PM10: Droplets,
  "NO₂": Flame,
  "O₃": Atom,
  "SO₂": Cigarette,
  CO: Wind,
};

const DashboardSkeleton = () => (
  <div className="space-y-8">
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
      {/* AQI overview — tall card */}
      <div className="lg:row-span-2 bg-card/60 border border-border/50 rounded-xl p-6 flex flex-col gap-4">
        <Skeleton className="h-4 w-24" />
        <Skeleton className="h-28 w-28 rounded-full mx-auto" />
        <Skeleton className="h-4 w-32 mx-auto" />
        <Skeleton className="h-3 w-20 mx-auto" />
      </div>
      {/* 6 pollutant cards */}
      {Array.from({ length: 6 }).map((_, i) => (
        <div key={i} className="bg-card/60 border border-border/50 rounded-xl p-5 flex flex-col gap-3">
          <div className="flex items-start justify-between">
            <Skeleton className="h-5 w-5 rounded" />
            <Skeleton className="h-5 w-16 rounded-full" />
          </div>
          <Skeleton className="h-8 w-24" />
          <Skeleton className="h-3 w-16" />
        </div>
      ))}
    </div>
    {/* Station map */}
    <div className="bg-card/60 border border-border/50 rounded-xl p-6 flex flex-col gap-4">
      <Skeleton className="h-4 w-40" />
      <Skeleton className="h-3 w-56" />
      <Skeleton className="h-64 w-full rounded-lg" />
    </div>
  </div>
);

const Dashboard = () => {
  const { data, isLoading, isError } = useAirQuality();

  if (isLoading) return <DashboardSkeleton />;

  if (isError || !data) {
    return (
      <p className="text-aqi-unhealthy text-sm">
        Failed to load air quality data.
      </p>
    );
  }

  const pollutants = data.pollutants.map((p, i) => ({
    ...p,
    icon: POLLUTANT_ICONS[p.name] ?? Cloud,
    index: i,
  }));

  return (
    <div className="space-y-8">
      <div id="dashboard" className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:row-span-2">
          <AqiOverview
            aqi={data.aqi}
            label={data.aqi_label}
            updatedAt={data.updated_at}
          />
        </div>
        {pollutants.map((p) => (
          <PollutantCard key={p.name} {...p} />
        ))}
      </div>

      <div className="grid grid-cols-1 gap-6">
        <StationMap stations={data.stations} />
      </div>
    </div>
  );
};

export default Dashboard;
