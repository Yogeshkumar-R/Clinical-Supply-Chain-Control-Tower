import os
import asyncio
import httpx
import json

class OpenRouterClient:
    def __init__(self, api_key: str, base_url: str = "https://openrouter.ai/api/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    # -------------------------------
    # Normalization helpers
    # -------------------------------
    def normalize_full_response(self, resp: dict) -> dict:
        """Normalize a full completion response into a clean schema."""
        choice = resp["choices"][0]
        msg = choice["message"]
        return {
            "id": resp.get("id"),
            "model": resp.get("model"),
            "provider": resp.get("provider"),
            "created": resp.get("created"),
            "role": msg.get("role"),
            "content": msg.get("content"),
            "metadata": {
                "finish_reason": choice.get("finish_reason"),
                "usage": resp.get("usage", {})
            },
            "reasoning_details": msg.get("reasoning_details", [])
        }

    # -------------------------------
    # API methods
    # -------------------------------
    async def chat_completion(self, model: str, messages: list, reasoning: bool = False):
        """Non-streaming chat completion."""
        url = f"{self.base_url}/chat/completions"
        payload = {"model": model, "messages": messages}
        if reasoning:
            payload["extra_body"] = {"reasoning": {"enabled": True}}

        timeout = httpx.Timeout(60.0)  # 60 seconds

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return self.normalize_full_response(response.json())


# import os
# import asyncio
# from src.service.llm_service import OpenRouterClient 
# from src.core.config.config import config   

# async def main():
#     client = OpenRouterClient(config.openrouter_api_key)

#     # Full response
#     result = await client.chat_completion(
#         model="x-ai/grok-4.1-fast:free",
#         messages=[{"role": "user", "content": "Explain quantum entanglement simply."}],
#         reasoning=True
#     )
#     print("Normalized Full Response:", result['content'])

# if __name__ == "__main__":
#     asyncio.run(main())