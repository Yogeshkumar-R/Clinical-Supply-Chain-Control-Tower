from typing import TypedDict, List, Optional


class WatchdogState(TypedDict):
    expiry_risks: Optional[List[dict]]
    shortfall_risks: Optional[List[dict]]
    final_alerts: Optional[List[dict]]


class ScenarioState(TypedDict):
    question: str

    trial_id: Optional[str]
    batch_id: Optional[str]
    country: Optional[str]

    inventory_result: Optional[dict]
    regulatory_result: Optional[dict]
    logistics_result: Optional[dict]

    decision: Optional[str]
    confidence_score: Optional[float]
    reasoning: Optional[list]