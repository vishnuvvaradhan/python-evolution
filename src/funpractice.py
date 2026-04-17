# You've created a new programming language, and now you've decided to add hashmap support to it.
# Actually you are quite disappointed that in common programming languages it's impossible
# to add a number to all hashmap keys, or all its values. So you've decided to take matters
# into your own hands and implement your own hashmap in your new language that has the
# following operations:
#
# - insert x y — insert an object with key x and value y.
# - get x — return the value of an object with key x.
# - addToKey x — add x to all keys in map.
# - addToValue y — add y to all values in map.
#
# To test out your new hashmap, you have a list of queries in the form of two arrays:
# queryTypes contains the names of the methods to be called (e.g. insert, get, etc),
# and queries contains the arguments for those methods (the x and y values).
#
# Your task is to implement this hashmap, apply the given queries, and to find the sum
# of all the results for get operations.
# 
# 
# 
# 
# 
# [(2,3), (2,3) (5,5)] -> 3
# [(4, 5)]
# 
# []


class CustomHashmap:
    
    
    def __init__(self) -> None:
        
        self.map = dict()
        self.key_counter = 0        
        self.value_counter = 0 
        
        
    def insert(self, key, value):
 
        key += self.key_counter 
        value += self.value_counter
        
        self.map[key] = value
        
 
    def get(self, key):
        
        value = self.map.get(key - self.key_counter, None)
        
        if not value:
            return None
            
        return value + self.value_counter
            
            
    def addToKey(self, value):
        
        self.key_counter += value
        
        
    def addToValue(self, value):
        
        self.value_counter += value 
    
    
    
    