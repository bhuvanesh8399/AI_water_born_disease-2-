import type {
  AdminActionResult,
  AlertItem,
  District,
  DistrictDetail,
  Hotspot,
  MonitoringStatus,
  Summary,
  TrendPoint,
} from "../types/api";

export const mockSummary: Summary = {
  totalDistricts: 45,
  highRiskCount: 6,
  mediumRiskCount: 14,
  lowRiskCount: 25,
  activeAlerts: 8,
  averageConfidence: 84,
  lastUpdated: new Date().toISOString(),
  mostCriticalDistrict: {
    districtId: "D001",
    districtName: "Chennai",
    riskScore: 84,
    riskLevel: "high",
    confidence: 88,
    primaryReason: "Rainfall pressure, sanitation weakness, and historical alert similarity.",
    trend: "up",
  },
};

export const mockHotspots: Hotspot[] = [
  {
    districtId: "D001",
    districtName: "Chennai",
    riskScore: 84,
    riskLevel: "high",
    confidence: 88,
    trend: "up",
    primaryReason: "Heavy rainfall trend",
    activeAlert: true,
  },
  {
    districtId: "D002",
    districtName: "Madurai",
    riskScore: 79,
    riskLevel: "high",
    confidence: 82,
    trend: "up",
    primaryReason: "Water quality stress",
    activeAlert: true,
  },
  {
    districtId: "D003",
    districtName: "Coimbatore",
    riskScore: 67,
    riskLevel: "medium",
    confidence: 77,
    trend: "stable",
    primaryReason: "Rising vulnerability blend",
    activeAlert: false,
  }
];

export const mockAlerts: AlertItem[] = [
  {
    id: 1,
    districtId: "D001",
    districtName: "Chennai",
    riskLevel: "high",
    title: "Escalating district risk",
    message: "Hybrid score crossed high threshold with strong model agreement.",
    status: "ACTIVE",
    createdAt: new Date().toISOString(),
    confidence: 88,
    reasonStack: ["Rainfall anomaly", "Sanitation weakness", "Alert history recurrence"],
  },
];

export const mockDistricts: District[] = [
  {
    districtId: "D001",
    districtName: "Chennai",
    riskScore: 84,
    riskLevel: "high",
    confidence: 88,
    primaryReason: "Rainfall pressure",
  },
];

export const mockDistrictDetail: DistrictDetail = {
  districtId: "D001",
  districtName: "Chennai",
  riskScore: 84,
  riskLevel: "high",
  confidence: 88,
  lastUpdated: new Date().toISOString(),
  population: 4646732,
  sanitationScore: 58,
  waterQualityScore: 61,
  vulnerabilityIndex: 71,
  explainabilityReasons: [
    "Rainfall trend remained elevated across recent days.",
    "Sanitation score is weak relative to safer districts.",
    "District matches historical alert conditions.",
  ],
  recommendedActions: {
    immediate: ["Increase water sample testing", "Alert field inspection teams"],
    preventive: ["Sanitation sweep in vulnerable blocks", "Push local advisory messaging"],
    monitoring: ["Track rainfall for next 48 hours", "Review contamination updates tomorrow"],
  },
  modelScores: {
    ruleBased: 81,
    randomForest: 86,
    xgboost: 84,
    hybrid: 84,
  },
  signalBreakdown: {
    weather: 82,
    waterQuality: 64,
    sanitation: 58,
    vulnerability: 71,
    historicalAlerts: 75,
  },
  dataReliability: {
    completeness: 86,
    freshness: 90,
    missingFields: 2,
    fallbackUsed: false,
  },
};

export const mockTrends: TrendPoint[] = Array.from({ length: 30 }).map((_, index) => ({
  date: new Date(Date.now() - (29 - index) * 24 * 60 * 60 * 1000).toISOString(),
  riskScore: 54 + Math.round(Math.sin(index / 4) * 8 + index * 0.8),
  confidence: 72 + (index % 8),
  rainfall: 18 + ((index * 7) % 25),
}));

export const mockMonitoringStatus: MonitoringStatus = {
  backendStatus: "healthy",
  databaseStatus: "healthy",
  weatherStatus: "healthy",
  modelStatus: "healthy",
  pipelineStatus: "degraded",
  lastPipelineRun: new Date(Date.now() - 1000 * 60 * 35).toISOString(),
  lastWeatherSync: new Date(Date.now() - 1000 * 60 * 14).toISOString(),
  staleDistrictCount: 2,
  missingEnrichmentCount: 6,
  notes: ["Pipeline completed with partial enrichment gaps.", "Weather sync is recent."],
};

export const mockAdminResult: AdminActionResult = {
  success: true,
  message: "Triggered successfully",
  startedAt: new Date().toISOString(),
};
