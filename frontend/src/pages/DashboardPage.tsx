import { useMemo, useState } from "react";
import { CriticalDistrictHero } from "../components/dashboard/CriticalDistrictHero";
import { AlertFeed } from "../components/dashboard/AlertFeed";
import { HotspotQueue } from "../components/dashboard/HotspotQueue";
import { LiveDeltaPanel } from "../components/dashboard/LiveDeltaPanel";
import { MonitoringRibbon } from "../components/dashboard/MonitoringRibbon";
import { QuickInsightRail } from "../components/dashboard/QuickInsightRail";
import { ErrorState } from "../components/common/ErrorState";
import { LoadingPanel } from "../components/common/LoadingPanel";
import { PageHeader } from "../components/common/PageHeader";
import { DistrictQuickDrawer } from "../components/districts/DistrictQuickDrawer";
import { MetricCard } from "../components/ui/MetricCard";
import { useAsyncData } from "../hooks/useAsyncData";
import { formatPercent } from "../lib/utils";
import { dataSource } from "../services/dataSource";

export function DashboardPage() {
  const summary = useAsyncData(() => dataSource.getSummary(), []);
  const hotspots = useAsyncData(() => dataSource.getHotspots(), []);
  const alerts = useAsyncData(() => dataSource.getAlerts(), []);
  const monitoring = useAsyncData(() => dataSource.getMonitoringStatus(), []);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [selectedDistrictId, setSelectedDistrictId] = useState<string | null>(null);
  const districtDetail = useAsyncData(() => (selectedDistrictId ? dataSource.getDistrictDetail(selectedDistrictId) : Promise.resolve(null)), [selectedDistrictId]);
  const loading = summary.loading || hotspots.loading || alerts.loading || monitoring.loading;
  const error = summary.error || hotspots.error || alerts.error || monitoring.error;
  const metrics = useMemo(() => {
    const s = summary.data;
    return [
      { label: "Total Districts", value: s?.totalDistricts ?? "—" },
      { label: "High Risk", value: s?.highRiskCount ?? "—" },
      { label: "Active Alerts", value: s?.activeAlerts ?? "—" },
      { label: "Avg Confidence", value: formatPercent(s?.averageConfidence) },
    ];
  }, [summary.data]);

  return (
    <div>
      <PageHeader title="Dashboard" subtitle="Water-oriented district risk command center with trust, explainability, and action guidance built into the operational view." />
      <MonitoringRibbon monitoring={monitoring.data} />
      {loading ? <LoadingPanel /> : null}
      {error ? <ErrorState message={error} onRetry={() => window.location.reload()} /> : null}
      {!loading && !error ? (
        <>
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            {metrics.map((item) => <MetricCard key={item.label} label={item.label} value={item.value} />)}
          </div>
          <div className="mt-6"><CriticalDistrictHero summary={summary.data} /></div>
          <div className="mt-6 grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
            <div className="space-y-6">
              <HotspotQueue hotspots={hotspots.data ?? []} onQuickView={(districtId) => { setSelectedDistrictId(districtId); setDrawerOpen(true); }} />
              <AlertFeed alerts={alerts.data ?? []} />
            </div>
            <div className="space-y-6">
              <LiveDeltaPanel />
              <QuickInsightRail detail={districtDetail.data} />
            </div>
          </div>
        </>
      ) : null}
      <DistrictQuickDrawer open={drawerOpen} onClose={() => setDrawerOpen(false)} detail={districtDetail.data} />
    </div>
  );
}
