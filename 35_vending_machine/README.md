# 35 — Vending Machine — Specification (S/M, interview sim)

Protocol: parts in order; no reading ahead. Python + pytest.

## Part 1 — coins and purchases

Coins: 1, 5, 10, 25, 100.
`stock(slot, item_name, price, qty)`
`insert(coin)` ; `balance() -> int`
`select(slot) -> (item_name, change_coins) | refusal` — dispenses if
the balance covers the price; change is returned as coins; the balance
resets after a sale.
`refund() -> list[coin]` — returns the current balance as coins.

## Part 2 — the machine's coins are finite

The machine holds a physical coin inventory: its starting float plus
every coin inserted, minus every coin paid out. Change can only be made
from coins the machine actually holds; if exact change for a sale is
impossible, the sale is refused, nothing is dispensed, and the balance
is kept. The machine never creates or destroys coins.

## Part 3 — operations

`restock_coins(counts)` ; `collect_cash() -> counts` — empties earnings
while leaving a working float (decide what that means).
`report() -> ...` — units and revenue sold per slot since the last
collection. The report must reconcile: revenue plus float movements
equals the physical coin inventory, always.

## Part 4 (stretch) — pricing rules

Discounts, e.g. "every third item from slot B is half price" or a
two-item bundle price. Design how rules are represented so a new rule
doesn't mean rewriting select.

## Deliverables

Implementation + tests. Test design is part of the work.
Deliberately underspecified in places — finding the ambiguities and
deciding those contracts is part of the work.
