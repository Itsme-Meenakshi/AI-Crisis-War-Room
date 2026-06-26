import { createFileRoute, Link, useParams } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import {
  ArrowLeft, Briefcase, Megaphone, Scale, Wrench, FileText, Image as ImageIcon,
} from "lucide-react";
import { getCrisis, type CrisisAnalysis, type Perspective } from "@/lib/crisis-data";
import { SeverityRing } from "@/components/severity-ring";

export const Route = createFileRoute("/_shell/analysis/$id")({
  component: AnalysisPage,
});

const PERSPECTIVE_META: Record<Perspective, { icon: typeof Briefcase; color: string }> = {
  Business: { icon: Briefcase, color: "var(--accent)" },
  PR: { icon: Megaphone, color: "var(--warning)" },
  Legal: { icon: Scale, color: "var(--destructive)" },
  Operations: { icon: Wrench, color: "var(--success)" },
};

function AnalysisPage() {
  const { id } = useParams({ from: "/_shell/analysis/$id" });
  const [crisis, setCrisis] = useState<CrisisAnalysis | null>(null);
  const [tab, setTab] = useState<Perspective>("Business");

  useEffect(() => {
    getCrisis(id).then((c) => setCrisis(c ?? null));
  }, [id]);

  if (!crisis) {
    return (
      <div className="mx-auto max-w-3xl p-8 text-center">
        <p className="text-sm text-muted-foreground">Crisis not found.</p>
        <Link to="/dashboard" className="mt-4 inline-flex text-sm text-accent hover:underline">
          ← Back to dashboard
        </Link>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl space-y-6 p-6 lg:p-8">
      <div>
        <Link to="/dashboard" className="inline-flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground">
          <ArrowLeft className="h-3 w-3" /> Dashboard
        </Link>
        <div className="mt-3 flex flex-wrap items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-[10px] uppercase tracking-[0.2em]">
              <span className="text-accent">{crisis.category}</span>
              <span className="text-muted-foreground">·</span>
              <span className="text-muted-foreground">{new Date(crisis.createdAt).toLocaleString()}</span>
            </div>
            <h1 className="mt-2 text-3xl font-semibold tracking-tight">{crisis.title}</h1>
            <p className="mt-2 max-w-2xl text-sm text-muted-foreground">{crisis.description}</p>
          </div>
          <div className="flex items-center gap-2">
            <button className="rounded-md border border-border px-3 py-2 text-xs hover:bg-secondary">Export brief</button>
            <button className="rounded-md bg-accent px-3 py-2 text-xs font-medium text-accent-foreground hover:bg-accent/90">
              Share war room
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[320px_1fr]">
        <div className="panel grid place-items-center p-6">
          <SeverityRing value={crisis.severity} />
          <div className="mt-6 grid w-full grid-cols-3 gap-2 text-center">
            <Stat label="Stakeholders" value={crisis.stakeholders.length} />
            <Stat label="Risks" value={crisis.risks.length} />
            <Stat label="Actions" value={crisis.timeline.length} />
          </div>
        </div>

        <div className="panel p-6">
          <div className="mb-4 flex items-baseline justify-between">
            <h2 className="text-sm font-semibold">Stakeholder impact</h2>
            <span className="text-[10px] uppercase tracking-wider text-muted-foreground">Estimated</span>
          </div>
          <div className="space-y-3.5">
            {crisis.stakeholders.map((s) => {
              const color =
                s.sentiment === "negative" ? "var(--destructive)"
                : s.sentiment === "neutral" ? "var(--warning)" : "var(--success)";
              return (
                <div key={s.name}>
                  <div className="mb-1.5 flex items-center justify-between text-xs">
                    <div className="flex items-center gap-2">
                      <span className="font-medium">{s.name}</span>
                      <span
                        className="rounded-full px-1.5 py-0.5 text-[9px] uppercase tracking-wider"
                        style={{ background: `color-mix(in oklab, ${color} 15%, transparent)`, color }}
                      >{s.sentiment}</span>
                    </div>
                    <span className="tabular-nums text-muted-foreground">{s.impact}</span>
                  </div>
                  <div className="h-1.5 overflow-hidden rounded-full bg-secondary">
                    <div className="h-full rounded-full" style={{ width: `${s.impact}%`, background: color, transition: "width 700ms ease" }} />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="panel p-6">
          <h2 className="text-sm font-semibold">Risk matrix</h2>
          <p className="text-xs text-muted-foreground">Likelihood vs. impact, by category</p>
          <RiskScatter risks={crisis.risks} />
        </div>

        <div className="panel p-6">
          <h2 className="text-sm font-semibold">Multi-perspective analysis</h2>
          <p className="text-xs text-muted-foreground">Switch lenses to compare recommendations</p>
          <div className="mt-4 flex gap-1 rounded-md border border-border bg-secondary/40 p-1">
            {(Object.keys(PERSPECTIVE_META) as Perspective[]).map((p) => {
              const Icon = PERSPECTIVE_META[p].icon;
              return (
                <button
                  key={p}
                  onClick={() => setTab(p)}
                  className={`flex flex-1 items-center justify-center gap-1.5 rounded px-2 py-1.5 text-xs font-medium transition ${
                    tab === p ? "bg-background text-foreground shadow-sm" : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  <Icon className="h-3.5 w-3.5" /> {p}
                </button>
              );
            })}
          </div>

          {(() => {
            const insight = crisis.perspectives.find((p) => p.perspective === tab);
            if (!insight) return <p className="mt-4 text-xs text-muted-foreground">No analysis available.</p>;
            return (
              <div className="mt-4 space-y-3">
                <p className="text-sm leading-relaxed text-muted-foreground">{insight.summary}</p>
                <div className="space-y-1.5">
                  {insight.recommendations.map((r, i) => (
                    <div key={i} className="flex items-start gap-2 rounded-md border border-border bg-card/40 p-2.5">
                      <div className="mt-0.5 grid h-4 w-4 shrink-0 place-items-center rounded-full bg-accent/15 text-[9px] font-bold text-accent">
                        {i + 1}
                      </div>
                      <span className="text-xs leading-relaxed">{r}</span>
                    </div>
                  ))}
                </div>
              </div>
            );
          })()}
        </div>
      </div>

      {crisis.timeline.length > 0 && (
        <div className="panel p-6">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h2 className="text-sm font-semibold">Response timeline</h2>
              <p className="text-xs text-muted-foreground">Prioritized 72-hour action plan</p>
            </div>
          </div>
          <div className="relative">
            <div className="absolute left-[68px] top-0 h-full w-px bg-border" />
            <div className="space-y-3">
              {crisis.timeline.map((a, i) => {
                const pColor = a.priority === "P0" ? "var(--destructive)" : a.priority === "P1" ? "var(--accent)" : "var(--muted-foreground)";
                const meta = PERSPECTIVE_META[a.owner];
                const Icon = meta.icon;
                return (
                  <div key={i} className="flex items-start gap-4">
                    <div className="w-14 shrink-0 pt-2 text-right text-[11px] font-medium tabular-nums text-muted-foreground">
                      {a.time}
                    </div>
                    <div className="relative grid h-9 w-9 shrink-0 place-items-center rounded-full border border-border bg-background">
                      <Icon className="h-4 w-4" style={{ color: meta.color }} />
                    </div>
                    <div className="flex-1 rounded-md border border-border bg-card/40 p-3">
                      <div className="flex items-center justify-between gap-3">
                        <div className="text-sm font-medium">{a.title}</div>
                        <span
                          className="rounded px-1.5 py-0.5 text-[9px] font-bold tracking-wider"
                          style={{ background: `color-mix(in oklab, ${pColor} 15%, transparent)`, color: pColor }}
                        >{a.priority}</span>
                      </div>
                      <div className="mt-1 text-[11px] text-muted-foreground">Owner: {a.owner}</div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {crisis.attachments.length > 0 && (
        <div className="panel p-6">
          <h2 className="mb-3 text-sm font-semibold">Evidence</h2>
          <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
            {crisis.attachments.map((a, i) => {
              const isImg = /\.(png|jpe?g|gif|webp)$/i.test(a.name);
              return (
                <div key={i} className="flex items-center gap-2 rounded-md border border-border bg-card/40 p-2">
                  <div className="grid h-8 w-8 place-items-center rounded bg-secondary">
                    {isImg ? <ImageIcon className="h-4 w-4 text-accent" /> : <FileText className="h-4 w-4 text-accent" />}
                  </div>
                  <div className="min-w-0">
                    <div className="truncate text-xs">{a.name}</div>
                    <div className="text-[10px] text-muted-foreground">{(a.size / 1024).toFixed(1)} KB</div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}

function Stat({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-md border border-border bg-card/40 p-2">
      <div className="text-lg font-semibold tabular-nums">{value}</div>
      <div className="text-[10px] uppercase tracking-wider text-muted-foreground">{label}</div>
    </div>
  );
}

function RiskScatter({ risks }: { risks: { category: string; likelihood: number; impact: number }[] }) {
  const w = 100, h = 100;
  return (
    <div className="mt-4">
      <div className="relative">
        <svg viewBox={`0 0 ${w} ${h}`} className="aspect-square w-full">
          <rect x={50} y={0} width={50} height={50} fill="var(--destructive)" opacity="0.08" />
          <rect x={0} y={0} width={50} height={50} fill="var(--accent)" opacity="0.05" />
          <rect x={50} y={50} width={50} height={50} fill="var(--accent)" opacity="0.05" />
          {[25, 50, 75].map((n) => (
            <g key={n}>
              <line x1={n} y1={0} x2={n} y2={h} stroke="var(--border)" strokeWidth="0.3" />
              <line x1={0} y1={n} x2={w} y2={n} stroke="var(--border)" strokeWidth="0.3" />
            </g>
          ))}
          {risks.map((r, i) => {
            const score = (r.likelihood + r.impact) / 2;
            const color = score >= 70 ? "var(--destructive)" : score >= 50 ? "var(--accent)" : "var(--success)";
            return (
              <g key={i}>
                <circle cx={r.likelihood} cy={100 - r.impact} r={3} fill={color} opacity="0.9" />
                <circle cx={r.likelihood} cy={100 - r.impact} r={6} fill={color} opacity="0.2" />
              </g>
            );
          })}
        </svg>
        <div className="pointer-events-none absolute bottom-1 left-1 text-[9px] uppercase tracking-wider text-muted-foreground">Likelihood →</div>
        <div className="pointer-events-none absolute left-1 top-1 -rotate-90 origin-top-left translate-y-12 text-[9px] uppercase tracking-wider text-muted-foreground">Impact →</div>
      </div>
      <div className="mt-3 flex flex-wrap gap-2">
        {risks.map((r) => (
          <div key={r.category} className="flex items-center gap-1.5 rounded border border-border bg-card/40 px-2 py-1 text-[10px]">
            <span className="font-medium">{r.category}</span>
            <span className="text-muted-foreground tabular-nums">{Math.round((r.likelihood + r.impact) / 2)}</span>
          </div>
        ))}
      </div>
    </div>
  );
}