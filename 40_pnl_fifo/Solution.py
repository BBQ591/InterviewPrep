from enum import Enum
from collections import defaultdict, deque


class Order:
    def __init__(self, symbol, side, qty, price):
        self.symbol = symbol
        self.side = side
        self.qty = qty
        self.price = price


class Side(Enum):
    SELL = "sell"
    BUY = "buy"


class Solution:
    def __init__(self):
        self.positions = defaultdict(lambda: 0)
        self.buy_orders = defaultdict(lambda: deque())
        self.sell_orders = defaultdict(lambda: deque())
        self.realized_pl = defaultdict(lambda: 0)

    def _match(self, multiply, to_pop, order, to_add):
        out = 0
        while len(to_pop) > 0 and to_pop[0].qty <= order.qty:
            smallest = to_pop.popleft()
            order.qty -= smallest.qty
            out += (
                multiply * (smallest.price - order.price) * smallest.qty
            )  # multiply is 1 for buy, -1 for sell
        if order.qty > 0 and len(to_pop) > 0:
            to_pop[0].qty -= order.qty
            out += multiply * (to_pop[0].price - order.price) * order.qty
            order.qty = 0
        if order.qty > 0:
            to_add.append(order)
        return out

    def fill(self, symbol, side, qty, price):
        order = Order(symbol, side, qty, price)
        if side == Side.SELL:
            self.positions[symbol] -= qty
            self.realized_pl[symbol] += self._match(
                -1, self.buy_orders[symbol], order, self.sell_orders[symbol]
            )
        else:
            self.positions[symbol] += qty
            self.realized_pl[symbol] += self._match(
                1, self.sell_orders[symbol], order, self.buy_orders[symbol]
            )

    def position(self, symbol):
        return self.positions[symbol]

    def compute_depth(self, orders):
        total = 0
        for order in orders:
            total += order.qty
        return total

    def compute_total(self, orders):
        total = 0
        for order in orders:
            total += order.qty * order.price
        return total

    def unrealized(self, symbol, mark) -> float:
        buy_qty = self.compute_depth(self.buy_orders[symbol])
        buy_sum = self.compute_total(self.buy_orders[symbol])
        sell_qty = self.compute_depth(self.sell_orders[symbol])
        sell_sum = self.compute_total(self.sell_orders[symbol])
        return buy_qty * mark - buy_sum + sell_sum - sell_qty * mark
