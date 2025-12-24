# agents/regulatory.py
from app.db import run_query


def check_regulatory(state):
    """
    Checks whether shelf-life extension is approved
    for the given material/batch in the specified country.
    """

    country = state.get("country")
    batch_id = state.get("batch_id")

    if not country or not batch_id:
        return {
            "regulatory_result": {
                "status": "UNKNOWN",
                "error": "Country or batch_id missing"
            }
        }

    query = """
        SELECT
            submission_status,
            source_system
        FROM rim_submissions
        WHERE batch_id = %s
          AND country_code = %s
        ORDER BY last_updated DESC
        LIMIT 1
    """

    rows = run_query(query, (batch_id, country))

    if not rows:
        return {
            "regulatory_result": {
                "status": "NOT_APPROVED",
                "source": "RIM",
                "error": "No regulatory submission found"
            }
        }

    row = rows[0]

    status = (
        "APPROVED"
        if row["submission_status"] == "APPROVED"
        else "NOT_APPROVED"
    )

    return {
        "regulatory_result": {
            "status": status,
            "source": row.get("source_system", "RIM")
        }
    }
