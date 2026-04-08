export const endpoints = {
  dashboardSummary: "/api/dashboard/summary",
  dashboardHotspots: "/api/dashboard/hotspots",
  dashboardAlerts: "/api/dashboard/alerts",
  districts: "/api/districts",
  districtDetail: (districtId: string) => `/api/districts/${encodeURIComponent(districtId)}`,
  districtTrends: (districtId: string, days = 30) =>
    `/api/dashboard/trends/${encodeURIComponent(districtId)}?days=${days}`,
  monitoringStatus: "/api/monitoring/status",
  adminRunFullPipeline: "/api/admin/run-full-pipeline",
  adminTrainModels: "/api/admin/train-models",
  adminGeneratePredictions: "/api/admin/generate-predictions",
};
