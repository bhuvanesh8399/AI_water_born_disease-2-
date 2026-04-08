import type { ModelScores } from "../../types/api";
import { formatNumber } from "../../lib/utils";

export function ConsensusMeter({ scores }: { scores?: ModelScores }) {
  const values = [scores?.ruleBased, scores?.randomForest, scores?.xgboost].filter(
    (v): v is number => typeof v === "number",
  );
  const spread = values.length >= 2 ? Math.max(...values) - Math.min(...values) : 0;
  const label = spread <= 6 ? "Strong Agreement" : spread <= 15 ? "Partial Disagreement" : "Weak Agreement";

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <div className="tiny-label">Model Consensus</div>
        <div className="text-sm text-cyan-50/70">{label}</div>
      </div>
      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <div className="rounded-2xl border border-white/10 bg-white/5 p-3">
          <div className="tiny-label">Rule Engine</div>
          <div className="mt-2 text-2xl font-semibold text-white">{formatNumber(scores?.ruleBased)}</div>
        </div>
        <div className="rounded-2xl border border-white/10 bg-white/5 p-3">
          <div className="tiny-label">Random Forest</div>
          <div className="mt-2 text-2xl font-semibold text-white">{formatNumber(scores?.randomForest)}</div>
        </div>
        <div className="rounded-2xl border border-white/10 bg-white/5 p-3">
          <div className="tiny-label">XGBoost</div>
          <div className="mt-2 text-2xl font-semibold text-white">{formatNumber(scores?.xgboost)}</div>
        </div>
        <div className="rounded-2xl border border-cyan-300/15 bg-cyan-400/8 p-3">
          <div className="tiny-label">Hybrid</div>
          <div className="mt-2 text-2xl font-semibold text-white">{formatNumber(scores?.hybrid)}</div>
        </div>
      </div>
    </div>
  );
}
