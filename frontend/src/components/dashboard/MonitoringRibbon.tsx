import type { MonitoringStatus } from "../../types/api";
import { formatDateTime } from "../../lib/utils";
import { HealthChip } from "../ui/HealthChip";

export function MonitoringRibbon({ monitoring }: { monitoring?: MonitoringStatus | null }) {
  return (
    <div className="mb-6 grid gap-3 rounded-3xl border border-cyan-300/10 bg-slate-950/35 p-4 backdrop-blur-xl md:grid-cols-5">
      <div>
        <div className="tiny-label">Backend</div>
        <div className="mt-2"><HealthChip state={String(monitoring?.backendStatus ?? "unknown")} /></div>
      </div>
      <div>
        <div className="tiny-label">Database</div>
        <div className="mt-2"><HealthChip state={String(monitoring?.databaseStatus ?? "unknown")} /></div>
      </div>
      <div>
        <div className="tiny-label">Weather Sync</div>
        <div className="mt-2"><HealthChip state={String(monitoring?.weatherStatus ?? "unknown")} /></div>
      </div>
      <div>
        <div className="tiny-label">Models</div>
        <div className="mt-2"><HealthChip state={String(monitoring?.modelStatus ?? "unknown")} /></div>
      </div>
      <div>
        <div className="tiny-label">Last Pipeline Run</div>
        <div className="mt-2 text-sm text-cyan-50/75">{formatDateTime(monitoring?.lastPipelineRun)}</div>
      </div>
    </div>
  );
}
