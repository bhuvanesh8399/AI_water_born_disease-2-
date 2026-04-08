import { ArrowDownRight, ArrowUpRight } from "lucide-react";
import { GlassPanel } from "../ui/GlassPanel";

const items = [
  { label: "Districts moved to high risk", value: "+3", up: true },
  { label: "Alerts triggered in last cycle", value: "+2", up: true },
  { label: "Average confidence change", value: "+4%", up: true },
  { label: "Districts with stale data", value: "-1", up: false },
];

export function LiveDeltaPanel() {
  return (
    <GlassPanel title="What Changed Now" subtitle="Quick operational deltas since the last cycle">
      <div className="space-y-3">
        {items.map((item) => (
          <div key={item.label} className="flex items-center justify-between rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
            <div className="text-sm text-cyan-50/75">{item.label}</div>
            <div className="flex items-center gap-2 text-sm font-medium text-white">
              {item.up ? <ArrowUpRight className="h-4 w-4 text-cyan-300" /> : <ArrowDownRight className="h-4 w-4 text-emerald-300" />}
              {item.value}
            </div>
          </div>
        ))}
      </div>
    </GlassPanel>
  );
}
