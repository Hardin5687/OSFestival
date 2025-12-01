import threading
import random
import time
import numpy as np
from Search import Search

from stageClass import Stage

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
                         'ID':ID,
                         'health':100,
                         'fun':50
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
            #The idea here is to return whether the action was succesful. Afterwards, we will maybe sleep (if we did do a thing)
            #This can affect our preferences. If we didnt do the thing (we dont like the music, we were rejected, whatever), we will inevitably grow angrier + other effects
            #This mean action functions shoudl return wether or not we were successful
            elif decision == 'hunger':
                didIDoTheThing = self.goEat()
            elif decision == 'flirt':
                didIDoTheThing = self.goFlirt()
            elif decision == 'fight':
                didIDoTheThing = self.goFight()
            elif decision == 'thirst':
                didIDoTheThing = self.goWater()
            elif decision == 'alcohol':
                didIDoTheThing = self.goAlcohol()
            elif decision == 'drug':
                didIDoTheThing = self.goDrugs()
            elif decision == 'bathroom':
                didIDoTheThing = self.goBathroom()
            #ETC
            #At the end of each loop we update values? We get hungrier, thirstier, etc according to our decision
            self.updatePreferences(decision=decision, didIDoTheThing=didIDoTheThing)
    
    def updatePreferences(self, decision, didIDoTheThing):
        updateList = {
            'dance': {
                True: {'fun':10, 'dance':-1, 'hunger':1, 'thirst':1, 'flirt':0, 'fight':-1, 'alcohol':0, 'drug':0, 'bathroom':0},
                False: {'fun':-10, 'dance':0, 'hunger':0, 'thirst':0, 'flirt':1, 'fight':1, 'alcohol':1, 'drug':1, 'bathroom':0}
                }
            }
        update = updateList[decision][didIDoTheThing]
        for key in update.keys():
            if key in self.attributes.keys():
                self.attributes[key]+=update[key]
            else:
                self.preferences[key]+=update[key]

    def goDance(self):
        if type(self.location) == Stage:
            if self.location.music == self.attributes['musicHate']:
                return False
            else:
                return True
        else:
            for stage in self.locationList['stages']:
                if stage.music == self.attributes['musicFave']:
                    Search(spectator=self, request=[stage], start=self.location)
                    return True
            Search(spectator=self, request=self.locationList['stages'], start=self.location)
            time.sleep(5)
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

    def goFight(self,target):
        #we add both spectators to fighting state in case security needs to break it up
        self.location.addState(self, 'fighting')
        self.location.addState(target, 'fighting')
        #we will check if the fight gets interrupted by security here
        # Flags for interruption
        self.is_fighting = True
        target.is_fighting = True

        print(f"{self.attributes['ID']} starts fighting {target.attributes['ID']}!")

        # Fight lasts up to 5 seconds, but can be interrupted
        fight_duration = 5.0
        step = 0.1
        waited = 0.0

        # Check every 100ms if security broke the fight
        while waited < fight_duration:
            # If security removed fighting state → break up
            if not self.is_fighting or not target.is_fighting:
                print(f"Fight between {self.attributes['ID']} and {target.attributes['ID']} was broken up by security.")
                return False  # fight ended early

            time.sleep(step)
            waited += step

        # If we reach here → fight was NOT interrupted → resolve normally

        #Fight logic here  
        def fight_power(s):
            # We have 3 variables that determine fight power: anger level, drunkness, and size of friend group
            #check friend group size
            if len(s.relationships) > 1:
                friends = len(s.relationships)
            else: #if the friend group is 0 or 1, we consider it as alone or with a partner 
                friends = 0
            anger = s.preferences['fight']
            drunkness = 0   #once we implement we will add 
            return anger + drunkness + friends
        
        my_power = fight_power(self)
        target_power = fight_power(target)

        #determine winner
        if my_power > target_power:
            winner = self
            loser = target
        elif target_power > my_power:
            winner = target
            loser = self
        else: #in case of tie, random winner
            if random.randint(0,1) == 0:
                winner = self
                loser = target
            else:
                winner = target
                loser = self
  
  

    def goFlirt(self):
        pass
    
    def goBathroom(self):
        pass
    
    def goWater(self):
        pass
    
    def goAlcohol(self):
        pass
    
    def goDrugs(self):
        pass
    