import { motion } from "framer-motion";
import type { LucideIcon } from "lucide-react";

interface Props {
  name: string;
  value: number;
  unit: string;
  icon: LucideIcon;
  trend: "up" | "down" | "stable";
  index: number;
}

const PollutantCard = ({
  name,
  value,
  unit,
  icon: Icon,
  trend,
  index,
}: Props) => {
  return (
    <motion.div
      className="bg-card/60 backdrop-blur-xl border border-border/50 rounded-xl p-5 hover:border-primary/30 transition-colors group"
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.4, delay: index * 0.1 }}
    >
      <div className="flex items-start justify-between mb-3">
        <Icon className="h-5 w-5 text-muted-foreground group-hover:text-primary transition-colors" />
        <span className={`text-xs font-medium ${[trend]}`}>{trend}</span>
      </div>
      <p className="font-display text-2xl font-bold text-foreground">
        {value}
        <span className="text-sm text-muted-foreground ml-1 font-normal">
          {unit}
        </span>
      </p>
      <p className="text-xs text-muted-foreground mt-1">{name}</p>
    </motion.div>
  );
};

export default PollutantCard;
