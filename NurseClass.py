import threading
import time
import random

from LocationClass import Location

class NurseTent(Location):
    def __init__(self, name="Nurse Tent"):
        super().__init__()
        self.name = name
        self.neighbours = []  # For movement via Search()
        self.states['healing'] = {'list': [], 'lock': threading.Lock()}

    def heal(self, spectator):

        print(f"Nurse: Treating {spectator.attributes['ID']}...")

        # Mark as healing
        with self.states['healing']['lock']:
            self.states['healing']['list'].append(spectator)

        # Treatment time
        treatment_time = random.randint(2, 5)
        time.sleep(treatment_time)

        # Remove bad states (wasted, drugged)
        for bad_state in ['wasted', 'drugged']:
            if spectator in self.states.get(bad_state, {}).get('list', []):
                with self.states[bad_state]['lock']:
                    self.states[bad_state]['list'].remove(spectator)

        # Reset intoxication levels if your Spectator has them
        if hasattr(spectator, "drunkness"):
            spectator.drunkness -= 1
        if hasattr(spectator, "drug_level"):
            spectator.drug_level -= 1

        print(f"Nurse: {spectator.attributes['ID']} is better and can return to the festival.")

        # Remove from healing list
        with self.states['healing']['lock']:
            self.states['healing']['list'].remove(spectator)

        return True

