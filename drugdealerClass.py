import threading
import random
import time
from global_metrics import metrics

class DrugDealer:
    def __init__(self, location, name=None):
        self.name = name
        self.location = location   # Dealers stay in a fixed location
        self.inventory = {         # THIS is the inventory
            'weed':     {'price': 15, 'stock': 30},
            'cocaine':  {'price': 50, 'stock': 20},
            'ecstasy':  {'price': 25, 'stock': 40},
            'ketamine': {'price': 40, 'stock': 15}
        }
        self.lock = threading.Lock()
        self.cash = 0

    def sell(self, spectator, drug):
        with self.lock:
            if drug not in self.inventory:
                print(f"{self.name}: I don’t sell {drug}.")
                return False

            price = self.inventory[drug]['price']
            if self.inventory[drug]['stock'] <= 0:
                print(f"{self.name}: I'm out of {drug}.")
                return False

            if spectator.inventory['money'] < price:
                print(f"{spectator.attributes['ID']} can’t afford {drug}.")
                return False

            # Process sale
            spectator.inventory['money'] -= price
            spectator.inventory['drugs'] += 1
            self.inventory[drug]['stock'] -= 1
            self.cash += price

            print(f"{self.name} sold {drug} to {spectator.attributes['ID']} for ${price}.")

            metrics.log_drug_sale(
                drug,
                price,
                self.name,
                spectator.attributes['ID']
            )
            return drug


    def restock(self):
        with self.lock:
            for drug in self.inventory:
                self.inventory[drug]['stock'] += random.randint(3, 8)
            print(f"{self.name} restocked.")
