import { getJson, postJson } from "./api";
import { endpoints } from "./endpoints";
import {
  mockAdminResult,
  mockAlerts,
  mockDistrictDetail,
  mockDistricts,
  mockHotspots,
  mockMonitoringStatus,
  mockSummary,
  mockTrends,
} from "../lib/mock";
import type {
  AdminActionResult,
  AlertItem,
  District,
  DistrictDetail,
  Hotspot,
  MonitoringStatus,
  RiskLevel,
  Summary,
  TrendDirection,
  TrendPoint,
} from "../types/api";

const USE_MOCK = import.meta.env.VITE_USE_MOCK === "true";

type SummaryPayload = {
  total_districts: number;
  high_risk: number;
  medium_risk: number;
  low_risk: number;
  active_alerts: number;
  average_confidence_score: number;
  last_updated: string;
};

type HotspotPayload = {
  district_id: string;
  district_name: string;
  final_score: number;
  risk_level: string;
  confidence_score: number;
  reasons: string[];
};

type AlertPayload = {
  id: number;
  district_id: string;
  district_name: string;
  severity: string;
  status: string;
  title: string;
  message: string;
  confidence_score: number;
  predicted_date: string;
  reasons: string[];
  recommended_actions: string[];
};

type DistrictPayload = {
  district_id: string;
  district_name: string;
};

type DistrictDetailPayload = {
  district: {
    district_id: string;
    district_name: string;
    population: number | null;
  };
  profile: {
    sanitation_score: number | null;
    water_quality_index: number | null;
    vulnerability_index: number | null;
  } | null;
  latest_prediction: {
    predicted_date: string;
    final_score: number;
    risk_level: string;
    confidence_score: number;
    data_completeness: number;
    data_freshness_score: number;
    reasons: string[];
    recommended_actions: string[];
    rule_score: number | null;
    rf_score: number | null;
    xgb_score: number | null;
  } | null;
  latest_metric: {
    sanitation_score: number | null;
    vulnerability_index: number | null;
    historical_alert_count: number | null;
  } | null;
  latest_weather: {
    rainfall_mm: number | null;
  } | null;
};

type TrendPayload = {
  date: string;
  final_score: number | null;
  risk_level: string | null;
  rf_score: number | null;
  xgb_score: number | null;
  rule_score: number | null;
  rainfall_mm: number | null;
};

type MonitoringPayload = {
  districts_total: number;
  enrichments_total: number;
  latest_weather_date: string | null;
  latest_metric_date: string | null;
  rf_model_loaded: boolean;
  xgb_model_loaded: boolean;
};

async function withFallback<T>(runner: () => Promise<T>, fallback: T): Promise<T> {
  if (USE_MOCK) return fallback;
  try {
    return await runner();
  } catch {
    return fallback;
  }
}

function toRiskLevel(value?: string | null): RiskLevel {
  const key = String(value ?? "").toLowerCase();
  if (key === "critical") return "critical";
  if (key === "high") return "high";
  if (key === "medium") return "medium";
  return "low";
}

function toTrendDirection(level?: string | null): TrendDirection {
  const risk = toRiskLevel(level);
  if (risk === "high" || risk === "critical") return "up";
  if (risk === "medium") return "stable";
  return "down";
}

function toHotspot(item: HotspotPayload): Hotspot {
  return {
    districtId: item.district_id,
    districtName: item.district_name,
    riskScore: item.final_score,
    riskLevel: toRiskLevel(item.risk_level),
    confidence: item.confidence_score,
    trend: toTrendDirection(item.risk_level),
    primaryReason: item.reasons?.[0] ?? "Signal pressure",
    activeAlert: toRiskLevel(item.risk_level) === "high",
  };
}

function splitActions(actions: string[] | undefined) {
  const list = actions ?? [];
  return {
    immediate: list.slice(0, 2),
    preventive: list.slice(2, 4),
    monitoring: list.slice(4),
  };
}

export const dataSource = {
  getSummary: () =>
    withFallback<Summary>(async () => {
      const [summary, hotspots] = await Promise.all([
        getJson<SummaryPayload>(endpoints.dashboardSummary),
        getJson<HotspotPayload[]>(endpoints.dashboardHotspots),
      ]);
      const mappedHotspots = hotspots.map(toHotspot);
      const mostCritical = mappedHotspots[0];
      return {
        totalDistricts: summary.total_districts,
        highRiskCount: summary.high_risk,
        mediumRiskCount: summary.medium_risk,
        lowRiskCount: summary.low_risk,
        activeAlerts: summary.active_alerts,
        averageConfidence: summary.average_confidence_score,
        lastUpdated: summary.last_updated,
        mostCriticalDistrict: mostCritical
          ? {
              districtId: mostCritical.districtId,
              districtName: mostCritical.districtName,
              riskScore: mostCritical.riskScore,
              riskLevel: mostCritical.riskLevel,
              confidence: mostCritical.confidence,
              primaryReason: mostCritical.primaryReason,
              trend: mostCritical.trend,
            }
          : undefined,
      };
    }, mockSummary),

  getHotspots: () =>
    withFallback<Hotspot[]>(async () => {
      const data = await getJson<HotspotPayload[]>(endpoints.dashboardHotspots);
      return data.map(toHotspot);
    }, mockHotspots),

  getAlerts: () =>
    withFallback<AlertItem[]>(async () => {
      const data = await getJson<AlertPayload[]>(endpoints.dashboardAlerts);
      return data.map((item) => ({
        id: item.id,
        districtId: item.district_id,
        districtName: item.district_name,
        riskLevel: toRiskLevel(item.severity),
        title: item.title,
        message: item.message,
        status: item.status,
        createdAt: item.predicted_date,
        confidence: item.confidence_score,
        reasonStack: item.reasons,
      }));
    }, mockAlerts),

  getDistricts: () =>
    withFallback<District[]>(async () => {
      const [districts, hotspots] = await Promise.all([
        getJson<DistrictPayload[]>(endpoints.districts),
        getJson<HotspotPayload[]>(endpoints.dashboardHotspots),
      ]);
      const hotspotMap = new Map(hotspots.map((item) => [item.district_id, toHotspot(item)]));
      return districts.map((item) => {
        const hotspot = hotspotMap.get(item.district_id);
        return {
          districtId: item.district_id,
          districtName: item.district_name,
          riskScore: hotspot?.riskScore,
          riskLevel: hotspot?.riskLevel,
          confidence: hotspot?.confidence,
          primaryReason: hotspot?.primaryReason,
        };
      });
    }, mockDistricts),

  getDistrictDetail: (districtId: string) =>
    withFallback<DistrictDetail>(async () => {
      const data = await getJson<DistrictDetailPayload>(endpoints.districtDetail(districtId));
      const prediction = data.latest_prediction;
      return {
        districtId: data.district.district_id,
        districtName: data.district.district_name,
        riskScore: prediction?.final_score ?? 0,
        riskLevel: toRiskLevel(prediction?.risk_level),
        confidence: prediction?.confidence_score ?? 0,
        lastUpdated: prediction?.predicted_date,
        population: data.district.population ?? undefined,
        sanitationScore: data.profile?.sanitation_score ?? data.latest_metric?.sanitation_score ?? undefined,
        waterQualityScore: data.profile?.water_quality_index ?? undefined,
        vulnerabilityIndex:
          data.profile?.vulnerability_index ?? data.latest_metric?.vulnerability_index ?? undefined,
        explainabilityReasons: prediction?.reasons ?? [],
        recommendedActions: splitActions(prediction?.recommended_actions),
        modelScores: {
          ruleBased: prediction?.rule_score ?? undefined,
          randomForest: prediction?.rf_score ?? undefined,
          xgboost: prediction?.xgb_score ?? undefined,
          hybrid: prediction?.final_score ?? undefined,
        },
        signalBreakdown: {
          weather: data.latest_weather?.rainfall_mm ?? undefined,
          waterQuality: data.profile?.water_quality_index ?? undefined,
          sanitation: data.profile?.sanitation_score ?? data.latest_metric?.sanitation_score ?? undefined,
          vulnerability:
            data.profile?.vulnerability_index ?? data.latest_metric?.vulnerability_index ?? undefined,
          historicalAlerts: data.latest_metric?.historical_alert_count ?? undefined,
        },
        dataReliability: {
          completeness: prediction?.data_completeness ?? undefined,
          freshness: prediction?.data_freshness_score ?? undefined,
          fallbackUsed: false,
        },
      };
    }, { ...mockDistrictDetail, districtId }),

  getDistrictTrends: (districtId: string, days = 30) =>
    withFallback<TrendPoint[]>(async () => {
      const data = await getJson<TrendPayload[]>(endpoints.districtTrends(districtId, days));
      return data.map((item) => ({
        date: item.date,
        riskScore: item.final_score ?? 0,
        riskLevel: item.risk_level ?? undefined,
        confidence: item.rf_score ?? item.xgb_score ?? item.rule_score ?? item.final_score ?? undefined,
        rainfall: item.rainfall_mm ?? undefined,
      }));
    }, mockTrends),

  getMonitoringStatus: () =>
    withFallback<MonitoringStatus>(async () => {
      const data = await getJson<MonitoringPayload>(endpoints.monitoringStatus);
      return {
        backendStatus: "healthy",
        databaseStatus: "healthy",
        weatherStatus: data.latest_weather_date ? "healthy" : "degraded",
        modelStatus: data.rf_model_loaded || data.xgb_model_loaded ? "healthy" : "degraded",
        pipelineStatus: data.latest_metric_date ? "healthy" : "degraded",
        lastPipelineRun: data.latest_metric_date ?? undefined,
        lastWeatherSync: data.latest_weather_date ?? undefined,
        staleDistrictCount: Math.max(0, data.districts_total - data.enrichments_total),
        missingEnrichmentCount: Math.max(0, data.districts_total - data.enrichments_total),
        notes: [
          data.latest_metric_date
            ? "District metrics are available from the latest pipeline run."
            : "Latest district metrics are missing.",
          data.latest_weather_date
            ? "Weather sync is present in the backend."
            : "Weather sync has not populated yet.",
        ],
      };
    }, mockMonitoringStatus),

  runFullPipeline: () =>
    withFallback<AdminActionResult>(async () => {
      const result = await postJson<Record<string, unknown>>(endpoints.adminRunFullPipeline);
      return {
        success: true,
        message: typeof result.detail === "string" ? result.detail : "Full pipeline triggered successfully",
        startedAt: new Date().toISOString(),
      };
    }, mockAdminResult),

  trainModels: () =>
    withFallback<AdminActionResult>(async () => {
      const result = await postJson<Record<string, unknown>>(endpoints.adminTrainModels);
      return {
        success: true,
        message: typeof result.detail === "string" ? result.detail : "Model training completed",
        startedAt: new Date().toISOString(),
      };
    }, mockAdminResult),

  generatePredictions: () =>
    withFallback<AdminActionResult>(async () => {
      const result = await postJson<Record<string, unknown>>(endpoints.adminGeneratePredictions);
      return {
        success: true,
        message: typeof result.detail === "string" ? result.detail : "Predictions generated",
        startedAt: new Date().toISOString(),
      };
    }, mockAdminResult),
};
