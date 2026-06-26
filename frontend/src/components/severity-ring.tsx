export function SeverityRing({ value }: { value: number }) {
  const radius = 44;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (Math.min(100, Math.max(0, value)) / 100) * circumference;
  const color = value >= 75 ? "var(--destructive)" : value >= 50 ? "var(--accent)" : "var(--success)";

  return (
    <div className="relative grid h-44 w-44 place-items-center">
      <svg viewBox="0 0 112 112" className="h-full w-full -rotate-90">
        <circle
          cx="56"
          cy="56"
          r={radius}
          fill="none"
          stroke="var(--secondary)"
          strokeWidth="10"
        />
        <circle
          cx="56"
          cy="56"
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth="10"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
        />
      </svg>
      <div className="absolute text-center">
        <div className="text-4xl font-semibold tabular-nums" style={{ color }}>{value}</div>
        <div className="mt-1 text-[10px] uppercase tracking-[0.2em] text-muted-foreground">Severity</div>
      </div>
    </div>
  );
}
