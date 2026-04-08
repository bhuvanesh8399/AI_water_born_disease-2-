import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { TrendPoint } from "../../types/api";
import { formatDateTime } from "../../lib/utils";
import { GlassPanel } from "../ui/GlassPanel";

export function RiskTrendChart({ data, title = "Risk Trend", subtitle = "District risk evolution over time" }: { data: TrendPoint[]; title?: string; subtitle?: string }) {
  const chartData = data.map((item) => ({
    ...item,
    shortDate: new Date(item.date).toLocaleDateString("en-IN", { day: "2-digit", month: "short" }),
  }));

  return (
    <GlassPanel title={title} subtitle={subtitle}>
      <div className="h-[320px] rounded-2xl border border-white/10 bg-slate-950/30 p-4">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="riskFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="rgba(34,211,238,0.85)" />
                <stop offset="100%" stopColor="rgba(34,211,238,0.02)" />
              </linearGradient>
            </defs>
            <CartesianGrid stroke="rgba(255,255,255,0.06)" vertical={false} />
            <XAxis dataKey="shortDate" stroke="rgba(255,255,255,0.45)" tickLine={false} axisLine={false} />
            <YAxis stroke="rgba(255,255,255,0.45)" tickLine={false} axisLine={false} />
            <Tooltip
              contentStyle={{ background: "rgba(2,6,23,0.95)", border: "1px solid rgba(148,163,184,0.18)", borderRadius: 16 }}
              formatter={(value) => [value ?? "N/A", "Risk Score"]}
              labelFormatter={(label, payload) => (payload?.[0]?.payload?.date ? formatDateTime(payload[0].payload.date) : label)}
            />
            <Area type="monotone" dataKey="riskScore" stroke="rgba(34,211,238,1)" strokeWidth={3} fill="url(#riskFill)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </GlassPanel>
  );
}
