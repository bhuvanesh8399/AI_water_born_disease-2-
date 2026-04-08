import { cn, titleCase } from "../../lib/utils";

export function HealthChip({ state = "unknown" }: { state?: string }) {
  const key = state.toLowerCase();
  const style =
    key === "healthy"
      ? "border-emerald-400/30 bg-emerald-500/12 text-emerald-200"
      : key === "degraded"
        ? "border-amber-400/30 bg-amber-500/12 text-amber-200"
        : "border-slate-400/30 bg-slate-500/12 text-slate-200";
  return <span className={cn("badge", style)}>{titleCase(key)}</span>;
}
