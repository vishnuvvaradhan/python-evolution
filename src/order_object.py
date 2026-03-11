"""
Day 4 — Memory-Optimized Order Object (__slots__)

Goal:
Implement a lightweight Order object optimized for memory usage by
removing the default per-instance __dict__.

In trading systems, millions of order objects may exist simultaneously,
so reducing per-object overhead can significantly improve memory usage
and cache locality.

Requirements:

1. Implement:

       class Order:

2. Use __slots__ to eliminate the instance __dict__.

3. Fields the object must store:

       order_id: str
       price: float
       quantity: float
       side: str

4. Constructor:

       __init__(self, order_id: str, price: float, quantity: float, side: str)

   Initializes the object fields.

5. order_id must be read-only after initialization.
   Attempting to modify it should raise an error.

6. Implement __repr__.

   Example output:

       Order(order_id='A123', price=101.25, quantity=5.0, side='BUY')

7. Implement __eq__.

   Two orders should be considered equal if their order_id matches.

   Example:

       Order("A1", 100, 1, "BUY") == Order("A1", 200, 10, "SELL")

   should return True.

Constraints:

- Do NOT use dataclasses
- Do NOT use attrs
- No external libraries
- Do NOT use __dict__
- Must use __slots__

Target:
~40–60 lines of code.

Mindset:
Imagine a backtest creating millions of Order objects.
Memory overhead per object matters.
"""



from enum import Enum

class Side(Enum):
    BUY = 0
    SELL = 1



class Order:
    
    #effcient memory allocation, rids the pyobject/object of using a dictionary to store instance attributes 
    __slots__ = ("_order_id", "price", "quantity", "side")
    
    def __init__(self, order_id:str, price:float, quantity:float, side: Side):
        
        if (price < 0 or quantity < 0):
            raise(ValueError("Price/Quantity Must Be Greater Than 0"))
            
        if (side != Side.BUY and side != Side.SELL):
            raise(ValueError("Side Must be SELL or BUY"))
            
                    
        self._order_id = order_id
        self.price = price
        self.quantity = quantity
        self.side = side
        
    
    
    #to string
    def __repr__(self) -> str:
        return f"Order(order = {self._order_id}, price = {self.price}, quantity = {self.quantity}, side = {self.side})"
        
    
    
    def __eq__(self, other: object) -> bool:
        
        if not isinstance(other ,Order):
            #will first try reverse comparison then will finally return false, because reverse could have a check implemented for obj ur comparing.
            return NotImplemented
            
        return self._order_id == other._order_id
        
    #lets a method behave like an attribute.
    @property
    def order_id(self):
        return self._order_id
        
        
        
        



"""
========================
Day 4 Review — Slotted Order Object (Revised)
========================

Overall Grade: A

This revision shows strong understanding of Python internals and object
design. The implementation now includes validation, correct equality
protocol usage, and proper slot-based memory optimization.

------------------------
What Was Done Well
------------------------

1. __slots__ usage
   Correctly removes the per-instance __dict__, reducing memory overhead.
   This is important in systems that may create millions of objects.

2. Constructor validation
   Price and quantity checks prevent invalid order states.

3. Equality protocol
   __eq__ correctly checks type and returns NotImplemented when the
   comparison is unsupported, allowing Python's fallback mechanism.

4. Read-only order_id
   Using a property ensures order_id cannot be modified through the
   public API while still allowing internal storage.

5. Clean object representation
   __repr__ provides useful debugging output.

------------------------
Minor Improvements
------------------------

1. Validation style
   Prefer:

       if price <= 0 or quantity <= 0:

   since zero-price or zero-quantity orders are usually invalid.

2. Enum validation
   Instead of:

       if side != Side.BUY and side != Side.SELL:

   prefer:

       if not isinstance(side, Side):

   This protects against invalid types.

3. __repr__ formatting
   Slightly more conventional representation:

       Order(order_id='A1', price=100.0, quantity=5.0, side=Side.BUY)

4. Style improvement
   Avoid parentheses around if conditions in Python:

       if price < 0:

   not

       if (price < 0):

------------------------
Complexity / Performance
------------------------

Attribute access: O(1)
Memory footprint: reduced due to __slots__
No per-instance dictionary allocation

------------------------
Engineering Notes
------------------------

This pattern is common in performance-sensitive Python systems such as:

- trading engines
- backtest frameworks
- market data pipelines

It demonstrates understanding of:

- Python object memory layout
- descriptor usage via @property
- rich comparison protocol
- defensive object construction

Strong work.
"""


        
        
        
        
        
        