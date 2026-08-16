#include <set>
#include <vector>
using namespace std;
struct Trade {
  int taker_id;
  int maker_id;
  int price;
  int qty;
};

enum class Side { SELL, BUY };

struct Order {
  int id;
  Side side;
  int price;
  int qty;
};

template <typename Compare>
class Comparator {
 public:
  bool operator()(Order a, Order b) { return _comp(a.price, b.price); }

 private:
  Compare _comp;
};

class TemplateMap {
 public:
  bool valid(Order a) {}

 private:
  set<Order, Comparator<less<int>>> map_buy;
  set<Order, Comparator<greater<int>>> map_sell;
};

class OrderBook {
 public:
  vector<Trade> add_order(Order order) {
    TemplateMap map = order.side == Side::SELL ? buy_side : sell_side;
  }

 private:
  TemplateMap<less<int>> buy_side;
  TemplateMap<greater<int>> sell_side;
};
