import java.util.*;

class OrderBook {
  public enum Side {
    BUY, SELL
  };

  public record Trade(int price, int qty, int buy_id, int sell_id) {
  };

  public record Order(int price, int qty, int id, Side side) {
  };

  public record Entry(int price, int total_qty, Set<Order> orders, boolean in_heap) {
  };

  public class OperationSide {
    PriorityQueue<Integer> heap; // heap of prices
    Map<Integer, Entry> orders; // hashmap from price to entries
    HashMap<Integer, Order> id_obj; // hashmap from id to price

    public OperationSide(boolean sell_side) {
      if (sell_side) {
        heap = new PriorityQueue<>();
      } else {
        heap = new PriorityQueue<>(Comparator.reverseOrder());
      }
      orders = new HashMap<>();
      id_obj = new HashMap<>();
    }

    void disable_heap_value(int price) {
      Entry entry = orders.get(price);
      orders.put(price, new Entry(entry.price, entry.total_qty, entry.orders, false));
    }

    Integer get_best_price() {
      while (heap.size() > 0 && orders.get(heap.peek()).total_qty == 0) {
        int val = heap.poll();
        disable_heap_value(val);
      }
      if (heap.size() == 0) {
        return null;
      }
      return heap.peek();
    }

    public Entry peek() {
      Integer best_price = get_best_price();
      if (best_price == null) {
        return null;
      }
      return orders.get(best_price);
    }

    public Entry pop() {
      Integer best_price = get_best_price();
      if (best_price == null) {
        return null;
      }
      heap.poll();
      disable_heap_value(best_price);
      Entry entry = orders.get(best_price);
      orders.remove(best_price);
      return entry;
    }

    public void put_data(int price, Set<Order> add_orders) {
      Entry entry = orders.getOrDefault(price, new Entry(price, 0, new HashSet<>(), false));
      if (!entry.in_heap) {
        heap.add(price);
      }
      int total_amount = 0;
      for (Order ord : add_orders) {
        total_amount += ord.qty;
        id_obj.put(ord.id, ord);
      }
      entry.orders.addAll(add_orders);
      orders.put(price, new Entry(price, total_amount + entry.total_qty, entry.orders, true));
    }

    public void delete_order(int id) {
      if (!id_obj.containsKey(id)) {
        return;
      }
      Order obj = id_obj.get(id);
      int price = obj.price;
      if (!orders.containsKey(price) || !orders.get(price).orders.contains(obj)) {
        return;
      }
      Entry entry = orders.get(price);
      entry.orders.remove(obj);
      orders.put(price, new Entry(entry.price, entry.total_qty - obj.qty, entry.orders, entry.in_heap));
    }
  }

  boolean fulfill(Order order) {
    if (order.side == Side.SELL) {
      Entry best_entry = buy_side.peek();
      if (best_entry == null) {
        return false;
      }
      if (best_entry.price >= order.price && order.qty >= best_entry.total_qty) {
        return true;
      }
      return false;
    } else {
      Entry best_entry = sell_side.peek();
      if (best_entry == null) {
        return false;
      }
      if (best_entry.price <= order.price && order.qty >= best_entry.total_qty) {
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

  Entry pop_best(Side side) {
    if (side == Side.SELL) {
      return sell_side.pop();
    }
    return buy_side.pop();
  }

  List<Trade> convert_trades(Order order, Set<Order> orders) {
    List<Trade> out = new ArrayList<>();
    for (Order order_tmp : orders) {
      if (order_tmp.qty == 0) {
        continue;
      }
      if (order.side == Side.SELL) {
        out.add(new Trade(order_tmp.price, order_tmp.qty, order_tmp.id, order.id));
      } else {
        out.add(new Trade(order_tmp.price, order_tmp.qty, order.id, order_tmp.id));
      }
    }
    return out;
  }

  boolean partial_fulfill(Order order) {
    if (order.side == Side.BUY) {
      Entry best_option = sell_side.peek();
      if (best_option == null) {
        return false;
      }
      if (best_option.price <= order.price) {
        return true;
      }
      return false;
    } else {
      Entry best_option = buy_side.peek();
      if (best_option == null) {
        return false;
      }
      if (best_option.price >= order.price) {
        return true;
      }
      return false;
    }
  }

  Set<Order> get_to_subtract(Order order, Entry best_entry) {
    int total_amount = best_entry.total_qty;
    int total_covered = 0;
    for (Order ord : best_entry.orders) {
      int to_add = order.qty * ord.qty / total_amount;
      total_covered += to_add;
    }
    int remaining = order.qty - total_covered;
    List<Order> all_ords = new ArrayList<>(best_entry.orders);
    all_ords.sort(Comparator.comparingInt(Order::qty).reversed().thenComparingInt(Order::id));
    Set<Integer> ids = new HashSet<>();
    for (int i = 0; i < remaining; i++) {
      ids.add(all_ords.get(i).id);
    }
    Set<Order> out = new HashSet<>();
    for (Order ord : best_entry.orders) {
      int to_add = order.qty * ord.qty / total_amount;
      if (ids.contains(ord.id)) {
        to_add += 1;
      }
      if (to_add == 0) {
        continue;
      }
      out.add(new Order(ord.price, to_add, ord.id, ord.side));
    }
    return out;
  }

  Set<Order> get_remaining(Set<Order> to_subtract, Set<Order> total) {
    Set<Order> out = new HashSet<>();
    Map<Integer, Integer> id_qty = new HashMap<>();
    for (Order ord : to_subtract) {
      id_qty.put(ord.id, ord.qty);
    }
    for (Order ord : total) {
      int replace = ord.qty;
      if (id_qty.containsKey(ord.id)) {
        replace -= id_qty.get(ord.id);
      }
      if (replace == 0) {
        continue;
      }
      out.add(new Order(ord.price, replace, ord.id, ord.side));
    }
    return out;
  }

  public List<Trade> add_order(int price, int qty, int id, Side side) {
    List<Trade> all_trades = new ArrayList<>();
    Order order = new Order(price, qty, id, side);
    while (fulfill(order)) {
      Entry best_entry = pop_best(opposite(order.side));
      List<Trade> trades = convert_trades(order, best_entry.orders);
      order = new Order(order.price, order.qty - best_entry.total_qty, order.id, order.side);
      all_trades.addAll(trades);
    }
    if (order.qty > 0 && partial_fulfill(order)) {
      Entry best_entry = pop_best(opposite(order.side));
      Set<Order> to_subtract = get_to_subtract(order, best_entry);
      Set<Order> remaining = get_remaining(to_subtract, best_entry.orders);
      List<Trade> trades = convert_trades(order, to_subtract);
      all_trades.addAll(trades);
      order = new Order(order.price, 0, order.id, order.side);
      put_data(best_entry.price, remaining);
    }
    if (order.qty > 0) {
      Set<Order> to_add = new HashSet<>();
      to_add.add(order);
      put_data(order.price, to_add);
    }
    return all_trades;
  }
}
