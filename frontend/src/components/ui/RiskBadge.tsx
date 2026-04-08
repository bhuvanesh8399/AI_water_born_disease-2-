import type { RiskLevel } from "../../types/api";
import { cn } from "../../lib/utils";

export function RiskBadge({ level = "low" }: { level?: RiskLevel | string }) {
  const key = String(level).toLowerCase();
  const style =
    key === "critical"
      ? "border-red-400/30 bg-red-500/12 text-red-200"
      : key === "high"
        ? "border-orange-400/30 bg-orange-500/12 text-orange-200"
        : key === "medium"
          ? "border-amber-400/30 bg-amber-500/12 text-amber-200"
          : "border-emerald-400/30 bg-emerald-500/12 text-emerald-200";
  return <span className={cn("badge", style)}>{key.toUpperCase()}</span>;
}
