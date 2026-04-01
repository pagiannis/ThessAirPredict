import { Atom, Cigarette, Cloud, Droplets, Flame, Wind } from "lucide-react";
import AqiOverview from "../components/AqiOverview";
import PollutantCard from "../components/PollutantCard";
import StationMap from "../components/StationMap";

const pollutants = [
  {
    name: "PM2.5",
    value: 28,
    unit: "μg/m³",
    icon: Cloud,
    trend: "up" as const,
  },
  {
    name: "PM10",
    value: 42,
    unit: "μg/m³",
    icon: Droplets,
    trend: "stable" as const,
  },
  { name: "NO₂", value: 35, unit: "ppb", icon: Flame, trend: "down" as const },
  { name: "O₃", value: 48, unit: "ppb", icon: Atom, trend: "up" as const },
  {
    name: "SO₂",
    value: 8,
    unit: "ppb",
    icon: Cigarette,
    trend: "down" as const,
  },
  { name: "CO", value: 0.6, unit: "ppm", icon: Wind, trend: "stable" as const },
];

const Dashboard = () => {
  return (
    <div className="space-y-8">
      <div id="dashboard" className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:row-span-2">
          <AqiOverview />
        </div>
        {pollutants.map((p, i) => (
          <PollutantCard key={p.name} {...p} index={i} />
        ))}
      </div>

      <div className="grid grid-cols-1 gap-6">
        <StationMap />
      </div>
    </div>
  );
};

export default Dashboard;
