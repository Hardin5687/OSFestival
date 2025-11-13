import threading
import random
import time
import numpy as np

class Stage():
  pass

personalities = {
    #A dictionary of archetypes. Different personalities prefer different things
    ['averageJoe']:{'flirt':3, 'fight':3, 'alcohol':3, 'drug':3, 'musicFave':None, 'musicHate':None, 'moneyMax':150, 'moneyMin':50}
}

#locations will be a dictionary of all locations by their types

class Spectator(threading.Thread):
  def __init__(self, ID, personality, locations:dict):
    super().__init__()
    self.locationList=locations
    self.attributes={ #A dictionary of attributes that are NOT weights for decision making
        'musicFave':personality['musicFave'],
        'musicHate':personality['musicHate'],
        'ID':ID
    }
    self.inventory={ #A dictionary of things the spectator has. If they already have food, when they get hungry they won't need to go elsewhere to buy it
        'food':0,
        'water':0,
        'alcohol':0,
        'money':random.randint(personality['moneyMin'], personality['moneyMax']),
        'drugs':0 #Could be part of personality
    }
    self.location = None
    self.relationships=[]
    self.interactions=[]
    self.preferences={ #A dictionary of values used for decision making. As we make choices this values will change. Higher values are more likely to get picked.
        'dance':5,
        'hunger':random.randint(1, 3),
        'thirst':random.randint(1, 3),
        'flirt':personality['flirt'],
        'fight':personality['fight'],
        'alcohol':personality['alcohol'],
        'drug':personality['drug'],
        'bathroom':0
    }

  def forcedDecisions(self):
    #This method will check mandatory decisions. Examples:
    #If someone is flirting with my partner, fight them
    #If I am already in a fight, keep fighting
    #If my favorite music is playing, I have a high chance to dance
    #In the end, return decision
    #return None if no decision was reached. That will trigger the normal decision making function
    #Expect this method to grow very long as we make the code more complex. A lot of interactions will be contained here.
    return None

  def decision(self):
    #This should run soft max and return the spectator's next action
    total=0
    softmax=[]
    for key in self.preferences.keys():
      val=np.e**self.preferences[key]
      softmax.append([key, val])
      total+=val
    choice=random.randint(range(total))
    total=0
    for decision in softmax:
      total+=decision[1]
      if choice < total:
        return decision[0]

  def run(self):
    while True:
      #First we should be checking things like relationships that may force our decision
      decision = self.forcedDecisions()
      if decision == None:
        decision = self.decision()
      if decision == 'dance':
        didIDoTheThing = self.goDance()
        if didIDoTheThing:
          time.sleep(5)
        #The idea here is to return whether the action was succesful. Afterwards, we will maybe sleep (if we did do a thing)
        #This can affect our preferences. If we didnt do the thing (we dont like the music, we were rejected, whatever), we will inevitably grow angrier + other effects
        #This mean action functions shoudl return wether or not we were successful
      elif decision == 'eat':
        didIDoTheThing = self.goEat()
      elif decision == 'flirt':
        didIDoTheThing = self.goFlirt()
      #ETC
      #At the end of each loop we update values? We get hungrier, thirstier, etc according to our decision

  def goDance(self):
    if type(self.location) == Stage:
      if self.location.music == self.attributes['musicHate']:
        return False
      else:
        return True
    else:
      for stage in self.locationList['stages']:
        if stage.music == self.attributes['musicFave']:
          self.location.sendTo(self, stage)
          return True
      stage = random.choice(self.locationList['stages'])
      self.location.sendTo(self, stage)
      return True

  def goEat(self):
    if self.inventory['food']==0:
      #If we have no food, go buy some
      #I'm still working on how to choose the closest decision or how to manage paths
      target=random.choice(self.locationList['foodCarts'])
      self.location.sendTo(self, target)
      #foodCart not implemented, so this is a draft
      food = random.choice(list(self.location.menu.keys()))
      if self.location.menu[food]['price']>self.inventory['money']:
        return False
      else:
        self.inventory['food']+=self.location.purchase(self, food)
    while self.inventory['food']>0 and self.preferences['hunger']>0:
      time.sleep(1)
      self.inventory['food']-=1
      self.preferences['hunger']-=1
    return True

  def goFight(self):
      pass
  
  

class Location:
  def __init__(self):
    #Here go the lists and locks of the location
    #Pay attention to the structure. The dictionary makes adding or removing new lists easier
    #Wasted, drugged, etc will be referred to as 'states'
    self.neighbours=[]
    self.states={
        'all':{'list':[], 'lock':threading.Lock()},
        'wasted':{'list':[], 'lock':threading.Lock()},
        'drugged':{'list':[], 'lock':threading.Lock()},
        'fighting':{'list':[], 'lock':threading.Lock()}
    }

  def addState(self, spectator, state):
    #Give a spectator a state
    #Returns True if the spectator is still at location, False if not, None if there was an error
    #Same holds for other methods
    if state in self.states.keys():
      with self.states['all']['lock']:
        if spectator not in self.states['all']['list']:
          #Keep in mind return breaks out of the function
          return False
      with self.states[state]['lock']:
        self.states[state]['list'].append(spectator)
        return True
    else:
      print(f"State {state} was requested but doesn't exist")
      return None

  def removeState(self, spectator, state):
    #Remove a spectator's state
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
    #Returns a list of all states of an spectator
    #Removed spectator in 'all' check
    #Should 'all' be returned?
    #Might need revision
    states=[]
    for state in self.states.keys():
      if state=='all':
        continue
      with self.states[state]['lock']:
        if spectator in self.states[state]['list']:
          states.append(state)
    return states

  def getStateList(self, state='all'):
    #Returns the list of all spectators that have a specific state
    if state not in self.states.keys():
      print(f"State {state} was requested but doesn't exist")
      return None
    else:
      with self.states[state]['lock']:
        return self.states[state]['list']

  def sendTo(self, spectator, target):
    #Sends an spectator to a neighbour location
    #Does it need to be a neighbour?
    with self.states['all']['lock']:
      if spectator not in self.states['all']['list']:
        return False
      else:
        states=self.checkStates(spectator)
        for state in states:
          self.removeState(spectator, state)
        target.receive(spectator, states)
        return True

  def receive(self, spectator, states=[]):
    #Receives an spectator from another location
    states = ['all'] + states
    for state in states:
      if state in self.states.keys():
        with self.states[state]['lock']:
          self.states[state]['list'].append(spectator)

