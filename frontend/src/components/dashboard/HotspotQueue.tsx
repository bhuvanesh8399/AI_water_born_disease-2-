import { Link } from "react-router-dom";
import type { Hotspot } from "../../types/api";
import { formatPercent } from "../../lib/utils";
import { GlassPanel } from "../ui/GlassPanel";
import { RiskBadge } from "../ui/RiskBadge";

export function HotspotQueue({ hotspots, onQuickView }: { hotspots: Hotspot[]; onQuickView?: (districtId: string) => void }) {
  return (
    <GlassPanel title="Priority District Queue" subtitle="Ranked by risk severity and operational importance">
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead>
            <tr className="border-b border-white/10 text-cyan-100/55">
              <th className="pb-3 pr-4">Rank</th>
              <th className="pb-3 pr-4">District</th>
              <th className="pb-3 pr-4">Risk</th>
              <th className="pb-3 pr-4">Confidence</th>
              <th className="pb-3 pr-4">Main Trigger</th>
              <th className="pb-3 pr-4">Action</th>
            </tr>
          </thead>
          <tbody>
            {hotspots.map((item, index) => (
              <tr key={item.districtId} className="border-b border-white/5 last:border-0">
                <td className="py-4 pr-4 text-cyan-50/70">#{index + 1}</td>
                <td className="py-4 pr-4 font-medium text-white">{item.districtName}</td>
                <td className="py-4 pr-4"><RiskBadge level={item.riskLevel} /></td>
                <td className="py-4 pr-4 text-cyan-50/75">{formatPercent(item.confidence)}</td>
                <td className="py-4 pr-4 text-cyan-50/65">{item.primaryReason ?? "Signal pressure"}</td>
                <td className="py-4 pr-4">
                  <div className="flex gap-2">
                    <button onClick={() => onQuickView?.(item.districtId)} className="rounded-xl border border-cyan-300/15 bg-white/5 px-3 py-2 text-xs text-white">Quick View</button>
                    <Link to={`/district/${item.districtId}`} className="rounded-xl border border-cyan-300/15 bg-cyan-400/10 px-3 py-2 text-xs text-cyan-100">Open</Link>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </GlassPanel>
  );
}
