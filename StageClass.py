import threading

class Stage:
    def __init__(self, name):
        self.name = name
        self.music = None  # Artist will set this
        self.neighbours = []  # For Search pathfinding

        # Track spectators at the stage
        self.states = {
            'all': {'list': [], 'lock': threading.Lock()},
            'dancing': {'list': [], 'lock': threading.Lock()}
        }

    def receive(self, spectator, states=[]):
        # Move spectator into stage and assign proper states
        states = ['all'] + states

        for state in states:
            if state in self.states:
                with self.states[state]['lock']:
                    self.states[state]['list'].append(spectator)

        # Update spectator current location
        spectator.location = self

    def remove(self, spectator):
        # Remove spectator from all state lists
        for state in self.states:
            with self.states[state]['lock']:
                if spectator in self.states[state]['list']:
                    self.states[state]['list'].remove(spectator)

    def setMusic(self, genre):
        # Artist sets the current music playing on this stage
        self.music = genre
        print(f"Stage {self.name}: Music changed to {self.music}")

    def addNeighbour(self, other_location):
        # Allow Search to navigate between locations
        if other_location not in self.neighbours:
            self.neighbours.append(other_location)
