import { useState } from "react";
import { Menu, X } from "lucide-react";
import { Link, NavLink } from "react-router-dom";
import logo from "@/assets/thita_logo.png";

const Header = () => {
  const [mobileOpen, setMobileOpen] = useState(false);

  const navItems = [
    { label: "Dashboard", path: "/" },
    { label: "Forecast", path: "/forecast" },
  ];

  return (
    <header className="mx-2 sm:mx-10 lg:mx-40 fixed top-0 left-0 right-0 z-50 bg-card/60 backdrop-blur-xl border border-border/50 rounded-xl border-t-0 rounded-t-none border-x-0">
      <div className="container flex items-center justify-between h-16">
        <div className="flex items-center gap-14">
          <Link
            to="/"
            className="flex items-center gap-2 hover:opacity-80 transition-opacity"
          >
            <img
              src={logo}
              alt="ThessAIRPredict logo"
              className="h-12 w-12 object-contain"
            />
            <span className="font-display font-bold text-lg text-foreground">
              ThessAIR Predict
            </span>
          </Link>

          <nav className="hidden md:flex items-center gap-4">
            {navItems.map(({ label, path }) => (
              <NavLink
                key={label}
                to={path}
                className={({ isActive }) =>
                  `text-base font-medium transition-colors hover:text-primary ${
                    isActive
                      ? "text-primary font-bold"
                      : "text-muted-foreground"
                  }`
                }
              >
                {label}
              </NavLink>
            ))}
          </nav>
        </div>

        <div className="flex items-center gap-2">
          <span className="hidden sm:inline font-medium text-base text-muted-foreground">
            Thessaloniki, GR
          </span>
          <div className="h-2 w-2 rounded-full bg-primary animate-pulse-glow" />
          <button
            className="md:hidden ml-2 p-1 text-muted-foreground hover:text-foreground transition-colors"
            onClick={() => setMobileOpen((o) => !o)}
            aria-label="Toggle menu"
          >
            {mobileOpen ? (
              <X className="h-5 w-5" />
            ) : (
              <Menu className="h-5 w-5" />
            )}
          </button>
        </div>
      </div>

      {mobileOpen && (
        <nav className="md:hidden border-t border-border/50 px-6 py-3 flex flex-col gap-1">
          {navItems.map(({ label, path }) => (
            <NavLink
              key={label}
              to={path}
              onClick={() => setMobileOpen(false)}
              className={({ isActive }) =>
                `text-base font-medium transition-colors hover:text-primary py-2 ${
                  isActive ? "text-primary font-bold" : "text-muted-foreground"
                }`
              }
            >
              {label}
            </NavLink>
          ))}
        </nav>
      )}
    </header>
  );
};

export default Header;
