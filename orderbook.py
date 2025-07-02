#!/usr/bin/env python
# coding: utf-8

# In[9]:


from collections import defaultdict
import random
import string
class OrderBook:
    def __init__(self):
        self.bids = defaultdict(list)   
        self.asks = defaultdict(list)   

    def add_limit_order(self, side, price, size, order_id):
        order = {'id': order_id, 'size': size}
        if side == 'buy':
            self.bids[price].append(order)
        else:
            self.asks[price].append(order)

    def match_market_order(self, side, quantity):
        trades = []
        if side == 'buy':  
            price_levels = sorted(self.asks.keys())
            book_side = self.asks
        else:  
            price_levels = sorted(self.bids.keys(), reverse=True)
            book_side = self.bids

        for price in price_levels:
            orders = book_side[price]
            while orders and quantity > 0:
                order = orders[0]
                trade_qty = min(quantity, order['size'])
                trades.append({'price': price, 'quantity': trade_qty, 'order_id': order['id']})
                order['size'] -= trade_qty
                quantity -= trade_qty
                if order['size'] == 0:
                    orders.pop(0)
            if not orders:
                del book_side[price]
            if quantity == 0:
                break

        return trades

    def show_orderbook_snapshot(self, depth=5):
        print("=== ORDER BOOK SNAPSHOT ===")

        ask_prices = sorted(self.asks.keys())[:depth]
        bid_prices = sorted(self.bids.keys(), reverse=True)[:depth]

        print("\n  Ask Side")
        print("  Price      Quantity")
        for price in ask_prices:
            total = sum(o['size'] for o in self.asks[price])
            print(f"  {price:.2f}      {total}")

        print("\n  Bid Side")
        print("  Price      Quantity")
        for price in bid_prices:
            total = sum(o['size'] for o in self.bids[price])
            print(f"  {price:.2f}      {total}")
        print("===========================\n")


def generate_random_orders(orderbook, num_orders=10):
    for i in range(num_orders):
        side = random.choice(['buy', 'sell'])
        price = round(random.uniform(95, 105), 2)
        size = random.randint(10, 200)
        order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        orderbook.add_limit_order(side, price, size, order_id)



# In[11]:


def main():
    ob = OrderBook()
    generate_random_orders(ob, 20)
    ob.show_orderbook_snapshot()

    ob.show_orderbook_snapshot()

    print(">>> Market buy order: 180")
    trades = ob.match_market_order('buy', 180)
    for trade in trades:
        print(f"Filled {trade['quantity']} @ {trade['price']} from order {trade['order_id']}")

    ob.show_orderbook_snapshot()

    print(">>> Market sell order: 250")
    trades = ob.match_market_order('sell', 250)
    for trade in trades:
        print(f"Filled {trade['quantity']} @ {trade['price']} from order {trade['order_id']}")

    ob.show_orderbook_snapshot()


if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




