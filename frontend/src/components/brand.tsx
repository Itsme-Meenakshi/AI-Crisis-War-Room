import { Shield } from "lucide-react";

export function Brand({ collapsed = false }: { collapsed?: boolean }) {
  return (
    <div className="flex items-center gap-2.5">
      <div className="relative grid h-8 w-8 place-items-center rounded-md border border-border bg-secondary">
        <Shield className="h-4 w-4 text-accent" />
        <span className="absolute -right-0.5 -top-0.5 h-1.5 w-1.5 rounded-full bg-accent animate-pulse" />
      </div>
      {!collapsed && (
        <div className="leading-tight">
          <div className="text-[13px] font-semibold tracking-tight">War Room</div>
          <div className="text-[10px] uppercase tracking-[0.18em] text-muted-foreground">AI Crisis OS</div>
        </div>
      )}
    </div>
  );
}
