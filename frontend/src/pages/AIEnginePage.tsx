import { AIWorkflowDiagram } from "../components/ai/AIWorkflowDiagram";
import { PageHeader } from "../components/common/PageHeader";
import { GlassPanel } from "../components/ui/GlassPanel";

export function AIEnginePage() {
  return (
    <div>
      <PageHeader title="AI Engine" subtitle="Transparent view of how environmental signals, district factors, and hybrid intelligence produce explainable warnings." />
      <AIWorkflowDiagram />
      <div className="mt-6 grid gap-6 xl:grid-cols-3">
        <GlassPanel title="Rule Engine" subtitle="Trust layer"><p className="text-sm leading-6 text-cyan-50/72">Keeps the system interpretable through human-readable thresholds and domain-driven warning logic.</p></GlassPanel>
        <GlassPanel title="Random Forest" subtitle="Pattern learner"><p className="text-sm leading-6 text-cyan-50/72">Learns non-linear relationships across district-level sanitation, weather, vulnerability, and historical signals.</p></GlassPanel>
        <GlassPanel title="XGBoost" subtitle="Accuracy layer"><p className="text-sm leading-6 text-cyan-50/72">Adds stronger gradient-boosted tabular prediction power while still feeding into the hybrid trust framework.</p></GlassPanel>
      </div>
    </div>
  );
}
