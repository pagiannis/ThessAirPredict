import { useState } from "react";
import { Menu, Moon, Sun, X } from "lucide-react";
import { GoSun } from "react-icons/go";
import { Link, NavLink } from "react-router-dom";
import logo from "@/assets/thita_logo.png";
import { useTheme } from "@/contexts/ThemeContext";
import { cn } from "@/lib/utils";

const Header = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const { theme, toggleTheme } = useTheme();

  const navItems = [
    { label: "Dashboard", path: "/" },
    { label: "Forecast", path: "/forecast" },
  ];

  return (
    <header className="mx-2 sm:mx-10 lg:mx-40 fixed top-0 left-0 right-0 z-50 bg-card/60 backdrop-blur-xl border border-border/50 rounded-xl border-t-0 rounded-t-none border-x-0">
      <div className="container flex items-center h-16">
        <div className="flex-1 flex items-center gap-14">
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

        <button
          onClick={toggleTheme}
          aria-label="Toggle theme"
          className="hidden md:flex items-center gap-2.5 rounded-full bg-muted/50 p-1.5 transition-colors hover:bg-muted"
        >
          <span
            className={cn(
              "rounded-full p-1.5 transition-colors text-muted-foreground",
              theme === "light"
                ? "bg-foreground/10 text-foreground"
                : "border border-foreground/10",
            )}
          >
            <GoSun />
          </span>
          <span
            className={cn(
              "rounded-full p-1.5 transition-colors text-muted-foreground",
              theme === "dark"
                ? "bg-foreground/10 text-foreground"
                : "border border-foreground/10",
            )}
          >
            <Moon className="h-4 w-4" />
          </span>
        </button>

        <div className="flex-1 flex items-center justify-end gap-2">
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
          <button
            onClick={toggleTheme}
            className="flex items-center gap-2 py-2 text-base font-medium text-muted-foreground hover:text-foreground transition-colors"
          >
            {theme === "dark" ? (
              <Sun className="h-4 w-4" />
            ) : (
              <Moon className="h-4 w-4" />
            )}
            {theme === "dark" ? "Light mode" : "Dark mode"}
          </button>
        </nav>
      )}
    </header>
  );
};

export default Header;
