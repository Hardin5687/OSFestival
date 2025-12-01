import threading
import random
import time
import numpy as np
from Search import Search

from stageClass import Stage
from FoodCart import FoodCart


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

    def goFight(self):
        target = random.choice([s for s in self.location.states['all']['list'] if s != self])
        # Mark fighting state
        self.location.addState(self, 'fighting')
        self.location.addState(target, 'fighting')

        self.is_fighting = True
        target.is_fighting = True

        print(f"{self.attributes['ID']} starts fighting {target.attributes['ID']}!")

        # Power calculation
        def fight_power(s):
            # friends = number of friends in relationship list, excluding partner relations
            if len(s.relationships) > 1:
                friends = len(s.relationships) 
            else:
                friends = 0    

            anger = s.preferences['fight']
            drunkness = 0  # To be implemented later
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
        # Proportional chances
        total_power = my_power + target_power
        my_chance = my_power / total_power
        target_chance = target_power / total_power

        # Fight simulation (up to 5 seconds)
        fight_time = 5.0
        step = 0.2
        elapsed = 0

        self_score = 0
        target_score = 0

        while elapsed < fight_time:
            # Security interrupts fight
            if not self.is_fighting or not target.is_fighting:
                print(f"Fight between {self.attributes['ID']} and {target.attributes['ID']} was stopped by security.")
                return False

            # Each 0.2 seconds, both have a chance to get a point based on their power 
            roll = random.random()
            if roll < my_chance:
                self_score += 1
            else:
                target_score += 1

            elapsed += step
            time.sleep(step)

        # Determine winner by total score
 
        print(f"Fight scores → {self.attributes['ID']}: {self_score}, {target.attributes['ID']}: {target_score}")

        if self_score > target_score:
            winner, loser = self, target
        elif target_score > self_score:
            winner, loser = target, self
        else:
            # Perfect tie → random winner
            winner = random.choice([self, target])
            loser = target if winner is self else self

        print(f"Fight resolved → Winner: {winner.attributes['ID']}  Loser: {loser.attributes['ID']}")

        # Remove fighting state
        self.location.removeState(self, 'fighting')
        self.location.removeState(target, 'fighting')
        self.is_fighting = False
        target.is_fighting = False

        return True


    def goFlirt(self):
        # Get all available people in the same location except myself
        people = [s for s in self.location.states['all']['list'] if s != self]

        if not people:
            return False  # nobody to flirt with

        # Choose someone randomly
        target = random.choice(people)

        # -----------------------------------------
        # 1. DETERMINE TARGET'S RELATIONSHIP STATUS
        # -----------------------------------------
        # 0 → alone
        # 1 → partner
        # >1 → friend group

        relation_count = len(target.relationships)

        # --- Case 1: Flirting with someone who has a partner ---
        if relation_count == 1:
            partner = target.relationships[0]
            print(f"{self.attributes['ID']} flirts with {target.attributes['ID']} who has a partner → fight!")
            self.goFight(partner)
            return True

        # --- Case 2: Flirting with someone in a friend group ---
        if relation_count > 1:
            # Friend group reacts more aggressively
            print(f"{self.attributes['ID']} tries flirting with {target.attributes['ID']} in a FRIEND GROUP!")
            # 40% chance group gets upset, causing a fight with a random friend
            if random.random() < 0.40:
                group_member = random.choice(target.relationships)
                print(f"Friend group doesn't like it → fight with {group_member.attributes['ID']}")
                self.goFight(group_member)
                return True
            # Otherwise just a normal flirt
            # Continue below

        # -----------------------------------------
        # 2. NORMAL FLIRT ATTEMPT (probability)
        # -----------------------------------------
        flirt_probability = self.preferences['flirt'] / 10  # 0–1 chance

        if random.random() < flirt_probability:
            print(f"{self.attributes['ID']} successfully flirts with {target.attributes['ID']}")
            return True
        else:
            print(f"{self.attributes['ID']} fails to flirt with {target.attributes['ID']}")
            return False

        
            
            
    def goBathroom(self):
        # Move to the nearest bathroom
        Search(self, request=self.locationList['bathrooms'], start=self.location)
        bathroom = self.location

        # Try to use a stall
        success = bathroom.useBathroom(self)
        if not success:
            return False

        # Decide IF spectator drinks
        if self.preferences['thirst'] > 1:         # only if thirsty
            if random.random() < 0.6:             # 60% chance to drink
                bathroom.drinkWater(self)
        return True

    def goWater(self):
        # 1 — Find all food carts that sell water
        water_sources = [fc for fc in self.locationList['foodCarts'] if 'water' in fc.menu]

        if not water_sources:
            print(f"{self.attributes['ID']} cannot find any water source.")
            return False

        # 2 — If already at a water source, use it directly
        if isinstance(self.location, FoodCart) and 'water' in self.location.menu:
            fc = self.location
        else:
            # 3 — Move to the closest water source using Search()
            target = random.choice(water_sources)
            Search(spectator=self, request=[target], start=self.location)
            fc = target

        # 4 — Try to buy water
        success = fc.purchase(self, 'water')

        if success:
            # 5 — Drink water immediately → reduce thirst
            self.preferences['thirst'] = 0
            print(f"{self.attributes['ID']} drank water and is no longer thirsty.")
            return True

        # Could not buy water (no money or sold out)
        return False

    
    def goAlcohol(self):
        # 1 — Find all food carts that sell alcohol
        alcohol_items = ['beer', 'wine', 'cocktail', 'shot']
        alcohol_sources = [
            fc for fc in self.locationList['foodCarts']
            if any(drink in fc.menu for drink in alcohol_items)
        ]

        if not alcohol_sources:
            print(f"{self.attributes['ID']} cannot find any alcohol source.")
            return False

        # 2 — If already at place selling alcohol
        if isinstance(self.location, FoodCart) and any(
            drink in self.location.menu for drink in alcohol_items
        ):
            fc = self.location
        else:
            # 3 — Move to an alcohol source using Search
            target = random.choice(alcohol_sources)
            Search(spectator=self, request=[target], start=self.location)
            fc = target

        # 4 — Pick a random alcohol item
        drink = random.choice(alcohol_items)

        # 5 — Try to buy the alcohol
        success = fc.purchase(self, drink)
        if not success:
            return False

        # 6 — IMMEDIATELY CONSUME the drink
        print(f"{self.attributes['ID']} drinks a {drink} immediately.")

        # 7 — Apply drunkenness effect
        if not hasattr(self, "drunkness"):
            self.drunkness = 0  # initialize if not yet created

        # Increase drunkenness level
        self.drunkness += 1

        # Cap values: 0 = sober, 1 = tipsy, 2 = drunk, 3 = wasted
        if self.drunkness >= 3:
            self.drunkness = 3
            # Add wasted state when fully drunk
            self.location.addState(self, "wasted")
            print(f"{self.attributes['ID']} is now WASTED from drinking.")
        elif self.drunkness == 2:
            print(f"{self.attributes['ID']} is DRUNK.")
        elif self.drunkness == 1:
            print(f"{self.attributes['ID']} is getting tipsy.")

        # 8 — Update alcohol preference (use it or not)
        self.preferences['alcohol'] = max(0, self.preferences['alcohol'] - 1)

        return True

    
    def goDrugs(self):
        # Find all dealers in the festival
        dealers = self.locationList['dealers']
        if not dealers:
            print(f"{self.attributes['ID']} cannot find any drug dealers.")
            return False

        # Choose a dealer randomly
        dealer = random.choice(dealers)
        dealer_location = dealer.location

        # If we are NOT at the dealer's location → walk there
        if self.location != dealer_location:
            Search(spectator=self, request=[dealer_location], start=self.location)

        # Choose drug type from dealer inventory
        drug = random.choice(list(dealer.inventory.keys()))

        # Try to buy the drug
        success = dealer.sell(self, drug)
        if not success:
            return False

        # Apply drug effect (simple version)
        print(f"{self.attributes['ID']} uses the {drug} immediately.")

        if not hasattr(self, "drug_level"):
            self.drug_level = 0

        self.drug_level += 1

        # Drug effect logic (customizable later)
        if self.drug_level == 1:
            print(f"{self.attributes['ID']} feels the effects.")
        elif self.drug_level == 2:
            print(f"{self.attributes['ID']} is getting HIGH.")
            self.location.addState(self, 'drugged')
        elif self.drug_level >= 3:
            print(f"{self.attributes['ID']} is EXTREMELY drugged!")
            self.location.addState(self, 'drugged')

        # Lower drug preference over time
        self.preferences['drug'] = max(0, self.preferences['drug'] - 1)

        return True
