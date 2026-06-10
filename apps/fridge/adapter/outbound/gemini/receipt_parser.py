import json
import re
from datetime import date

from fastapi import HTTPException

from fridge.app.dtos.receipt_dto import ReceiptLineParsedDto, ReceiptParseResultDto
from fridge.app.ports.output.receipt_parser import ReceiptParserPort
from core.matrix.wault_keymaker_serect_manager import get_keymaker

_RECEIPT_PROMPT = """이 영수증 이미지에서 구매 정보를 추출하세요.
반드시 아래 JSON 형식만 출력하고 다른 설명은 하지 마세요.
{
  "store_name": "매장명 또는 null",
  "purchased_date": "YYYY-MM-DD 또는 null",
  "items": [
    {"name": "품목명", "quantity": 1, "unit": "개"}
  ]
}
quantity는 1 이상 정수, unit은 개·팩·봉·통·g·ml 중 하나. 읽을 수 없는 품목은 제외."""


def _extract_json(text: str) -> dict:
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if fence:
        text = fence.group(1).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("JSON 블록을 찾을 수 없습니다.")
    return json.loads(text[start : end + 1])


def _parse_date(value: str | None) -> date | None:
    if not value or not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value.strip()[:10])
    except ValueError:
        return None


class GeminiReceiptParser(ReceiptParserPort):

    def parse(self, image_bytes: bytes, mime_type: str) -> ReceiptParseResultDto:
        keymaker = get_keymaker()
        if not keymaker.is_gemini_ready():
            raise HTTPException(
                status_code=503,
                detail="GEMINI_API_KEY가 설정되지 않았습니다. 영수증 인식을 사용할 수 없습니다.",
            )
        model = keymaker.get_gemini_model()
        try:
            response = model.generate_content(
                [
                    {"mime_type": mime_type, "data": image_bytes},
                    _RECEIPT_PROMPT,
                ],
            )
            raw = (response.text or "").strip()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"영수증 인식 실패: {e!s}") from e

        if not raw:
            raise HTTPException(status_code=502, detail="영수증에서 텍스트를 읽지 못했습니다.")

        try:
            data = _extract_json(raw)
        except (json.JSONDecodeError, ValueError) as e:
            raise HTTPException(
                status_code=422,
                detail=f"영수증 파싱 결과를 해석하지 못했습니다: {e!s}",
            ) from e

        items: list[ReceiptLineParsedDto] = []
        for row in data.get("items") or []:
            if not isinstance(row, dict):
                continue
            name = str(row.get("name") or "").strip()
            if not name:
                continue
            try:
                qty = int(row.get("quantity") or 1)
            except (TypeError, ValueError):
                qty = 1
            unit = str(row.get("unit") or "개").strip() or "개"
            items.append(ReceiptLineParsedDto(name=name, quantity=max(1, qty), unit=unit))

        store = data.get("store_name")
        store_name = str(store).strip() if store else None
        if store_name == "null":
            store_name = None

        return ReceiptParseResultDto(
            store_name=store_name,
            purchased_date=_parse_date(data.get("purchased_date")),
            items=items,
        )
