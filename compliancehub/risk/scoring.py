RISK_MATRIX = {
    ("low", "low"): "Low", ("low", "medium"): "Low", ("low", "high"): "Medium",
    ("medium", "low"): "Low", ("medium", "medium"): "Medium", ("medium", "high"): "High",
    ("high", "low"): "Medium", ("high", "medium"): "High", ("high", "high"): "Critical",
}

def score_risk(likelihood: str, impact: str) -> str:
    return RISK_MATRIX.get((likelihood.lower(), impact.lower()), "Unknown")
