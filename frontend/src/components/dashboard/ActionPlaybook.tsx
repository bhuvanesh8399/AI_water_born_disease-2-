import type { DistrictDetail } from "../../types/api";
import { GlassPanel } from "../ui/GlassPanel";

function Block({ title, items }: { title: string; items?: string[] }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
      <div className="tiny-label">{title}</div>
      <ul className="mt-3 space-y-2 text-sm text-cyan-50/72">
        {(items?.length ? items : ["No guidance available yet."]).map((item) => <li key={item}>• {item}</li>)}
      </ul>
    </div>
  );
}

export function ActionPlaybook({ detail }: { detail?: DistrictDetail | null }) {
  return (
    <GlassPanel title="Recommended Actions" subtitle="Bridge prediction into district-level response planning">
      <div className="grid gap-4 xl:grid-cols-3">
        <Block title="Immediate" items={detail?.recommendedActions?.immediate} />
        <Block title="Preventive" items={detail?.recommendedActions?.preventive} />
        <Block title="Monitoring" items={detail?.recommendedActions?.monitoring} />
      </div>
    </GlassPanel>
  );
}
