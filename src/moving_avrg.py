"""
Day 1 — O(1) Moving Average

Goal:
Implement a production-quality MovingAverage class.

Class Definition:
    class MovingAverage:

Required Methods:
    __init__(self, window_size: int)
        - window_size must be a positive integer
        - raise ValueError if invalid

    add(self, value: float) -> None
        - Add a new numeric value to the rolling window
        - Maintain only the last `window_size` values
        - Must run in O(1) time

    value(self) -> float
        - Return the current moving average
        - If fewer than window_size elements exist,
          compute the average of available elements

Constraints:
    - No numpy
    - No pandas
    - No statistics module
    - No recomputing sum from scratch
    - No list slicing
    - Must be O(1) per update

Design Expectations:
    - Use type hints
    - Use private attributes
    - Proper docstring for the class
    - No public attribute mutation
    - Clean, readable structure
    - Minimal but production-minded

Optional Stretch (3 minutes max):
    - Implement __repr__ that prints:
      MovingAverage(window=5, current=102.34)

Target Size:
    ~40–70 lines
    Keep it tight. No overengineering.

Mindset:
    Imagine this is used inside a high-frequency market data handler.
    Allocations matter. Recomputations matter. Structure matters.
"""

from collections import deque

class MovingAverage:
    """
    Calculate a Moving Average

    window_size: int - set size for window 
    
    """

    def __init__(self, window_size: int):

        if window_size <= 0:
            raise ValueError("window_size must be greater than 0")

        self.window_size: int = window_size
        self.current_total: float = 0.0
        self.window = deque()



    def add(self, value: float) -> None:
        """
        Parameters:
             value: float - value to add to window
        returns blahh
        """

        if len(self.window) == self.window_size:
            self.current_total -= self.window.popleft()
            self.window.append(value)
            self.current_total += value
            return

        self.window.append(value)
        self.current_total += value

        

    def value(self) -> float:
        '''
        Get Moving Average
        returns blahh
        '''

        if len(self.window) == 0:
            raise ValueError("No Items Added to Window")
        
        return self.current_total/len(self.window)
    

