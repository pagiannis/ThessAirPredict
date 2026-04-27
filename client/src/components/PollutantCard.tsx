import { motion } from "framer-motion";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";
import type { LucideIcon } from "lucide-react";

interface Props {
  name: string;
  value: number;
  unit: string;
  icon: LucideIcon;
  trend: "up" | "down" | "stable";
  index: number;
}

const TREND_CONFIG = {
  up:     { Icon: TrendingUp,   label: "Rising",  cls: "bg-red-500/15 text-red-400 border-red-500/20" },
  down:   { Icon: TrendingDown, label: "Falling", cls: "bg-emerald-500/15 text-emerald-400 border-emerald-500/20" },
  stable: { Icon: Minus,        label: "Stable",  cls: "bg-muted/40 text-muted-foreground border-border/50" },
} as const;

const PollutantCard = ({
  name,
  value,
  unit,
  icon: Icon,
  trend,
  index,
}: Props) => {
  const { Icon: TrendIcon, label, cls } = TREND_CONFIG[trend];

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
        <span className={`inline-flex items-center gap-1 text-[11px] font-medium px-2 py-0.5 rounded-full border ${cls}`}>
          <TrendIcon className="h-3 w-3" />
          {label}
        </span>
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
