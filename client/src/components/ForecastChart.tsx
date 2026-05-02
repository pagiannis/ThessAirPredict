import { motion } from "framer-motion";
import {
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Area,
  AreaChart,
} from "recharts";
import type { ForecastPoint } from "@/types/api";

interface Props {
  data: ForecastPoint[];
}

function formatForecastTime(time: string): string {
  if (time === "Now") return "Now";
  const match = time.match(/^\+(\d+)h$/);
  if (!match) return time;
  const hours = parseInt(match[1]);
  const base = new Date();
  base.setMinutes(0, 0, 0);
  const target = new Date(base.getTime() + hours * 3_600_000);
  const timeStr = target.toLocaleTimeString("en-US", {
    hour: "numeric",
    hour12: true,
  });
  if (target.getDate() === base.getDate()) return timeStr;
  const day = target.toLocaleDateString("en-US", { weekday: "short" });
  return `${day} ${timeStr}`;
}

const ForecastChart = ({ data }: Props) => {
  const chartData = data.map((p) => ({
    ...p,
    label: formatForecastTime(p.time),
  }));

  const aqiValues = chartData.map((d) => d.aqi);
  const domainMin = Math.max(0, Math.min(...aqiValues) - 10);
  const domainMax = Math.min(500, Math.max(...aqiValues) + 10);

  return (
    <motion.div
      className="bg-card/60 backdrop-blur-xl border border-border/50 rounded-xl p-4 sm:p-6"
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5, delay: 0.2 }}
    >
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="font-display text-lg font-semibold text-foreground">
            48h AQI Forecast
          </h3>
          <p className="text-xs text-muted-foreground">
            ML-based prediction model
          </p>
        </div>
      </div>
      <div className="h-48 sm:h-64">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="aqiGradient" x1="0" y1="0" x2="0" y2="1">
                <stop
                  offset="0%"
                  stopColor="hsl(174, 72%, 46%)"
                  stopOpacity={0.3}
                />
                <stop
                  offset="100%"
                  stopColor="hsl(174, 72%, 46%)"
                  stopOpacity={0}
                />
              </linearGradient>
            </defs>
            <XAxis
              dataKey="label"
              axisLine={false}
              tickLine={false}
              tick={{ fill: "hsl(215, 12%, 50%)", fontSize: 12 }}
              interval={3}
            />
            <YAxis
              axisLine={false}
              tickLine={false}
              tick={{ fill: "hsl(215, 12%, 50%)", fontSize: 12 }}
              domain={[domainMin, domainMax]}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "hsl(220, 18%, 11%)",
                border: "1px solid hsl(220, 14%, 18%)",
                borderRadius: "8px",
                color: "hsl(200, 20%, 92%)",
                fontSize: 12,
              }}
            />
            <Area
              type="monotone"
              dataKey="aqi"
              stroke="hsl(174, 72%, 46%)"
              strokeWidth={2}
              fill="url(#aqiGradient)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </motion.div>
  );
};

export default ForecastChart;
