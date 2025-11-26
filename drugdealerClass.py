#drug dealers 

import threading
import time
import random

class DrugDealer:
    def __init__(self, name, location, drug_type, price_per_unit):  
        self.name = name
        self.location = location
        self.drug_type = {'weed': {'price': 15, 'stock': 30},
                          'cocaine': {'price': 50, 'stock': 20},
                          'ecstasy': {'price': 25, 'stock': 40},
                          'ketamine': {'price': 40, 'stock': 15}}
        self.lock = threading.Lock()    
        self.cash = 0
    
    def sell(self, spectator, drug):
        # Spectator buys drug if available and has enough money
        with self.lock: 
            if drug not in self.inventory: #tries to buy a drug not sold here
                print(f"{self.name}: I don’t sell {drug}.")
                return False

            price = self.inventory[drug]['price'] 
            if self.inventory[drug]['stock'] <= 0: #out of stock
                print(f"{self.name}: I'm out of {drug}.")
                return False

            if spectator.inventory['money'] < price: #spectator can't afford
                print(f"{spectator.attributes['ID']} can’t afford {drug}.")
                return False

            # Process sale
            spectator.inventory['money'] -= price
            spectator.inventory['drugs'] += 1 #track which drug it was bought?
            self.inventory[drug]['stock'] -= 1
            self.cash += price

            print(f"{self.name} sold {drug} to {spectator.attributes['ID']} for ${price}.")
            return True

    def restock(self): #include inventory and have a thread and check 
        # Dealer restocks all drugs
        with self.lock:
            for drug in self.inventory:
                self.inventory[drug]['stock'] += random.randint(2, 6)
            print(f"{self.name} restocked.")

