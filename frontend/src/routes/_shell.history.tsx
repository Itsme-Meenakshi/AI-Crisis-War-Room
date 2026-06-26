import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect, useMemo, useState } from "react";
import { Search } from "lucide-react";
import { loadCrises, type CrisisAnalysis } from "@/lib/crisis-data";

export const Route = createFileRoute("/_shell/history")({
  head: () => ({
    meta: [
      { title: "Crisis history — AI Crisis War Room" },
      { name: "description", content: "Browse and audit all past crisis events and resolutions." },
    ],
  }),
  component: HistoryPage,
});

function HistoryPage() {
  const [list, setList] = useState<CrisisAnalysis[]>([]);
  const [q, setQ] = useState("");
  const [filter, setFilter] = useState<"all" | CrisisAnalysis["status"]>("all");

  useEffect(() => {
    loadCrises().then(setList);
  }, []);

  const filtered = useMemo(() => {
    return list.filter((c) => {
      if (filter !== "all" && c.status !== filter) return false;
      if (q && !`${c.title} ${c.category}`.toLowerCase().includes(q.toLowerCase())) return false;
      return true;
    });
  }, [list, q, filter]);

  return (
    <div className="mx-auto max-w-7xl space-y-6 p-6 lg:p-8">
      <div>
        <div className="text-[10px] uppercase tracking-[0.2em] text-muted-foreground">Audit log</div>
        <h1 className="mt-1.5 text-3xl font-semibold tracking-tight">Crisis history</h1>
        <p className="mt-1.5 text-sm text-muted-foreground">
          A complete, time-stamped record of every declared incident.
        </p>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <div className="relative flex-1 min-w-[240px]">
          <Search className="absolute left-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-muted-foreground" />
          <input
            value={q} onChange={(e) => setQ(e.target.value)}
            placeholder="Search by title or category…"
            className="h-10 w-full rounded-md border border-border bg-secondary/40 pl-9 pr-3 text-sm outline-none placeholder:text-muted-foreground focus:border-accent"
          />
        </div>
        <div className="flex gap-1 rounded-md border border-border bg-secondary/40 p-1">
          {(["all", "active", "monitoring", "resolved"] as const).map((s) => (
            <button
              key={s} onClick={() => setFilter(s)}
              className={`rounded px-3 py-1.5 text-xs font-medium capitalize transition ${
                filter === s ? "bg-background text-foreground" : "text-muted-foreground hover:text-foreground"
              }`}
            >{s}</button>
          ))}
        </div>
      </div>

      <div className="panel overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border bg-secondary/30 text-left text-[10px] uppercase tracking-wider text-muted-foreground">
              <th className="px-4 py-3 font-medium">Severity</th>
              <th className="px-4 py-3 font-medium">Incident</th>
              <th className="px-4 py-3 font-medium">Category</th>
              <th className="px-4 py-3 font-medium">Status</th>
              <th className="px-4 py-3 font-medium">Declared</th>
              <th className="px-4 py-3" />
            </tr>
          </thead>
          <tbody>
            {filtered.map((c) => {
              const color = c.severity >= 75 ? "var(--destructive)" : c.severity >= 50 ? "var(--accent)" : "var(--success)";
              return (
                <tr key={c.id} className="border-b border-border last:border-0 hover:bg-secondary/20">
                  <td className="px-4 py-3">
                    <span className="inline-flex h-7 w-10 items-center justify-center rounded text-xs font-semibold tabular-nums"
                      style={{ background: `color-mix(in oklab, ${color} 15%, transparent)`, color }}>
                      {c.severity}
                    </span>
                  </td>
                  <td className="px-4 py-3 font-medium">{c.title}</td>
                  <td className="px-4 py-3 text-muted-foreground">{c.category}</td>
                  <td className="px-4 py-3">
                    <span className="text-xs capitalize text-muted-foreground">{c.status}</span>
                  </td>
                  <td className="px-4 py-3 text-xs text-muted-foreground tabular-nums">
                    {new Date(c.createdAt).toLocaleString()}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <Link to="/analysis/$id" params={{ id: c.id }} className="text-xs text-accent hover:underline">Open →</Link>
                  </td>
                </tr>
              );
            })}
            {filtered.length === 0 && (
              <tr><td colSpan={6} className="px-4 py-12 text-center text-sm text-muted-foreground">No matching incidents.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
