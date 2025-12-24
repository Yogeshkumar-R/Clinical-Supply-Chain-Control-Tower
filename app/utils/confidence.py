def compute_confidence(state: ScenarioState):
    score = 0.0

    if state.get("inventory_result"):
        score += 0.3
    if state.get("regulatory_result"):
        score += 0.4
    if state.get("logistics_result"):
        score += 0.2

    score += 0.1  # entity resolution confidence

    return {
        "confidence_score": round(score * 100, 1)
    }
