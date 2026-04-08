import { useMemo, useState } from "react";
import { AlertInvestigationCard } from "../components/alerts/AlertInvestigationCard";
import { ErrorState } from "../components/common/ErrorState";
import { LoadingPanel } from "../components/common/LoadingPanel";
import { PageHeader } from "../components/common/PageHeader";
import { GlassPanel } from "../components/ui/GlassPanel";
import { RiskBadge } from "../components/ui/RiskBadge";
import { useAsyncData } from "../hooks/useAsyncData";
import { formatDateTime } from "../lib/utils";
import { dataSource } from "../services/dataSource";

export function AlertsPage() {
  const { data, loading, error, reload } = useAsyncData(() => dataSource.getAlerts(), []);
  const [selectedId, setSelectedId] = useState<number | string | null>(null);
  const selected = useMemo(() => (data ?? []).find((item) => item.id === selectedId) ?? data?.[0] ?? null, [data, selectedId]);

  return (
    <div>
      <PageHeader title="Alert Center" subtitle="Investigate district-level warning events, review evidence, and connect alerts back to district intelligence." />
      {loading ? <LoadingPanel /> : null}
      {error ? <ErrorState message={error} onRetry={reload} /> : null}
      {!loading && !error ? (
        <div className="grid gap-6 xl:grid-cols-[1fr_0.95fr]">
          <GlassPanel title="Active Alert Feed" subtitle="Operational alert stream with district and severity context">
            <div className="space-y-3">
              {(data ?? []).map((alert) => (
                <button key={alert.id} onClick={() => setSelectedId(alert.id)} className="block w-full rounded-2xl border border-white/10 bg-white/5 p-4 text-left transition-all hover:border-cyan-300/15 hover:bg-cyan-400/5">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <div className="flex items-center gap-2">
                        <h3 className="font-medium text-white">{alert.title ?? "District Alert"}</h3>
                        <RiskBadge level={alert.riskLevel} />
                      </div>
                      <p className="mt-2 text-sm text-cyan-50/72">{alert.message ?? "Hybrid score crossed alert threshold."}</p>
                      <div className="mt-2 text-xs text-cyan-100/50">{alert.districtName} • {formatDateTime(alert.createdAt)}</div>
                    </div>
                    <div className="text-xs text-cyan-100/60">{alert.status ?? "active"}</div>
                  </div>
                </button>
              ))}
            </div>
          </GlassPanel>
          <AlertInvestigationCard alert={selected} />
        </div>
      ) : null}
    </div>
  );
}
