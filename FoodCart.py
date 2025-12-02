#foodcart class

import threading
import time
import random
from LocationClass import Location

class FoodCart(Location): #spectator.inventory I do 
    def __init__(self,name=None):
        super().__init__()
        self.name = name
        self.menu = {
            #food item: price, stock
            'burger': {'price': 10, 'stock': 50,'satiety':3},
            'fries': {'price': 3, 'stock': 100},
            'hotdog': {'price': 7, 'stock': 80},
            'sandwich': {'price': 5, 'stock': 60},
            #alcoholic beverages
            'beer': {'price': 6, 'stock': 200},
            'wine': {'price': 12, 'stock': 150},
            'cocktail': {'price': 15, 'stock': 100},
            'shot': {'price': 4, 'stock': 300},
            #water
            'water': {'price': 2, 'stock': 500}
        }
        self.lock  = threading.Lock()
        self.states['eating'] = {'list': [], 'lock': threading.Lock()}

    def purchase(self, spectator, item):
        # Spectator tries to buy an item from the menu
        with self.lock:
            if item not in self.menu.keys():
                print(f"{spectator.attributes['ID']} tried to buy {item}, but it is not sold here.")
                return 0
            if self.menu[item]['stock'] <= 0:
                print(f"{spectator.attributes['ID']} tried to buy {item}, but it is sold out.")
                return 0
            price = self.menu[item]['price']
            if spectator.inventory['money'] < price:
                print(f"{spectator.attributes['ID']} doesn't have enough money for {item}.")
                return 0
            # Perform purchase
            spectator.inventory['money'] -= price
            self.menu[item]['stock'] -= 1
            time.sleep(random.uniform(0.5, 4))  # Simulate time taken to process purchase
            print(f"{spectator.attributes['ID']} bought {item} for ${price}. Remaining money: ${spectator.inventory['money']}.")
            if item in ['burger', 'fries', 'hotdog', 'sandwich']:
                spectator.inventory['food'] += self.menu[item]['satiety']
            elif item in ['water']:
                spectator.inventory['water'] += 1
            return 1  # Successfully purchased
    
    def restock(self, item, amount):
        # Refill stock for an item
        with self.lock:
            if item in self.menu.keys():
                self.menu[item]['stock'] += amount
                print(f"Restocked {item} (+{amount}). Now available: {self.menu[item]['stock']}")
                time.sleep(random.randint(1,5))  # Simulate time taken to restock
    

