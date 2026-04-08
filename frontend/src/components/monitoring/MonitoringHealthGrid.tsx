import type { MonitoringStatus } from "../../types/api";
import { formatDateTime } from "../../lib/utils";
import { GlassPanel } from "../ui/GlassPanel";
import { HealthChip } from "../ui/HealthChip";

function Item({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
      <div className="tiny-label">{label}</div>
      <div className="mt-2 text-xl font-semibold text-white">{value}</div>
    </div>
  );
}

export function MonitoringHealthGrid({ status }: { status?: MonitoringStatus | null }) {
  return (
    <GlassPanel title="System Monitoring" subtitle="Pipeline health, freshness, and platform trust layer">
      <div className="grid gap-4 xl:grid-cols-2">
        <div className="grid gap-4 sm:grid-cols-2">
          <Item label="Backend" value={String(status?.backendStatus ?? "unknown")} />
          <Item label="Database" value={String(status?.databaseStatus ?? "unknown")} />
          <Item label="Weather Sync" value={String(status?.weatherStatus ?? "unknown")} />
          <Item label="Models" value={String(status?.modelStatus ?? "unknown")} />
          <Item label="Stale Districts" value={status?.staleDistrictCount ?? "N/A"} />
          <Item label="Missing Enrichment" value={status?.missingEnrichmentCount ?? "N/A"} />
        </div>
        <div className="space-y-4">
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <div className="tiny-label">Pipeline State</div>
            <div className="mt-2"><HealthChip state={String(status?.pipelineStatus ?? "unknown")} /></div>
            <div className="mt-3 text-sm text-cyan-50/65">Last pipeline run: {formatDateTime(status?.lastPipelineRun)}</div>
            <div className="mt-2 text-sm text-cyan-50/65">Last weather sync: {formatDateTime(status?.lastWeatherSync)}</div>
          </div>
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <div className="tiny-label">Monitoring Notes</div>
            <ul className="mt-3 space-y-2 text-sm text-cyan-50/72">
              {(status?.notes?.length ? status.notes : ["No monitoring notes available."]).map((note) => <li key={note}>• {note}</li>)}
            </ul>
          </div>
        </div>
      </div>
    </GlassPanel>
  );
}
