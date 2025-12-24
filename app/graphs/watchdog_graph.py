from langgraph.graph import StateGraph, END
from app.models import WatchdogState
from app.agents.inventory import check_expiry
from app.agents.demand import check_shortfall


def build_watchdog_graph():
    graph = StateGraph(WatchdogState)

    graph.add_node("inventory_check", check_expiry)
    graph.add_node("demand_check", check_shortfall)
    graph.add_node("aggregate", aggregate_alerts)

    graph.set_entry_point("inventory_check")

    graph.add_edge("inventory_check", "demand_check")
    graph.add_edge("demand_check", "aggregate")
    graph.add_edge("aggregate", END)

    return graph.compile()


def aggregate_alerts(state: WatchdogState):
    alerts = []
    if state.get("expiry_risks"):
        alerts.extend(state["expiry_risks"])
    if state.get("shortfall_risks"):
        alerts.extend(state["shortfall_risks"])

    return {"final_alerts": alerts}