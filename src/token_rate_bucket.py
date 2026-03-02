"""
Day 3 — Token Bucket Rate Limiter

Goal:
Implement a production-style token bucket rate limiter.

Implement:
    
    class TokenBucket:

Constructor:
    __init__(self, capacity: int, refill_rate: float)

        capacity:
            Maximum number of tokens the bucket can hold.

        refill_rate:
            Tokens added per second (float).

Required Methods:

    allow(self) -> bool
        - Returns True if a token can be consumed.
        - Returns False otherwise.
        - Must update internal state correctly.

    tokens(self) -> float
        - Returns current number of tokens (for debugging).

Constraints:
    - No external libraries
    - No sleeping
    - Must use time.monotonic()
    - No background threads
    - O(1) per call

Design Expectations:
    - No redundant state
    - Careful floating point handling
    - No negative tokens
    - Clamp tokens to capacity
    - Clean invariants

Target:
    ~50–70 lines

Mindset:
    Imagine this sits in front of an order gateway.
    If it leaks tokens or drifts, you get exchange throttled.
"""

import time
from token import VBAREQUAL


class TokenBucket:
    
    def __init__(self, capacity:int, refill_rate: float):
        
        
        #max bucket can hold...
        self.capacity: float = capacity 
        
        self.refill_rate:float = refill_rate
        
        #allow for fractional refills
        self.token_amnt: float = capacity
        
        self.last_time : float = time.monotonic()
        
    
    
    def allow(self) -> bool:
        
        curr_time = time.monotonic()
        
        delta = curr_time - self.last_time
        
        self.last_time = curr_time 
        
        tokens_to_fill = self.refill_rate * delta
        
        self.token_amnt = min(self.capacity, self.token_amnt + tokens_to_fill)
        
        if(self.token_amnt >= 1.0):
            
            self.token_amnt-=1
            
            return True
        else:
            
            return False
            
        
    def tokens(self) -> float:
        
        return self.token_amnt
        
        



"""
========================
Day 3 Review — TokenBucket
========================

Overall Grade: A

This implementation is production-quality for a single-threaded
rate limiter.

------------------------
What You Did Correctly
------------------------

1. Monotonic clock:
   Uses time.monotonic(), which is correct for elapsed duration.

2. Fractional refill:
   Tokens stored as float to avoid drift and lost time.

3. Proper clamping:
   Uses min(capacity, tokens + refill) to enforce upper bound.

4. Correct consumption rule:
   Requires >= 1.0 token before allowing.

5. O(1) operations:
   No loops, no background threads, lazy refill model.

6. Clean invariants:
   0 <= token_amnt <= capacity always holds.

------------------------
Minor Production Polishing (Optional)
------------------------

- Validate capacity > 0 and refill_rate > 0 in constructor.
- Consider injecting time function (for testability).
- Add docstrings for public methods.
- Thread-safety would require a lock in real infra.

------------------------
Complexity
------------------------

allow(): O(1)
tokens(): O(1)
memory: O(1)

------------------------
Engineering Level
------------------------

This is legitimately infrastructure-grade logic.

Compared to Day 1, you've moved from:
"stateful utility class"
to
"time-based control system with invariants."

Strong progression.
"""
        
        