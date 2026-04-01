import Header from "@/components/Header";
import HeroSection from "@/components/HeroSection";
import { Outlet } from "react-router-dom";

const Layout = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <HeroSection />

      <main className="container py-12">
        <Outlet />
        <footer className="text-center py-8 border-t border-border">
          <p className="text-xs text-muted-foreground">
            ThessAIRPredict · AI-based Air Pollution Prediction
          </p>
        </footer>
      </main>
    </div>
  );
};

export default Layout;
