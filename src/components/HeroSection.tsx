import { motion } from "framer-motion";
import { ArrowDown } from "lucide-react";
import heroImage from "@/assets/thessaloniki-hero.jpg";

const HeroSection = () => {
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
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          <p className="text-primary font-display text-sm tracking-[0.2em] uppercase mb-3">
            AI-Powered Environmental Monitoring
          </p>
          <h1 className=" text-foreground font-display text-4xl md:text-6xl font-bold leading-tight mb-4">
            Air Pollution
            <br />
            <span className="text-primary">Prediction</span>
          </h1>
          <p className="text-muted-foreground max-w-lg text-base md:text-lg leading-relaxed">
            Real-time air quality monitoring and ML-based forecasting for the
            city of Thessaloniki.
          </p>
        </motion.div>

        <motion.div
          className="mt-8"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1, duration: 0.6 }}
        >
          <a
            href="#dashboard"
            className="inline-flex items-center gap-2 text-sm text-primary hover:text-primary/80 transition-colors"
          >
            Explore Data <ArrowDown className="h-4 w-4 animate-bounce" />
          </a>
        </motion.div>
      </div>
    </section>
  );
};

export default HeroSection;
