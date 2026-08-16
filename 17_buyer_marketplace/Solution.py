from typing import List


class Item:
    seller_name: str
    buyer_name: str | None
    item_name: str
    price: int


class Datastore:
    def put(self, item: Item) -> None:
        pass

    def get_all(self) -> List[Item]:
        pass


class BuyerMarketplace:
    def __init__(self, datastore: Datastore):
        self.datastore = datastore
        self.start = len(datastore)

    def buy_items(self, buyer_name, items: dict[str, int]) -> dict[str, Item]:
        all_items = self.datastore.get_all()
        fulfilled = {}
        for i in range(len(all_items) - 1, -1, -1):
            name = all_items[i].item_name
            buyer_name = all_items[i].buyer_name
            price = all_items[i].price
            if buyer_name is None and name in items:
                if name not in fulfilled and price <= items[name]:
                    fulfilled[name] = all_items[i]
                else:
                    tmp_item = fulfilled[name]
                    if price < tmp_item.price:
                        fulfilled[name] = all_items[i]

        for item in fulfilled:
            item.buyer_name = buyer_name
            self.datastore.put(item)

        return fulfilled

    def get_purchased(self, buyer, all_items) -> dict[Item]:
        pass

    def replay(self):


    def remove_buyers(self, buyers_to_exclude: set[str]) -> dict[str, int]:
        all_items = self.datastore.get_all()
        removed_items = {}
        for buyer in buyers_to_exclude:
            removed_items |= self.get_purchased(buyer, all_items)

        for item in removed_items:
            item.buyer = None

        self.replay()
