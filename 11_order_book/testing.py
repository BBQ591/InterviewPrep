from order_book import OrderBook, Sides, match_states, OrderTypes


def test_part_1():
    book = OrderBook()
    book.add_order(0, Sides.BUY, 10, 10)
    book.add_order(1, Sides.SELL, 5, 20)
    book.add_order(2, Sides.BUY, 20, 5)
    book.add_order(3, Sides.SELL, 10, 5)
    assert book.best_ask() == 5
    assert book.best_bid() == 20
    assert book.depth(10, Sides.BUY) == 10
    assert book.depth(5, Sides.SELL) == 20
    assert book.depth(7, Sides.BUY) == 0
    assert book.depth(2, Sides.SELL) == 0


def test_handle_sell():
    book = OrderBook()
    book.add_order(0, Sides.BUY, 10, 10)
    book.add_order(2, Sides.BUY, 20, 5)
    book.add_order(1, Sides.SELL, 40, 20)
    book.add_order(3, Sides.SELL, 30, 5)
    book, trades = match_states(book, 4, Sides.SELL, 15, 20)
    assert len(trades) == 1
    assert trades[0] == (2, 4, 5, 20)


def test_handle_buy():
    book = OrderBook()
    book.add_order(0, Sides.BUY, 10, 10)
    book.add_order(2, Sides.BUY, 20, 5)
    book.add_order(1, Sides.SELL, 40, 20)
    book.add_order(3, Sides.SELL, 30, 5)
    book, trades = match_states(book, 4, Sides.BUY, 35, 10)
    assert len(trades) == 1
    assert trades[0] == (3, 4, 5, 30)


def test_match_states_IOC():
    book = OrderBook()
    book.add_order(0, Sides.BUY, 10, 10)
    book.add_order(2, Sides.BUY, 20, 5)
    book.add_order(1, Sides.SELL, 40, 20)
    book.add_order(3, Sides.SELL, 30, 5)
    book, trades = match_states(book, 4, Sides.BUY, 35, 10, OrderTypes.IOC)
    assert len(trades) == 1
    assert trades[0] == (3, 4, 5, 30)
    contains = False
    for item in book.buy_side:
        trade = item[2]
        if trade.id == 4:
            contains = True
            break
    assert not contains


def test_match_states_FOK_NO():
    book = OrderBook()
    book.add_order(0, Sides.BUY, 10, 10)
    book.add_order(2, Sides.BUY, 20, 5)
    book.add_order(1, Sides.SELL, 40, 20)
    book.add_order(3, Sides.SELL, 30, 5)
    book, trades = match_states(book, 4, Sides.BUY, 35, 10, OrderTypes.FOK)
    assert len(trades) == 0
    contains = False
    for item in book.buy_side:
        trade = item[2]
        if trade.id == 4:
            contains = True
            break
    assert not contains


def test_match_states_FOK_YES():
    book = OrderBook()
    book.add_order(0, Sides.BUY, 10, 10)
    book.add_order(2, Sides.BUY, 20, 5)
    book.add_order(1, Sides.SELL, 40, 20)
    book.add_order(3, Sides.SELL, 30, 5)
    book, trades = match_states(book, 4, Sides.BUY, 35, 5, OrderTypes.FOK)
    assert len(trades) == 1
    assert trades[0] == (3, 4, 5, 30)
    contains = False
    for item in book.buy_side:
        trade = item[2]
        if trade.id == 4:
            contains = True
            break
    assert not contains
