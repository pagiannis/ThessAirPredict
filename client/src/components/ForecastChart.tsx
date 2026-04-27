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

const ForecastChart = ({ data }: Props) => {
  return (
    <motion.div
      className="glass-card p-6"
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
        <span className="text-xs text-primary bg-primary/10 px-3 py-1 rounded-full">
          LSTM Model
        </span>
      </div>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data}>
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
              dataKey="time"
              axisLine={false}
              tickLine={false}
              tick={{ fill: "hsl(215, 12%, 50%)", fontSize: 12 }}
            />
            <YAxis
              axisLine={false}
              tickLine={false}
              tick={{ fill: "hsl(215, 12%, 50%)", fontSize: 12 }}
              domain={[40, 90]}
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
