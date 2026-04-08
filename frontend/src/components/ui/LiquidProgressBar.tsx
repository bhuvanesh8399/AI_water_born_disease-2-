import { clamp, cn } from "../../lib/utils";

type Props = {
  value?: number | null;
  label?: string;
  className?: string;
};

export function LiquidProgressBar({ value = 0, label, className }: Props) {
  const pct = clamp(value ?? 0);
  return (
    <div className={cn("space-y-2", className)}>
      {label ? (
        <div className="flex items-center justify-between text-sm text-cyan-50/70">
          <span>{label}</span>
          <span>{pct}%</span>
        </div>
      ) : null}
      <div className="relative h-3 overflow-hidden rounded-full border border-cyan-300/10 bg-slate-900/70">
        <div
          className="absolute inset-y-0 left-0 rounded-full bg-[linear-gradient(90deg,rgba(34,211,238,0.85),rgba(59,130,246,0.85))] transition-all duration-500"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
