#foodcart class

import threading
import time
import random

class FoodCart:
    def __init__(self,name):
        self.name = name
        self.menu = {
            'burger': {'price': 10, 'stock': 50},
            'fries': {'price': 3, 'stock': 100},
            'hotdog': {'price': 7, 'stock': 80},
            'sandwich': {'price': 5, 'stock': 60}
        }
        self.lock  = threading.Lock()
        self.states = {
            'all': {'list': [], 'lock': threading.Lock()},
            'eating': {'list': [], 'lock': threading.Lock()}
        }
    def receive(self, spectator, states=[]):
        # Receives a spectator from another location
        states = ['all'] + states
        for state in states:
            if state in self.states.keys():
                with self.states[state]['lock']:
                    self.states[state]['list'].append(spectator)
    
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
            print(f"{spectator.attributes['ID']} bought {item} for ${price}. Remaining money: ${spectator.inventory['money']}.")
            return 1  # Returns 1 unit of food
    
    def restock(self, item, amount):
        # Refill stock for an item
        with self.lock:
            if item in self.menu.keys():
                self.menu[item]['stock'] += amount
                print(f"Restocked {item} (+{amount}). Now available: {self.menu[item]['stock']}")
                time.sleep(random.randint(1,5))  # Simulate time taken to restock
    

