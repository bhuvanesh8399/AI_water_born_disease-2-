import { X } from "lucide-react";
import type { DistrictDetail } from "../../types/api";
import { formatPercent } from "../../lib/utils";
import { RiskBadge } from "../ui/RiskBadge";

export function DistrictQuickDrawer({ open, onClose, detail }: { open: boolean; onClose: () => void; detail?: DistrictDetail | null }) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-slate-950/55 backdrop-blur-sm">
      <div className="h-full w-full max-w-lg border-l border-white/10 bg-[#06111c]/95 p-6 shadow-2xl">
        <div className="mb-5 flex items-start justify-between gap-4">
          <div>
            <div className="tiny-label">District Quick View</div>
            <h3 className="mt-2 text-2xl font-bold text-white">{detail?.districtName ?? "District"}</h3>
          </div>
          <button onClick={onClose} className="rounded-xl border border-white/10 p-2 text-slate-300"><X className="h-4 w-4" /></button>
        </div>
        <div className="space-y-4">
          <div className="flex items-center gap-3">
            <RiskBadge level={detail?.riskLevel} />
            <div className="text-sm text-cyan-50/70">Confidence: {formatPercent(detail?.confidence)}</div>
          </div>
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <div className="tiny-label">Top Drivers</div>
            <ul className="mt-3 space-y-2 text-sm text-cyan-50/72">
              {(detail?.explainabilityReasons ?? []).slice(0, 3).map((reason) => <li key={reason}>• {reason}</li>)}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
