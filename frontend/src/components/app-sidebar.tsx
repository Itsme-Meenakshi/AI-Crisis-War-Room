import { Link, useRouterState } from "@tanstack/react-router";
import { Activity, Clock, Plus, Settings, Shield } from "lucide-react";
import { useSidebar } from "@/components/ui/sidebar";
import { cn } from "@/lib/utils";

const nav = [
  { to: "/dashboard", label: "Dashboard", icon: Activity },
  { to: "/new", label: "Declare", icon: Plus },
  { to: "/history", label: "History", icon: Clock },
  { to: "/settings", label: "Settings", icon: Settings },
] as const;

export function AppSidebar() {
  const { open } = useSidebar();
  const path = useRouterState({ select: (state) => state.location.pathname });

  return (
    <aside
      className={cn(
        "hidden shrink-0 border-r border-sidebar-border bg-sidebar text-sidebar-foreground transition-[width] duration-200 md:block",
        open ? "w-64" : "w-16",
      )}
    >
      <div className="flex h-14 items-center gap-3 border-b border-sidebar-border px-4">
        <div className="grid h-8 w-8 shrink-0 place-items-center rounded-md border border-sidebar-border bg-sidebar-accent">
          <Shield className="h-4 w-4 text-accent" />
        </div>
        {open && (
          <div className="min-w-0">
            <div className="text-[13px] font-semibold tracking-tight">AI Crisis War Room</div>
            <div className="text-[10px] uppercase tracking-[0.18em] text-muted-foreground">Crisis Management OS</div>
          </div>
        )}
      </div>

      <nav className="space-y-1 p-3">
        {nav.map((item) => {
          const Icon = item.icon;
          const active = path === item.to;
          return (
            <Link
              key={item.to}
              to={item.to}
              className={cn(
                "flex h-10 items-center gap-3 rounded-md px-3 text-sm transition hover:bg-sidebar-accent hover:text-sidebar-accent-foreground",
                active && "bg-sidebar-accent text-sidebar-accent-foreground",
                !open && "justify-center px-0",
              )}
            >
              <Icon className="h-4 w-4 shrink-0" />
              {open && <span>{item.label}</span>}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
