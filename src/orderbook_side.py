"""
Day 2 — Order Book Side (Price-Time Priority)

Goal:
Implement one side of a limit order book (bid or ask).

Implement:

    class OrderBookSide:

Constructor:
    __init__(self, side: str)
        - side must be either "bid" or "ask"
        - raise ValueError otherwise

Required Methods:

    add(order_id: str, price: float, quantity: float) -> None
        - Add a new limit order
        - Enforce price-time priority
        - Orders at same price execute FIFO

    cancel(order_id: str) -> None
        - Remove order if it exists
        - Must be O(1) or O(log n)

    best_price() -> float
        - Return best bid (highest) or best ask (lowest)
        - Raise ValueError if empty

    total_quantity_at_price(price: float) -> float

Constraints:
    - No external libraries
    - No pandas / numpy
    - Must be efficient
    - Cannot scan entire book for each operation

Design Expectations:
    - Separate price levels from order storage
    - Maintain price-time priority
    - No duplicated state
    - Use appropriate data structures
    - Clean internal representation

Target:
    ~80–120 lines
    This is real infra.
"""



"""
Use RB Tree (sorted_map in python) as canceling an order would be tricky w heap/hm combo

Bid -> greatest to least -> price at which someone is willing to buy
Ask -> least to greatest -> price at which someone is willing to sell

Since this orderbook is only one sided, no need to worry about orderbooks "crossing"

"""
from enum import Enum

from sortedcontainers import sorteddict
from collections import deque



class Side(Enum):
    BID = 0
    ASK = 1


class Order:
    """
    Represents an Order
    
    """

    def __init__(self, order_id: str, side: Side, price: float, quantity: float):

        self.order_id : str = order_id
        self.price: float = price
        self.side: Side = side
        self.quantity: float = quantity

    
class pricelevel:

    def __init__(self, price: float):
        self.price :float = price
        self.volume: int = 0
        self.queue : deque= deque()
        self.size: int = 0

    def add_order(self, order: Order) -> None:
        self.queue.append(order)
        self.volume += order.quantity
        self.size += 1 

    def remove_order(self, order: Order) -> None:
        
        try:
            self.queue.remove(order)
        #if item not in deque a value error is thrown
        except ValueError:
            raise ValueError("Order not in price_level")
        
        self.volume -= order.quantity
        self.size -= 1 


    def get_size(self) -> int:
        return self.size
    

    def get_volume(self) -> int:
        return self.volume
    

class Orderbook:

    def __init__(self, side: Side):

        if side != Side.BID and side != Side.ASK:
            raise ValueError("enter Side object/enum: Side.BUY || Side.ASK")
        
        self.side = side

        if self.side ==  Side.BID:
            self.orderbook = sorteddict(lambda x: -x)
        else:
            self.orderbook = sorteddict()



    def add(self, order_id: str, price: float, quantity: float) -> None:
        """
        Add an order to the orderbook
        
        """

        order = Order(order_id, self.side, price, quantity)

        #adds order O(logn)
        self.orderbook.setdefault(price, pricelevel()).add_order(order)

    
    def cancel_order(self, order: Order) -> None:

        order_price: float = order.price

        price_level: pricelevel = self.orderbook.pop(order_price, None)

        if not price_level:
            raise ValueError("nonexistent order: check price_level")
        
        price_level.remove_order(order)

        if price_level.get_size() != 0:

            self.orderbook[order_price] = price_level


    def get_best_price(self) -> float:

        if len(self.orderbook) == 0:
            raise ValueError("orderbook is empty")

        return self.orderbook.peekitem(0)[0]
    

    def total_quantity_at_price(self, price: float) -> int:

        price_level: pricelevel = self.orderbook.get(price, None)

        if not price_level:
            raise ValueError("nonexistent: check price_level")
        
        return price_level.get_volume()
        
    




"""
========================
Day 2 Review — One-Sided OrderBook
========================

Overall Grade: B+

Still not production-grade due to cancel complexity.

------------------------
Good Things
------------------------


1. Side validation logic is correct.

2. Best price retrieval is clean and efficient.

3. Overall structural model remains solid:
   price -> PriceLevel -> FIFO queue.

------------------------
Remaining Structural Issues
------------------------

1. Cancel is still O(n) at the price level.

   deque.remove(order) scans the entire queue.
   In real markets, price levels may contain thousands of orders.
   Production systems require O(1) cancel via:
       - order_id -> node map
       - intrusive doubly linked list

   This is the primary blocker to A-level infra quality.

2. cancel_order still mutates the tree unnecessarily.

   You pop the entire price level before editing it.
   Tree structure should only change if the level becomes empty.

3. API realism.

   cancel_order takes an Order object.
   Real systems cancel by order_id.
   You need a global order index.

4. Redundant state.

   size duplicates len(self.queue).
   volume is fine to store (aggregate), but must be authoritative.

5. Naming / typing polish.

   - pricelevel should be PriceLevel.
   - volume annotated as int but quantity is float.

------------------------
Complexity Assessment
------------------------

Add: O(log n)
Best price: O(1)
Cancel: O(n) within price level  <-- still not acceptable for production
Volume lookup: O(log n)

------------------------
Engineering Level
------------------------

Conceptual understanding: 9 / 10
Structural cleanliness:   7 / 10
Production realism:       6.5 / 10

You are clearly thinking in systems terms now.

The only real missing piece is:
    direct order_id indexing + O(1) unlink.

Once that’s implemented,
this becomes legitimately strong infra code.

Tomorrow’s refactor will push this into A range.

Good progression.
"""




        













    







