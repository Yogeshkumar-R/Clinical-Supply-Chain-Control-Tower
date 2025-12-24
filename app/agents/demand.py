# agents/demand.py
from app.db import run_query


def check_shortfall(state):
    query = """
        WITH rates AS (
            SELECT trial_id, country_code,
                   AVG(enrollment_rate) AS weekly_rate
            FROM enrollment_rate_report
            GROUP BY trial_id, country_code
        ),
        inventory AS (
            SELECT trial_id, country_code,
                   SUM(available_quantity) AS qty
            FROM available_inventory_report
            GROUP BY trial_id, country_code
        )
        SELECT i.trial_id, i.country_code,
               i.qty / NULLIF(r.weekly_rate,0) AS weeks_remaining
        FROM inventory i
        JOIN rates r
        ON i.trial_id = r.trial_id
        AND i.country_code = r.country_code
        WHERE (i.qty / NULLIF(r.weekly_rate,0)) <= 8
    """
    rows = run_query(query)

    return {
        "shortfall_risks": [
            {
                "type": "SHORTFALL",
                "trial_id": r["trial_id"],
                "country": r["country_code"],
                "weeks_remaining": r["weeks_remaining"],
                "risk_level": "CRITICAL"
            }
            for r in rows
        ]
    }