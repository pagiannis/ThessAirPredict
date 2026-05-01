import { motion } from "framer-motion";
import type { AqiLabel } from "@/types/api";

const AQI_COLOR: Record<AqiLabel, string> = {
  Good: "text-aqi-good border-aqi-good",
  Moderate: "text-aqi-moderate border-aqi-moderate",
  Unhealthy: "text-aqi-unhealthy border-aqi-unhealthy",
  "Very Unhealthy": "text-aqi-very-unhealthy border-aqi-very-unhealthy",
  Hazardous: "text-aqi-hazardous border-aqi-hazardous",
};

interface Props {
  aqi: number;
  label: AqiLabel;
  updatedAt: string;
}

const AqiOverview = ({ aqi, label, updatedAt }: Props) => {
  const colorClass = AQI_COLOR[label];
  const time = new Date(updatedAt).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <motion.div
      className="bg-card/60 backdrop-blur-xl border border-border/50 rounded-xl p-8 shadow-lg flex flex-col items-center justify-center text-center"
      initial={{ opacity: 0, scale: 0.95 }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5 }}
    >
      <p className="text-xs text-muted-foreground uppercase tracking-widest mb-4">
        Current AQI
      </p>
      <div className="relative mb-4">
        <div
          className={`h-32 w-32 rounded-full border-4 flex items-center justify-center ${colorClass}`}
        >
          <span className={`font-display text-5xl font-bold ${colorClass}`}>
            {aqi}
          </span>
        </div>
      </div>
      <p className={`font-display text-lg font-semibold ${colorClass}`}>
        {label}
      </p>
      <p className="text-muted-foreground text-xs mt-2">Updated at {time}</p>
    </motion.div>
  );
};

export default AqiOverview;
