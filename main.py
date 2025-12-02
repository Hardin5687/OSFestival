from SpectatorClass import Spectator
from LocationClass import Location
from StageClass import Stage
from bathroomClass import Bathroom
from NurseClass import NurseTent
from FoodCart import FoodCart
from drugdealerClass import DrugDealer
from securityguardcorrect import SecurityGuard
from Clock import Clock

import random
import time

personalities = {
    #A dictionary of archetypes. Different personalities prefer different things
    'averageJoe':{'flirt':3, 'fight':3, 'alcohol':3, 'drug':3, 'musicFave':None, 'musicHate':None, 'moneyMax':150, 'moneyMin':50},
    'drunk':{'flirt':4, 'fight':4, 'alcohol':5, 'drug':3, 'musicFave':'rock', 'musicHate':'jazz', 'moneyMax':100, 'moneyMin':10},
    'punk':{'flirt':3, 'fight':4, 'alcohol':3, 'drug':4, 'musicFave':'rock', 'musicHate':'jazz', 'moneyMax':140, 'moneyMin':40},
    'junkie':{'flirt':2, 'fight':3, 'alcohol':3, 'drug':5, 'musicFave':'techno', 'musicHate':'pop', 'moneyMax':80, 'moneyMin':0},
    'hipster':{'flirt':3, 'fight':2, 'alcohol':2, 'drug':3, 'musicFave':'hiphop', 'musicHate':'techno', 'moneyMax':170, 'moneyMin':60},
    'businessman':{'flirt':2, 'fight':2, 'alcohol':3, 'drug':1, 'musicFave':'pop', 'musicHate':'rock', 'moneyMax':400, 'moneyMin':200},
    'artist':{'flirt':4, 'fight':2, 'alcohol':3, 'drug':4, 'musicFave':'jazz', 'musicHate':'pop', 'moneyMax':180, 'moneyMin':50},
    'goth':{'flirt':2, 'fight':3, 'alcohol':3, 'drug':2, 'musicFave':'rock', 'musicHate':'pop', 'moneyMax':120, 'moneyMin':40},
    'romantic':{'flirt':5, 'fight':3, 'alcohol':2, 'drug':1, 'musicFave':'pop', 'musicHate':'rock', 'moneyMax':160, 'moneyMin':60},
    'rebel':{'flirt':4, 'fight':4, 'alcohol':4, 'drug':4, 'musicFave':'rock', 'musicHate':'classical', 'moneyMax':130, 'moneyMin':30},
    'gamer':{'flirt':2, 'fight':2, 'alcohol':2, 'drug':2, 'musicFave':'techno', 'musicHate':'jazz', 'moneyMax':170, 'moneyMin':70},
    'intellectual':{'flirt':2, 'fight':1, 'alcohol':2, 'drug':1, 'musicFave':'jazz', 'musicHate':'reggaeton', 'moneyMax':250, 'moneyMin':100},
    'stoner':{'flirt':3, 'fight':2, 'alcohol':2, 'drug':5, 'musicFave':'hiphop', 'musicHate':'techno', 'moneyMax':120, 'moneyMin':20},
    'partyAnimal':{'flirt':5, 'fight':3, 'alcohol':5, 'drug':4, 'musicFave':'reggaeton', 'musicHate':'rock', 'moneyMax':220, 'moneyMin':40},
    'loner':{'flirt':1, 'fight':2, 'alcohol':1, 'drug':2, 'musicFave':'jazz', 'musicHate':'techno', 'moneyMax':100, 'moneyMin':20},
    'musician':{'flirt':4, 'fight':2, 'alcohol':3, 'drug':3, 'musicFave':'jazz', 'musicHate':'pop', 'moneyMax':180, 'moneyMin':60}
}

    
def main():
 # ------------------------------------------------
    # 1. CREATE LOCATIONS WITH NAMES
    # ------------------------------------------------
#make it into dictionary later 
#add exits 

    
    # Stages (3)
    stage1 = Stage("Stage 1")
    stage2 = Stage("Stage 2")
    stage3 = Stage("Stage 3")

    # Food carts (2)
    food1 = FoodCart("Food Court A")
    food2 = FoodCart("Food Court B")

    # Bathroom clusters (8)
    bathA1 = Bathroom("Bathroom A1")
    bathA2 = Bathroom("Bathroom A2")
    bathA3 = Bathroom("Bathroom A3")
    bathA4 = Bathroom("Bathroom A4")

    bathB1 = Bathroom("Bathroom B1")
    bathB2 = Bathroom("Bathroom B2")
    bathB3 = Bathroom("Bathroom B3")
    bathB4 = Bathroom("Bathroom B4")

    # Nurse tents (2)
    nurse1 = NurseTent("Nurse Tent A")
    nurse2 = NurseTent("Nurse Tent B")

    # Collect all for iteration
    all_locations = [
        stage1, stage2, stage3,
        food1, food2,
        bathA1, bathA2, bathA3, bathA4,
        bathB1, bathB2, bathB3, bathB4,
        nurse1, nurse2
    ]

    # ------------------------------------------------
    # 2. DEFINE NEIGHBORS (NO makeNeighbours)
    # ------------------------------------------------

    # Stages ↔ Food
    stage1.neighbours = [food1, bathA1]
    stage2.neighbours = [food1, food2]
    stage3.neighbours = [food2, bathB1]

    food1.neighbours = [stage1, stage2, bathA1]
    food2.neighbours = [stage2, stage3, bathB1]

    # Bathrooms cluster A: all connected to food1 + nurse1
    for b in [bathA1, bathA2, bathA3, bathA4]:
        b.neighbours = [food1, nurse1]

    # Bathrooms cluster B: all connected to food2 + nurse2
    for b in [bathB1, bathB2, bathB3, bathB4]:
        b.neighbours = [food2, nurse2]

    # Nurse tents connected back to cluster roots + food
    nurse1.neighbours = [bathA1, food1]
    nurse2.neighbours = [bathB1, food2]

    # ------------------------------------------------
    # 3. DRUG DEALERS
    # ------------------------------------------------
    dealers = [
        DrugDealer("Tony", stage1),
        DrugDealer("Mia", stage2),
        DrugDealer("Snake", stage3)
    ]

    # ------------------------------------------------
    # 4. SECURITY GUARDS
    # ------------------------------------------------

    guardA = SecurityGuard(#probably redo
        ID=1,
        locations=[stage1, food1, bathA1, bathA2, bathA3, bathA4, nurse1],
        nurse_location=nurse1,
        exit_location=nurse1   # placeholder: no exits yet
    )

    guardB = SecurityGuard(
        ID=2,
        locations=[stage3, food2, bathB1, bathB2, bathB3, bathB4, nurse2],
        nurse_location=nurse2,
        exit_location=nurse2   # placeholder
    )

    guardA.start()
    guardB.start()

    #dictionary to hold locations 


    # ------------------------------------------------
    # 5. LOCATION LIST FOR SPECTATOR CLASS
    # ------------------------------------------------

    locationList = {
        'stages': [stage1, stage2, stage3],
        'foodCarts': [food1, food2],
        'bathrooms': [
            bathA1, bathA2, bathA3, bathA4,
            bathB1, bathB2, bathB3, bathB4
        ],
        'dealers': dealers,
        'nurse': [nurse1, nurse2],
        'all': all_locations,
        'exists': []  
    }

    # ------------------------------------------------
    # 6. SPAWN SPECTATORS OVER TIME
    # ------------------------------------------------

    clock = Clock()
    spectators = []

    print("Spawning spectators...")

    while clock.getTime() < 5:
        time.sleep(0.1)

        personality = random.choice(list(personalities.values()))
        start_loc = random.choice(all_locations)

        sp = Spectator(
            ID=f"S{random.randint(1000,9999)}",
            personality=personality,
            locations=locationList,
            start=start_loc,
            clock=clock
        )

        sp.start()
        spectators.append(sp)


    # ------------------------------------------------
    # 7. LET SIMULATION RUN
    # ------------------------------------------------

    print("Simulation running...")

    time.sleep(60)  # run festival for 60 seconds

    # ------------------------------------------------
    # 8. STOP SECURITY GUARDS
    # ------------------------------------------------

    guardA.stop()
    guardB.stop()

    print("\nSimulation finished.\n")


    if __name__ == "__main__":
        main()

main()