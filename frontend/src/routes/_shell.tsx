import { createFileRoute, Outlet, Link, useRouterState } from "@tanstack/react-router";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { Bell, Search } from "lucide-react";

export const Route = createFileRoute("/_shell")({
  component: ShellLayout,
});

function ShellLayout() {
  const path = useRouterState({ select: (r) => r.location.pathname });
  const crumbs = path.split("/").filter(Boolean);

  return (
    <SidebarProvider>
      <div className="flex min-h-screen w-full bg-background">
        <AppSidebar />
        <div className="flex min-w-0 flex-1 flex-col">
          <header className="sticky top-0 z-20 flex h-14 items-center gap-3 border-b border-border bg-background/80 px-4 backdrop-blur">
            <SidebarTrigger className="h-8 w-8" />
            <div className="hidden items-center gap-1.5 text-xs text-muted-foreground sm:flex">
              <Link to="/dashboard" className="hover:text-foreground">Workspace</Link>
              {crumbs.slice(1).map((c, i) => (
                <span key={i} className="flex items-center gap-1.5">
                  <span className="text-muted-foreground/50">/</span>
                  <span className="capitalize text-foreground">{c}</span>
                </span>
              ))}
            </div>

            <div className="ml-auto flex items-center gap-2">
              <div className="hidden items-center gap-2 rounded-md border border-border bg-secondary/40 px-2.5 py-1.5 text-xs text-muted-foreground md:flex">
                <Search className="h-3.5 w-3.5" />
                <span>Search incidents</span>
                <kbd className="ml-2 rounded border border-border bg-background px-1 font-mono text-[10px]">⌘K</kbd>
              </div>
              <button className="relative grid h-8 w-8 place-items-center rounded-md border border-border hover:bg-secondary">
                <Bell className="h-4 w-4" />
                <span className="absolute right-1.5 top-1.5 h-1.5 w-1.5 rounded-full bg-accent" />
              </button>
            </div>
          </header>

          <main className="flex-1 overflow-x-hidden">
            <Outlet />
          </main>
        </div>
      </div>
    </SidebarProvider>
  );
}
