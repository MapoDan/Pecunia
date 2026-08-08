from decimal import Decimal

from app.services.expenses import normalize_name, quantize_money


def test_normalize_name_is_deterministic() -> None:
    assert normalize_name("  Esselunga   Roma  ") == "esselunga roma"


def test_money_quantization_uses_decimal() -> None:
    assert quantize_money(Decimal("10.005")) == Decimal("10.01")
