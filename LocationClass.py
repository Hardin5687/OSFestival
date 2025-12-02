# Libraries
import threading
# import random
import time


# Location class
class Location:
    def __init__(self):
        # Here go the lists and locks of the location
        # Pay attention to the structure. The dictionary makes adding or removing new lists easier
        # Wasted, drugged, etc will be referred to as 'states'
        self.neighbours = []
        self.queues = {'lock':threading.Lock()}
        self.states = {
            'all': {'list': [], 'lock': threading.Lock()},
            'wasted': {'list': [], 'lock': threading.Lock()},
            'drugged': {'list': [], 'lock': threading.Lock()},
            'fighting': {'list': [], 'lock': threading.Lock()}
        }
        
    def makeNeighbours(self, neighbour):
        if neighbour not in self.neighbours:
            self.neighbours.append(neighbour)
            neighbour.makeNeighbours(self)
        
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

    def sendTo(self, spectator, path, states=[]):
        # Sends an spectator to a neighbour location
        # Does it need to be a neighbour?
        with self.states['all']['lock']:
            if spectator not in self.states['all']['list']:
                return False
            else:
                states = self.checkStates(spectator)
                if 'fighting' in states:
                    return False
                for state in states:
                    self.removeState(spectator, state)
        with self.queues['lock']:
                    self.queues[path[0]].append(spectator)
        time.sleep(0.1)
        while self.queues[path[0]][0] != spectator:
            time.sleep(0.1)
            continue
        with self.queues['lock']:
             self.queues[path[0]].pop(0)
        path[0].receive(spectator, states, path[1:])
        return True

    def receive(self, spectator, states, path):
        # Receives an spectator from another location
        if path==[]:
            states = ['all'] + states
            for state in states:
                if state in self.states.keys():
                    with self.states[state]['lock']:
                        self.states[state]['list'].append(spectator)
        else:
            self.sendTo(spectator, path, states)

