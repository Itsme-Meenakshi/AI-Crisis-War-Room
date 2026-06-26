import { Fragment } from "react";
import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import {
  Activity, AlertTriangle, Clock, ShieldCheck, ArrowUpRight, Plus,
} from "lucide-react";
import { loadCrises, type CrisisAnalysis } from "@/lib/crisis-data";

export const Route = createFileRoute("/_shell/dashboard")({
  component: Dashboard,
});

function Dashboard() {
  const [crises, setCrises] = useState<CrisisAnalysis[]>([]);
  useEffect(() => setCrises(loadCrises()), []);

  const active = crises.filter((c) => c.status === "active");
  const avgSeverity = Math.round(
    crises.reduce((a, c) => a + c.severity, 0) / Math.max(crises.length, 1)
  );

  const kpis = [
    { label: "Active incidents", value: active.length, icon: AlertTriangle, accent: true },
    { label: "Avg. severity", value: avgSeverity, icon: Activity, suffix: "/100" },
    { label: "Avg. response", value: "42m", icon: Clock },
    { label: "Resolved (30d)", value: crises.filter(c => c.status === "resolved").length, icon: ShieldCheck },
  ];

  return (
    <div className="mx-auto max-w-7xl space-y-8 p-6 lg:p-8">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <div className="text-[10px] uppercase tracking-[0.2em] text-muted-foreground">Operations</div>
          <h1 className="mt-1.5 text-3xl font-semibold tracking-tight">War Room Overview</h1>
          <p className="mt-1.5 text-sm text-muted-foreground">
            Real-time situational awareness across all active crisis events.
          </p>
        </div>
        <Link
          to="/new"
          className="inline-flex items-center gap-2 rounded-md bg-accent px-4 py-2 text-sm font-medium text-accent-foreground hover:bg-accent/90"
        >
          <Plus className="h-4 w-4" /> Declare crisis
        </Link>
      </div>

      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        {kpis.map((k) => (
          <div key={k.label} className="panel relative overflow-hidden p-5">
            {k.accent && <span className="absolute right-4 top-4 h-1.5 w-1.5 animate-pulse rounded-full bg-accent" />}
            <k.icon className="h-4 w-4 text-muted-foreground" />
            <div className="mt-3 text-[11px] uppercase tracking-wider text-muted-foreground">{k.label}</div>
            <div className="mt-1 flex items-baseline gap-1">
              <span className="text-3xl font-semibold tracking-tight tabular-nums">{k.value}</span>
              {k.suffix && <span className="text-xs text-muted-foreground">{k.suffix}</span>}
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="panel p-5 lg:col-span-2">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h2 className="text-sm font-semibold">Active crises</h2>
              <p className="text-xs text-muted-foreground">Sorted by severity</p>
            </div>
            <Link to="/history" className="text-xs text-muted-foreground hover:text-foreground">View all →</Link>
          </div>

          <div className="space-y-2">
            {[...crises].sort((a, b) => b.severity - a.severity).slice(0, 5).map((c) => (
              <Link
                key={c.id}
                to="/analysis/$id"
                params={{ id: c.id }}
                className="group flex items-center gap-4 rounded-md border border-border bg-card/40 p-3 transition hover:bg-card"
              >
                <SeverityBadge value={c.severity} />
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <div className="truncate text-sm font-medium">{c.title}</div>
                    <StatusPill status={c.status} />
                  </div>
                  <div className="mt-0.5 text-xs text-muted-foreground">
                    {c.category} · {new Date(c.createdAt).toLocaleString()}
                  </div>
                </div>
                <ArrowUpRight className="h-4 w-4 text-muted-foreground transition group-hover:text-foreground" />
              </Link>
            ))}
            {crises.length === 0 && (
              <div className="rounded-md border border-dashed border-border p-8 text-center text-sm text-muted-foreground">
                No crises yet. Declare one to begin analysis.
              </div>
            )}
          </div>
        </div>

        <div className="panel p-5">
          <h2 className="text-sm font-semibold">Risk heatmap</h2>
          <p className="text-xs text-muted-foreground">Likelihood × impact, org-wide</p>
          <Heatmap crises={crises} />
          <div className="mt-3 flex items-center justify-between text-[10px] text-muted-foreground">
            <span>Low</span>
            <div className="flex gap-1">
              {[0.2, 0.4, 0.6, 0.8, 1].map((o) => (
                <div key={o} className="h-2 w-4 rounded-sm" style={{ background: `color-mix(in oklab, var(--destructive) ${o * 100}%, transparent)` }} />
              ))}
            </div>
            <span>Critical</span>
          </div>
        </div>
      </div>

      <div className="panel p-5">
        <h2 className="text-sm font-semibold">Response activity</h2>
        <p className="text-xs text-muted-foreground">Last 14 days</p>
        <Sparkline />
      </div>
    </div>
  );
}

function SeverityBadge({ value }: { value: number }) {
  const color = value >= 75 ? "var(--destructive)" : value >= 50 ? "var(--accent)" : "var(--success)";
  return (
    <div className="grid h-10 w-10 shrink-0 place-items-center rounded-md border border-border" style={{ background: `color-mix(in oklab, ${color} 12%, transparent)` }}>
      <span className="text-sm font-semibold tabular-nums" style={{ color }}>{value}</span>
    </div>
  );
}

function StatusPill({ status }: { status: CrisisAnalysis["status"] }) {
  const map = {
    active: { label: "Active", color: "var(--destructive)" },
    monitoring: { label: "Monitoring", color: "var(--accent)" },
    resolved: { label: "Resolved", color: "var(--success)" },
  } as const;
  const s = map[status];
  return (
    <span
      className="inline-flex items-center gap-1 rounded-full border border-border px-1.5 py-0.5 text-[9px] font-medium uppercase tracking-wider"
      style={{ color: s.color }}
    >
      <span className="h-1 w-1 rounded-full" style={{ background: s.color }} /> {s.label}
    </span>
  );
}

function Heatmap({ crises }: { crises: CrisisAnalysis[] }) {
  const cats = ["Financial", "Reputation", "Legal", "Operational", "Compliance"];
  const buckets = ["Low", "Med", "High", "Crit"];
  const grid = cats.map((cat) =>
    buckets.map((_, bi) => {
      const items = crises.flatMap((c) => c.risks.filter((r) => r.category === cat));
      const inBucket = items.filter((r) => {
        const s = (r.likelihood + r.impact) / 2;
        return s >= bi * 25 && s < (bi + 1) * 25;
      }).length;
      return inBucket;
    })
  );
  const max = Math.max(1, ...grid.flat());

  return (
    <div className="mt-4">
      <div className="grid grid-cols-[80px_repeat(4,1fr)] gap-1 text-[10px] text-muted-foreground">
        <div />
        {buckets.map((b) => <div key={b} className="text-center">{b}</div>)}
        {cats.map((cat, i) => (
          <Fragment key={cat}>
            <div className="flex items-center text-[10px]">{cat}</div>
            {grid[i].map((v, j) => (
              <div
                key={j}
                className="aspect-square rounded-sm border border-border"
                style={{ background: `color-mix(in oklab, var(--destructive) ${(v / max) * 80}%, transparent)` }}
                title={`${cat} / ${buckets[j]}: ${v}`}
              />
            ))}
          </Fragment>
        ))}
      </div>
    </div>
  );
}

function Sparkline() {
  const pts = [3, 5, 4, 7, 6, 9, 8, 12, 9, 11, 14, 10, 13, 16];
  const max = Math.max(...pts);
  const w = 100, h = 40;
  const path = pts
    .map((p, i) => `${(i / (pts.length - 1)) * w},${h - (p / max) * h}`)
    .join(" L ");

  return (
    <div className="mt-4">
      <svg viewBox={`0 0 ${w} ${h}`} className="h-32 w-full" preserveAspectRatio="none">
        <defs>
          <linearGradient id="g" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%" stopColor="var(--accent)" stopOpacity="0.4" />
            <stop offset="100%" stopColor="var(--accent)" stopOpacity="0" />
          </linearGradient>
        </defs>
        <path d={`M 0,${h} L ${path} L ${w},${h} Z`} fill="url(#g)" />
        <path d={`M ${path}`} fill="none" stroke="var(--accent)" strokeWidth="0.8" />
      </svg>
      <div className="mt-2 flex justify-between text-[10px] text-muted-foreground">
        <span>2 weeks ago</span><span>Today</span>
      </div>
    </div>
  );
}