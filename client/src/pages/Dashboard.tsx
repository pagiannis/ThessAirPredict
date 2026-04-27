import { Atom, Cigarette, Cloud, Droplets, Flame, Wind } from "lucide-react";
import type { LucideIcon } from "lucide-react";
import AqiOverview from "../components/AqiOverview";
import PollutantCard from "../components/PollutantCard";
import StationMap from "../components/StationMap";
import DashboardSkeleton from "@/components/DashboardSkeleton";
import { useAirQuality } from "@/hooks/useAirQuality";

const POLLUTANT_ICONS: Record<string, LucideIcon> = {
  "PM2.5": Cloud,
  PM10: Droplets,
  "NO₂": Flame,
  "O₃": Atom,
  "SO₂": Cigarette,
  CO: Wind,
};

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
