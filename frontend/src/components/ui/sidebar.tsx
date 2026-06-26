import * as React from "react";
import { PanelLeft } from "lucide-react";
import { cn } from "@/lib/utils";

type SidebarContextValue = {
  open: boolean;
  setOpen: React.Dispatch<React.SetStateAction<boolean>>;
};

const SidebarContext = React.createContext<SidebarContextValue | null>(null);

export function SidebarProvider({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = React.useState(true);
  return (
    <SidebarContext.Provider value={{ open, setOpen }}>
      {children}
    </SidebarContext.Provider>
  );
}

export function useSidebar() {
  const context = React.useContext(SidebarContext);
  if (!context) throw new Error("useSidebar must be used within SidebarProvider");
  return context;
}

export function SidebarTrigger({ className }: { className?: string }) {
  const { setOpen } = useSidebar();
  return (
    <button
      type="button"
      aria-label="Toggle sidebar"
      onClick={() => setOpen((value) => !value)}
      className={cn("grid place-items-center rounded-md border border-border hover:bg-secondary", className)}
    >
      <PanelLeft className="h-4 w-4" />
    </button>
  );
}
