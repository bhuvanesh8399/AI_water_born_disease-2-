import type { AlertItem } from "../../types/api";
import { formatDateTime, formatPercent } from "../../lib/utils";
import { GlassPanel } from "../ui/GlassPanel";
import { RiskBadge } from "../ui/RiskBadge";

export function AlertInvestigationCard({ alert }: { alert?: AlertItem | null }) {
  return (
    <GlassPanel title="Alert Investigation" subtitle="Evidence, timing, and recommended interpretation" rightSlot={<RiskBadge level={alert?.riskLevel} />}>
      {alert ? (
        <div className="space-y-4">
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <div className="tiny-label">District</div>
            <div className="mt-2 text-xl font-semibold text-white">{alert.districtName}</div>
            <div className="mt-2 text-sm text-cyan-50/65">Created {formatDateTime(alert.createdAt)}</div>
            <div className="mt-2 text-sm text-cyan-50/65">Confidence {formatPercent(alert.confidence)}</div>
          </div>
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <div className="tiny-label">Reason Stack</div>
            <ul className="mt-3 space-y-2 text-sm text-cyan-50/72">
              {(alert.reasonStack ?? []).map((reason) => <li key={reason}>• {reason}</li>)}
            </ul>
          </div>
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4 text-sm text-cyan-50/72">{alert.message ?? "Alert explanation is not available yet."}</div>
        </div>
      ) : (
        <p className="text-sm text-cyan-50/65">Select an alert to inspect it.</p>
      )}
    </GlassPanel>
  );
}
