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
