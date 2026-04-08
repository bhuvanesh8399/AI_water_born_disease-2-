import type { DistrictDetail } from "../../types/api";
import { GlassPanel } from "../ui/GlassPanel";
import { ConsensusMeter } from "../ui/ConsensusMeter";
import { DataReliabilityCard } from "./DataReliabilityCard";

export function QuickInsightRail({ detail }: { detail?: DistrictDetail | null }) {
  return (
    <div className="space-y-6">
      <GlassPanel title="Decision Summary" subtitle="Why the system is leaning this way">
        <ul className="space-y-3 text-sm text-cyan-50/72">
          {(detail?.explainabilityReasons ?? ["Explanation will appear here once district detail loads."]).map((reason) => (
            <li key={reason} className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3">{reason}</li>
          ))}
        </ul>
      </GlassPanel>
      <GlassPanel title="Model Agreement" subtitle="Compare all core intelligence layers">
        <ConsensusMeter scores={detail?.modelScores} />
      </GlassPanel>
      <DataReliabilityCard detail={detail} />
    </div>
  );
}
