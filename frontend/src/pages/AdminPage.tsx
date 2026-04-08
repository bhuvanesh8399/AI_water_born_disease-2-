import { AdminActionPanel } from "../components/admin/AdminActionPanel";
import { PageHeader } from "../components/common/PageHeader";
import { GlassPanel } from "../components/ui/GlassPanel";

export function AdminPage() {
  return (
    <div>
      <PageHeader title="Admin Control" subtitle="Manual execution points for ingestion pipeline, model training, and prediction generation." />
      <AdminActionPanel />
      <div className="mt-6">
        <GlassPanel title="Safety Note" subtitle="Operational reminder">
          <p className="text-sm leading-6 text-cyan-50/72">This page triggers heavy backend operations. Keep confirmation and execution logs when you wire the final backend.</p>
        </GlassPanel>
      </div>
    </div>
  );
}
