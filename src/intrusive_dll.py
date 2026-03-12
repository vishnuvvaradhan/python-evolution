"""
Day 6 — Intrusive Doubly Linked List (Order Queue)

Goal:
Implement a high-performance order queue using an intrusive doubly
linked list.

This structure is used inside price levels of order books to support:

    - O(1) insertion
    - O(1) cancellation
    - FIFO execution

Implement:

    class OrderNode
    class OrderQueue

OrderNode fields:
    order_id: str
    quantity: float
    prev: OrderNode | None
    next: OrderNode | None

OrderQueue methods:

    append(order_id: str, quantity: float) -> OrderNode
        - Add order to end of queue
        - Return the node created

    remove(node: OrderNode) -> None
        - Remove a node in O(1)

    popleft() -> OrderNode
        - Remove and return the first order (FIFO execution)

    __len__(self)

Constraints:

- All operations must be O(1)
- No Python list scanning
- Maintain head and tail pointers
- Maintain queue size

Target:
~80–120 lines

Mindset:
This queue could sit inside a price level of a matching engine
processing millions of orders per second.
"""


class OrderNode:
    
    __slots__ = ("order_id", "quantity", "next", "prev")
    
    def __init__(self, order_id: str, quantity: float):
        
        self.order_id: str = order_id
        self.quantity: float = quantity
        self.next: OrderNode | None = None
        self.prev: OrderNode | None = None
    
    def __str__(self) -> str:
        return self.order_id
        
    def __eq__(self, other: object) -> bool:
        
        if not isinstance(other, OrderNode):
            return NotImplemented
            
        return self.order_id == other.order_id
            
        
        
        
        


class OrderQueue:
    
    """
    doublelinked list
    hashmap: order_id -> OrderNode, to remove in constant time:
        1. Grab Node
        2. Grab Prev
        3. Grab Next
        4. Point Prev->Next = Next
        5. Point Next->Prev = Prev
        
    Append in constant time, we must have a reference to the end
    
    """
    
    def __init__(self):
        
        self.ref_map = dict()
        self.head: OrderNode | None = None
        self.tail: OrderNode | None  = None
        self.size = 0
    
        
    
    
    def append(self, order_id:str, quantity: float) -> OrderNode:
        
        if(order_id in self.ref_map):
            raise ValueError("Order Already Exists")
        
        #create order object
        order_to_insert = OrderNode(order_id= order_id, quantity = quantity)
        
        #insert into refrence_map
        self.ref_map[order_id] = order_to_insert
        
        
        if(self.size == 0):
            self.head = order_to_insert
            self.tail = order_to_insert
            self.size += 1
            return order_to_insert
        
        #needed for pylance, type check...
        if self.tail is None:
            raise RuntimeError("tail is None")
            
        self.tail.next = order_to_insert
        order_to_insert.prev = self.tail
        self.tail = order_to_insert
        self.size += 1
        

        return order_to_insert
        
        
    def pop_left(self) -> OrderNode:
            
        if(self.size == 0):
            raise IndexError("Size is 0: OrderQueue is empty")
            
            
        #runtime error to make sure we are returning correct type
        if self.head is None:
            raise RuntimeError("head is None")
            
        order_to_return = self.head 
            
        if(self.size == 1):
            self.head = None
            self.tail = None
            self.size -= 1 
            self.ref_map.pop(order_to_return.order_id)
            return order_to_return
            
        next_order = order_to_return.next
        
        if next_order is None:
            raise RuntimeError("Next is None")
            
        order_to_return.next = None
        
        next_order.prev = None
         
        self.head = next_order
        
        self.size -= 1 
        
        self.ref_map.pop(order_to_return.order_id, None)
        
        return order_to_return
            
        
    def __str__(self) -> str:
        
        ll: list = []
        
        cur = self.head
        
        while(cur):
            
            o_id = cur.order_id
            quant = cur.quantity
            str_node = f'(order_id={o_id}, quantity={quant})'
            
            ll.append(str_node)
            
            if (cur.next):
                ll.append("->")
            
            cur = cur.next
        
        return " ".join(ll)
        
    def pop_right(self) -> OrderNode:
        
         if(self.size == 0):
             raise IndexError("Size is 0: OrderQueue is empty")
             
             
         #runtime error to make sure we are returning correct type
         if self.tail is None:
             raise RuntimeError("head is None")
             
         order_to_return = self.tail
             
         if(self.size == 1):
             self.head = None
             self.tail = None
             self.size -= 1 
             self.ref_map.pop(order_to_return.order_id)
             return order_to_return
             
         prev_order = order_to_return.prev
         
         if prev_order is None:
             raise RuntimeError("Next is None")
        
        #not rlly needed if refcount is 0, memory is freed automatically, 
         order_to_return.prev = None
         
         prev_order.next = None
          
         self.tail = prev_order
         
         self.size -= 1 
         
         self.ref_map.pop(order_to_return.order_id, None)
         
         return order_to_return
        
        
        
        
    
    def remove(self, order: OrderNode) -> None:
        
        order_id = order.order_id
        
        if order_id not in self.ref_map:
            raise ValueError("Order Not in Queue")
            
        if(self.size == 1):
            self.head = None
            self.tail = None
            self.size -= 1
            self.ref_map.pop(order_id, None)
            return
            
        #use is, make sure same obj
        if(order is self.head):
            self.pop_left()
            return
        
        if(order is self.tail):
            self.pop_right()
            return 
            
        order_to_remove = self.ref_map.pop(order_id, None)
        
        prev_node = order_to_remove.prev
        next_node = order_to_remove.next
        
        prev_node.next = next_node
        next_node.prev = prev_node
        
        order_to_remove.prev = None
        order_to_remove.next = None
        
        self.size -= 1
        
            
    def __len__(self) -> int:
        return self.size
        
    def contains(self, order: OrderNode) -> bool:
        return order.order_id in self.ref_map
        
        


"""
========================
OrderQueue Test Cases
========================
"""

# Assume:
# q = OrderQueue()

# ------------------------
# 1. Append to empty queue
# ------------------------

q = OrderQueue()
node1 = q.append("A1", 10)

assert len(q) == 1
assert q.head == node1
assert q.tail == node1
assert node1.prev is None
assert node1.next is None

print("test1 passed")


# ------------------------
# 2. Append multiple orders
# ------------------------

node2 = q.append("A2", 20)
node3 = q.append("A3", 30)

assert len(q) == 3
assert q.head == node1
assert q.tail == node3

assert node1.next == node2
assert node2.prev == node1

assert node2.next == node3
assert node3.prev == node2
print("test2 passed")


# ------------------------
# 3. Remove head
# ------------------------

q.remove(node1)

assert len(q) == 2
assert q.head == node2
assert node2.prev is None
print("test3 passed")


# ------------------------
# 4. Remove tail
# ------------------------

q.remove(node3)

assert len(q) == 1
assert q.tail == node2
assert node2.next is None

print("test4 passed")



# ------------------------
# 5. Remove only node
# ------------------------

q.remove(node2)

assert len(q) == 0
assert q.head is None
assert q.tail is None
print("test5 passed")


# ------------------------
# 6. FIFO pop left
# ------------------------

q = OrderQueue()

n1 = q.append("B1", 10)
n2 = q.append("B2", 20)
n3 = q.append("B3", 30)

node = q.pop_left()

assert node.order_id == "B1"
assert len(q) == 2
assert q.head == n2
assert n2.prev is None

print("test6 passed")


# ------------------------
# 7. pop left until empty
# ------------------------

q.pop_left()
q.pop_left()

assert len(q) == 0
assert q.head is None
assert q.tail is None

print("test7 passed")


# ------------------------
# 8. pop left from empty queue
# ------------------------

q = OrderQueue()

try:
    q.pop_left()
    assert False
except IndexError:
    pass
    
print("test8 passed")


# ------------------------
# 9. pop right
# ------------------------

q = OrderQueue()

n1 = q.append("C1", 10)
n2 = q.append("C2", 20)
n3 = q.append("C3", 30)

node = q.pop_right()

assert node.order_id == "C3"
assert q.tail == n2
assert n2.next is None
assert len(q) == 2

print("test9 passed")


# ------------------------
# 10. pop right until empty
# ------------------------

q.pop_right()
q.pop_right()

assert len(q) == 0
assert q.head is None
assert q.tail is None

print("test10 passed")


# ------------------------
# 11. Remove middle node
# ------------------------

q = OrderQueue()

n1 = q.append("D1", 10)
n2 = q.append("D2", 20)
n3 = q.append("D3", 30)
n4 = q.append("D4", 40)

print(q)

q.remove(n3)

assert len(q) == 3
assert n2.next == n4
assert n4.prev == n2


print("test11 passed")

# ------------------------
# 12. Remove head with multiple nodes
# ------------------------

q.remove(n1)

assert q.head == n2
assert n2.prev is None

print("test12 passed")


# ------------------------
# 13. Remove tail with multiple nodes
# ------------------------

q.remove(n4)

assert q.tail == n2
assert n2.next is None



print("test13 passed")


# ------------------------
# 14. Duplicate order_id detection (if implemented)
# ------------------------

q = OrderQueue()
q.append("E1", 10)

try:
    q.append("E1", 20)
    assert False
except ValueError:
    pass


print("test14 passed")

# ------------------------
# 15. Size integrity
# ------------------------

q = OrderQueue()

for i in range(10):
    q.append(f"O{i}", i)

assert len(q) == 10

for _ in range(10):
    q.pop_left()

assert len(q) == 0


print("test15 passed")


# ------------------------
# 16. Pointer integrity after many operations
# ------------------------

q = OrderQueue()

nodes = []
for i in range(5):
    nodes.append(q.append(f"T{i}", i))

q.remove(nodes[2])
q.remove(nodes[0])
q.remove(nodes[4])

assert len(q) == 2
assert q.head == nodes[1]
assert q.tail == nodes[3]
assert nodes[1].next == nodes[3]
assert nodes[3].prev == nodes[1]

print("test16 passed")
            
        
   


"""
========================
Day 6 Review — Intrusive Order Queue
========================

Overall Grade: A

This implementation constructs a doubly linked list order queue
with O(1) append, cancel, and FIFO execution using an intrusive
node structure and an order_id → node lookup table.

------------------------
Strengths
------------------------

1. Correct doubly-linked list implementation with head/tail pointers.

2. O(1) cancellation via hashmap lookup.

3. Proper handling of edge cases:
   - empty queue
   - single-node queue
   - head removal
   - tail removal
   - middle removal

4. Efficient append logic.

5. Use of __slots__ for memory efficiency.

6. Excellent test coverage verifying pointer integrity.

------------------------
Complexity
------------------------

append      O(1)
remove      O(1)
pop_left    O(1)
pop_right   O(1)
contains    O(1)

Memory: O(n) nodes + hashmap.

------------------------
Engineering Insight
------------------------

This structure mirrors the design used in many matching engines
for price levels:

    price_level
        └── intrusive doubly linked list of orders

Cancellation is performed by mapping order_id → node,
allowing constant-time unlinking without scanning the queue.

A strong systems-level implementation.
"""
        
        
    
    
    
        
        
        
        
        
        
        
        