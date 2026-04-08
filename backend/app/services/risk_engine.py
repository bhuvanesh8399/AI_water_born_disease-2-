from dataclasses import dataclass


LOW_RISK_THRESHOLD = 0.40
MEDIUM_RISK_THRESHOLD = 0.70


@dataclass
class RiskInputs:
    confirmed_cases_latest: int
    avg_confirmed_cases_7d: float
    avg_confirmed_cases_prev_7d: float
    contamination_7d: float
    rainfall_7d: float
    vulnerability_index: float
    recent_alert_count: int
    water_quality_index: float
    sanitation_score: float
    healthcare_access_score: float


@dataclass
class RiskResult:
    score: float
    risk_level: str
    explanation: str


def _clamp_01(value: float) -> float:
    return max(0.0, min(value, 1.0))


def _ratio(value: float, upper: float) -> float:
    if upper <= 0:
        return 0.0
    return _clamp_01(value / upper)


def compute_risk(inputs: RiskInputs) -> RiskResult:
    previous = max(inputs.avg_confirmed_cases_prev_7d, 1.0)
    trend_pct = (inputs.avg_confirmed_cases_7d - previous) / previous

    case_burden = _ratio(float(inputs.confirmed_cases_latest), 6000.0)
    trend_risk = _clamp_01((trend_pct + 0.10) / 0.60)
    contamination_risk = _ratio(inputs.contamination_7d, 6.0)
    rainfall_risk = _ratio(inputs.rainfall_7d, 120.0)
    vulnerability_risk = _ratio(inputs.vulnerability_index, 100.0)
    alert_pressure = _ratio(float(inputs.recent_alert_count), 8.0)
    water_quality_risk = _ratio(100.0 - inputs.water_quality_index, 100.0)
    sanitation_risk = _ratio(100.0 - inputs.sanitation_score, 100.0)
    healthcare_gap = _ratio(100.0 - inputs.healthcare_access_score, 100.0)

    weighted_score = (
        (case_burden * 0.28)
        + (trend_risk * 0.14)
        + (contamination_risk * 0.16)
        + (rainfall_risk * 0.08)
        + (vulnerability_risk * 0.14)
        + (alert_pressure * 0.08)
        + (water_quality_risk * 0.04)
        + (sanitation_risk * 0.04)
        + (healthcare_gap * 0.04)
    )

    score = round(weighted_score, 3)

    if score < LOW_RISK_THRESHOLD:
        risk_level = "low"
    elif score < MEDIUM_RISK_THRESHOLD:
        risk_level = "medium"
    else:
        risk_level = "high"

    explanation = (
        f"Score {score:.3f} driven by latest confirmed cases {inputs.confirmed_cases_latest}, "
        f"7-day trend {trend_pct * 100:.1f}%, contamination {inputs.contamination_7d:.2f}, "
        f"vulnerability {inputs.vulnerability_index:.2f}, and recent alerts {inputs.recent_alert_count}."
    )

    return RiskResult(score=score, risk_level=risk_level, explanation=explanation)
