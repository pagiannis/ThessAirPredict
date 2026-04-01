import Header from "@/components/Header";
import HeroSection from "@/components/HeroSection";
import { Outlet, useLocation } from "react-router-dom";

const Layout = () => {
  const location = useLocation();

  const getHeroContent = () => {
    switch (location.pathname) {
      case "/forecast":
        return {
          badge: "48-hour AI Forecast",
          title: (
            <>
              Atmospheric <br />
              <span className="text-primary">Forecast</span>
            </>
          ),
        };
      default:
        return {
          badge: "AI-Powered Environmental Monitoring",
          title: (
            <>
              Air Pollution <br />
              <span className="text-primary">Prediction</span>
            </>
          ),
          subtitle:
            "Real-time air quality monitoring and ML-based forecasting for the city of Thessaloniki.",
        };
    }
  };

  const currentHero = getHeroContent();

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <HeroSection
        badge={currentHero.badge}
        title={currentHero.title}
        subtitle={currentHero.subtitle}
      />

      <main className="container py-12">
        <Outlet />
        <footer className="text-center py-8 border-t border-border mt-12">
          <p className="text-xs text-muted-foreground">
            ThessAIRPredict · AI-based Air Pollution Prediction
          </p>
        </footer>
      </main>
    </div>
  );
};

export default Layout;
