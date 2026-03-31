import { motion } from "framer-motion";
import { MapPin } from "lucide-react";

const stations = [
  { name: "Kordelio", x: 25, y: 40, aqi: 85 },
  { name: "Sindos", x: 15, y: 30, aqi: 92 },
  { name: "Agia Sofia", x: 55, y: 55, aqi: 62 },
  { name: "Panorama", x: 75, y: 35, aqi: 45 },
  { name: "Kalamaria", x: 65, y: 70, aqi: 58 },
];

const getAqiColor = (aqi: number) => {
  if (aqi <= 50) return "text-aqi-good";
  if (aqi <= 100) return "text-aqi-moderate";
  return "text-aqi-unhealthy";
};

const StationMap = () => {
  return (
    <motion.div
      className="bg-card/60 backdrop-blur-xl border border-border/50 rounded-xl p-6"
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5, delay: 0.3 }}
    >
      <h3 className="font-display text-lg font-semibold text-foreground mb-1">
        Monitoring Stations
      </h3>
      <p className="text-xs text-muted-foreground mb-6">
        Live AQI readings across Thessaloniki
      </p>

      <div className="relative bg-secondary/50 rounded-lg h-64 overflow-hidden">
        {/* Stylized map grid */}
        <div className="absolute inset-0 opacity-10">
          {Array.from({ length: 8 }).map((_, i) => (
            <div
              key={`h-${i}`}
              className="absolute w-full border-t border-foreground"
              style={{ top: `${(i + 1) * 12}%` }}
            />
          ))}
          {Array.from({ length: 8 }).map((_, i) => (
            <div
              key={`v-${i}`}
              className="absolute h-full border-l border-foreground"
              style={{ left: `${(i + 1) * 12}%` }}
            />
          ))}
        </div>

        {stations.map((station) => (
          <div
            key={station.name}
            className="absolute group cursor-pointer"
            style={{ left: `${station.x}%`, top: `${station.y}%` }}
          >
            <MapPin
              className={`h-5 w-5 ${getAqiColor(station.aqi)} drop-shadow-lg -translate-x-1/2 -translate-y-full`}
            />
            <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 opacity-0 group-hover:opacity-100 transition-opacity bg-card/60 backdrop-blur-xl border border-border/50 rounded-xl px-2 py-1 whitespace-nowrap">
              <p className="text-xs font-medium text-foreground">
                {station.name}
              </p>
              <p className={`text-xs ${getAqiColor(station.aqi)}`}>
                AQI: {station.aqi}
              </p>
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  );
};

export default StationMap;
