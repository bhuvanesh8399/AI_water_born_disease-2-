import { useState } from "react";
import { Play, RefreshCw, Sparkles } from "lucide-react";
import { dataSource } from "../../services/dataSource";
import { GlassPanel } from "../ui/GlassPanel";

export function AdminActionPanel() {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  async function run(action: () => Promise<{ message: string }>) {
    setLoading(true);
    setMessage(null);
    try {
      const result = await action();
      setMessage(result.message);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Action failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <GlassPanel title="Admin Control" subtitle="Manual control points for pipeline, training, and prediction generation">
      <div className="grid gap-4 md:grid-cols-3">
        <button disabled={loading} onClick={() => void run(() => dataSource.runFullPipeline())} className="flex items-center justify-center gap-2 rounded-2xl border border-cyan-300/15 bg-cyan-400/10 px-4 py-4 text-sm font-medium text-white disabled:opacity-60"><Play className="h-4 w-4" /> Run Full Pipeline</button>
        <button disabled={loading} onClick={() => void run(() => dataSource.trainModels())} className="flex items-center justify-center gap-2 rounded-2xl border border-cyan-300/15 bg-white/5 px-4 py-4 text-sm font-medium text-white disabled:opacity-60"><RefreshCw className="h-4 w-4" /> Train Models</button>
        <button disabled={loading} onClick={() => void run(() => dataSource.generatePredictions())} className="flex items-center justify-center gap-2 rounded-2xl border border-cyan-300/15 bg-white/5 px-4 py-4 text-sm font-medium text-white disabled:opacity-60"><Sparkles className="h-4 w-4" /> Generate Predictions</button>
      </div>
      {message ? <div className="mt-4 rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-cyan-50/72">{message}</div> : null}
    </GlassPanel>
  );
}
