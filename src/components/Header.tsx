import { Activity, Info, Map, Wind } from "lucide-react";

const Header = () => {
  return (
    <header className="mx-2 sm:mx-10 lg:mx-40 fixed top-0 left-0 right-0 z-50 bg-card/60 backdrop-blur-xl border border-border/50 rounded-xl border-t-0 rounded-t-none border-x-0">
      <div className="container flex items-center justify-between h-16">
        <div className="flex items-center gap-2">
          <Wind className="h-6 w-6 text-primary" />
          <span className="font-display font-bold text-lg text-foreground">
            ThessAirPredict
          </span>
        </div>
        <nav className="hidden md:flex items-center gap-8">
          {[
            { label: "Dashboard", icon: Activity },
            { label: "Map", icon: Map },
            { label: "About", icon: Info },
          ].map(({ label, icon: Icon }) => (
            <a
              key={label}
              href={`#${label.toLowerCase()}`}
              className="flex items-center gap-1.5 text-sm text-muted-foreground hover:text-primary transition-colors"
            >
              <Icon className="h-4 w-4" />
              {label}
            </a>
          ))}
        </nav>
        <div className="flex items-center gap-2">
          <span className="hidden sm:inline text-xs text-muted-foreground">
            Thessaloniki, GR
          </span>
          <div className="h-2 w-2 rounded-full bg-primary animate-pulse-glow" />
        </div>
      </div>
    </header>
  );
};

export default Header;
