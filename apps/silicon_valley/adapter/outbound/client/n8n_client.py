# adapter/outbound/client/n8n_client.py

from typing import Any

import httpx


class N8nClient:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    async def send_event(self, payload: dict[str, Any]) -> bool:
        """
        FastAPI에서 발생한 데이터를 n8n의 Webhook으로 전송합니다.
        (스타 토폴로지의 중심에서 바깥으로 뻗어나가는 통신)
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.webhook_url, json=payload)
                # 성공 시 True, 실패 시 False 반환
                return response.status_code == 200
            except Exception as e:
                print(f"n8n 전송 실패: {e}")
                return False
