"""
Day 5 — Streaming VWAP Engine

Goal:
Implement a streaming VWAP (Volume Weighted Average Price) calculator.

VWAP = sum(price * volume) / sum(volume)

The system must update incrementally as trades arrive.

Implement:

    class VWAPCalculator:

Constructor:
    __init__(self)

Required Methods:

    add_trade(self, price: float, volume: float) -> None
        - Updates internal state using the incoming trade.

    vwap(self) -> float
        - Returns the current VWAP.
        - Raise ValueError if no trades have been processed.

    total_volume(self) -> float
        - Returns total traded volume processed so far.

Constraints:

- O(1) update per trade
- Do NOT store full trade history
- Maintain minimal internal state
- Use floating point safely

Target:
~40–60 lines

Mindset:
Imagine this object processes millions of trade ticks from a market data feed.
Memory must remain constant.
Updates must be extremely cheap.
"""

"""
if we walk multiple levels of ob, per share what price did we get?

incoming order price 200 vol 200, total 200

200 * 200 = 4000 spent 4k

on average, 200 dollars a share, vwap is 200

now consume another level of ob 

300 * 300 = 9000 spent

9000 + 4000/ 500 

13000 / 500 = 260



"""

class StreamingVwap:
    
    __slots__ = ("total_spent", "total_vol", "num_trades_processed", "current_vwap")
    
    def __init__(self):
        
        #memory remains constant
        
        self.current_vwap = 0.0
        
        self.total_spent = 0.0
        
        self.total_vol = 0.0
        
        self.num_trades_processed = 0
        
    
    def process_trade(self, price:float, volume:float) -> None :
        
        if(volume <= 0 or price <= 0):
            raise ValueError("Invalid Trade: price & volume must be greater than 0")
            
        self.num_trades_processed += 1 
        
        self.total_spent += (price * volume)
        
        self.total_vol += volume
        
        self.current_vwap = self.total_spent / self.total_vol
        
    
    def vwap(self) -> float:
        if(self.num_trades_processed <=0):
            raise ValueError("No Trades Processed")
        return self.current_vwap
        
    
    def total_volume(self) -> float:
        return self.total_vol
        
    def __repr__(self):
        
        return f"streaming_vwap(total_vol={self.total_vol}, num_trades_processed={self.num_trades_processed}, total_spent={self.total_spent} current_vwap={self.current_vwap})"
        
        



        
        
    
    
    
        