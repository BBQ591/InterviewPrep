import java.util.*;

class OrderBook {
  public enum Side {
    BUY, SELL
  };

  public record Trade(int price, int qty, int buy_id, int sell_id) {
  };

  public record Order(int price, int qty, int id, Side side) {
  };

  public record MapEntry(int total_amount, List<Order> orders) {
  };

  public List<Trade> add_order(Order order) {
    List<Trade> trades = new ArrayList<>();
    while (full_trade(order)) {
      MapEntry entry = get_best_entry(opposite(order.side));
      List<Trade> all_trades = get_full_trades(order, entry.orders);
      pop_best(opposite(order.side));
      order = new Order(order.price, order.qty - entry.total_amount, order.id, order.side);
      trades.addAll(all_trades);
    }
    if (order.qty > 0 && partial_trade(order)) {
      MapEntry entry = get_best_entry(opposite(order.side));
      List<Order> orders = entry.orders;
      int total_amount = entry.total_amount;
      List<Order> take_orders = get_fraction_total(total_amount, orders);
      int take_amount = get_sum(take_orders);
      List<Trade> partial_trades = get_full_trades(order, take_orders);
      trades.addAll(partial_trades);
      List<Order> remaining = subtract_remaining(orders, take_orders);
      int remaining_total = get_sum(remaining);
      put_map(opposite(order.side), new MapEntry(remaining_total, remaining));
      pop_best(opposite(order.side));
      order = new Order(order.price, order.qty - take_amount, order.id, order.side);
    }
    if (order.qty > 0) {
      List<Order> tmp = new ArrayList<>();
      tmp.add(order);
      put_map(order.side, new MapEntry(order.qty, tmp));
    }
    return trades;
  }
}
