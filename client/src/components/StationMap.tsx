import { motion } from "framer-motion";
import { MapContainer, TileLayer, CircleMarker, Tooltip } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import type { StationReading } from "@/types/api";

const THESS_CENTER: [number, number] = [40.6401, 22.9444];

const getAqiColor = (aqi: number): string => {
  if (aqi <= 50)  return "hsl(var(--aqi-good))";
  if (aqi <= 100) return "hsl(var(--aqi-moderate))";
  if (aqi <= 150) return "hsl(var(--aqi-unhealthy-sensitive))";
  if (aqi <= 200) return "hsl(var(--aqi-unhealthy))";
  if (aqi <= 300) return "hsl(var(--aqi-very-unhealthy))";
  return "hsl(var(--aqi-hazardous))";
};

interface Props {
  stations: StationReading[];
}

const StationMap = ({ stations }: Props) => {
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

      <div className="rounded-lg overflow-hidden h-64">
        <MapContainer
          center={THESS_CENTER}
          zoom={11}
          style={{ height: "100%", width: "100%" }}
          scrollWheelZoom={false}
          zoomControl={false}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            opacity={0.45}
          />
          {stations.map((station) => (
            <CircleMarker
              key={station.name}
              center={[station.lat, station.lon]}
              radius={10}
              fillColor={getAqiColor(station.aqi)}
              color="white"
              weight={2}
              fillOpacity={0.9}
            >
              <Tooltip permanent direction="top" offset={[0, -14]}>
                <span className="font-medium">{station.name}</span>
                <br />
                <span>AQI {station.aqi}</span>
              </Tooltip>
            </CircleMarker>
          ))}
        </MapContainer>
      </div>
    </motion.div>
  );
};

export default StationMap;
