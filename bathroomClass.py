import threading
import random
import time
from LocationClass import Location
from global_metrics import metrics


class Bathroom(Location): 
    def __init__(self, name=None, capacity=3):
        super().__init__()
        self.name = name
        self.capacity = capacity

        self.states['occupied'] = {'list': [], 'lock': threading.Lock()}
        self.states['waiting']  = {'list': [], 'lock': threading.Lock()}

    def useBathroom(self, spectator):
        start_time = time.time()   # Track wait time

        with self.states['occupied']['lock']:
            if len(self.states['occupied']['list']) < self.capacity:

                # Remove from waiting if already waiting
                with self.states['waiting']['lock']:
                    if spectator in self.states['waiting']['list']:
                        self.states['waiting']['list'].remove(spectator)

                self.states['occupied']['list'].append(spectator)
                print(f"{spectator.attributes['ID']} entered {self.name}.")

                # They got in immediately → wait time = 0
                metrics.log_bathroom_wait(
                    spectator.attributes['ID'],
                    0
                )

                time.sleep(random.randint(1, 3))

                self.drinkWater(spectator)
                self.states['occupied']['list'].remove(spectator)
                print(f"{spectator.attributes['ID']} left {self.name}.")
                return True

        with self.states['waiting']['lock']:
            self.states['waiting']['list'].append(spectator)
            print(f"{spectator.attributes['ID']} is waiting for {self.name}.")

        metrics.log_bathroom_wait(
            spectator.attributes['ID'],
            round(time.time()-start_time, 2)
        )

        return False


    def drinkWater(self, spectator):
        print(f"{spectator.attributes['ID']} drinks water at {self.name}.")
        spectator.preferences['thirst'] = 0

    def freeSpot(self):
        with self.states['occupied']['lock']:
            return len(self.states['occupied']['list']) < self.capacity
