import json
from app.services.llm_service import OpenRouterClient
import os

client = OpenRouterClient(
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODEL = "x-ai/grok-4.1-fast:free"  # deterministic, reliable


async def parse_user_question(question: str) -> dict:
    """
    Extracts trial, batch, country from user question.
    Returns STRICT JSON.
    """

    system_prompt = """
You extract structured entities from clinical supply chain questions.

Rules:
- Return ONLY valid JSON
- Do not add explanations
- Use null if entity not present

Schema:
{
  "trial_id": string | null,
  "batch_id": string | null,
  "country": string | null
}
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]

    resp = await client.chat_completion(
        model=MODEL,
        messages=messages,
        reasoning=False
    )

    return json.loads(resp["content"])