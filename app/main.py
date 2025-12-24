from fastapi import FastAPI
from app.graphs.watchdog_graph import build_watchdog_graph
from app.graphs.scenario_graph import build_scenario_graph

app = FastAPI()

watchdog = build_watchdog_graph()
scenario = build_scenario_graph()


@app.post("/watchdog/run")
def run_watchdog():
    return watchdog.invoke({})


@app.post("/scenario/query")
def run_scenario(payload: dict):
    return scenario.invoke({
        "question": payload["question"]
    })