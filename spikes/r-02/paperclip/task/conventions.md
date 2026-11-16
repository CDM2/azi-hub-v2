# Pricing conventions (made-up, for the R-02 spike)

- Money is integer cents everywhere. No floats in a returned value.
- Bulk discount on an order line: 10 or more units, 5% off the line; 50 or more units, 12% off the line. Fewer than 10 units, no discount.
- Round once, on the line total, half up to the nearest cent. Never round per unit. 1890.5 cents becomes 1891.
- An invalid quantity (negative, or not a whole number) raises ValueError.
- Every change adds one line directly under the "# Changes" heading of CHANGES.md, above the older lines. The line starts with "Added:", "Changed:" or "Fixed:".
