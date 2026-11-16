"""Prices for the made-up shop used by the R-02 spike. All money is integer cents."""


def line_total(unit_cents: int, quantity: int) -> int:
    """Price of one order line with no discount."""
    if quantity < 0:
        raise ValueError("quantity must not be negative")
    return unit_cents * quantity
