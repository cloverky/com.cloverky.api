from datetime import date, timedelta

from models.ingredient_manager import IngredientManager

STORAGE_CHOICES = ("냉장", "냉동", "실온")
UNIT_CHOICES = ("개", "근", "팩", "통", "봉", "g", "ml")

_SHELF_LIFE_KEYWORDS: list[tuple[tuple[str, ...], int]] = [
    (("우유", "요구르트", "치즈"), 7),
    (("계란", "달걀", "란"), 21),
    (("닭", "돼지", "소고기", "고기", "삼겹", "목살", "햄"), 3),
    (("생선", "연어", "고등어", "참치"), 2),
    (("상추", "양상추", "시금치", "쌈", "샐러드", "깻잎"), 5),
    (("브로콜리", "파프리카", "당근", "오이", "토마토"), 7),
    (("만두",), 90),
    (("김치",), 30),
    (("양파", "감자", "마늘", "대파"), 30),
    (("빵", "식빵"), 5),
    (("두부",), 4),
    (("라면", "컵라면", "짜파", "너구리", "우동", "면"), 180),
]
DEFAULT_SHELF_LIFE_DAYS = 7


def estimate_shelf_life_days(name: str, storage: str = "냉장") -> int:
    """구매일만 알 때 품목명·보관 방식으로 유통기한(일) 추정."""
    n = name.strip().lower()
    days = DEFAULT_SHELF_LIFE_DAYS
    for keywords, d in _SHELF_LIFE_KEYWORDS:
        if any(k in n for k in keywords):
            days = d
            break
    if storage == "냉동" and days < 60:
        days = max(days * 3, 60)
    elif storage == "실온":
        if any(k in n for k in ("우유", "계란", "달걀", "생선", "고기", "닭")):
            days = max(1, days // 2)
        else:
            days = min(days * 2, 60)
    return days


def expiry_from_purchase(
    name: str,
    purchased: date,
    storage: str = "냉장",
) -> date:
    return purchased + timedelta(days=estimate_shelf_life_days(name, storage))


def format_quantity(quantity: int, unit: str) -> str:
    return f"{quantity}{unit}"


def compute_status(item: IngredientManager, today: date | None = None) -> str:
    today = today or date.today()
    if item.quantity < item.min_quantity:
        return "부족"
    if item.expiry_date is not None:
        days_left = (item.expiry_date - today).days
        if days_left <= 0:
            return "긴급"
        if days_left <= 3:
            return "임박"
    return "양호"


def count_expiring_soon(items: list[IngredientManager], today: date | None = None) -> int:
    today = today or date.today()
    limit = today + timedelta(days=3)
    n = 0
    for item in items:
        if item.expiry_date is not None and item.expiry_date <= limit:
            n += 1
    return n


def count_low_stock(items: list[IngredientManager]) -> int:
    return sum(1 for item in items if item.quantity < item.min_quantity)
