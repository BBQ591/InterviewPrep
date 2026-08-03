# Data Pipeline Problems

Multi-step transformation problems. Each has a **Level 0** and a series of
**extensions**. Implement Level 0 fully, then take the extensions in order — each
one is a new requirement dropped on an existing design.

---

## 1. Portfolio Look-Through & Rebalancing

**Given**
- Direct stock holdings: `(ticker, shares, price)`
- ETF holdings: `(etf_ticker, shares, price)`
- ETF compositions: for each ETF, a list of `(constituent_ticker, weight)`, weights summing to 1. A constituent may be a stock **or another ETF**.

**Level 0.** Report total portfolio equity; the effective dollar exposure to each underlying stock (counting both direct holdings and the portion held inside ETFs); and each stock's concentration as a percentage of total equity.

**Extensions**
1. ETFs may hold other ETFs to arbitrary depth. Reject any portfolio whose ETF composition graph contains a cycle.
2. Given a target maximum concentration (e.g. no stock above 5%), output a list of sells that brings every stock under the target. You may only sell direct stock holdings.
3. You may now also sell ETF holdings.
4. Whole shares only. You may not sell more than you hold, and you may not short.
5. Multiple simultaneous targets — e.g. no single stock above 5% **and** no sector above 30%. Each stock belongs to a sector.
6. Among all valid solutions, minimize the number of separate sell orders.

---

## 2. Bill of Materials Explosion

**Given**
- A catalog of items. Each item is either a **raw part** (purchased) or an **assembly** (built from other items).
- For each assembly: a list of `(component_item, quantity_per_unit)`.
- Inventory on hand: `(item, quantity)`.
- Supplier data for raw parts: `(part, supplier, unit_cost, minimum_order_quantity, lead_time_days)`.

**Level 0.** Given an order for N units of a top-level product, report the total quantity of every raw part required.

**Extensions**
1. Assemblies nest to arbitrary depth, and the same component may appear at multiple levels and inside multiple assemblies. Reject catalogs whose composition graph contains a cycle.
2. Net the requirement against inventory on hand. Inventory of an *assembly* satisfies demand for that assembly directly.
3. Emit purchase orders grouped by supplier, respecting minimum order quantities.
4. Given a due date for the finished product and per-part lead times, report the date each purchase order must be placed.
5. A part may have several suppliers with different costs and lead times. Choose between them.

---

## 3. Tax Lot Optimizer

**Given**
- Lots of a single security: `(lot_id, purchase_date, quantity, cost_per_share)`
- Current price, today's date, and a quantity to sell.
- Tax rates: long-term rate `L`, short-term rate `S` (`S > L`).

**Rules.** A lot held more than 365 days is long-term; otherwise short-term. Losses offset gains.

**Level 0.** Choose which lots (partial lots allowed) to sell to fill the requested quantity while minimizing total tax owed. Report the selection, the realized gain/loss, and the estimated tax.

**Extensions**
1. Add a mode that minimizes the number of lots touched, and a mode that maximizes harvested losses.
2. Wash-sale rule: a loss is disallowed if the same security is purchased within 30 days before or after the sale. Given a trade history, flag disallowed losses.
3. Multiple securities, one overall tax bill, and a target amount of **cash** to raise.

---

## 4. Debt Payoff Optimizer

**Given**
- Loans: `(name, balance, annual_interest_rate, minimum_monthly_payment)`
- A total monthly budget.

**Rules.** Interest accrues monthly at `rate / 12` on the remaining balance. Every month you must pay at least the minimum on every loan; whatever remains of the budget is "extra."

**Level 0.** Produce a month-by-month payoff schedule under the **avalanche** strategy (extra goes to the highest interest rate first). Report total interest paid and the payoff date.

**Extensions**
1. Support **snowball** (extra goes to the smallest balance first). Compare total interest and payoff date across strategies.
2. When a loan is fully paid off, its minimum payment rolls into the extra from the next month onward.
3. Reject infeasible inputs (budget below the sum of minimums). Never overpay a loan on its final month.
4. Support one-off lump-sum payments on given dates, and loans with a promotional 0% rate that expires on a given date.

---

## 5. Limit Order Book / Matching Engine

**Given.** A stream of orders: `(order_id, side, price, quantity, timestamp)`.

**Rules.** Orders rest in a book until matched. A buy matches a sell when `buy_price >= sell_price`. Priority is **price first, then time** (earliest first among equal prices). The **resting** order's price is the trade price.

**Level 0.** Process the stream. For each incoming order, output the fills it generates — `(buy_order_id, sell_order_id, price, quantity)` — and show the resulting book.

**Extensions**
1. Partial fills: an order may be filled by several counterparties and may rest with a remaining quantity.
2. Cancel and amend resting orders. Amending the price loses time priority.
3. Market orders (no price — take whatever is available). Handle the book running out.
4. Report best bid, best ask, spread, and depth (total quantity at each price level).
5. Iceberg orders: only part of the quantity is displayed; when the displayed part fills, more is revealed and it goes to the back of the time queue at that price.

---

## 6. P&L Attribution

**Given**
- Trades: `(timestamp, symbol, side, quantity, price, fee, strategy)`
- End-of-day prices per symbol.

**Rules.** Sells are matched against buy lots **FIFO**. Realized P&L = proceeds − cost basis − fees. Open positions are marked to market; unrealized P&L = (market price − cost basis) × quantity.

**Level 0.** Report total realized P&L, total unrealized P&L, and per-symbol positions with cost basis.

**Extensions**
1. Break P&L down by strategy and by symbol.
2. Support short positions (sell before buy), with correct cost basis and signs.
3. Corporate actions: a stock split (ratio R on date D) adjusts quantities and cost bases of all lots held before D.
4. Multi-currency trades, reported in a base currency using daily FX rates.

---

## 7. Multi-Currency Portfolio Valuation

**Given**
- Positions: `(symbol, quantity, price, currency)`
- FX rates: `(from_currency, to_currency, rate)` — **not all pairs are present**.
- A base currency.

**Level 0.** Report total portfolio value in the base currency.

**Extensions**
1. If a direct rate is missing, derive it. If no conversion is possible, report which currencies are unreachable.
2. Rates may be supplied in one direction only; the inverse is `1 / rate`.
3. Detect and report inconsistencies — where two different conversion routes between the same pair disagree by more than a tolerance.
4. Rates come as bid/ask spreads rather than a single number. Value using the correct side.

---

## 8. Billing / Invoice Engine

**Given**
- Usage records: `(customer, metric, quantity, timestamp)`
- Per-metric tiered price schedules (e.g. first 1,000 units free, next 10,000 at $0.01, remainder at $0.005).
- A billing period, discounts (percentage or fixed, at line-item or invoice level), and a tax rate.

**Level 0.** Produce an invoice: line items per metric with quantity and charge, subtotal, tax, total.

**Extensions**
1. A customer may change plans mid-period. Prorate.
2. Apply discounts. You must specify and honor the order of operations between line-level discounts, invoice-level discounts, and tax.
3. Credits carried over from a previous invoice, and a minimum monthly commitment (charge the greater of usage and commitment).
4. Multiple currencies and per-jurisdiction tax rates.

---

## 9. Payroll Engine

**Given**
- Employee: `(name, hourly_rate, filing_status)`
- Timesheet: hours per day for the period.
- Pre-tax elections: 401(k) as % of gross, health premium as fixed $.
- Post-tax deductions: fixed $.
- Progressive federal brackets `[(upper_bound, rate), ...]`, a flat state rate, Social Security at X% up to an **annual wage cap**, Medicare at Y% with no cap.

**Rules.** Hours over 40 in a week are paid at 1.5×.

**Level 0.** For one employee for one period: gross pay, every deduction, every tax, and net pay.

**Extensions**
1. Pre-tax deductions reduce federal and state taxable income, but **not** Social Security / Medicare wages.
2. The Social Security cap is annual — year-to-date wages determine when it stops applying.
3. Multiple employees, plus a payroll register totalling employer-side taxes.
4. Mid-year rate or election changes.

---

## 10. League Standings

**Given.** Match results: `(home_team, away_team, home_goals, away_goals)`.
**Rules.** Win = 3 points, draw = 1, loss = 0.

**Level 0.** Produce a table with, per team: played, won, drawn, lost, goals for, goals against, goal difference, points — sorted by points descending.

**Extensions**
1. Tiebreaks in order: points, then goal difference, then goals scored, then alphabetical.
2. **Head-to-head tiebreak:** when teams are level on points, rank them using a mini-table computed *only from the matches played among those tied teams* (points, then goal difference, then goals scored, within that mini-table). Fall back to the overall tiebreaks only if still level.
3. Handle three or more teams tied, where the head-to-head mini-table itself produces ties.
4. Support alternate rulesets: 2 points for a win; away goals counting double in head-to-head.

---

## 11. Meeting Scheduler

**Given**
- People, each with busy intervals `(start, end)` and a timezone.
- Working hours per person (e.g. 09:00–17:00 local).
- A required meeting duration and a search window.

**Level 0.** Return every slot in the window where all people are free, within their working hours, for the full duration.

**Extensions**
1. Required vs optional attendees. Return slots where all required attendees are free, ranked by how many optional attendees can also make it.
2. Timezones, including a DST transition inside the search window.
3. Buffer time: no meeting may start within N minutes of another meeting for any attendee.
4. Rooms, with capacities and their own busy intervals. Return `(slot, room)` pairs.
