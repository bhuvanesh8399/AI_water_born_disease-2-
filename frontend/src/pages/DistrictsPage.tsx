import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { ErrorState } from "../components/common/ErrorState";
import { LoadingPanel } from "../components/common/LoadingPanel";
import { PageHeader } from "../components/common/PageHeader";
import { GlassPanel } from "../components/ui/GlassPanel";
import { RiskBadge } from "../components/ui/RiskBadge";
import { SearchBar } from "../components/ui/SearchBar";
import { useAsyncData } from "../hooks/useAsyncData";
import { formatPercent } from "../lib/utils";
import { dataSource } from "../services/dataSource";

export function DistrictsPage() {
  const { data, loading, error, reload } = useAsyncData(() => dataSource.getDistricts(), []);
  const [query, setQuery] = useState("");
  const filtered = useMemo(() => {
    const base = data ?? [];
    const lower = query.trim().toLowerCase();
    if (!lower) return base;
    return base.filter((item) => item.districtName.toLowerCase().includes(lower) || item.districtId.toLowerCase().includes(lower));
  }, [data, query]);

  return (
    <div>
      <PageHeader title="District Intelligence" subtitle="Search, scan, and compare districts through a water-risk and public-health monitoring lens." rightSlot={<div className="w-[260px]"><SearchBar value={query} onChange={setQuery} placeholder="Search district or ID" /></div>} />
      {loading ? <LoadingPanel /> : null}
      {error ? <ErrorState message={error} onRetry={reload} /> : null}
      {!loading && !error ? (
        <GlassPanel title="District List" subtitle="Operational district view with risk, confidence, and dominant pressure signal">
          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead>
                <tr className="border-b border-white/10 text-cyan-100/55">
                  <th className="pb-3 pr-4">District</th><th className="pb-3 pr-4">ID</th><th className="pb-3 pr-4">Risk</th><th className="pb-3 pr-4">Confidence</th><th className="pb-3 pr-4">Primary Reason</th><th className="pb-3 pr-4">Action</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((item) => (
                  <tr key={item.districtId} className="border-b border-white/5 last:border-0">
                    <td className="py-4 pr-4 font-medium text-white">{item.districtName}</td>
                    <td className="py-4 pr-4 text-cyan-50/65">{item.districtId}</td>
                    <td className="py-4 pr-4"><RiskBadge level={item.riskLevel} /></td>
                    <td className="py-4 pr-4 text-cyan-50/70">{formatPercent(item.confidence)}</td>
                    <td className="py-4 pr-4 text-cyan-50/65">{item.primaryReason ?? "Signal pressure"}</td>
                    <td className="py-4 pr-4"><Link to={`/district/${item.districtId}`} className="rounded-xl border border-cyan-300/15 bg-cyan-400/10 px-3 py-2 text-xs text-cyan-100">Open Profile</Link></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </GlassPanel>
      ) : null}
    </div>
  );
}
