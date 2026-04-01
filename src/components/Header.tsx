import { Wind } from "lucide-react";
import { Link, NavLink } from "react-router-dom";

const Header = () => {
  const navItems = [
    { label: "Dashboard", path: "/" },
    { label: "Forecast", path: "/forecast" },
  ];

  return (
    <header className="mx-2 sm:mx-10 lg:mx-40 fixed top-0 left-0 right-0 z-50 bg-card/60 backdrop-blur-xl border border-border/50 rounded-xl border-t-0 rounded-t-none border-x-0">
      <div className="container flex items-center justify-between h-16">
        <Link
          to="/"
          className="flex items-center gap-2 hover:opacity-80 transition-opacity"
        >
          <Wind className="h-6 w-6 text-primary" />
          <span className="font-display font-bold text-lg text-foreground">
            ThessAIRPredict
          </span>
        </Link>

        <nav className="hidden md:flex items-center gap-8">
          {navItems.map(({ label, path }) => (
            <NavLink
              key={label}
              to={path}
              className={({ isActive }) =>
                `text-sm font-medium transition-colors hover:text-primary ${
                  isActive ? "text-primary" : "text-muted-foreground"
                }`
              }
            >
              {label}
            </NavLink>
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
