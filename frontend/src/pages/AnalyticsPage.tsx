import { RiskDriverBarChart } from "../components/charts/RiskDriverBarChart";
import { RiskTrendChart } from "../components/charts/RiskTrendChart";
import { PageHeader } from "../components/common/PageHeader";
import { DistrictCompareTable } from "../components/districts/DistrictCompareTable";
import { useAsyncData } from "../hooks/useAsyncData";
import { mockTrends } from "../lib/mock";
import { dataSource } from "../services/dataSource";

const driverData = [
  { name: "Rainfall", value: 88 },
  { name: "Sanitation", value: 74 },
  { name: "Alert History", value: 69 },
  { name: "Water Quality", value: 66 },
  { name: "Vulnerability", value: 61 },
];

export function AnalyticsPage() {
  const districts = useAsyncData(() => dataSource.getDistricts(), []);
  return (
    <div>
      <PageHeader title="Risk Analytics" subtitle="Cross-district intelligence views, recurring risk drivers, and trend-based analysis for monitoring teams." />
      <div className="grid gap-6 xl:grid-cols-2">
        <RiskTrendChart data={mockTrends} title="System Risk Trend" subtitle="Illustrative district-level movement across recent days" />
        <RiskDriverBarChart data={driverData} />
      </div>
      <div className="mt-6"><DistrictCompareTable districts={districts.data ?? []} /></div>
    </div>
  );
}
