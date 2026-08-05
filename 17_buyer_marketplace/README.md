# 17 — Buyer Marketplace — Specification (interview rep)

The Jane-style stateful question, run AS an interview: parts revealed in
order, each timeboxed, test list written before bodies (standing rule).
Python + pytest — this doubles as an 11_order_book testing rep.

## Given

```python
class Item:
    seller_name: str
    buyer_name: str | None
    item_name: str
    price: int

class Datastore:
    def put(self, item: Item) -> None: ...      # insert or update
    def get_all(self) -> list[Item]: ...        # original insertion order

class BuyerMarketplace:
    def __init__(self, datastore: Datastore): ...
    def buy_items(self, buyer_name: str,
                  items: dict[str, int]) -> dict[str, Item]: ...
    def remove_buyers(self, buyers_to_exclude: set[str]) -> dict[str, int]: ...
```

You write Datastore too (it's ~10 lines), but BuyerMarketplace may use ONLY
these two methods — it is dumb storage, no queries.

## Part 1 — buy_items (timebox: 25 min, tests included)

`buy_items(buyer_name, items: dict[str, int]) -> dict[str, Item]`

For each requested name: cheapest unsold item with that name and
price <= max; tie → earliest in get_all(); mark with the buyer and persist
via put; return the successes.

## Part 2 — remove_buyers (timebox: 35 min)

`remove_buyers(buyers_to_exclude: set[str]) -> dict[str, int]`

Roll back excluded buyers' purchases — but only ones in THIS instance's
transaction history; pre-existing sold items are never touched even when the
buyer_name matches. Replay the surviving purchase requests in original
order; remaining buyers may land on cheaper items. Return refunds owed.

Golden test — the worked example: offers 80, 85, 89; Alice(max 100)→80,
Bob(max 90)→85; offer 84 arrives; Charlie(max 84)→84; remove Alice ⇒
Bob→80 refund 5, Charlie unchanged ⇒ `{"Bob": 5}`.

## Part 3 — the escalation the interviewer keeps in reserve

1. `remove_buyers` is called a SECOND time (different buyers). What is the
   transaction history after a replay? Decide, write it down, test it.
2. A buyer's original request was partly unfilled (wanted "gpu" <= 85, none
   eligible). During a later replay a matching item IS available. Does the
   replay fill it? If yes, the "refund" is negative — what does the return
   value mean now? Decide the contract; test the decision.
3. A removed buyer calls buy_items again afterwards. Fresh start or refused?

## Part 4 (stretch) — external writes

New offers are put() directly into the datastore between your calls (they
show up in get_all()). Replays run against the datastore as it NOW is. Does
anything you wrote assume the world only changes through you? Find out by
testing it.

## Part 5 (stretch) — wallets

See 21_wallet_marketplace: each buyer gets a total budget across all
purchases. One sentence, and the per-name independence dies. Which of your
machinery survives?

## Required behavior

- Only tracked purchases roll back; pre-existing buyer_names are frozen
  history.
- Tie-break and cheapest-first exactly as Part 1, on every replay.
- Killer property: after ANY sequence of operations, the datastore's
  sold-state equals folding the surviving purchase requests, in original
  order, over the initial datastore contents. (Principle 13 made
  executable — the history IS an event log; replay is a fold. Assert it
  with an oracle that literally does that fold.)

## Where the bugs live (speak the scan after each part)

- boundaries: price exactly == max; empty request dict; item name absent.
- second operation: buy after remove; remove twice; same buyer requests the
  same name across two calls.
- facts twice: history vs datastore — after every mutating op they must
  agree.
- undecided contracts: all of Part 3 — the "hm, what should this do?"
  flicker is the bug report from the future.
