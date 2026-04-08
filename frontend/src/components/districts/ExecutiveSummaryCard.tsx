import type { DistrictDetail } from "../../types/api";
import { formatPercent } from "../../lib/utils";
import { GlassPanel } from "../ui/GlassPanel";
import { RiskBadge } from "../ui/RiskBadge";

export function ExecutiveSummaryCard({ detail }: { detail?: DistrictDetail | null }) {
  return (
    <GlassPanel title="Executive Summary" subtitle="Auto-generated district intelligence summary" rightSlot={<RiskBadge level={detail?.riskLevel} />}>
      <p className="text-sm leading-7 text-cyan-50/72">
        {detail
          ? `${detail.districtName} is currently ${detail.riskLevel.toUpperCase()} risk with ${formatPercent(detail.confidence)} confidence. The strongest drivers are ${(detail.explainabilityReasons ?? []).slice(0, 2).join(" and ") || "multi-signal environmental and vulnerability pressure"}.`
          : "District summary will appear here."}
      </p>
    </GlassPanel>
  );
}
