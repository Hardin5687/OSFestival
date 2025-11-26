#bathroom class
import threading
import random
import time

class Bathroom: 
    def __init__(self, name, capacity = 3):
        self.name = name
        self.capacity = capacity
        self.state = {
            'all': {'list' : [], 'lock' : threading.Lock() },
            'occupied': {'list' : [], 'lock' : threading.Lock()},
            'waiting': {'list' : [], 'lock' : threading.Lock() }
        }

    def receive(self, spectator, states = []):
    #Receive a spectator into the bathroom's tracking system
        states = ['all'] + states
        for state in states:
            if state in self.state.keys():
                with self.state[state]['lock']:
                    self.state[state]['list'].append(spectator) 
    
    def useBathroom(self, spectator): #add time.sleep
        # Spectator tries to use the bathroom
        with self.states['occupied']['lock']:
            if len(self.states['occupied']['list']) < self.capacity:
                self.states['occupied']['list'].append(spectator)
                print(f"{spectator.attributes['ID']} entered {self.name}.")
                time.sleep(random.randint(1, 3))  # simulate bathroom use
                self.states['occupied']['list'].remove(spectator)
                print(f"{spectator.attributes['ID']} left {self.name}.")
                return True
            else:
                with self.states['waiting']['lock']:
                    self.states['waiting']['list'].append(spectator)
                    print(f"{spectator.attributes['ID']} is waiting for {self.name}.")
                    return False
    def freeSpot(self):
        # Check if a spot is available
        with self.states['occupied']['lock']:
            return len(self.states['occupied']['list']) < self.capacity