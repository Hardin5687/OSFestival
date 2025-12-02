import threading
import time
import random
from LocationClass import Location

class NurseTent(Location):
    def __init__(self, name="Nurse Tent"):
        super().__init__()
        self.states['healing'] = {'list': [], 'lock': threading.Lock()}

    def heal(self, spectator):
        print(f"Nurse: Treating {spectator.attributes['ID']}...")

        # Mark as healing
        with self.states['healing']['lock']:
            self.states['healing']['list'].append(spectator)

        # Treatment time
        time.sleep(random.randint(2, 5))

        # Remove all harmful states
        for bad_state in ['wasted', 'drugged', 'fighting']:
            self.removeState(spectator, bad_state)

        if hasattr(spectator, "drunkness"):
            spectator.drunkness -= 1

        if hasattr(spectator, "drug_level"):
            spectator.drug_level -= 1

        # Reset fighting flag if it exists
        if hasattr(spectator, "is_fighting"):
            spectator.is_fighting = False
        
        spectator.attributes['health']+=50
        
        print(f"Nurse: {spectator.attributes['ID']} is fully recovered and ready to return.")
        
        # Remove from healing list
        with self.states['healing']['lock']:
            if spectator in self.states['healing']['list']:
                self.states['healing']['list'].remove(spectator)

        return True
