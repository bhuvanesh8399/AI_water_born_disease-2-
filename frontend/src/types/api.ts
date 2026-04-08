export type RiskLevel = "low" | "medium" | "high" | "critical";
export type TrendDirection = "up" | "down" | "stable";
export type HealthState = "healthy" | "degraded" | "error" | "fallback" | "unknown";

export interface Summary {
  totalDistricts: number;
  highRiskCount: number;
  mediumRiskCount: number;
  lowRiskCount: number;
  activeAlerts: number;
  averageConfidence?: number;
  lastUpdated?: string;
  mostCriticalDistrict?: {
    districtId: string;
    districtName: string;
    riskScore: number;
    riskLevel: RiskLevel;
    confidence?: number;
    primaryReason?: string;
    trend?: TrendDirection;
  };
}

export interface Hotspot {
  districtId: string;
  districtName: string;
  riskScore: number;
  riskLevel: RiskLevel;
  confidence?: number;
  trend?: TrendDirection;
  primaryReason?: string;
  activeAlert?: boolean;
}

export interface AlertItem {
  id: number | string;
  districtId: string;
  districtName: string;
  riskLevel: RiskLevel;
  title?: string;
  message?: string;
  status?: string;
  createdAt?: string;
  confidence?: number;
  reasonStack?: string[];
}

export interface District {
  districtId: string;
  districtName: string;
  riskScore?: number;
  riskLevel?: RiskLevel;
  confidence?: number;
  primaryReason?: string;
}

export interface ModelScores {
  ruleBased?: number;
  randomForest?: number;
  xgboost?: number;
  hybrid?: number;
}

export interface DistrictDetail {
  districtId: string;
  districtName: string;
  riskScore: number;
  riskLevel: RiskLevel;
  confidence?: number;
  lastUpdated?: string;
  population?: number;
  sanitationScore?: number;
  waterQualityScore?: number;
  vulnerabilityIndex?: number;
  explainabilityReasons?: string[];
  recommendedActions?: {
    immediate?: string[];
    preventive?: string[];
    monitoring?: string[];
  };
  modelScores?: ModelScores;
  signalBreakdown?: {
    weather?: number;
    waterQuality?: number;
    sanitation?: number;
    vulnerability?: number;
    historicalAlerts?: number;
  };
  dataReliability?: {
    completeness?: number;
    freshness?: number;
    missingFields?: number;
    fallbackUsed?: boolean;
  };
}

export interface TrendPoint {
  date: string;
  riskScore: number;
  riskLevel?: string;
  confidence?: number;
  rainfall?: number;
}

export interface MonitoringStatus {
  backendStatus?: HealthState | string;
  databaseStatus?: HealthState | string;
  weatherStatus?: HealthState | string;
  modelStatus?: HealthState | string;
  pipelineStatus?: HealthState | string;
  lastPipelineRun?: string;
  lastWeatherSync?: string;
  staleDistrictCount?: number;
  missingEnrichmentCount?: number;
  notes?: string[];
}

export interface AdminActionResult {
  success: boolean;
  message: string;
  startedAt?: string;
  completedAt?: string;
}
