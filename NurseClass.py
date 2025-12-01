import threading
import time
import random

class Nurse:
    def __init__(self, name="Nurse Tent"):
        self.name = name
        self.neighbours = []  # For movement via Search()
        self.states = {
            'all':     {'list': [], 'lock': threading.Lock()},
            'healing': {'list': [], 'lock': threading.Lock()},
        }

    def receive(self, spectator, states=[]):
        # Always add to "all"
        states = ['all'] + states
        for state in states:
            if state in self.states:
                with self.states[state]['lock']:
                    self.states[state]['list'].append(spectator)

        # Set current location
        spectator.location = self

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

    def addNeighbour(self, other_location):
        if other_location not in self.neighbours:
            self.neighbours.append(other_location)
