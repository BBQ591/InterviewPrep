import java.util.*;



class Solution {
  public enum Side {
    SELL,
    BUY
  }
  public record Order(int price, Side side, int qty, int id) {}
  public record Trade(int price, int buy_id, int sell_id, int qty) {}

  PriorityQueue<Order> sell_side;
  PriorityQueue<Order> buy_side;
  public Solution() {
    this.sell_side = new PriorityQueue<>((a, b) -> (a.price == b.price) ? a.id - b.id: a.price - b.price);
    this.buy_side = new PriorityQueue<>((a, b) -> (a.price == b.price) ? a.id - b.id : b.price - a.price);
  }

  public boolean try_fulfill(Order order) {
    if (order.qty == 0) {
      return false;
    }
    if (order.side == Side.SELL) {
      if (this.buy_side.size() == 0) {
        return false;
      }
      return order.price <= this.buy_side.peek().price;
    }
    if (this.sell_side.size() == 0) {
      return false;
    }
    return order.price >= this.sell_side.peek().price;
  }

  public Trade fulfill(Order order) {
    if (order.side == Side.SELL) {
      Order best_buy= this.buy_side.poll();
      int qty = Math.min(best_buy.qty, order.qty);
      int sell_id = order.id;
      int buy_id = best_buy.id;
      int price = best_buy.price;
      if (best_buy.qty - qty > 0) {
        Order remaining_fulfill = new Order(best_buy.price, best_buy.side, best_buy.qty - qty, best_buy.id);
        this.buy_side.add(remaining_fulfill);
      }
      return new Trade(price, buy_id, sell_id, qty);
    }
    Order best_sell= this.sell_side.poll();
    int qty = Math.min(best_sell.qty, order.qty);
    int buy_id = order.id;
    int sell_id = best_sell.id;
    int price = best_sell.price;
    if (best_sell.qty - qty > 0) {
      Order remaining_fulfill = new Order(best_sell.price, best_sell.side, best_sell.qty - qty, best_sell.id);
      this.sell_side.add(remaining_fulfill);
    }
    return new Trade(price, buy_id, sell_id, qty);
  }

  public void add_remaining(Order order) {
    if (order.side == Side.SELL) {
      this.sell_side.add(order);
    }
    else {
      this.buy_side.add(order);
    }
  }

  public List<Trade> AddOrder(Order order) {
    List<Trade> trades = new ArrayList<>();
    while (try_fulfill(order)) {
      Trade trade = fulfill(order);
      Order new_order = new Order(order.price, order.side, order.qty - trade.qty, order.id);
      order = new_order;
      trades.add(trade);
    }
    if (order.qty > 0) {
      add_remaining(order);
    }
    return trades;
  }
}
