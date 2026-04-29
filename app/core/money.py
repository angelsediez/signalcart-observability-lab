from decimal import Decimal, ROUND_HALF_UP


MONEY_QUANT = Decimal("0.01")


def to_money(value: float | int | str | Decimal) -> Decimal:
    return Decimal(str(value)).quantize(MONEY_QUANT, rounding=ROUND_HALF_UP)
