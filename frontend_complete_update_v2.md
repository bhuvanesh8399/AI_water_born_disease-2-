# AI-Based Early Warning System — Complete Frontend Update (Water-Intelligence UI)

This bundle gives you a **full frontend rewrite/update** shaped around the project identity:

- **water-oriented visual system**
- **district risk command center**
- **public health seriousness**
- **AI trust + explainability + action guidance**
- **new backend contract service layer**
- **stronger page architecture**

> Assumptions:
>
> - React + Vite + TypeScript + Tailwind CSS
> - `react-router-dom`, `lucide-react`, `framer-motion`, `recharts`, `clsx`, `tailwind-merge`
> - backend connection happens later, but the frontend service layer is already aligned to the new backend contract

---

## Folder Structure

```txt
frontend/
  src/
    app/
      layout/
        AppShell.tsx
      routes/
        router.tsx
    components/
      background/
        WaterBackground.tsx
      charts/
        RiskTrendChart.tsx
        RiskDriverBarChart.tsx
      common/
        EmptyState.tsx
        ErrorState.tsx
        LoadingPanel.tsx
        PageHeader.tsx
        SectionCard.tsx
      ui/
        ConsensusMeter.tsx
        DeltaItem.tsx
        GlassPanel.tsx
        HealthChip.tsx
        LiquidProgressBar.tsx
        MetricCard.tsx
        RiskBadge.tsx
        SearchBar.tsx
      dashboard/
        ActionPlaybook.tsx
        AlertFeed.tsx
        CriticalDistrictHero.tsx
        DataReliabilityCard.tsx
        HotspotQueue.tsx
        LiveDeltaPanel.tsx
        MonitoringRibbon.tsx
        QuickInsightRail.tsx
      districts/
        DistrictCompareTable.tsx
        DistrictQuickDrawer.tsx
        ExecutiveSummaryCard.tsx
        SignalBreakdownPanel.tsx
      alerts/
        AlertInvestigationCard.tsx
      monitoring/
        MonitoringHealthGrid.tsx
      ai/
        AIWorkflowDiagram.tsx
      admin/
        AdminActionPanel.tsx
    hooks/
      useAsyncData.ts
    lib/
      mock.ts
      utils.ts
    pages/
      AdminPage.tsx
      AIEnginePage.tsx
      AlertsPage.tsx
      AnalyticsPage.tsx
      DashboardPage.tsx
      DistrictDetailPage.tsx
      DistrictsPage.tsx
      MonitoringPage.tsx
    services/
      api.ts
      dataSource.ts
      endpoints.ts
    types/
      api.ts
    index.css
    main.tsx
```

---

## 1) `frontend/package.json`

```json
{
  "name": "ai-early-warning-system-frontend",
  "private": true,
  "version": "0.0.1",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "clsx": "^2.1.1",
    "framer-motion": "^12.23.12",
    "lucide-react": "^0.542.0",
    "react": "^19.1.1",
    "react-dom": "^19.1.1",
    "react-router-dom": "^7.8.2",
    "recharts": "^3.2.1",
    "tailwind-merge": "^3.3.1"
  },
  "devDependencies": {
    "@types/react": "^19.1.10",
    "@types/react-dom": "^19.1.7",
    "@vitejs/plugin-react": "^5.0.0",
    "autoprefixer": "^10.4.20",
    "postcss": "^8.5.6",
    "tailwindcss": "^4.1.11",
    "typescript": "^5.9.2",
    "vite": "^7.1.3"
  }
}
```

---

## 2) `frontend/src/main.tsx`

```tsx
import React from "react";
import ReactDOM from "react-dom/client";
import { RouterProvider } from "react-router-dom";
import { router } from "./app/routes/router";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
```

---

## 3) `frontend/src/index.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  color-scheme: dark;
}

html,
body,
#root {
  min-height: 100%;
}

body {
  margin: 0;
  font-family:
    Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
    sans-serif;
  background:
    radial-gradient(circle at top, rgba(34, 211, 238, 0.08), transparent 24%),
    radial-gradient(circle at right, rgba(59, 130, 246, 0.08), transparent 20%),
    linear-gradient(180deg, #020617 0%, #05111d 45%, #06101a 100%);
  color: #e5eef8;
}

* {
  box-sizing: border-box;
}

::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

::-webkit-scrollbar-thumb {
  background: rgba(148, 163, 184, 0.28);
  border-radius: 999px;
}

@layer components {
  .surface-glass {
    @apply border border-white/10 bg-white/5 backdrop-blur-xl;
  }

  .surface-dark {
    @apply border border-cyan-300/10 bg-slate-950/45 backdrop-blur-xl;
  }

  .ring-water {
    box-shadow:
      inset 0 1px 0 rgba(255,255,255,0.06),
      0 10px 34px rgba(0,0,0,0.28),
      0 0 0 1px rgba(34,211,238,0.05);
  }

  .text-muted {
    @apply text-slate-400;
  }

  .tiny-label {
    @apply text-[11px] uppercase tracking-[0.18em] text-cyan-100/55;
  }

  .panel-title {
    @apply text-base font-semibold text-white;
  }

  .hover-lift {
    @apply transition-all duration-300 hover:-translate-y-1;
  }
}
```

---

## 4) `frontend/src/lib/utils.ts`

```ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatNumber(value?: number | null, compact = false) {
  if (value === undefined || value === null || Number.isNaN(value)) return "N/A";
  return new Intl.NumberFormat("en-IN", {
    notation: compact ? "compact" : "standard",
    maximumFractionDigits: compact ? 1 : 0,
  }).format(value);
}

export function formatPercent(value?: number | null) {
  if (value === undefined || value === null || Number.isNaN(value)) return "N/A";
  return `${Math.round(value)}%`;
}

export function formatDateTime(value?: string | null) {
  if (!value) return "Not available";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat("en-IN", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

export function titleCase(value?: string | null) {
  if (!value) return "N/A";
  return value
    .replace(/_/g, " ")
    .split(" ")
    .filter(Boolean)
    .map((part) => part[0].toUpperCase() + part.slice(1).toLowerCase())
    .join(" ");
}

export function clamp(value: number, min = 0, max = 100) {
  return Math.max(min, Math.min(max, value));
}

export function getRiskTone(risk?: string | null) {
  switch ((risk ?? "").toLowerCase()) {
    case "critical":
      return "critical";
    case "high":
      return "high";
    case "medium":
      return "medium";
    default:
      return "low";
  }
}
```

---

## 5) `frontend/src/types/api.ts`

```ts
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
```

---

## 6) `frontend/src/services/endpoints.ts`

```ts
export const endpoints = {
  dashboardSummary: "/api/dashboard/summary",
  dashboardHotspots: "/api/dashboard/hotspots",
  dashboardAlerts: "/api/dashboard/alerts",
  districts: "/api/districts",
  districtDetail: (districtId: string) => `/api/districts/${districtId}`,
  districtTrends: (districtId: string, days = 30) =>
    `/api/dashboard/trends/${districtId}?days=${days}`,
  monitoringStatus: "/api/monitoring/status",
  adminRunFullPipeline: "/api/admin/run-full-pipeline",
  adminTrainModels: "/api/admin/train-models",
  adminGeneratePredictions: "/api/admin/generate-predictions",
};
```

---

## 7) `frontend/src/services/api.ts`

```ts
const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
    },
    ...options,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`${response.status} ${response.statusText}: ${text}`);
  }

  if (response.status === 204) {
    return {} as T;
  }

  return response.json() as Promise<T>;
}

export function getJson<T>(path: string): Promise<T> {
  return request<T>(path, { method: "GET" });
}

export function postJson<T>(path: string, body?: unknown): Promise<T> {
  return request<T>(path, {
    method: "POST",
    body: body ? JSON.stringify(body) : undefined,
  });
}
```

---

## 8) `frontend/src/lib/mock.ts`

```ts
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
  },
  {
    districtId: "D004",
    districtName: "Tiruchirappalli",
    riskScore: 72,
    riskLevel: "high",
    confidence: 80,
    trend: "up",
    primaryReason: "Historical alert recurrence",
    activeAlert: true,
  },
];

export const mockAlerts: AlertItem[] = [
  {
    id: 1,
    districtId: "D001",
    districtName: "Chennai",
    riskLevel: "high",
    title: "Escalating district risk",
    message: "Hybrid score crossed high threshold with strong model agreement.",
    status: "active",
    createdAt: new Date().toISOString(),
    confidence: 88,
    reasonStack: ["Rainfall anomaly", "Sanitation weakness", "Alert history recurrence"],
  },
  {
    id: 2,
    districtId: "D002",
    districtName: "Madurai",
    riskLevel: "high",
    title: "Water quality warning",
    message: "Contamination and vulnerability combination remains elevated.",
    status: "active",
    createdAt: new Date(Date.now() - 1000 * 60 * 80).toISOString(),
    confidence: 82,
    reasonStack: ["Water quality pressure", "Population density", "Historical alerts"],
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
  {
    districtId: "D002",
    districtName: "Madurai",
    riskScore: 79,
    riskLevel: "high",
    confidence: 82,
    primaryReason: "Water quality stress",
  },
  {
    districtId: "D003",
    districtName: "Coimbatore",
    riskScore: 67,
    riskLevel: "medium",
    confidence: 77,
    primaryReason: "Vulnerability cluster",
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
  notes: [
    "Pipeline completed with partial enrichment gaps.",
    "Weather sync is recent.",
  ],
};

export const mockAdminResult: AdminActionResult = {
  success: true,
  message: "Triggered successfully",
  startedAt: new Date().toISOString(),
};
```

---

## 9) `frontend/src/services/dataSource.ts`

```ts
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
  Summary,
  TrendPoint,
} from "../types/api";

const USE_MOCK = import.meta.env.VITE_USE_MOCK === "true";

async function withFallback<T>(runner: () => Promise<T>, fallback: T): Promise<T> {
  if (USE_MOCK) return fallback;
  try {
    return await runner();
  } catch {
    return fallback;
  }
}

export const dataSource = {
  getSummary: () =>
    withFallback<Summary>(() => getJson<Summary>(endpoints.dashboardSummary), mockSummary),

  getHotspots: () =>
    withFallback<Hotspot[]>(() => getJson<Hotspot[]>(endpoints.dashboardHotspots), mockHotspots),

  getAlerts: () =>
    withFallback<AlertItem[]>(() => getJson<AlertItem[]>(endpoints.dashboardAlerts), mockAlerts),

  getDistricts: () =>
    withFallback<District[]>(() => getJson<District[]>(endpoints.districts), mockDistricts),

  getDistrictDetail: (districtId: string) =>
    withFallback<DistrictDetail>(
      () => getJson<DistrictDetail>(endpoints.districtDetail(districtId)),
      { ...mockDistrictDetail, districtId }
    ),

  getDistrictTrends: (districtId: string, days = 30) =>
    withFallback<TrendPoint[]>(
      () => getJson<TrendPoint[]>(endpoints.districtTrends(districtId, days)),
      mockTrends
    ),

  getMonitoringStatus: () =>
    withFallback<MonitoringStatus>(
      () => getJson<MonitoringStatus>(endpoints.monitoringStatus),
      mockMonitoringStatus
    ),

  runFullPipeline: () =>
    withFallback<AdminActionResult>(
      () => postJson<AdminActionResult>(endpoints.adminRunFullPipeline),
      mockAdminResult
    ),

  trainModels: () =>
    withFallback<AdminActionResult>(
      () => postJson<AdminActionResult>(endpoints.adminTrainModels),
      mockAdminResult
    ),

  generatePredictions: () =>
    withFallback<AdminActionResult>(
      () => postJson<AdminActionResult>(endpoints.adminGeneratePredictions),
      mockAdminResult
    ),
};
```

---

## 10) `frontend/src/hooks/useAsyncData.ts`

```ts
import { useCallback, useEffect, useState } from "react";

export function useAsyncData<T>(loader: () => Promise<T>, deps: unknown[] = []) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await loader();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }, deps);

  useEffect(() => {
    void load();
  }, [load]);

  return { data, loading, error, reload: load };
}
```

---

## 11) `frontend/src/components/background/WaterBackground.tsx`

```tsx
export function WaterBackground() {
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(34,211,238,0.08),transparent_30%),linear-gradient(180deg,#020617_0%,#071220_45%,#061019_100%)]" />

      <div className="absolute left-[-10%] top-[-14%] h-[420px] w-[420px] animate-pulse rounded-full bg-cyan-300/8 blur-3xl" />
      <div className="absolute bottom-[-12%] right-[-8%] h-[460px] w-[460px] animate-pulse rounded-full bg-blue-500/10 blur-3xl [animation-delay:900ms]" />
      <div className="absolute left-1/4 top-1/2 h-[280px] w-[280px] rounded-full bg-sky-300/5 blur-3xl" />

      <div className="absolute inset-x-0 top-[12%] h-px bg-gradient-to-r from-transparent via-cyan-200/10 to-transparent" />
      <div className="absolute inset-x-0 top-[34%] h-px bg-gradient-to-r from-transparent via-cyan-200/5 to-transparent" />
      <div className="absolute inset-x-0 top-[62%] h-px bg-gradient-to-r from-transparent via-cyan-200/6 to-transparent" />
    </div>
  );
}
```

---

## 12) `frontend/src/components/ui/GlassPanel.tsx`

```tsx
import type { ReactNode } from "react";
import { cn } from "../../lib/utils";

type Props = {
  title?: string;
  subtitle?: string;
  rightSlot?: ReactNode;
  className?: string;
  children: ReactNode;
};

export function GlassPanel({ title, subtitle, rightSlot, className, children }: Props) {
  return (
    <section
      className={cn(
        "group relative overflow-hidden rounded-3xl surface-dark ring-water hover-lift",
        className
      )}
    >
      <div className="pointer-events-none absolute inset-x-0 top-0 h-24 bg-gradient-to-b from-white/8 to-transparent" />
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(34,211,238,0.08),transparent_28%),radial-gradient(circle_at_bottom_left,rgba(59,130,246,0.07),transparent_30%)]" />

      <div className="relative z-10 p-5 md:p-6">
        {(title || subtitle || rightSlot) && (
          <div className="mb-4 flex items-start justify-between gap-4">
            <div>
              {title ? <h3 className="panel-title">{title}</h3> : null}
              {subtitle ? <p className="mt-1 text-sm text-cyan-50/65">{subtitle}</p> : null}
            </div>
            {rightSlot ? <div>{rightSlot}</div> : null}
          </div>
        )}

        {children}
      </div>
    </section>
  );
}
```

---

## 13) `frontend/src/components/ui/MetricCard.tsx`

```tsx
import { GlassPanel } from "./GlassPanel";

type Props = {
  label: string;
  value: string | number;
  hint?: string;
};

export function MetricCard({ label, value, hint }: Props) {
  return (
    <GlassPanel className="min-h-[140px]">
      <div className="flex h-full flex-col justify-between">
        <div className="tiny-label">{label}</div>
        <div className="mt-4 text-4xl font-bold tracking-tight text-white">{value}</div>
        {hint ? <div className="mt-4 text-sm text-cyan-50/65">{hint}</div> : null}
      </div>
    </GlassPanel>
  );
}
```

---

## 14) `frontend/src/components/ui/RiskBadge.tsx`

```tsx
import { cn } from "../../lib/utils";
import type { RiskLevel } from "../../types/api";

type Props = {
  level?: RiskLevel | string;
};

export function RiskBadge({ level = "low" }: Props) {
  const key = String(level).toLowerCase();

  const style =
    key === "critical"
      ? "border-red-400/30 bg-red-500/12 text-red-200"
      : key === "high"
        ? "border-orange-400/30 bg-orange-500/12 text-orange-200"
        : key === "medium"
          ? "border-amber-400/30 bg-amber-500/12 text-amber-200"
          : "border-emerald-400/30 bg-emerald-500/12 text-emerald-200";

  return <span className={cn("badge", style)}>{key.toUpperCase()}</span>;
}
```

---

## 15) `frontend/src/components/ui/LiquidProgressBar.tsx`

```tsx
import { clamp, cn } from "../../lib/utils";

type Props = {
  value?: number | null;
  label?: string;
  className?: string;
};

export function LiquidProgressBar({ value = 0, label, className }: Props) {
  const pct = clamp(value ?? 0);

  return (
    <div className={cn("space-y-2", className)}>
      {label ? <div className="flex items-center justify-between text-sm text-cyan-50/70"><span>{label}</span><span>{pct}%</span></div> : null}
      <div className="relative h-3 overflow-hidden rounded-full border border-cyan-300/10 bg-slate-900/70">
        <div
          className="absolute inset-y-0 left-0 rounded-full bg-[linear-gradient(90deg,rgba(34,211,238,0.85),rgba(59,130,246,0.85))] transition-all duration-500"
          style={{ width: `${pct}%` }}
        />
        <div className="absolute inset-0 opacity-50 [background-image:linear-gradient(135deg,transparent_25%,rgba(255,255,255,0.18)_25%,rgba(255,255,255,0.18)_50%,transparent_50%,transparent_75%,rgba(255,255,255,0.18)_75%)] [background-size:20px_20px]" />
      </div>
    </div>
  );
}
```

---

## 16) `frontend/src/components/ui/ConsensusMeter.tsx`

```tsx
import type { ModelScores } from "../../types/api";
import { formatNumber } from "../../lib/utils";

type Props = {
  scores?: ModelScores;
};

export function ConsensusMeter({ scores }: Props) {
  const values = [scores?.ruleBased, scores?.randomForest, scores?.xgboost].filter(
    (v): v is number => typeof v === "number"
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
```

---

## 17) `frontend/src/components/ui/HealthChip.tsx`

```tsx
import { cn, titleCase } from "../../lib/utils";

type Props = {
  state?: string;
};

export function HealthChip({ state = "unknown" }: Props) {
  const key = state.toLowerCase();
  const style =
    key === "healthy"
      ? "border-emerald-400/30 bg-emerald-500/12 text-emerald-200"
      : key === "degraded"
        ? "border-amber-400/30 bg-amber-500/12 text-amber-200"
        : key === "fallback"
          ? "border-sky-400/30 bg-sky-500/12 text-sky-200"
          : key === "error"
            ? "border-red-400/30 bg-red-500/12 text-red-200"
            : "border-slate-400/30 bg-slate-500/12 text-slate-200";

  return <span className={cn("badge", style)}>{titleCase(key)}</span>;
}
```

---

## 18) `frontend/src/components/ui/SearchBar.tsx`

```tsx
import { Search } from "lucide-react";

type Props = {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
};

export function SearchBar({ value, onChange, placeholder = "Search" }: Props) {
  return (
    <div className="relative">
      <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
      <input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="h-11 w-full rounded-2xl border border-white/10 bg-slate-950/50 pl-10 pr-4 text-sm text-white outline-none ring-0 placeholder:text-slate-500 focus:border-cyan-300/20"
      />
    </div>
  );
}
```

---

## 19) `frontend/src/components/common/PageHeader.tsx`

```tsx
import type { ReactNode } from "react";

type Props = {
  title: string;
  subtitle?: string;
  rightSlot?: ReactNode;
};

export function PageHeader({ title, subtitle, rightSlot }: Props) {
  return (
    <div className="mb-6 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
      <div>
        <div className="tiny-label">AI-Based Early Warning System</div>
        <h1 className="mt-2 text-3xl font-bold tracking-tight text-white md:text-4xl">{title}</h1>
        {subtitle ? <p className="mt-2 max-w-3xl text-sm leading-6 text-cyan-50/65">{subtitle}</p> : null}
      </div>
      {rightSlot ? <div>{rightSlot}</div> : null}
    </div>
  );
}
```

---

## 20) `frontend/src/components/common/LoadingPanel.tsx`

```tsx
export function LoadingPanel() {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-6 backdrop-blur-xl">
      <div className="animate-pulse space-y-4">
        <div className="h-6 w-40 rounded bg-white/10" />
        <div className="h-24 rounded-2xl bg-white/10" />
        <div className="h-24 rounded-2xl bg-white/10" />
      </div>
    </div>
  );
}
```

---

## 21) `frontend/src/components/common/EmptyState.tsx`

```tsx
import type { ReactNode } from "react";

type Props = {
  title: string;
  description?: string;
  action?: ReactNode;
};

export function EmptyState({ title, description, action }: Props) {
  return (
    <div className="rounded-3xl border border-dashed border-cyan-300/15 bg-slate-950/35 p-8 text-center">
      <h3 className="text-lg font-semibold text-white">{title}</h3>
      {description ? <p className="mx-auto mt-2 max-w-lg text-sm text-cyan-50/60">{description}</p> : null}
      {action ? <div className="mt-4">{action}</div> : null}
    </div>
  );
}
```

---

## 22) `frontend/src/components/common/ErrorState.tsx`

```tsx
type Props = {
  message: string;
  onRetry?: () => void;
};

export function ErrorState({ message, onRetry }: Props) {
  return (
    <div className="rounded-3xl border border-red-400/15 bg-red-500/6 p-6">
      <h3 className="text-lg font-semibold text-red-100">Could not load data</h3>
      <p className="mt-2 text-sm text-red-100/70">{message}</p>
      {onRetry ? (
        <button
          onClick={onRetry}
          className="mt-4 rounded-2xl border border-red-300/20 bg-white/5 px-4 py-2 text-sm text-white"
        >
          Retry
        </button>
      ) : null}
    </div>
  );
}
```

---

## 23) `frontend/src/components/dashboard/MonitoringRibbon.tsx`

```tsx
import type { MonitoringStatus } from "../../types/api";
import { HealthChip } from "../ui/HealthChip";
import { formatDateTime } from "../../lib/utils";

type Props = {
  monitoring?: MonitoringStatus | null;
};

export function MonitoringRibbon({ monitoring }: Props) {
  return (
    <div className="mb-6 grid gap-3 rounded-3xl border border-cyan-300/10 bg-slate-950/35 p-4 backdrop-blur-xl md:grid-cols-5">
      <div>
        <div className="tiny-label">Backend</div>
        <div className="mt-2"><HealthChip state={String(monitoring?.backendStatus ?? "unknown")} /></div>
      </div>
      <div>
        <div className="tiny-label">Database</div>
        <div className="mt-2"><HealthChip state={String(monitoring?.databaseStatus ?? "unknown")} /></div>
      </div>
      <div>
        <div className="tiny-label">Weather Sync</div>
        <div className="mt-2"><HealthChip state={String(monitoring?.weatherStatus ?? "unknown")} /></div>
      </div>
      <div>
        <div className="tiny-label">Models</div>
        <div className="mt-2"><HealthChip state={String(monitoring?.modelStatus ?? "unknown")} /></div>
      </div>
      <div>
        <div className="tiny-label">Last Pipeline Run</div>
        <div className="mt-2 text-sm text-cyan-50/75">{formatDateTime(monitoring?.lastPipelineRun)}</div>
      </div>
    </div>
  );
}
```

---

## 24) `frontend/src/components/dashboard/CriticalDistrictHero.tsx`

```tsx
import { AlertTriangle, ArrowUpRight, Droplets } from "lucide-react";
import type { Summary } from "../../types/api";
import { GlassPanel } from "../ui/GlassPanel";
import { LiquidProgressBar } from "../ui/LiquidProgressBar";
import { RiskBadge } from "../ui/RiskBadge";
import { formatNumber, formatPercent } from "../../lib/utils";

type Props = {
  summary?: Summary | null;
};

export function CriticalDistrictHero({ summary }: Props) {
  const district = summary?.mostCriticalDistrict;

  return (
    <GlassPanel
      title="Most Critical District"
      subtitle="Immediate focus point for district-level intervention"
      rightSlot={district ? <RiskBadge level={district.riskLevel} /> : null}
      className="min-h-[260px]"
    >
      {district ? (
        <div className="grid gap-6 lg:grid-cols-[1.25fr_0.75fr]">
          <div>
            <div className="flex items-start justify-between gap-4">
              <div>
                <div className="text-3xl font-bold text-white md:text-4xl">{district.districtName}</div>
                <p className="mt-3 max-w-2xl text-sm leading-6 text-cyan-50/70">
                  {district.primaryReason ??
                    "Risk remains elevated due to a combination of environmental and vulnerability signals."}
                </p>
              </div>
              <ArrowUpRight className="mt-1 h-5 w-5 text-cyan-200/70" />
            </div>

            <div className="mt-6 grid gap-3 sm:grid-cols-3">
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="tiny-label">Risk Score</div>
                <div className="mt-2 text-3xl font-semibold text-white">{formatNumber(district.riskScore)}</div>
              </div>
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="tiny-label">Confidence</div>
                <div className="mt-2 text-3xl font-semibold text-white">{formatPercent(district.confidence)}</div>
              </div>
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="tiny-label">Trend</div>
                <div className="mt-2 text-2xl font-semibold text-white">{String(district.trend ?? "stable").toUpperCase()}</div>
              </div>
            </div>
          </div>

          <div className="rounded-3xl border border-cyan-300/12 bg-slate-950/35 p-5">
            <div className="flex items-center gap-2 text-cyan-100/80">
              <Droplets className="h-4 w-4" />
              <span className="text-sm font-medium">Immediate Response Playbook</span>
            </div>
            <ul className="mt-4 space-y-3 text-sm text-cyan-50/72">
              <li className="flex gap-2"><AlertTriangle className="mt-0.5 h-4 w-4 text-orange-300" />Increase water quality testing in vulnerable blocks.</li>
              <li className="flex gap-2"><AlertTriangle className="mt-0.5 h-4 w-4 text-orange-300" />Run sanitation inspection where risk remains clustered.</li>
              <li className="flex gap-2"><AlertTriangle className="mt-0.5 h-4 w-4 text-orange-300" />Monitor rainfall and contamination signals for the next 48 hours.</li>
            </ul>
            <div className="mt-6">
              <LiquidProgressBar value={district.confidence ?? 0} label="Decision Confidence" />
            </div>
          </div>
        </div>
      ) : (
        <p className="text-sm text-cyan-50/65">No critical district data available.</p>
      )}
    </GlassPanel>
  );
}
```

---

## 25) `frontend/src/components/dashboard/LiveDeltaPanel.tsx`

```tsx
import { ArrowDownRight, ArrowUpRight, Minus } from "lucide-react";
import { GlassPanel } from "../ui/GlassPanel";

type DeltaItem = {
  label: string;
  value: string;
  direction: "up" | "down" | "flat";
};

const items: DeltaItem[] = [
  { label: "Districts moved to high risk", value: "+3", direction: "up" },
  { label: "Alerts triggered in last cycle", value: "+2", direction: "up" },
  { label: "Average confidence change", value: "+4%", direction: "up" },
  { label: "Districts with stale data", value: "-1", direction: "down" },
];

export function LiveDeltaPanel() {
  return (
    <GlassPanel title="What Changed Now" subtitle="Quick operational deltas since the last cycle">
      <div className="space-y-3">
        {items.map((item) => (
          <div key={item.label} className="flex items-center justify-between rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
            <div className="text-sm text-cyan-50/75">{item.label}</div>
            <div className="flex items-center gap-2 text-sm font-medium text-white">
              {item.direction === "up" ? (
                <ArrowUpRight className="h-4 w-4 text-cyan-300" />
              ) : item.direction === "down" ? (
                <ArrowDownRight className="h-4 w-4 text-emerald-300" />
              ) : (
                <Minus className="h-4 w-4 text-slate-300" />
              )}
              {item.value}
            </div>
          </div>
        ))}
      </div>
    </GlassPanel>
  );
}
```

---

## 26) `frontend/src/components/dashboard/HotspotQueue.tsx`

```tsx
import { Link } from "react-router-dom";
import type { Hotspot } from "../../types/api";
import { GlassPanel } from "../ui/GlassPanel";
import { RiskBadge } from "../ui/RiskBadge";
import { formatPercent } from "../../lib/utils";

type Props = {
  hotspots: Hotspot[];
  onQuickView?: (districtId: string) => void;
};

export function HotspotQueue({ hotspots, onQuickView }: Props) {
  return (
    <GlassPanel title="Priority District Queue" subtitle="Ranked by risk severity and operational importance">
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead>
            <tr className="border-b border-white/10 text-cyan-100/55">
              <th className="pb-3 pr-4">Rank</th>
              <th className="pb-3 pr-4">District</th>
              <th className="pb-3 pr-4">Risk</th>
              <th className="pb-3 pr-4">Confidence</th>
              <th className="pb-3 pr-4">Main Trigger</th>
              <th className="pb-3 pr-4">Action</th>
            </tr>
          </thead>
          <tbody>
            {hotspots.map((item, index) => (
              <tr key={item.districtId} className="border-b border-white/5 last:border-0">
                <td className="py-4 pr-4 text-cyan-50/70">#{index + 1}</td>
                <td className="py-4 pr-4 font-medium text-white">{item.districtName}</td>
                <td className="py-4 pr-4"><RiskBadge level={item.riskLevel} /></td>
                <td className="py-4 pr-4 text-cyan-50/75">{formatPercent(item.confidence)}</td>
                <td className="py-4 pr-4 text-cyan-50/65">{item.primaryReason ?? "Signal pressure"}</td>
                <td className="py-4 pr-4">
                  <div className="flex gap-2">
                    <button
                      onClick={() => onQuickView?.(item.districtId)}
                      className="rounded-xl border border-cyan-300/15 bg-white/5 px-3 py-2 text-xs text-white"
                    >
                      Quick View
                    </button>
                    <Link
                      to={`/district/${item.districtId}`}
                      className="rounded-xl border border-cyan-300/15 bg-cyan-400/10 px-3 py-2 text-xs text-cyan-100"
                    >
                      Open
                    </Link>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </GlassPanel>
  );
}
```

---

## 27) `frontend/src/components/dashboard/AlertFeed.tsx`

```tsx
import { Link } from "react-router-dom";
import type { AlertItem } from "../../types/api";
import { GlassPanel } from "../ui/GlassPanel";
import { RiskBadge } from "../ui/RiskBadge";
import { formatDateTime } from "../../lib/utils";

type Props = {
  alerts: AlertItem[];
};

export function AlertFeed({ alerts }: Props) {
  return (
    <GlassPanel title="Recent Alerts" subtitle="Latest district-level warning events">
      <div className="space-y-3">
        {alerts.map((alert) => (
          <div key={alert.id} className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <div className="flex items-start justify-between gap-4">
              <div>
                <div className="flex items-center gap-2">
                  <h4 className="font-medium text-white">{alert.title ?? "District Risk Alert"}</h4>
                  <RiskBadge level={alert.riskLevel} />
                </div>
                <p className="mt-2 text-sm text-cyan-50/70">{alert.message ?? "Warning generated by the hybrid risk engine."}</p>
                <div className="mt-2 text-xs text-cyan-100/50">{alert.districtName} • {formatDateTime(alert.createdAt)}</div>
              </div>
              <Link to={`/district/${alert.districtId}`} className="rounded-xl border border-cyan-300/15 px-3 py-2 text-xs text-cyan-100">
                View District
              </Link>
            </div>
          </div>
        ))}
      </div>
    </GlassPanel>
  );
}
```

---

## 28) `frontend/src/components/dashboard/DataReliabilityCard.tsx`

```tsx
import type { DistrictDetail } from "../../types/api";
import { GlassPanel } from "../ui/GlassPanel";
import { LiquidProgressBar } from "../ui/LiquidProgressBar";

type Props = {
  detail?: DistrictDetail | null;
};

export function DataReliabilityCard({ detail }: Props) {
  return (
    <GlassPanel title="Data Reliability" subtitle="Trust visibility for the current district view">
      <div className="space-y-4">
        <LiquidProgressBar value={detail?.dataReliability?.completeness ?? 0} label="Completeness" />
        <LiquidProgressBar value={detail?.dataReliability?.freshness ?? 0} label="Freshness" />
        <div className="grid gap-3 sm:grid-cols-2">
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <div className="tiny-label">Missing Fields</div>
            <div className="mt-2 text-2xl font-semibold text-white">{detail?.dataReliability?.missingFields ?? "N/A"}</div>
          </div>
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <div className="tiny-label">Fallback Logic</div>
            <div className="mt-2 text-2xl font-semibold text-white">{detail?.dataReliability?.fallbackUsed ? "Used" : "Not Used"}</div>
          </div>
        </div>
      </div>
    </GlassPanel>
  );
}
```

---

## 29) `frontend/src/components/dashboard/QuickInsightRail.tsx`

```tsx
import type { DistrictDetail } from "../../types/api";
import { GlassPanel } from "../ui/GlassPanel";
import { ConsensusMeter } from "../ui/ConsensusMeter";
import { DataReliabilityCard } from "./DataReliabilityCard";

type Props = {
  detail?: DistrictDetail | null;
};

export function QuickInsightRail({ detail }: Props) {
  return (
    <div className="space-y-6">
      <GlassPanel title="Decision Summary" subtitle="Why the system is leaning this way">
        <ul className="space-y-3 text-sm text-cyan-50/72">
          {(detail?.explainabilityReasons ?? ["Explanation will appear here once district detail loads."]).map((reason) => (
            <li key={reason} className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
              {reason}
            </li>
          ))}
        </ul>
      </GlassPanel>

      <GlassPanel title="Model Agreement" subtitle="Compare all core intelligence layers">
        <ConsensusMeter scores={detail?.modelScores} />
      </GlassPanel>

      <DataReliabilityCard detail={detail} />
    </div>
  );
}
```

---

## 30) `frontend/src/components/dashboard/ActionPlaybook.tsx`

```tsx
import type { DistrictDetail } from "../../types/api";
import { GlassPanel } from "../ui/GlassPanel";

type Props = {
  detail?: DistrictDetail | null;
};

function Block({ title, items }: { title: string; items?: string[] }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
      <div className="tiny-label">{title}</div>
      <ul className="mt-3 space-y-2 text-sm text-cyan-50/72">
        {(items?.length ? items : ["No guidance available yet."]).map((item) => (
          <li key={item}>• {item}</li>
        ))}
      </ul>
    </div>
  );
}

export function ActionPlaybook({ detail }: Props) {
  return (
    <GlassPanel title="Recommended Actions" subtitle="Bridge prediction into district-level response planning">
      <div className="grid gap-4 xl:grid-cols-3">
        <Block title="Immediate" items={detail?.recommendedActions?.immediate} />
        <Block title="Preventive" items={detail?.recommendedActions?.preventive} />
        <Block title="Monitoring" items={detail?.recommendedActions?.monitoring} />
      </div>
    </GlassPanel>
  );
}
```

---

## 31) `frontend/src/components/districts/ExecutiveSummaryCard.tsx`

```tsx
import type { DistrictDetail } from "../../types/api";
import { GlassPanel } from "../ui/GlassPanel";
import { RiskBadge } from "../ui/RiskBadge";
import { formatPercent } from "../../lib/utils";

type Props = {
  detail?: DistrictDetail | null;
};

export function ExecutiveSummaryCard({ detail }: Props) {
  return (
    <GlassPanel
      title="Executive Summary"
      subtitle="Auto-generated district intelligence summary"
      rightSlot={<RiskBadge level={detail?.riskLevel} />}
    >
      <p className="text-sm leading-7 text-cyan-50/72">
        {detail
          ? `${detail.districtName} is currently ${detail.riskLevel.toUpperCase()} risk with ${formatPercent(detail.confidence)} confidence. The strongest drivers are ${(detail.explainabilityReasons ?? []).slice(0, 2).join(" and ") || "multi-signal environmental and vulnerability pressure"}.`
          : "District summary will appear here."}
      </p>
    </GlassPanel>
  );
}
```

---

## 32) `frontend/src/components/districts/SignalBreakdownPanel.tsx`

```tsx
import type { DistrictDetail } from "../../types/api";
import { GlassPanel } from "../ui/GlassPanel";
import { LiquidProgressBar } from "../ui/LiquidProgressBar";

type Props = {
  detail?: DistrictDetail | null;
};

export function SignalBreakdownPanel({ detail }: Props) {
  const signals = detail?.signalBreakdown;

  return (
    <GlassPanel title="Signal Breakdown" subtitle="Environmental, infrastructure, and historical drivers">
      <div className="space-y-4">
        <LiquidProgressBar value={signals?.weather ?? 0} label="Weather Pressure" />
        <LiquidProgressBar value={signals?.waterQuality ?? 0} label="Water Quality Stress" />
        <LiquidProgressBar value={signals?.sanitation ?? 0} label="Sanitation Weakness" />
        <LiquidProgressBar value={signals?.vulnerability ?? 0} label="Vulnerability" />
        <LiquidProgressBar value={signals?.historicalAlerts ?? 0} label="Historical Alert Similarity" />
      </div>
    </GlassPanel>
  );
}
```

---

## 33) `frontend/src/components/districts/DistrictQuickDrawer.tsx`

```tsx
import { X } from "lucide-react";
import type { DistrictDetail } from "../../types/api";
import { RiskBadge } from "../ui/RiskBadge";
import { formatPercent } from "../../lib/utils";

type Props = {
  open: boolean;
  onClose: () => void;
  detail?: DistrictDetail | null;
};

export function DistrictQuickDrawer({ open, onClose, detail }: Props) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-slate-950/55 backdrop-blur-sm">
      <div className="h-full w-full max-w-lg border-l border-white/10 bg-[#06111c]/95 p-6 shadow-2xl">
        <div className="mb-5 flex items-start justify-between gap-4">
          <div>
            <div className="tiny-label">District Quick View</div>
            <h3 className="mt-2 text-2xl font-bold text-white">{detail?.districtName ?? "District"}</h3>
          </div>
          <button onClick={onClose} className="rounded-xl border border-white/10 p-2 text-slate-300">
            <X className="h-4 w-4" />
          </button>
        </div>

        <div className="space-y-4">
          <div className="flex items-center gap-3">
            <RiskBadge level={detail?.riskLevel} />
            <div className="text-sm text-cyan-50/70">Confidence: {formatPercent(detail?.confidence)}</div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <div className="tiny-label">Top Drivers</div>
            <ul className="mt-3 space-y-2 text-sm text-cyan-50/72">
              {(detail?.explainabilityReasons ?? []).slice(0, 3).map((reason) => (
                <li key={reason}>• {reason}</li>
              ))}
            </ul>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <div className="tiny-label">Immediate Action</div>
            <ul className="mt-3 space-y-2 text-sm text-cyan-50/72">
              {(detail?.recommendedActions?.immediate ?? []).slice(0, 3).map((item) => (
                <li key={item}>• {item}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
```

---

## 34) `frontend/src/components/districts/DistrictCompareTable.tsx`

```tsx
import type { District[] } from "../../types/api";
import { GlassPanel } from "../ui/GlassPanel";
import { RiskBadge } from "../ui/RiskBadge";
import { formatPercent } from "../../lib/utils";

type Props = {
  districts: District[];
};

export function DistrictCompareTable({ districts }: Props) {
  return (
    <GlassPanel title="District Comparison" subtitle="Quick side-by-side operational overview">
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead>
            <tr className="border-b border-white/10 text-cyan-100/55">
              <th className="pb-3 pr-4">District</th>
              <th className="pb-3 pr-4">Risk</th>
              <th className="pb-3 pr-4">Confidence</th>
              <th className="pb-3 pr-4">Primary Reason</th>
            </tr>
          </thead>
          <tbody>
            {districts.map((item) => (
              <tr key={item.districtId} className="border-b border-white/5 last:border-0">
                <td className="py-4 pr-4 font-medium text-white">{item.districtName}</td>
                <td className="py-4 pr-4"><RiskBadge level={item.riskLevel} /></td>
                <td className="py-4 pr-4 text-cyan-50/72">{formatPercent(item.confidence)}</td>
                <td className="py-4 pr-4 text-cyan-50/65">{item.primaryReason ?? "Signal pressure"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </GlassPanel>
  );
}
```

---

## 35) `frontend/src/components/alerts/AlertInvestigationCard.tsx`

```tsx
import type { AlertItem } from "../../types/api";
import { GlassPanel } from "../ui/GlassPanel";
import { RiskBadge } from "../ui/RiskBadge";
import { formatDateTime, formatPercent } from "../../lib/utils";

type Props = {
  alert?: AlertItem | null;
};

export function AlertInvestigationCard({ alert }: Props) {
  return (
    <GlassPanel
      title="Alert Investigation"
      subtitle="Evidence, timing, and recommended interpretation"
      rightSlot={<RiskBadge level={alert?.riskLevel} />}
    >
      {alert ? (
        <div className="space-y-4">
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <div className="tiny-label">District</div>
            <div className="mt-2 text-xl font-semibold text-white">{alert.districtName}</div>
            <div className="mt-2 text-sm text-cyan-50/65">Created {formatDateTime(alert.createdAt)}</div>
            <div className="mt-2 text-sm text-cyan-50/65">Confidence {formatPercent(alert.confidence)}</div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <div className="tiny-label">Reason Stack</div>
            <ul className="mt-3 space-y-2 text-sm text-cyan-50/72">
              {(alert.reasonStack ?? []).map((reason) => (
                <li key={reason}>• {reason}</li>
              ))}
            </ul>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/5 p-4 text-sm text-cyan-50/72">
            {alert.message ?? "Alert explanation is not available yet."}
          </div>
        </div>
      ) : (
        <p className="text-sm text-cyan-50/65">Select an alert to inspect it.</p>
      )}
    </GlassPanel>
  );
}
```

---

## 36) `frontend/src/components/monitoring/MonitoringHealthGrid.tsx`

```tsx
import type { MonitoringStatus } from "../../types/api";
import { GlassPanel } from "../ui/GlassPanel";
import { HealthChip } from "../ui/HealthChip";
import { formatDateTime } from "../../lib/utils";

type Props = {
  status?: MonitoringStatus | null;
};

function Item({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
      <div className="tiny-label">{label}</div>
      <div className="mt-2 text-xl font-semibold text-white">{value}</div>
    </div>
  );
}

export function MonitoringHealthGrid({ status }: Props) {
  return (
    <GlassPanel title="System Monitoring" subtitle="Pipeline health, freshness, and platform trust layer">
      <div className="grid gap-4 xl:grid-cols-2">
        <div className="grid gap-4 sm:grid-cols-2">
          <Item label="Backend" value={String(status?.backendStatus ?? "unknown")} />
          <Item label="Database" value={String(status?.databaseStatus ?? "unknown")} />
          <Item label="Weather Sync" value={String(status?.weatherStatus ?? "unknown")} />
          <Item label="Models" value={String(status?.modelStatus ?? "unknown")} />
          <Item label="Stale Districts" value={status?.staleDistrictCount ?? "N/A"} />
          <Item label="Missing Enrichment" value={status?.missingEnrichmentCount ?? "N/A"} />
        </div>

        <div className="space-y-4">
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <div className="tiny-label">Pipeline State</div>
            <div className="mt-2"><HealthChip state={String(status?.pipelineStatus ?? "unknown")} /></div>
            <div className="mt-3 text-sm text-cyan-50/65">Last pipeline run: {formatDateTime(status?.lastPipelineRun)}</div>
            <div className="mt-2 text-sm text-cyan-50/65">Last weather sync: {formatDateTime(status?.lastWeatherSync)}</div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <div className="tiny-label">Monitoring Notes</div>
            <ul className="mt-3 space-y-2 text-sm text-cyan-50/72">
              {(status?.notes?.length ? status.notes : ["No monitoring notes available."]).map((note) => (
                <li key={note}>• {note}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </GlassPanel>
  );
}
```

---

## 37) `frontend/src/components/ai/AIWorkflowDiagram.tsx`

```tsx
import { Database, Droplets, Radar, ShieldAlert, Sparkles } from "lucide-react";
import { GlassPanel } from "../ui/GlassPanel";

const steps = [
  {
    icon: Database,
    title: "Data Sources",
    desc: "District master, profiles, observations, historical alerts, enrichment layers, and weather inputs.",
  },
  {
    icon: Droplets,
    title: "Cleaning + Aggregation",
    desc: "Normalize district IDs, aggregate lower-level observations to district-day, tolerate missing enrichment.",
  },
  {
    icon: Radar,
    title: "Feature Engineering",
    desc: "Build rainfall pressure, sanitation weakness, water stress, vulnerability, and historical alert signals.",
  },
  {
    icon: Sparkles,
    title: "Models",
    desc: "Rule engine for trust, Random Forest for tabular patterns, XGBoost for stronger predictive accuracy.",
  },
  {
    icon: ShieldAlert,
    title: "Hybrid Warning Output",
    desc: "Produce risk score, confidence, top reasons, and recommended actions for officials.",
  },
];

export function AIWorkflowDiagram() {
  return (
    <GlassPanel title="AI Workflow" subtitle="How the system transforms water and public-health signals into actionable warnings">
      <div className="grid gap-4 xl:grid-cols-5">
        {steps.map((step, index) => {
          const Icon = step.icon;
          return (
            <div key={step.title} className="relative rounded-3xl border border-white/10 bg-white/5 p-5">
              <div className="mb-4 inline-flex rounded-2xl border border-cyan-300/15 bg-cyan-400/10 p-3 text-cyan-100">
                <Icon className="h-5 w-5" />
              </div>
              <div className="tiny-label">Step {index + 1}</div>
              <div className="mt-2 text-lg font-semibold text-white">{step.title}</div>
              <p className="mt-3 text-sm leading-6 text-cyan-50/68">{step.desc}</p>
            </div>
          );
        })}
      </div>
    </GlassPanel>
  );
}
```

---

## 38) `frontend/src/components/admin/AdminActionPanel.tsx`

```tsx
import { useState } from "react";
import { Play, RefreshCw, Sparkles } from "lucide-react";
import { GlassPanel } from "../ui/GlassPanel";
import { dataSource } from "../../services/dataSource";

type ActionState = {
  loading: boolean;
  message: string | null;
};

export function AdminActionPanel() {
  const [state, setState] = useState<ActionState>({ loading: false, message: null });

  async function run(action: () => Promise<{ message: string }>) {
    setState({ loading: true, message: null });
    try {
      const result = await action();
      setState({ loading: false, message: result.message });
    } catch (error) {
      setState({ loading: false, message: error instanceof Error ? error.message : "Action failed" });
    }
  }

  return (
    <GlassPanel title="Admin Control" subtitle="Manual control points for pipeline, training, and prediction generation">
      <div className="grid gap-4 md:grid-cols-3">
        <button
          disabled={state.loading}
          onClick={() => void run(() => dataSource.runFullPipeline())}
          className="flex items-center justify-center gap-2 rounded-2xl border border-cyan-300/15 bg-cyan-400/10 px-4 py-4 text-sm font-medium text-white disabled:opacity-60"
        >
          <Play className="h-4 w-4" /> Run Full Pipeline
        </button>

        <button
          disabled={state.loading}
          onClick={() => void run(() => dataSource.trainModels())}
          className="flex items-center justify-center gap-2 rounded-2xl border border-cyan-300/15 bg-white/5 px-4 py-4 text-sm font-medium text-white disabled:opacity-60"
        >
          <RefreshCw className="h-4 w-4" /> Train Models
        </button>

        <button
          disabled={state.loading}
          onClick={() => void run(() => dataSource.generatePredictions())}
          className="flex items-center justify-center gap-2 rounded-2xl border border-cyan-300/15 bg-white/5 px-4 py-4 text-sm font-medium text-white disabled:opacity-60"
        >
          <Sparkles className="h-4 w-4" /> Generate Predictions
        </button>
      </div>

      {state.message ? (
        <div className="mt-4 rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-cyan-50/72">{state.message}</div>
      ) : null}
    </GlassPanel>
  );
}
```

---

## 39) `frontend/src/components/charts/RiskTrendChart.tsx`

```tsx
import type { TrendPoint } from "../../types/api";
import { GlassPanel } from "../ui/GlassPanel";
import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { formatDateTime } from "../../lib/utils";

type Props = {
  data: TrendPoint[];
  title?: string;
  subtitle?: string;
};

export function RiskTrendChart({ data, title = "Risk Trend", subtitle = "District risk evolution over time" }: Props) {
  const chartData = data.map((item) => ({
    ...item,
    shortDate: new Date(item.date).toLocaleDateString("en-IN", { day: "2-digit", month: "short" }),
  }));

  return (
    <GlassPanel title={title} subtitle={subtitle}>
      <div className="h-[320px] rounded-2xl border border-white/10 bg-slate-950/30 p-4">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="riskFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="rgba(34,211,238,0.85)" />
                <stop offset="100%" stopColor="rgba(34,211,238,0.02)" />
              </linearGradient>
            </defs>
            <CartesianGrid stroke="rgba(255,255,255,0.06)" vertical={false} />
            <XAxis dataKey="shortDate" stroke="rgba(255,255,255,0.45)" tickLine={false} axisLine={false} />
            <YAxis stroke="rgba(255,255,255,0.45)" tickLine={false} axisLine={false} />
            <Tooltip
              contentStyle={{
                background: "rgba(2,6,23,0.95)",
                border: "1px solid rgba(148,163,184,0.18)",
                borderRadius: 16,
              }}
              formatter={(value: number) => [value, "Risk Score"]}
              labelFormatter={(label, payload) =>
                payload?.[0]?.payload?.date ? formatDateTime(payload[0].payload.date) : label
              }
            />
            <Area type="monotone" dataKey="riskScore" stroke="rgba(34,211,238,1)" strokeWidth={3} fill="url(#riskFill)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </GlassPanel>
  );
}
```

---

## 40) `frontend/src/components/charts/RiskDriverBarChart.tsx`

```tsx
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { GlassPanel } from "../ui/GlassPanel";

type Props = {
  data: Array<{ name: string; value: number }>;
};

export function RiskDriverBarChart({ data }: Props) {
  return (
    <GlassPanel title="Risk Driver Leaderboard" subtitle="Most common contributors in the current intelligence layer">
      <div className="h-[320px] rounded-2xl border border-white/10 bg-slate-950/30 p-4">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <CartesianGrid stroke="rgba(255,255,255,0.06)" vertical={false} />
            <XAxis dataKey="name" stroke="rgba(255,255,255,0.45)" tickLine={false} axisLine={false} />
            <YAxis stroke="rgba(255,255,255,0.45)" tickLine={false} axisLine={false} />
            <Tooltip
              contentStyle={{
                background: "rgba(2,6,23,0.95)",
                border: "1px solid rgba(148,163,184,0.18)",
                borderRadius: 16,
              }}
            />
            <Bar dataKey="value" radius={[12, 12, 0, 0]} fill="rgba(34,211,238,0.85)" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </GlassPanel>
  );
}
```

---

## 41) `frontend/src/app/layout/AppShell.tsx`

```tsx
import { NavLink, Outlet } from "react-router-dom";
import {
  Activity,
  Bell,
  Gauge,
  LayoutDashboard,
  Settings2,
  ShieldAlert,
  Sparkles,
  Waves,
} from "lucide-react";
import { WaterBackground } from "../../components/background/WaterBackground";
import { cn } from "../../lib/utils";

const navItems = [
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/districts", label: "District Intelligence", icon: Waves },
  { to: "/alerts", label: "Alert Center", icon: ShieldAlert },
  { to: "/analytics", label: "Risk Analytics", icon: Gauge },
  { to: "/ai-engine", label: "AI Engine", icon: Sparkles },
  { to: "/monitoring", label: "Monitoring", icon: Activity },
  { to: "/admin", label: "Admin Control", icon: Settings2 },
];

export function AppShell() {
  return (
    <div className="relative min-h-screen overflow-hidden">
      <WaterBackground />

      <div className="relative z-10 grid min-h-screen grid-cols-1 xl:grid-cols-[280px_1fr]">
        <aside className="border-r border-white/8 bg-slate-950/45 p-5 backdrop-blur-xl">
          <div className="rounded-3xl border border-cyan-300/10 bg-white/5 p-5">
            <div className="tiny-label">Project</div>
            <div className="mt-2 text-xl font-bold text-white">AI Early Warning</div>
            <p className="mt-2 text-sm leading-6 text-cyan-50/65">
              District-level public-health and water-borne risk intelligence command center.
            </p>
          </div>

          <nav className="mt-6 space-y-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    cn(
                      "flex items-center gap-3 rounded-2xl border px-4 py-3 text-sm transition-all",
                      isActive
                        ? "border-cyan-300/15 bg-cyan-400/10 text-white"
                        : "border-transparent bg-transparent text-slate-300 hover:border-white/8 hover:bg-white/5"
                    )
                  }
                >
                  <Icon className="h-4 w-4" />
                  {item.label}
                </NavLink>
              );
            })}
          </nav>
        </aside>

        <div className="flex min-h-screen flex-col">
          <header className="sticky top-0 z-20 border-b border-white/8 bg-slate-950/45 px-6 py-4 backdrop-blur-xl">
            <div className="flex items-center justify-between gap-4">
              <div>
                <div className="tiny-label">Water + Public Health Intelligence</div>
                <div className="mt-1 text-lg font-semibold text-white">District Risk Command Center</div>
              </div>
              <div className="flex items-center gap-3">
                <div className="hidden rounded-2xl border border-cyan-300/12 bg-white/5 px-4 py-2 text-sm text-cyan-50/70 md:block">
                  Mode: Water-Oriented Monitoring UI
                </div>
                <button className="rounded-2xl border border-white/10 bg-white/5 p-3 text-slate-300">
                  <Bell className="h-4 w-4" />
                </button>
              </div>
            </div>
          </header>

          <main className="flex-1 p-6 xl:p-8">
            <Outlet />
          </main>
        </div>
      </div>
    </div>
  );
}
```

---

## 42) `frontend/src/app/routes/router.tsx`

```tsx
import { createBrowserRouter, Navigate } from "react-router-dom";
import { AppShell } from "../layout/AppShell";
import { DashboardPage } from "../../pages/DashboardPage";
import { DistrictsPage } from "../../pages/DistrictsPage";
import { DistrictDetailPage } from "../../pages/DistrictDetailPage";
import { AlertsPage } from "../../pages/AlertsPage";
import { AnalyticsPage } from "../../pages/AnalyticsPage";
import { AIEnginePage } from "../../pages/AIEnginePage";
import { MonitoringPage } from "../../pages/MonitoringPage";
import { AdminPage } from "../../pages/AdminPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AppShell />,
    children: [
      { index: true, element: <Navigate to="/dashboard" replace /> },
      { path: "/dashboard", element: <DashboardPage /> },
      { path: "/districts", element: <DistrictsPage /> },
      { path: "/district/:districtId", element: <DistrictDetailPage /> },
      { path: "/alerts", element: <AlertsPage /> },
      { path: "/analytics", element: <AnalyticsPage /> },
      { path: "/ai-engine", element: <AIEnginePage /> },
      { path: "/monitoring", element: <MonitoringPage /> },
      { path: "/admin", element: <AdminPage /> },
    ],
  },
]);
```

---

## 43) `frontend/src/pages/DashboardPage.tsx`

```tsx
import { useMemo, useState } from "react";
import { PageHeader } from "../components/common/PageHeader";
import { MetricCard } from "../components/ui/MetricCard";
import { CriticalDistrictHero } from "../components/dashboard/CriticalDistrictHero";
import { HotspotQueue } from "../components/dashboard/HotspotQueue";
import { AlertFeed } from "../components/dashboard/AlertFeed";
import { LiveDeltaPanel } from "../components/dashboard/LiveDeltaPanel";
import { MonitoringRibbon } from "../components/dashboard/MonitoringRibbon";
import { QuickInsightRail } from "../components/dashboard/QuickInsightRail";
import { DistrictQuickDrawer } from "../components/districts/DistrictQuickDrawer";
import { LoadingPanel } from "../components/common/LoadingPanel";
import { ErrorState } from "../components/common/ErrorState";
import { dataSource } from "../services/dataSource";
import { useAsyncData } from "../hooks/useAsyncData";
import { formatPercent } from "../lib/utils";

export function DashboardPage() {
  const summary = useAsyncData(() => dataSource.getSummary(), []);
  const hotspots = useAsyncData(() => dataSource.getHotspots(), []);
  const alerts = useAsyncData(() => dataSource.getAlerts(), []);
  const monitoring = useAsyncData(() => dataSource.getMonitoringStatus(), []);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [selectedDistrictId, setSelectedDistrictId] = useState<string | null>(null);
  const districtDetail = useAsyncData(
    () => (selectedDistrictId ? dataSource.getDistrictDetail(selectedDistrictId) : Promise.resolve(null)),
    [selectedDistrictId]
  );

  const loading = summary.loading || hotspots.loading || alerts.loading || monitoring.loading;
  const error = summary.error || hotspots.error || alerts.error || monitoring.error;

  const metrics = useMemo(() => {
    const s = summary.data;
    return [
      { label: "Total Districts", value: s?.totalDistricts ?? "—" },
      { label: "High Risk", value: s?.highRiskCount ?? "—" },
      { label: "Active Alerts", value: s?.activeAlerts ?? "—" },
      { label: "Avg Confidence", value: formatPercent(s?.averageConfidence) },
    ];
  }, [summary.data]);

  function openQuickView(districtId: string) {
    setSelectedDistrictId(districtId);
    setDrawerOpen(true);
  }

  return (
    <div>
      <PageHeader
        title="Dashboard"
        subtitle="Water-oriented district risk command center with trust, explainability, and action guidance built into the operational view."
      />

      <MonitoringRibbon monitoring={monitoring.data} />

      {loading ? <LoadingPanel /> : null}
      {error ? <ErrorState message={error} onRetry={() => window.location.reload()} /> : null}

      {!loading && !error ? (
        <>
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            {metrics.map((item) => (
              <MetricCard key={item.label} label={item.label} value={item.value} />
            ))}
          </div>

          <div className="mt-6">
            <CriticalDistrictHero summary={summary.data} />
          </div>

          <div className="mt-6 grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
            <div className="space-y-6">
              <HotspotQueue hotspots={hotspots.data ?? []} onQuickView={openQuickView} />
              <AlertFeed alerts={alerts.data ?? []} />
            </div>
            <div className="space-y-6">
              <LiveDeltaPanel />
              <QuickInsightRail detail={districtDetail.data} />
            </div>
          </div>
        </>
      ) : null}

      <DistrictQuickDrawer
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        detail={districtDetail.data}
      />
    </div>
  );
}
```

---

## 44) `frontend/src/pages/DistrictsPage.tsx`

```tsx
import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { PageHeader } from "../components/common/PageHeader";
import { SearchBar } from "../components/ui/SearchBar";
import { RiskBadge } from "../components/ui/RiskBadge";
import { GlassPanel } from "../components/ui/GlassPanel";
import { LoadingPanel } from "../components/common/LoadingPanel";
import { ErrorState } from "../components/common/ErrorState";
import { dataSource } from "../services/dataSource";
import { useAsyncData } from "../hooks/useAsyncData";
import { formatPercent } from "../lib/utils";

export function DistrictsPage() {
  const { data, loading, error, reload } = useAsyncData(() => dataSource.getDistricts(), []);
  const [query, setQuery] = useState("");

  const filtered = useMemo(() => {
    const base = data ?? [];
    const lower = query.trim().toLowerCase();
    if (!lower) return base;
    return base.filter(
      (item) =>
        item.districtName.toLowerCase().includes(lower) || item.districtId.toLowerCase().includes(lower)
    );
  }, [data, query]);

  return (
    <div>
      <PageHeader
        title="District Intelligence"
        subtitle="Search, scan, and compare districts through a water-risk and public-health monitoring lens."
        rightSlot={<div className="w-[260px]"><SearchBar value={query} onChange={setQuery} placeholder="Search district or ID" /></div>}
      />

      {loading ? <LoadingPanel /> : null}
      {error ? <ErrorState message={error} onRetry={reload} /> : null}

      {!loading && !error ? (
        <GlassPanel title="District List" subtitle="Operational district view with risk, confidence, and dominant pressure signal">
          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead>
                <tr className="border-b border-white/10 text-cyan-100/55">
                  <th className="pb-3 pr-4">District</th>
                  <th className="pb-3 pr-4">ID</th>
                  <th className="pb-3 pr-4">Risk</th>
                  <th className="pb-3 pr-4">Confidence</th>
                  <th className="pb-3 pr-4">Primary Reason</th>
                  <th className="pb-3 pr-4">Action</th>
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
                    <td className="py-4 pr-4">
                      <Link to={`/district/${item.districtId}`} className="rounded-xl border border-cyan-300/15 bg-cyan-400/10 px-3 py-2 text-xs text-cyan-100">
                        Open Profile
                      </Link>
                    </td>
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
```

---

## 45) `frontend/src/pages/DistrictDetailPage.tsx`

```tsx
import { useParams } from "react-router-dom";
import { PageHeader } from "../components/common/PageHeader";
import { LoadingPanel } from "../components/common/LoadingPanel";
import { ErrorState } from "../components/common/ErrorState";
import { MetricCard } from "../components/ui/MetricCard";
import { ExecutiveSummaryCard } from "../components/districts/ExecutiveSummaryCard";
import { SignalBreakdownPanel } from "../components/districts/SignalBreakdownPanel";
import { ActionPlaybook } from "../components/dashboard/ActionPlaybook";
import { ConsensusMeter } from "../components/ui/ConsensusMeter";
import { GlassPanel } from "../components/ui/GlassPanel";
import { RiskTrendChart } from "../components/charts/RiskTrendChart";
import { dataSource } from "../services/dataSource";
import { useAsyncData } from "../hooks/useAsyncData";
import { formatDateTime, formatPercent } from "../lib/utils";

export function DistrictDetailPage() {
  const { districtId = "D001" } = useParams();
  const detail = useAsyncData(() => dataSource.getDistrictDetail(districtId), [districtId]);
  const trends = useAsyncData(() => dataSource.getDistrictTrends(districtId, 30), [districtId]);

  const loading = detail.loading || trends.loading;
  const error = detail.error || trends.error;

  return (
    <div>
      <PageHeader
        title="District Profile"
        subtitle="Deep district intelligence with signal breakdown, model agreement, trust visibility, and recommended actions."
      />

      {loading ? <LoadingPanel /> : null}
      {error ? <ErrorState message={error} onRetry={() => window.location.reload()} /> : null}

      {!loading && !error && detail.data ? (
        <>
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            <MetricCard label="District" value={detail.data.districtName} />
            <MetricCard label="Risk Score" value={detail.data.riskScore} />
            <MetricCard label="Confidence" value={formatPercent(detail.data.confidence)} />
            <MetricCard label="Last Updated" value={formatDateTime(detail.data.lastUpdated)} />
          </div>

          <div className="mt-6 grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
            <div className="space-y-6">
              <ExecutiveSummaryCard detail={detail.data} />
              <RiskTrendChart data={trends.data ?? []} title="District Risk Trajectory" subtitle="Last 30 days of risk movement" />
              <SignalBreakdownPanel detail={detail.data} />
              <ActionPlaybook detail={detail.data} />
            </div>

            <div className="space-y-6">
              <GlassPanel title="Model Comparison" subtitle="Cross-check rule-based and ML outputs for trust visibility">
                <ConsensusMeter scores={detail.data.modelScores} />
              </GlassPanel>

              <GlassPanel title="District Attributes" subtitle="Key demographic and infrastructure context used by the system">
                <div className="grid gap-3 sm:grid-cols-2">
                  <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                    <div className="tiny-label">Population</div>
                    <div className="mt-2 text-2xl font-semibold text-white">{detail.data.population ?? "N/A"}</div>
                  </div>
                  <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                    <div className="tiny-label">Sanitation Score</div>
                    <div className="mt-2 text-2xl font-semibold text-white">{detail.data.sanitationScore ?? "N/A"}</div>
                  </div>
                  <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                    <div className="tiny-label">Water Quality Score</div>
                    <div className="mt-2 text-2xl font-semibold text-white">{detail.data.waterQualityScore ?? "N/A"}</div>
                  </div>
                  <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                    <div className="tiny-label">Vulnerability Index</div>
                    <div className="mt-2 text-2xl font-semibold text-white">{detail.data.vulnerabilityIndex ?? "N/A"}</div>
                  </div>
                </div>
              </GlassPanel>
            </div>
          </div>
        </>
      ) : null}
    </div>
  );
}
```

---

## 46) `frontend/src/pages/AlertsPage.tsx`

```tsx
import { useMemo, useState } from "react";
import { PageHeader } from "../components/common/PageHeader";
import { LoadingPanel } from "../components/common/LoadingPanel";
import { ErrorState } from "../components/common/ErrorState";
import { GlassPanel } from "../components/ui/GlassPanel";
import { RiskBadge } from "../components/ui/RiskBadge";
import { AlertInvestigationCard } from "../components/alerts/AlertInvestigationCard";
import { dataSource } from "../services/dataSource";
import { useAsyncData } from "../hooks/useAsyncData";
import { formatDateTime } from "../lib/utils";

export function AlertsPage() {
  const { data, loading, error, reload } = useAsyncData(() => dataSource.getAlerts(), []);
  const [selectedId, setSelectedId] = useState<number | string | null>(null);

  const selected = useMemo(() => (data ?? []).find((item) => item.id === selectedId) ?? data?.[0] ?? null, [data, selectedId]);

  return (
    <div>
      <PageHeader
        title="Alert Center"
        subtitle="Investigate district-level warning events, review evidence, and connect alerts back to district intelligence."
      />

      {loading ? <LoadingPanel /> : null}
      {error ? <ErrorState message={error} onRetry={reload} /> : null}

      {!loading && !error ? (
        <div className="grid gap-6 xl:grid-cols-[1fr_0.95fr]">
          <GlassPanel title="Active Alert Feed" subtitle="Operational alert stream with district and severity context">
            <div className="space-y-3">
              {(data ?? []).map((alert) => (
                <button
                  key={alert.id}
                  onClick={() => setSelectedId(alert.id)}
                  className="block w-full rounded-2xl border border-white/10 bg-white/5 p-4 text-left transition-all hover:border-cyan-300/15 hover:bg-cyan-400/5"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <div className="flex items-center gap-2">
                        <h3 className="font-medium text-white">{alert.title ?? "District Alert"}</h3>
                        <RiskBadge level={alert.riskLevel} />
                      </div>
                      <p className="mt-2 text-sm text-cyan-50/72">{alert.message ?? "Hybrid score crossed alert threshold."}</p>
                      <div className="mt-2 text-xs text-cyan-100/50">{alert.districtName} • {formatDateTime(alert.createdAt)}</div>
                    </div>
                    <div className="text-xs text-cyan-100/60">{alert.status ?? "active"}</div>
                  </div>
                </button>
              ))}
            </div>
          </GlassPanel>

          <AlertInvestigationCard alert={selected} />
        </div>
      ) : null}
    </div>
  );
}
```

---

## 47) `frontend/src/pages/AnalyticsPage.tsx`

```tsx
import { PageHeader } from "../components/common/PageHeader";
import { RiskTrendChart } from "../components/charts/RiskTrendChart";
import { RiskDriverBarChart } from "../components/charts/RiskDriverBarChart";
import { DistrictCompareTable } from "../components/districts/DistrictCompareTable";
import { dataSource } from "../services/dataSource";
import { useAsyncData } from "../hooks/useAsyncData";
import { mockTrends } from "../lib/mock";

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
      <PageHeader
        title="Risk Analytics"
        subtitle="Cross-district intelligence views, recurring risk drivers, and trend-based analysis for monitoring teams."
      />

      <div className="grid gap-6 xl:grid-cols-2">
        <RiskTrendChart data={mockTrends} title="System Risk Trend" subtitle="Illustrative district-level movement across recent days" />
        <RiskDriverBarChart data={driverData} />
      </div>

      <div className="mt-6">
        <DistrictCompareTable districts={districts.data ?? []} />
      </div>
    </div>
  );
}
```

---

## 48) `frontend/src/pages/AIEnginePage.tsx`

```tsx
import { PageHeader } from "../components/common/PageHeader";
import { AIWorkflowDiagram } from "../components/ai/AIWorkflowDiagram";
import { GlassPanel } from "../components/ui/GlassPanel";

export function AIEnginePage() {
  return (
    <div>
      <PageHeader
        title="AI Engine"
        subtitle="Transparent view of how environmental signals, district factors, and hybrid intelligence produce explainable warnings."
      />

      <AIWorkflowDiagram />

      <div className="mt-6 grid gap-6 xl:grid-cols-3">
        <GlassPanel title="Rule Engine" subtitle="Trust layer">
          <p className="text-sm leading-6 text-cyan-50/72">
            Keeps the system interpretable through human-readable thresholds and domain-driven warning logic.
          </p>
        </GlassPanel>
        <GlassPanel title="Random Forest" subtitle="Pattern learner">
          <p className="text-sm leading-6 text-cyan-50/72">
            Learns non-linear relationships across district-level sanitation, weather, vulnerability, and historical signals.
          </p>
        </GlassPanel>
        <GlassPanel title="XGBoost" subtitle="Accuracy layer">
          <p className="text-sm leading-6 text-cyan-50/72">
            Adds stronger gradient-boosted tabular prediction power while still feeding into the hybrid trust framework.
          </p>
        </GlassPanel>
      </div>
    </div>
  );
}
```

---

## 49) `frontend/src/pages/MonitoringPage.tsx`

```tsx
import { PageHeader } from "../components/common/PageHeader";
import { LoadingPanel } from "../components/common/LoadingPanel";
import { ErrorState } from "../components/common/ErrorState";
import { MonitoringHealthGrid } from "../components/monitoring/MonitoringHealthGrid";
import { dataSource } from "../services/dataSource";
import { useAsyncData } from "../hooks/useAsyncData";

export function MonitoringPage() {
  const { data, loading, error, reload } = useAsyncData(() => dataSource.getMonitoringStatus(), []);

  return (
    <div>
      <PageHeader
        title="Monitoring"
        subtitle="System-health view for ingestion, model readiness, weather synchronization, and district data freshness."
      />

      {loading ? <LoadingPanel /> : null}
      {error ? <ErrorState message={error} onRetry={reload} /> : null}
      {!loading && !error ? <MonitoringHealthGrid status={data} /> : null}
    </div>
  );
}
```

---

## 50) `frontend/src/pages/AdminPage.tsx`

```tsx
import { PageHeader } from "../components/common/PageHeader";
import { AdminActionPanel } from "../components/admin/AdminActionPanel";
import { GlassPanel } from "../components/ui/GlassPanel";

export function AdminPage() {
  return (
    <div>
      <PageHeader
        title="Admin Control"
        subtitle="Manual execution points for ingestion pipeline, model training, and prediction generation."
      />

      <AdminActionPanel />

      <div className="mt-6">
        <GlassPanel title="Safety Note" subtitle="Operational reminder">
          <p className="text-sm leading-6 text-cyan-50/72">
            This page triggers heavy backend operations. Keep confirmation and execution logs when you wire the final backend.
          </p>
        </GlassPanel>
      </div>
    </div>
  );
}
```

---

## 51) Optional `.env`

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_USE_MOCK=true
```

Set `VITE_USE_MOCK=false` when you are ready to connect the real backend.

---

## 52) What this frontend already solves

### Visual identity
- deep-water animated background
- frosted intelligence panels
- public-health seriousness + water-monitoring feel

### Product structure
- dashboard command center
- district intelligence page
- alert center
- analytics
- AI engine page
- monitoring page
- admin control page

### Trust and action features
- critical district hero
- model consensus meter
- signal breakdown
- action playbook
- data reliability framing
- alert investigation card
- system monitoring ribbon

### Backend-ready layer
- new backend endpoints wired
- clean service layer
- central API types
- mock fallback support for UI-first development

---

## 53) Later backend notes (parked for later)

When you connect fully later:

- verify exact field names from backend responses
- remove any remaining mock fallback paths if not needed
- confirm district detail shape matches `DistrictDetail`
- confirm trends response shape matches `TrendPoint[]`
- confirm monitoring response shape matches `MonitoringStatus`
- once backend is stable, set `VITE_USE_MOCK=false`

---

## 54) Practical integration order

1. replace service layer files first
2. replace app shell + router
3. add shared UI components
4. add dashboard page
5. add district detail page
6. add alert center
7. add analytics + monitoring + admin
8. then switch mock off and align final response shapes

---

That is the **complete frontend update bundle** in markdown form.
