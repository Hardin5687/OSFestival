import threading

class Stage:
    def __init__(self, name):
        self.name = name
        self.music = None  # artist will set this
        self.neighbours = []  # needed for Search pathfinding
        self.states = {
            'all': {'list': [], 'lock': threading.Lock()},
            'dancing': {'list': [], 'lock': threading.Lock()}
        }

    def receive(self, spectator, states=[]):
        # Move spectator into stage and apply states
        states = ['all'] + states
        for state in states:
            if state in self.states:
                with self.states[state]['lock']:
                    self.states[state]['list'].append(spectator)

        # Set spectator's current location   
        spectator.location = self

    def remove(self, spectator):
        # Useful if someone leaves the stage
        for state in self.states:
            with self.states[state]['lock']:
                if spectator in self.states[state]['list']:
                    self.states[state]['list'].remove(spectator)

    def setMusic(self, music_type):
        # Artist changes the music of the stage
        self.music = music_type
        print(f"Stage {self.name}: Music changed to {self.music}")

    def addNeighbour(self, other_location):
        # Use for Search pathfinding
        if other_location not in self.neighbours:
            self.neighbours.append(other_location)
