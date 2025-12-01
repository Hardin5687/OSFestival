import threading
import random
import time

class Bathroom: 
    def __init__(self, name, capacity = 3):
        self.name = name
        self.capacity = capacity
        self.state = {
            'all': {'list': [], 'lock': threading.Lock()},
            'occupied': {'list': [], 'lock': threading.Lock()},
            'waiting': {'list': [], 'lock': threading.Lock()}
        }

    def receive(self, spectator, states=[]):
        # Track spectators inside the bathroom
        states = ['all'] + states
        for state in states:
            if state in self.state:
                with self.state[state]['lock']:
                    self.state[state]['list'].append(spectator)

    def useBathroom(self, spectator):
        # Try to use a bathroom stall
        with self.state['occupied']['lock']:
            if len(self.state['occupied']['list']) < self.capacity:
                self.state['occupied']['list'].append(spectator)
                print(f"{spectator.attributes['ID']} entered {self.name}.")
                time.sleep(random.randint(1, 3))  # simulate bathroom use

                # optional: spectator can drink water
                self.drinkWater(spectator)

                self.state['occupied']['list'].remove(spectator)
                print(f"{spectator.attributes['ID']} left {self.name}.")
                return True

            else:
                with self.state['waiting']['lock']:
                    self.state['waiting']['list'].append(spectator)
                    print(f"{spectator.attributes['ID']} is waiting for {self.name}.")
                    return False

    def drinkWater(self, spectator):
        print(f"{spectator.attributes['ID']} drinks water at {self.name}.")
        spectator.preferences['thirst'] = 0


    def freeSpot(self):
        with self.state['occupied']['lock']:
            return len(self.state['occupied']['list']) < self.capacity