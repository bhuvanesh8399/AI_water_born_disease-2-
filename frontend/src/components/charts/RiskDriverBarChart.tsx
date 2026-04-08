import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { GlassPanel } from "../ui/GlassPanel";

export function RiskDriverBarChart({ data }: { data: Array<{ name: string; value: number }> }) {
  return (
    <GlassPanel title="Risk Driver Leaderboard" subtitle="Most common contributors in the current intelligence layer">
      <div className="h-[320px] rounded-2xl border border-white/10 bg-slate-950/30 p-4">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <CartesianGrid stroke="rgba(255,255,255,0.06)" vertical={false} />
            <XAxis dataKey="name" stroke="rgba(255,255,255,0.45)" tickLine={false} axisLine={false} />
            <YAxis stroke="rgba(255,255,255,0.45)" tickLine={false} axisLine={false} />
            <Tooltip contentStyle={{ background: "rgba(2,6,23,0.95)", border: "1px solid rgba(148,163,184,0.18)", borderRadius: 16 }} />
            <Bar dataKey="value" radius={[12, 12, 0, 0]} fill="rgba(34,211,238,0.85)" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </GlassPanel>
  );
}
