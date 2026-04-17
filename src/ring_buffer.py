"""
Day 7 — Lock-Free Style Market Data Ring Buffer

Goal:
Implement a fixed-size ring buffer optimized for market data events.

The buffer must:

    - Preallocate memory
    - Avoid runtime allocations
    - Use circular indexing
    - Maintain predictable latency

This pattern is used in trading systems to process millions of
events per second without triggering garbage collection.

Implement:

    class MarketEvent
    class RingBuffer

MarketEvent fields:
    price: float
    size: float
    timestamp: int

RingBuffer methods:

    __init__(self, capacity: int)

        - Preallocate all storage
        - capacity must be power of two

    push(event: MarketEvent) -> None

        - Write event to buffer
        - Overwrite oldest element if full

    latest() -> MarketEvent | None

        - Return most recent event

    get(index: int) -> MarketEvent

        - Retrieve event relative to head
        - 0 = oldest

    __len__()

Constraints:

- No list append
- Preallocate memory
- All operations O(1)
- No dynamic allocations after initialization

Target:
~120 lines

Mindset:
Imagine this receives millions of market ticks from a websocket
feed and feeds them into signal engines.
"""
import time


"""
head should point to the oldest element/index.
if capacity == size we can consume the head and increment it
head and tail

[1,2,3,4]

size = 4
head = 0

size % capacity = 0

self.tail = self.tail % capacity



"""



class MarketEvent:
    
    __slots__ = ("price", "size", "timestamp")
    
    def __init__(self, price:float, size:int):
        
        self.price = price
        self.size = size
        self.timestamp = time.monotonic_ns()
    
        
        

class RingBuffer:
    
    def __init__(self, capacity: int):
        
        if capacity <= 0 or (capacity & (capacity - 1)) != 0:
            raise ValueError("Capacity Must be a Power of 2")
            
        self.capacity = capacity
        self.buffer: list[MarketEvent | None]= [None] * capacity
        self.head: int = 0
        self.tail = 0
        self.size: int = 0

       
        
    def latest(self):
        '''
        commented out for tests
        if(self.size == 0):
            raise IndexError("Size is 0")
        '''
        
        if(self.size == 0):
            return None
        
            
        return self.buffer[(self.tail-1) & (self.capacity - 1)]
    
    
    def get(self, index:int):
        
        if(self.size == 0 or index >= self.size):
           raise IndexError("Index out of Range")
    
        idx = (self.head + index) & (self.capacity - 1)
        
        return self.buffer[idx]
        
    def push(self, market_event: MarketEvent):
        
        if(self.size == self.capacity):
            self.head += 1
            #AND rax, rbx, so one cpu cycle rather than mod
            self.head = self.head & (self.capacity - 1)
        else: 
            self.size += 1
        
        index_to_insert = self.tail
        self.buffer[index_to_insert] = market_event   
        self.tail += 1    
        self.tail = self.tail & (self.capacity - 1)
            
 
        
    def __len__(self) -> int:
        return self.size
        
    
    
        
    
        
    
        
        
    
        
        
    
    
"""
========================
RingBuffer Test Suite
========================
"""


def make_event(price, size):
    return MarketEvent(price, size)


# ------------------------
# 1. Initialization
# ------------------------

rb = RingBuffer(8)

assert len(rb) == 0
assert rb.latest() is None

print("test1 passed")


# ------------------------
# 2. Single push
# ------------------------

e1 = make_event(100, 5)
rb.push(e1)

assert len(rb) == 1
assert rb.latest() == e1
assert rb.get(0) == e1

print("test2 passed")


# ------------------------
# 3. Multiple pushes
# ------------------------

e2 = make_event(101, 3)
e3 = make_event(102, 2)

rb.push(e2)
rb.push(e3)

assert len(rb) == 3
assert rb.get(0) == e1
assert rb.get(1) == e2
assert rb.get(2) == e3
assert rb.latest() == e3

print("test3 passed")


# ------------------------
# 4. Fill buffer to capacity
# ------------------------

rb = RingBuffer(4)

events = []
for i in range(4):
    ev = make_event(100 + i, 1)
    events.append(ev)
    rb.push(ev)

assert len(rb) == 4
assert rb.get(0) == events[0]
assert rb.get(3) == events[3]

print("test4 passed")


# ------------------------
# 5. Overwrite oldest element
# ------------------------

e5 = make_event(200, 1)
rb.push(e5)

# Oldest element should now be events[1]
assert len(rb) == 4
assert rb.get(0) == events[1]
assert rb.get(3) == e5

print("test5 passed")


# ------------------------
# 6. Multiple overwrites
# ------------------------

rb.push(make_event(300, 1))
rb.push(make_event(400, 1))

assert len(rb) == 4
assert rb.latest().price == 400

print("test6 passed")


# ------------------------
# 7. Wraparound indexing
# ------------------------

rb = RingBuffer(8)

for i in range(20):
    rb.push(make_event(i, 1))

assert len(rb) == 8

# last 8 events should remain
for i in range(8):
    ev = rb.get(i)
    assert ev.price == 12 + i

print("test7 passed")


# ------------------------
# 8. latest() correctness
# ------------------------

rb = RingBuffer(4)

rb.push(make_event(10, 1))
rb.push(make_event(20, 1))
rb.push(make_event(30, 1))

assert rb.latest().price == 30

rb.push(make_event(40, 1))
assert rb.latest().price == 40

print("test8 passed")


# ------------------------
# 9. get() out-of-range
# ------------------------

rb = RingBuffer(4)

rb.push(make_event(1,1))

try:
    rb.get(2)
    assert False
except IndexError:
    pass

print("test9 passed")


# ------------------------
# 10. Empty buffer get
# ------------------------

rb = RingBuffer(4)

try:
    rb.get(0)
    assert False
except IndexError:
    pass

print("test10 passed")


# ------------------------
# 11. Power-of-two validation
# ------------------------

try:
    RingBuffer(10)
    assert False
except ValueError:
    pass

print("test11 passed")


# ------------------------
# 12. Heavy stress test
# ------------------------

rb = RingBuffer(16)

for i in range(10000):
    rb.push(make_event(i, 1))

assert len(rb) == 16

# ensure last events are correct
for i in range(16):
    ev = rb.get(i)
    if ev is None:
        raise RuntimeError("Ev is None")
    assert ev.price == 10000 - 16 + i

print("test12 passed")


print("\nALL TESTS PASSED")



"""
========================
Day 7 Review — Market Data Ring Buffer
========================

Overall Grade: A+

This implementation builds a fixed-capacity market data ring buffer with
correct wraparound semantics, constant-time operations, and predictable
memory usage. The structure closely resembles event buffers used in
high-performance trading systems.

------------------------
Strengths
------------------------

1. Preallocated storage
   The buffer is created using a fixed-size list, preventing dynamic
   resizing and ensuring predictable memory behavior.

2. Power-of-two capacity enforcement
   The constructor correctly validates that capacity is both positive
   and a power of two using the classic bit trick:

       capacity & (capacity - 1) == 0

3. Efficient wraparound indexing
   All circular indexing uses bit masking instead of modulo:

       index & (capacity - 1)

   which mirrors techniques used in low-latency systems such as ring
   buffers and event queues.

4. Correct FIFO overwrite semantics
   When the buffer is full, pushing a new event advances the head and
   overwrites the oldest event.

5. Correct latest() implementation
   The most recent element is retrieved safely using masked indexing:

       (tail - 1) & (capacity - 1)

   ensuring correct behavior even when the buffer wraps around.

6. Clean logical indexing
   get(index) maps logical order (oldest → newest) onto the circular
   storage correctly using masked indexing.

------------------------
Complexity
------------------------

push        O(1)
get         O(1)
latest      O(1)
len         O(1)

Memory usage: O(capacity)

No dynamic allocation occurs inside the buffer itself.

------------------------
Engineering Insight
------------------------

This structure mirrors ring buffers used in:

    • market data ingestion pipelines
    • packet processing systems
    • low-latency event queues
    • the LMAX Disruptor architecture

Using power-of-two capacities allows modulo operations to be replaced
with fast bit masking, improving throughput and reducing CPU cost in
high-frequency systems.

Strong implementation with production-style design considerations.
"""
