import type { DistrictDetail } from "../../types/api";
import { GlassPanel } from "../ui/GlassPanel";
import { LiquidProgressBar } from "../ui/LiquidProgressBar";

export function SignalBreakdownPanel({ detail }: { detail?: DistrictDetail | null }) {
  const signals = detail?.signalBreakdown;
  return (
    <GlassPanel title="Signal Breakdown" subtitle="Environmental, infrastructure, and historical drivers">
      <div className="space-y-4">
        <LiquidProgressBar value={signals?.weather ?? 0} label="Weather Pressure" />
        <LiquidProgressBar value={signals?.waterQuality ?? 0} label="Water Quality Stress" />
        <LiquidProgressBar value={signals?.sanitation ?? 0} label="Sanitation Weakness" />
        <LiquidProgressBar value={signals?.vulnerability ?? 0} label="Vulnerability" />
        <LiquidProgressBar value={signals?.historicalAlerts ?? 0} label="Historical Alert Similarity" />
      </div>
    </GlassPanel>
  );
}
