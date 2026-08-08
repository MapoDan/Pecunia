from decimal import Decimal

from app.services.expenses import normalize_name, payment_total, quantize_money


def test_normalize_name_is_deterministic() -> None:
    assert normalize_name("  Esselunga   Roma  ") == "esselunga roma"


def test_money_quantization_uses_decimal() -> None:
    assert quantize_money(Decimal("10.005")) == Decimal("10.01")


def test_payment_total_uses_quantized_decimal_components() -> None:
    assert payment_total([Decimal("8"), Decimal("2.00")]) == Decimal("10.00")
