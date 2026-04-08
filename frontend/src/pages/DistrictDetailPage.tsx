import { useParams } from "react-router-dom";
import { RiskTrendChart } from "../components/charts/RiskTrendChart";
import { ErrorState } from "../components/common/ErrorState";
import { LoadingPanel } from "../components/common/LoadingPanel";
import { PageHeader } from "../components/common/PageHeader";
import { ActionPlaybook } from "../components/dashboard/ActionPlaybook";
import { ExecutiveSummaryCard } from "../components/districts/ExecutiveSummaryCard";
import { SignalBreakdownPanel } from "../components/districts/SignalBreakdownPanel";
import { ConsensusMeter } from "../components/ui/ConsensusMeter";
import { GlassPanel } from "../components/ui/GlassPanel";
import { MetricCard } from "../components/ui/MetricCard";
import { useAsyncData } from "../hooks/useAsyncData";
import { formatDateTime, formatPercent } from "../lib/utils";
import { dataSource } from "../services/dataSource";

export function DistrictDetailPage() {
  const { districtId = "D001" } = useParams();
  const detail = useAsyncData(() => dataSource.getDistrictDetail(districtId), [districtId]);
  const trends = useAsyncData(() => dataSource.getDistrictTrends(districtId, 30), [districtId]);
  const loading = detail.loading || trends.loading;
  const error = detail.error || trends.error;

  return (
    <div>
      <PageHeader title="District Profile" subtitle="Deep district intelligence with signal breakdown, model agreement, trust visibility, and recommended actions." />
      {loading ? <LoadingPanel /> : null}
      {error ? <ErrorState message={error} onRetry={() => window.location.reload()} /> : null}
      {!loading && !error && detail.data ? (
        <>
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            <MetricCard label="District" value={detail.data.districtName} />
            <MetricCard label="Risk Score" value={detail.data.riskScore} />
            <MetricCard label="Confidence" value={formatPercent(detail.data.confidence)} />
            <MetricCard label="Last Updated" value={formatDateTime(detail.data.lastUpdated)} />
          </div>
          <div className="mt-6 grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
            <div className="space-y-6">
              <ExecutiveSummaryCard detail={detail.data} />
              <RiskTrendChart data={trends.data ?? []} title="District Risk Trajectory" subtitle="Last 30 days of risk movement" />
              <SignalBreakdownPanel detail={detail.data} />
              <ActionPlaybook detail={detail.data} />
            </div>
            <div className="space-y-6">
              <GlassPanel title="Model Comparison" subtitle="Cross-check rule-based and ML outputs for trust visibility">
                <ConsensusMeter scores={detail.data.modelScores} />
              </GlassPanel>
              <GlassPanel title="District Attributes" subtitle="Key demographic and infrastructure context used by the system">
                <div className="grid gap-3 sm:grid-cols-2">
                  <div className="rounded-2xl border border-white/10 bg-white/5 p-4"><div className="tiny-label">Population</div><div className="mt-2 text-2xl font-semibold text-white">{detail.data.population ?? "N/A"}</div></div>
                  <div className="rounded-2xl border border-white/10 bg-white/5 p-4"><div className="tiny-label">Sanitation Score</div><div className="mt-2 text-2xl font-semibold text-white">{detail.data.sanitationScore ?? "N/A"}</div></div>
                  <div className="rounded-2xl border border-white/10 bg-white/5 p-4"><div className="tiny-label">Water Quality Score</div><div className="mt-2 text-2xl font-semibold text-white">{detail.data.waterQualityScore ?? "N/A"}</div></div>
                  <div className="rounded-2xl border border-white/10 bg-white/5 p-4"><div className="tiny-label">Vulnerability Index</div><div className="mt-2 text-2xl font-semibold text-white">{detail.data.vulnerabilityIndex ?? "N/A"}</div></div>
                </div>
              </GlassPanel>
            </div>
          </div>
        </>
      ) : null}
    </div>
  );
}
