import threading
import random


class Location:
    def __init__(self):
        # Here go the lists and locks of the location
        # Pay attention to the structure. The dictionary makes adding or removing new lists easier
        # Wasted, drugged, etc will be referred to as 'states'
        self.neighbours = []
        self.states = {
            'all': {'list': [], 'lock': threading.Lock()},
            'wasted': {'list': [], 'lock': threading.Lock()},
            'drugged': {'list': [], 'lock': threading.Lock()},
            'fighting': {'list': [], 'lock': threading.Lock()}
        }

    def addState(self, spectator, state):
        # Give a spectator a state
        # Returns True if the spectator is still at location, False if not, None if there was an error
        # Same holds for other methods
        if state in self.states.keys():
            with self.states['all']['lock']:
                if spectator not in self.states['all']['list']:
                    # Keep in mind return breaks out of the function
                    return False
            with self.states[state]['lock']:
                self.states[state]['list'].append(spectator)
            return True
        else:
            print(f"State {state} was requested but doesn't exist")
            return None

    def removeState(self, spectator, state):
        # Remove a spectator's state
        if state in self.states.keys():
            with self.states[state]['lock']:
                if spectator not in self.states[state]['list']:
                    return False
                else:
                    self.states[state]['list'].remove(spectator)
                    return True
        else:
            print(f"State {state} was requested but doesn't exist")
            return None

    def checkStates(self, spectator):
        # Returns a list of all states of an spectator
        # Removed spectator in 'all' check
        # Should 'all' be returned?
        # Might need revision
        states = []
        for state in self.states.keys():
            if state == 'all':
                continue
            with self.states[state]['lock']:
                if spectator in self.states[state]['list']:
                    states.append(state)
        return states

    def getStateList(self, state='all'):
        # Returns the list of all spectators that have a specific state
        if state not in self.states.keys():
            print(f"State {state} was requested but doesn't exist")
            return None
        else:
            with self.states[state]['lock']:
                return self.states[state]['list']

    def sendTo(self, spectator, target):
        # Sends an spectator to a neighbour location
        # Does it need to be a neighbour?
        with self.states['all']['lock']:
            if spectator not in self.states['all']['list']:
                return False
            else:
                states = self.checkStates(spectator)
                for state in states:
                    self.removeState(spectator, state)
                target.receive(spectator, states)
                return True

    def receive(self, spectator, states=[]):
        # Receives an spectator from another location
        states = ['all'] + states
        for state in states:
            if state in self.states.keys():
                with self.states[state]['lock']:
                    self.states[state]['list'].append(spectator)


class Spectator(threading.Thread):
    def __init__(self, id, state, location):
        # define what the customer is
        threading.Thread.__init__(self)
        self.id = id
        self.budget = 0
        self.hunger = 0
        self.location = None

    def state_aquired(self, state):
        # we are going to give to the spectator a random state from the possible states
        self.state = {
            'drunkness': {"sober": 0, "tipsy": 1, "drunk": 2, "wasted": 3},
            'drugs': {"none": 0, "weed": 1, "coke": 2, "mdma": 3},
            'flirting': {"none": 0, "looking": 1, "approaching": 2, "dancing": 3},
            'music_taste': {"pop": 0, "rock": 1, "rap": 2, "techno": 3},
        }
        state_choice = random.choice(list(self.state[state].keys()))
        if state == 'drunkness':
            self.drunkness = state_choice
        elif state == 'drugs':
            self.drugs = state_choice
        elif state == 'flirting':
            self.flirting = state_choice
        else:
            self.music_taste = state_choice

    def fixed_values(self):
        self.budget = random.randint(50, 200)
        self.hunger = random.randint(0, 100)
