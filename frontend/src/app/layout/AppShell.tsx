import { NavLink, Outlet } from "react-router-dom";
import {
  Activity,
  Bell,
  Gauge,
  LayoutDashboard,
  Settings2,
  ShieldAlert,
  Sparkles,
  Waves,
} from "lucide-react";
import { WaterBackground } from "../../components/background/WaterBackground";
import { cn } from "../../lib/utils";

const navItems = [
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/districts", label: "District Intelligence", icon: Waves },
  { to: "/alerts", label: "Alert Center", icon: ShieldAlert },
  { to: "/analytics", label: "Risk Analytics", icon: Gauge },
  { to: "/ai-engine", label: "AI Engine", icon: Sparkles },
  { to: "/monitoring", label: "Monitoring", icon: Activity },
  { to: "/admin", label: "Admin Control", icon: Settings2 },
];

export function AppShell() {
  return (
    <div className="relative min-h-screen overflow-hidden">
      <WaterBackground />

      <div className="relative z-10 grid min-h-screen grid-cols-1 xl:grid-cols-[280px_1fr]">
        <aside className="border-r border-white/8 bg-slate-950/45 p-5 backdrop-blur-xl">
          <div className="rounded-3xl border border-cyan-300/10 bg-white/5 p-5">
            <div className="tiny-label">Project</div>
            <div className="mt-2 text-xl font-bold text-white">AI Early Warning</div>
            <p className="mt-2 text-sm leading-6 text-cyan-50/65">
              District-level public-health and water-borne risk intelligence command center.
            </p>
          </div>

          <nav className="mt-6 space-y-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    cn(
                      "flex items-center gap-3 rounded-2xl border px-4 py-3 text-sm transition-all",
                      isActive
                        ? "border-cyan-300/15 bg-cyan-400/10 text-white"
                        : "border-transparent bg-transparent text-slate-300 hover:border-white/8 hover:bg-white/5",
                    )
                  }
                >
                  <Icon className="h-4 w-4" />
                  {item.label}
                </NavLink>
              );
            })}
          </nav>
        </aside>

        <div className="flex min-h-screen flex-col">
          <header className="sticky top-0 z-20 border-b border-white/8 bg-slate-950/45 px-6 py-4 backdrop-blur-xl">
            <div className="flex items-center justify-between gap-4">
              <div>
                <div className="tiny-label">Water + Public Health Intelligence</div>
                <div className="mt-1 text-lg font-semibold text-white">District Risk Command Center</div>
              </div>
              <div className="flex items-center gap-3">
                <div className="hidden rounded-2xl border border-cyan-300/12 bg-white/5 px-4 py-2 text-sm text-cyan-50/70 md:block">
                  Mode: Water-Oriented Monitoring UI
                </div>
                <button className="rounded-2xl border border-white/10 bg-white/5 p-3 text-slate-300">
                  <Bell className="h-4 w-4" />
                </button>
              </div>
            </div>
          </header>

          <main className="flex-1 p-6 xl:p-8">
            <Outlet />
          </main>
        </div>
      </div>
    </div>
  );
}
