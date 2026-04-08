import { Database, Droplets, Radar, ShieldAlert, Sparkles } from "lucide-react";
import { GlassPanel } from "../ui/GlassPanel";

const steps = [
  { icon: Database, title: "Data Sources", desc: "District master, profiles, observations, historical alerts, enrichment layers, and weather inputs." },
  { icon: Droplets, title: "Cleaning + Aggregation", desc: "Normalize district IDs, aggregate lower-level observations to district-day, tolerate missing enrichment." },
  { icon: Radar, title: "Feature Engineering", desc: "Build rainfall pressure, sanitation weakness, water stress, vulnerability, and historical alert signals." },
  { icon: Sparkles, title: "Models", desc: "Rule engine for trust, Random Forest for tabular patterns, XGBoost for stronger predictive accuracy." },
  { icon: ShieldAlert, title: "Hybrid Warning Output", desc: "Produce risk score, confidence, top reasons, and recommended actions for officials." },
];

export function AIWorkflowDiagram() {
  return (
    <GlassPanel title="AI Workflow" subtitle="How the system transforms water and public-health signals into actionable warnings">
      <div className="grid gap-4 xl:grid-cols-5">
        {steps.map((step, index) => {
          const Icon = step.icon;
          return (
            <div key={step.title} className="rounded-3xl border border-white/10 bg-white/5 p-5">
              <div className="mb-4 inline-flex rounded-2xl border border-cyan-300/15 bg-cyan-400/10 p-3 text-cyan-100"><Icon className="h-5 w-5" /></div>
              <div className="tiny-label">Step {index + 1}</div>
              <div className="mt-2 text-lg font-semibold text-white">{step.title}</div>
              <p className="mt-3 text-sm leading-6 text-cyan-50/68">{step.desc}</p>
            </div>
          );
        })}
      </div>
    </GlassPanel>
  );
}
