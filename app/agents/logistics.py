# agents/logistics.py
from app.db import run_query
from datetime import date


def check_logistics(state):
    """
    Checks whether there is sufficient time to execute
    shelf-life extension based on shipping / execution lead times.
    """

    country = state.get("country")
    inventory = state.get("inventory_result") or {}

    expiry_date = inventory.get("expiry_date")

    if not country or not expiry_date:
        return {
            "logistics_result": {
                "feasible": False,
                "error": "Missing country or expiry_date"
            }
        }

    query = """
        SELECT
            estimated_lead_time_days
        FROM ip_shipping_timelines
        WHERE country_code = %s
    """

    rows = run_query(query, (country,))

    if not rows:
        return {
            "logistics_result": {
                "feasible": False,
                "error": "No logistics lead time available"
            }
        }

    lead_time = rows[0]["estimated_lead_time_days"]
    days_remaining = (expiry_date - date.today()).days

    feasible = days_remaining >= lead_time

    return {
        "logistics_result": {
            "feasible": feasible,
            "lead_time_days": lead_time,
            "days_remaining": days_remaining
        }
    }
