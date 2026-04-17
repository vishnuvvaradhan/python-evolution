"""
Day 8 — Object Pool for Market Events

Goal:
Implement a fixed-size object pool for MarketEvent objects so that
events can be reused instead of allocated repeatedly.

Why this matters:
In low-latency trading systems, repeated object allocation creates
GC pressure and latency instability. A pool lets us recycle objects
and keep runtime behavior more predictable.

Implement:

    class MarketEvent
    class EventPool

MarketEvent fields:
    price: float
    size: float
    timestamp: int

EventPool methods:

    __init__(self, capacity: int)
        - Preallocate exactly `capacity` MarketEvent objects
        - No allocations should happen after initialization

    acquire() -> MarketEvent
        - Return an available MarketEvent from the pool
        - Raise IndexError if pool is exhausted

    release(event: MarketEvent) -> None
        - Return an event object back to the pool
        - Raise ValueError if event did not come from this pool
        - Raise ValueError if event is released twice

    available() -> int
        - Return number of currently free objects

Constraints:
- O(1) acquire
- O(1) release
- No dynamic allocations after __init__
- Must track which objects are in use vs free
- Keep the design tight and production-minded

Target:
~80–120 lines

Mindset:
Imagine a market data gateway processing millions of events per day.
You want to reuse event objects instead of constantly creating new ones.
"""


