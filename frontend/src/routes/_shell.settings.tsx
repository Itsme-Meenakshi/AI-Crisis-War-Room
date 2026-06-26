import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/_shell/settings")({
  component: SettingsPage,
});

function SettingsPage() {
  return (
    <div className="mx-auto max-w-5xl space-y-6 p-6 lg:p-8">
      <div>
        <div className="text-[10px] uppercase tracking-[0.2em] text-muted-foreground">Workspace</div>
        <h1 className="mt-1.5 text-3xl font-semibold tracking-tight">Settings</h1>
        <p className="mt-1.5 text-sm text-muted-foreground">
          Configure response defaults and governance controls for the war room.
        </p>
      </div>

      <div className="panel p-6">
        <h2 className="text-sm font-semibold">Response profile</h2>
        <div className="mt-4 grid gap-4 sm:grid-cols-2">
          <Setting label="Escalation policy" value="Executive review for severity 75+" />
          <Setting label="Default window" value="72-hour action plan" />
          <Setting label="Evidence handling" value="Local browser storage" />
          <Setting label="Audit mode" value="Enabled" />
        </div>
      </div>
    </div>
  );
}

function Setting({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-border bg-card/40 p-4">
      <div className="text-[10px] uppercase tracking-wider text-muted-foreground">{label}</div>
      <div className="mt-1 text-sm font-medium">{value}</div>
    </div>
  );
}
