from langgraph.graph import StateGraph, END
from app.models import ScenarioState
from app.agents.inventory import check_batch
from app.agents.regulatory import check_regulatory
from app.agents.logistics import check_logistics
from app.utils.confidence import compute_confidence
from app.services.query_parser import parse_user_question



def build_scenario_graph():
    graph = StateGraph(ScenarioState)

    graph.add_node("parse_question", parse_question)
    graph.add_node("inventory", check_batch)
    graph.add_node("regulatory", check_regulatory)
    graph.add_node("logistics", check_logistics)
    graph.add_node("decide", decide)
    graph.add_node("confidence", compute_confidence)

    graph.set_entry_point("parse_question")

    graph.add_edge("parse_question", "inventory")
    graph.add_edge("inventory", "regulatory")
    graph.add_edge("regulatory", "logistics")
    graph.add_edge("logistics", "decide")
    graph.add_edge("decide", "confidence")
    graph.add_edge("confidence", END)

    return graph.compile()

def decide(state: ScenarioState):
    reasons = []
    decision = "YES"

    regulatory = state.get("regulatory_result") or {}
    inventory = state.get("inventory_result") or {}
    logistics = state.get("logistics_result") or {}

    if regulatory.get("status") != "APPROVED":
        decision = "NO"
        reasons.append("Regulatory approval missing")

    if not inventory.get("re_evaluated", False):
        decision = "NO"
        reasons.append("No prior re-evaluation")

    if not logistics.get("feasible", False):
        decision = "NO"
        reasons.append("Insufficient time to execute extension")

    return {
        "decision": decision,
        "reasoning": reasons
    }


async def parse_question(state: ScenarioState):
    entities = await parse_user_question(state["question"])
    return {
        "trial_id": entities.get("trial_id"),
        "batch_id": entities.get("batch_id"),
        "country": entities.get("country"),
    }
