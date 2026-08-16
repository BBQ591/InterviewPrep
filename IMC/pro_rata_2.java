import java.util.*;

class OrderBook {
  public enum Side {
    BUY, SELL
  };

  public record Trade(int price, int qty, int buy_id, int sell_id) {
  };

  public record Order(int price, int qty, int id, Side side) {
  };

  public record QtyOrders(int total_qty, Set<Order> orders, int price) {
  };

  boolean fulfill(Order order) {
    if (order.side == Side.BUY) {
      QtyOrders peek = sell_side.peek();
      if (peek == null) {
        return false;
      }
      if (peek.price <= order.price && peek.total_qty <= order.qty) {
        return true;
      }
      return false;
    } else {
      QtyOrders peek = buy_side.peek();
      if (peek == null) {
        return false;
      }
      if (peek.price >= order.price && peek.total_qty <= order.qty) {
        return true;
      }
      return false;
    }
  }

  Side opposite(Side side) {
    if (side == Side.SELL) {
      return Side.BUY;
    }
    return Side.SELL;
  }

  QtyOrders pop_element(Side side) {
    if (side == Side.SELL) {
      return sell_side.pop();
    }
    return buy_side.pop();
  }

  List<Trade> convert_trades(Order order, Set<Order> best_orders) {
    if (order.side == Side.BUY) {
      List<Trade> out = new ArrayList<>();
      for (Order order_tmp : best_orders) {
        if (order_tmp.qty == 0) {
          continue;
        }
        out.add(new Trade(order_tmp.price, order_tmp.qty, order.id, order_tmp.id));
      }
      return out;
    }
    List<Trade> out = new ArrayList<>();
    for (Order order_tmp : best_orders) {
      if (order_tmp.qty == 0) {
        continue;
      }
      out.add(new Trade(order_tmp.price, order_tmp.qty, order_tmp.id, order.id));
    }
    return out;
  }

  boolean partial_fulfill(Order order) {
    if (order.side == Side.BUY) {
      QtyOrders best = sell_side.peek();
      if (best == null) {
        return false;
      }
      if (best.price <= order.price) {
        return true;
      }
      return false;
    }
    QtyOrders best = buy_side.peek();
    if (best == null) {
      return false;
    }
    if (best.price >= order.price) {
      return true;
    }
    return false;
  }

  List<Order> get_order_fill(int to_fill, QtyOrders best_match) {
    int total = 0;
    for (Order ord : best_match.orders) {
      int to_add = ord.qty * to_fill / best_match.total_qty;
      total += to_add;
    }
    int remaining = to_fill - total;
    List<Order> all_orders = new ArrayList<>(best_match.orders);
    all_orders.sort(Comparator.comparingInt(Order::qty).reversed().thenComparingInt(Order::id));
    Set<Integer> ids = new HashSet<>();
    for (int i = 0; i < remaining; i++) {
      ids.add(all_orders.get(i).id);
    }
    List<Order> out = new ArrayList<>();
    for (Order ord : best_match.orders) {
      int to_add = ord.qty * to_fill / best_match.total_qty;
      if (ids.contains(ord.id)) {
        to_add += 1;
      }
      out.add(new Order(ord.price, to_add, ord.id, ord.side));
    }
    return out;
  }

  List<Order> get_remaining(List<Order> fill_amount, Set<Order> original) {
    List<Order> remaining = new ArrayList<>();
    Map<Integer, Integer> id_qty = new HashMap<>();
    for (Order ord : original) {
      id_qty.put(ord.id, ord.qty);
    }
    for (Order ord : fill_amount) {
      if (id_qty.get(ord.id) - ord.qty == 0) {
        continue;
      }
      remaining.add(new Order(ord.price, id_qty.get(ord.id) - ord.qty, ord.id, ord.side));
    }
    return remaining;
  }

  public List<Trade> add_order(int price, int qty, int id, Side side) {
    Order order = new Order(price, qty, id, side);
    List<Trade> all_trades = new ArrayList<>();
    while (fulfill(order)) { // checks if the best element has quantity less than or equal to order.qty
      QtyOrders best_match = pop_element(opposite(order.side)); // should pop from the heap, then remove from the map
                                                                // as well
      List<Trade> trades = convert_trades(order, best_match.orders); // basically takes order and then just creates
                                                                     // trade objects with best match
      all_trades.addAll(trades);
      order = new Order(order.price, order.qty - best_match.total_qty, order.id, order.side);
    }
    if (order.qty > 0 && partial_fulfill(order)) { // checks if best element has quantity greater than order.qty
      QtyOrders best_match = pop_element(opposite(order.side)); // pops from heap and removing from hashmap
      List<Order> fill_amount = get_order_fill(order.qty, best_match); // getting fraction for pro rata, multiplying by
                                                                       // best match, then adds 1 order to the top k
                                                                       // elements
      List<Order> remaining_amount = get_remaining(fill_amount, best_match.orders); // subtracts fill_amount from
                                                                                    // best_match.orders
      put_element(opposite(order.side), remaining_amount); // puts remaining amount in the opposite of order.side
      List<Trade> trades = convert_trades(order, new HashSet<>(fill_amount)); // once again, just converts trades
      all_trades.addAll(trades);
      order = new Order(order.price, 0, order.id, order.side);
    }
    if (order.qty > 0) {
      List<Order> tmp = new ArrayList<>();
      tmp.add(order);
      put_element(order.side, tmp); // same as above
    }
    return all_trades;
  }
}
