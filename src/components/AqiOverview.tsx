import { motion } from "framer-motion";

const AqiOverview = () => {
  const aqiValue = 72;
  const aqiLabel = "Moderate";

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
        <div className="h-32 w-32 rounded-full border-4 border-aqi-moderate flex items-center justify-center">
          <span className="font-display text-5xl font-bold text-aqi-moderate">
            {aqiValue}
          </span>
        </div>
      </div>
      <p className="font-display text-lg font-semibold text-aqi-moderate">
        {aqiLabel}
      </p>
      <p className="text-muted-foreground text-xs mt-2">Updated 5 min ago</p>
    </motion.div>
  );
};

export default AqiOverview;
