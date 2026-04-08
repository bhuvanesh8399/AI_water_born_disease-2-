import type { District } from "../../types/api";
import { formatPercent } from "../../lib/utils";
import { GlassPanel } from "../ui/GlassPanel";
import { RiskBadge } from "../ui/RiskBadge";

export function DistrictCompareTable({ districts }: { districts: District[] }) {
  return (
    <GlassPanel title="District Comparison" subtitle="Quick side-by-side operational overview">
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead>
            <tr className="border-b border-white/10 text-cyan-100/55">
              <th className="pb-3 pr-4">District</th>
              <th className="pb-3 pr-4">Risk</th>
              <th className="pb-3 pr-4">Confidence</th>
              <th className="pb-3 pr-4">Primary Reason</th>
            </tr>
          </thead>
          <tbody>
            {districts.map((item) => (
              <tr key={item.districtId} className="border-b border-white/5 last:border-0">
                <td className="py-4 pr-4 font-medium text-white">{item.districtName}</td>
                <td className="py-4 pr-4"><RiskBadge level={item.riskLevel} /></td>
                <td className="py-4 pr-4 text-cyan-50/72">{formatPercent(item.confidence)}</td>
                <td className="py-4 pr-4 text-cyan-50/65">{item.primaryReason ?? "Signal pressure"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </GlassPanel>
  );
}
