import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/_shell/settings")({
  component: SettingsPage,
});

function SettingsPage() {
  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6 lg:p-8">
      <div>
        <div className="text-[10px] uppercase tracking-[0.2em] text-muted-foreground">Workspace</div>
        <h1 className="mt-1.5 text-3xl font-semibold tracking-tight">Settings</h1>
        <p className="mt-1.5 text-sm text-muted-foreground">Configure response defaults and AI model preferences.</p>
      </div>

      {[
        { title: "AI Model", desc: "Configure Qwen3 8B model settings and Ollama connection." },
        { title: "RAG Knowledge Base", desc: "Manage ChromaDB documents, embeddings, and retrieval settings." },
        { title: "Agent Preferences", desc: "Customize Business, Legal, PR, and Operations agent behavior." },
        { title: "Severity Thresholds", desc: "Set escalation policies and severity scoring rules." },
        { title: "Notifications", desc: "Configure alerts for active and critical crisis events." },
      ].map((s) => (
        <div key={s.title} className="panel flex items-center justify-between p-5">
          <div>
            <div className="text-sm font-medium">{s.title}</div>
            <div className="text-xs text-muted-foreground">{s.desc}</div>
          </div>
          <button className="rounded-md border border-border px-3 py-1.5 text-xs hover:bg-secondary">Configure</button>
        </div>
      ))}
    </div>
  );
}