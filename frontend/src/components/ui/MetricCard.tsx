import { GlassPanel } from "./GlassPanel";

type Props = {
  label: string;
  value: string | number;
  hint?: string;
};

export function MetricCard({ label, value, hint }: Props) {
  return (
    <GlassPanel className="min-h-[140px]">
      <div className="flex h-full flex-col justify-between">
        <div className="tiny-label">{label}</div>
        <div className="mt-4 text-4xl font-bold tracking-tight text-white">{value}</div>
        {hint ? <div className="mt-4 text-sm text-cyan-50/65">{hint}</div> : null}
      </div>
    </GlassPanel>
  );
}
