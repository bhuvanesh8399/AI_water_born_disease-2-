import { ErrorState } from "../components/common/ErrorState";
import { LoadingPanel } from "../components/common/LoadingPanel";
import { PageHeader } from "../components/common/PageHeader";
import { MonitoringHealthGrid } from "../components/monitoring/MonitoringHealthGrid";
import { useAsyncData } from "../hooks/useAsyncData";
import { dataSource } from "../services/dataSource";

export function MonitoringPage() {
  const { data, loading, error, reload } = useAsyncData(() => dataSource.getMonitoringStatus(), []);
  return (
    <div>
      <PageHeader title="Monitoring" subtitle="System-health view for ingestion, model readiness, weather synchronization, and district data freshness." />
      {loading ? <LoadingPanel /> : null}
      {error ? <ErrorState message={error} onRetry={reload} /> : null}
      {!loading && !error ? <MonitoringHealthGrid status={data} /> : null}
    </div>
  );
}
