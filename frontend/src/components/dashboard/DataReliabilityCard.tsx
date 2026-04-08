import type { DistrictDetail } from "../../types/api";
import { GlassPanel } from "../ui/GlassPanel";
import { LiquidProgressBar } from "../ui/LiquidProgressBar";

export function DataReliabilityCard({ detail }: { detail?: DistrictDetail | null }) {
  return (
    <GlassPanel title="Data Reliability" subtitle="Trust visibility for the current district view">
      <div className="space-y-4">
        <LiquidProgressBar value={detail?.dataReliability?.completeness ?? 0} label="Completeness" />
        <LiquidProgressBar value={detail?.dataReliability?.freshness ?? 0} label="Freshness" />
      </div>
    </GlassPanel>
  );
}
