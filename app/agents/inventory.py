# agents/inventory.py
from app.db import run_query
from datetime import date


def check_expiry(state):
    query = """
        SELECT batch_id, expiry_date,
               expiry_date - CURRENT_DATE AS days_to_expiry
        FROM allocated_materials
        WHERE expiry_date <= CURRENT_DATE + INTERVAL '90 days'
    """
    rows = run_query(query)

    risks = []
    for r in rows:
        if r["days_to_expiry"] <= 30:
            level = "CRITICAL"
        elif r["days_to_expiry"] <= 60:
            level = "HIGH"
        else:
            level = "MEDIUM"

        risks.append({
            "type": "EXPIRY",
            "batch_id": r["batch_id"],
            "days_to_expiry": r["days_to_expiry"],
            "risk_level": level
        })

    return {"expiry_risks": risks}

def check_batch(state):
    """
    Scenario-specific inventory check.
    Answers: has this batch been re-evaluated and is it still valid?
    """

    batch_id = state.get("batch_id")
    if not batch_id:
        return {
            "inventory_result": {
                "re_evaluated": False,
                "error": "Batch ID missing"
            }
        }

    query = """
        SELECT
            batch_id,
            last_re_evaluation_date,
            expiry_date
        FROM batch_master
        WHERE batch_id = %s
    """

    rows = run_query(query, (batch_id,))

    if not rows:
        return {
            "inventory_result": {
                "re_evaluated": False,
                "error": "Batch not found"
            }
        }

    row = rows[0]

    return {
        "inventory_result": {
            "re_evaluated": row["last_re_evaluation_date"] is not None,
            "expiry_date": row["expiry_date"],
            "last_re_evaluation_date": row["last_re_evaluation_date"]
        }
    }