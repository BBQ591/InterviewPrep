import heapq
from enum import Enum
from collections import defaultdict
import copy
from typing import NamedTuple


class OrderTypes(Enum):
    IOC = "IOC"
    FOK = "FOK"
    NORMAL = "NORMAL"


class Sides(Enum):
    BUY = "buy"
    SELL = "sell"


class Trade:
    def __init__(self, price: int, side: Sides, id: int, qty: int):
        self.price = price
        self.side = side
        self.id = id
        self.qty = qty


class OrderBook:
    def __init__(self):
        self.buy_side = []
        self.sell_side = []
        self.depth_sell = defaultdict(lambda: 0)
        self.depth_buy = defaultdict(lambda: 0)
        self.deleted = set()
        self.info = defaultdict(lambda: None)

    def add_order(self, id, side, price, qty):
        trade = Trade(price, side, id, qty)
        self._add_order(trade)
        self.info[trade.id] = trade

    def _add_order(self, trade: Trade):
        if trade.side == Sides.BUY:
            heapq.heappush(self.buy_side, (-trade.price, trade.id, trade))
            self.depth_buy[trade.price] += trade.qty
        else:
            assert trade.side == Sides.SELL
            heapq.heappush(self.sell_side, (trade.price, trade.id, trade))
            self.depth_sell[trade.price] += trade.qty

    def best_ask(self):
        return self.sell_side[0][0]

    def best_bid(self):
        return -self.buy_side[0][0]

    def depth(self, price, side: Sides):
        if side == Sides.BUY:
            return self.depth_buy[price]
        else:
            return self.depth_sell[price]

    def can_fulfill_sell(self, price, qty):
        depth = 0
        for new_price, new_qty in self.depth_buy.items():
            if new_price >= price:
                depth += new_qty
        return depth >= qty

    def get_sell_trades(self, trade: Trade):
        trades = []
        while (
            len(self.buy_side) > 0
            and -self.buy_side[0][0] >= trade.price
            and trade.qty > 0
        ):
            price, id, tmp_trade = heapq.heappop(self.buy_side)
            if id in self.deleted:
                continue
            trades.append(
                (id, trade.id, min(trade.qty, tmp_trade.qty), tmp_trade.price)
            )
            self.depth_buy[tmp_trade.price] -= min(trade.qty, tmp_trade.qty)
            if tmp_trade.qty > trade.qty:
                tmp_trade.qty -= trade.qty
                trade.qty = 0
                heapq.heappush(self.buy_side, (price, id, tmp_trade))
            elif tmp_trade.qty < trade.qty:
                trade.qty -= tmp_trade.qty
                tmp_trade.qty = 0
            else:
                tmp_trade.qty = 0
                trade.qty = 0

        return trades

    def handle_sell(self, trade: Trade, type: OrderTypes):
        trades = []
        if type == OrderTypes.NORMAL or type == OrderTypes.IOC:
            trades = self.get_sell_trades(trade)
            if trade.qty > 0 and type == OrderTypes.NORMAL:
                heapq.heappush(self.sell_side, (trade.price, trade.id, trade))
                self.depth_sell[trade.price] += trade.qty
                self.info[trade.id] = trade

        elif type == OrderTypes.FOK:
            if self.can_fulfill_sell(trade.price, trade.qty):
                trades = self.get_sell_trades(trade)

        return trades

    def can_fulfill_buy(self, price, qty):
        total_depth = 0
        for new_price, depth in self.depth_sell.items():
            if new_price <= price:
                total_depth += depth
        return total_depth >= qty

    def get_buy_trades(self, trade: Trade):
        trades = []
        while (
            len(self.sell_side) > 0
            and self.sell_side[0][0] <= trade.price
            and trade.qty > 0
        ):
            price, id, tmp_trade = heapq.heappop(self.sell_side)
            if id in self.deleted:
                continue
            trades.append(
                (id, trade.id, min(trade.qty, tmp_trade.qty), tmp_trade.price)
            )
            self.depth_sell[tmp_trade.price] -= min(trade.qty, tmp_trade.qty)
            if tmp_trade.qty > trade.qty:
                tmp_trade.qty -= trade.qty
                trade.qty = 0
                heapq.heappush(self.sell_side, (price, id, tmp_trade))
            elif tmp_trade.qty < trade.qty:
                trade.qty -= tmp_trade.qty
                tmp_trade.qty = 0
            else:
                tmp_trade.qty = 0
                trade.qty = 0

        return trades

    def handle_buy(self, trade: Trade, type: OrderTypes):
        trades = []
        if type == OrderTypes.NORMAL or type == OrderTypes.IOC:
            trades = self.get_buy_trades(trade)
            if trade.qty > 0 and type == OrderTypes.NORMAL:
                heapq.heappush(self.buy_side, (-trade.price, trade.id, trade))
                self.depth_buy[trade.price] += trade.qty
                self.info[trade.id] = trade
        if type == OrderTypes.FOK:
            if self.can_fulfill_buy(trade.price, trade.qty):
                trades = self.get_buy_trades(trade)

        return trades

    def cancel_order(self, id):
        trade = self.info[id]
        if trade is None:
            raise Exception("Trade not here")

        self.deleted.add(id)
        if Sides.BUY == trade.side:
            self.depth_buy[trade.price] -= trade.qty
        if Sides.SELL == trade.side:
            self.depth_sell[trade.price] -= trade.qty


#    def get_quantity(self, t1: Trade, t2: Trade):
#        if t1.is_new_order:
#            return t2.price
#        return t1.price

# kinda mid
#    def execute(self):
#        trades = []
#        while (
#            len(self.sell_side) > 0
#            and len(self.buy_side) > 0
#            and self.sell_side[0][0] <= -self.buy_side[0][0]
#        ):
#            sell_price, sell_id, sell_trade = heapq.heappop(self.sell_side)
#            buy_price, buy_id, buy_trade = heapq.heappop(self.buy_side)
#            buy_price *= -1
#            price = self.get_quantity(sell_trade, buy_trade)
#            if sell_trade.qty == buy_trade.qty:
#                trades.append((buy_trade.qty, sell_trade.qty, buy_id, sell_id, price))
#            elif sell_trade.qty < buy_trade.qty:
#                trades.append((sell_trade.qty, buy_id, sell_id, price))
#                buy_trade.qty -= sell_trade.qty
#                heapq.heappush(self.buy_side, (-buy_price, buy_id, buy_trade))
#            elif sell_trade.qty > buy_trade.qty:
#                trades.append((buy_trade.qty, buy_id, sell_id, price))
#                sell_trade.qty -= buy_trade.qty
#                heapq.heappush(self.sell_side, (sell_price, sell_id, sell_trade))
#        return trades


def match_states(book, id, side, price, qty, type: OrderTypes = OrderTypes.NORMAL):
    trade = Trade(price, side, id, qty)
    if side == Sides.SELL:
        trades = book.handle_sell(trade, type)
    else:
        trades = book.handle_buy(trade, type)
    return book, trades
