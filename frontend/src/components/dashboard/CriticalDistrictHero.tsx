import { AlertTriangle, ArrowUpRight, Droplets } from "lucide-react";
import type { Summary } from "../../types/api";
import { formatNumber, formatPercent } from "../../lib/utils";
import { GlassPanel } from "../ui/GlassPanel";
import { LiquidProgressBar } from "../ui/LiquidProgressBar";
import { RiskBadge } from "../ui/RiskBadge";

export function CriticalDistrictHero({ summary }: { summary?: Summary | null }) {
  const district = summary?.mostCriticalDistrict;
  return (
    <GlassPanel
      title="Most Critical District"
      subtitle="Immediate focus point for district-level intervention"
      rightSlot={district ? <RiskBadge level={district.riskLevel} /> : null}
      className="min-h-[260px]"
    >
      {district ? (
        <div className="grid gap-6 lg:grid-cols-[1.25fr_0.75fr]">
          <div>
            <div className="flex items-start justify-between gap-4">
              <div>
                <div className="text-3xl font-bold text-white md:text-4xl">{district.districtName}</div>
                <p className="mt-3 max-w-2xl text-sm leading-6 text-cyan-50/70">
                  {district.primaryReason ?? "Risk remains elevated due to a combination of environmental and vulnerability signals."}
                </p>
              </div>
              <ArrowUpRight className="mt-1 h-5 w-5 text-cyan-200/70" />
            </div>
            <div className="mt-6 grid gap-3 sm:grid-cols-3">
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="tiny-label">Risk Score</div>
                <div className="mt-2 text-3xl font-semibold text-white">{formatNumber(district.riskScore)}</div>
              </div>
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="tiny-label">Confidence</div>
                <div className="mt-2 text-3xl font-semibold text-white">{formatPercent(district.confidence)}</div>
              </div>
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="tiny-label">Trend</div>
                <div className="mt-2 text-2xl font-semibold text-white">{String(district.trend ?? "stable").toUpperCase()}</div>
              </div>
            </div>
          </div>
          <div className="rounded-3xl border border-cyan-300/12 bg-slate-950/35 p-5">
            <div className="flex items-center gap-2 text-cyan-100/80">
              <Droplets className="h-4 w-4" />
              <span className="text-sm font-medium">Immediate Response Playbook</span>
            </div>
            <ul className="mt-4 space-y-3 text-sm text-cyan-50/72">
              <li className="flex gap-2"><AlertTriangle className="mt-0.5 h-4 w-4 text-orange-300" />Increase water quality testing in vulnerable blocks.</li>
              <li className="flex gap-2"><AlertTriangle className="mt-0.5 h-4 w-4 text-orange-300" />Run sanitation inspection where risk remains clustered.</li>
              <li className="flex gap-2"><AlertTriangle className="mt-0.5 h-4 w-4 text-orange-300" />Monitor rainfall and contamination signals for the next 48 hours.</li>
            </ul>
            <div className="mt-6">
              <LiquidProgressBar value={district.confidence ?? 0} label="Decision Confidence" />
            </div>
          </div>
        </div>
      ) : (
        <p className="text-sm text-cyan-50/65">No critical district data available.</p>
      )}
    </GlassPanel>
  );
}
