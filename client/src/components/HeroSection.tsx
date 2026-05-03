import { AnimatePresence, motion } from "framer-motion";
import heroImage from "@/assets/thessaloniki-hero.jpg";

interface Props {
  title: React.ReactNode;
  subtitle?: string;
  badge?: string;
}

const HeroSection = ({ title, subtitle, badge }: Props) => {
  return (
    <section className="relative h-[70vh] min-h-[500px] flex items-end overflow-hidden">
      <img
        src={heroImage}
        alt="Thessaloniki skyline with haze"
        className="absolute inset-0 w-full h-full object-cover select-none"
        width={1920}
        height={800}
      />
      <div className="absolute inset-0 bg-gradient-to-t from-background via-background/70 to-background/20 select-none" />

      <div className="container relative z-10 pb-16">
        <AnimatePresence mode="wait">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
          >
            <p className="text-primary font-display text-base tracking-[0.1em] uppercase mb-3">
              {badge}
            </p>
            <h1 className=" text-foreground font-display text-4xl md:text-6xl font-bold leading-tight mb-4">
              {title}
            </h1>
            <p className="text-muted-foreground max-w-lg text-base md:text-lg leading-relaxed">
              {subtitle}
            </p>
          </motion.div>
        </AnimatePresence>
      </div>
    </section>
  );
};

export default HeroSection;
