from SpectatorClass import Spectator
from LocationClass import Location
from StageClass import Stage
from bathroomClass import Bathroom
from NurseClass import NurseTent
from FoodCart import FoodCart
from drugdealerClass import DrugDealer
from securityGuard import SecurityGuard
from Clock import Clock
from ArtistClass import Artist
from global_metrics import metrics

import random
import time

personalities = {
    #A dictionary of archetypes. Different personalities prefer different things
    'averageJoe':{'flirt':3, 'fight':3, 'alcohol':3, 'drug':3, 'musicFave':None, 'musicHate':None, 'moneyMax':150, 'moneyMin':50},
    'drunk':{'flirt':4, 'fight':4, 'alcohol':5, 'drug':3, 'musicFave':'rock', 'musicHate':'jazz', 'moneyMax':100, 'moneyMin':30},
    'punk':{'flirt':3, 'fight':4, 'alcohol':3, 'drug':4, 'musicFave':'rock', 'musicHate':'jazz', 'moneyMax':140, 'moneyMin':40},
    'junkie':{'flirt':2, 'fight':3, 'alcohol':3, 'drug':5, 'musicFave':'techno', 'musicHate':'pop', 'moneyMax':80, 'moneyMin':30},
    'hipster':{'flirt':3, 'fight':2, 'alcohol':2, 'drug':3, 'musicFave':'hiphop', 'musicHate':'techno', 'moneyMax':170, 'moneyMin':60},
    'businessman':{'flirt':2, 'fight':2, 'alcohol':3, 'drug':1, 'musicFave':'pop', 'musicHate':'rock', 'moneyMax':400, 'moneyMin':200},
    'artist':{'flirt':4, 'fight':2, 'alcohol':3, 'drug':4, 'musicFave':'jazz', 'musicHate':'pop', 'moneyMax':180, 'moneyMin':50},
    'goth':{'flirt':2, 'fight':3, 'alcohol':3, 'drug':2, 'musicFave':'rock', 'musicHate':'pop', 'moneyMax':120, 'moneyMin':40},
    'romantic':{'flirt':5, 'fight':3, 'alcohol':2, 'drug':1, 'musicFave':'pop', 'musicHate':'rock', 'moneyMax':160, 'moneyMin':60},
    'rebel':{'flirt':4, 'fight':4, 'alcohol':4, 'drug':4, 'musicFave':'rock', 'musicHate':'classical', 'moneyMax':130, 'moneyMin':30},
    'gamer':{'flirt':2, 'fight':2, 'alcohol':2, 'drug':2, 'musicFave':'techno', 'musicHate':'jazz', 'moneyMax':170, 'moneyMin':70},
    'intellectual':{'flirt':2, 'fight':1, 'alcohol':2, 'drug':1, 'musicFave':'jazz', 'musicHate':'reggaeton', 'moneyMax':250, 'moneyMin':100},
    'stoner':{'flirt':3, 'fight':2, 'alcohol':2, 'drug':5, 'musicFave':'hiphop', 'musicHate':'techno', 'moneyMax':120, 'moneyMin':30},
    'partyAnimal':{'flirt':5, 'fight':3, 'alcohol':5, 'drug':4, 'musicFave':'reggaeton', 'musicHate':'rock', 'moneyMax':220, 'moneyMin':40},
    'loner':{'flirt':1, 'fight':2, 'alcohol':1, 'drug':2, 'musicFave':'jazz', 'musicHate':'techno', 'moneyMax':100, 'moneyMin':30},
    'musician':{'flirt':4, 'fight':2, 'alcohol':3, 'drug':3, 'musicFave':'jazz', 'musicHate':'pop', 'moneyMax':180, 'moneyMin':60}
}

musicStyles = ['rock', 'reggaeton', 'techno', 'pop', 'hiphop', 'jazz']

def main():
    # Stages (3)
    stage1 = Stage("Stage 1")
    stage2 = Stage("Stage 2")
    stage3 = Stage("Stage 3")

    # Food carts (2)
    food1 = FoodCart("Food Court A")
    food2 = FoodCart("Food Court B")

    # Bathroom clusters (2)
    bath1 = Bathroom("Bathroom A", capacity=12)
    bath2 = Bathroom("Bathroom B", capacity=12)

    # Nurse tents (2)
    nurse1 = NurseTent("Nurse Tent A")
    nurse2 = NurseTent("Nurse Tent B")

    # Exit gate (plain Location)
    gate = Location()
    gate.name = "Exit Gate"

    # Collect all for iteration
    all_locations = [
        stage1, stage2, stage3,
        food1, food2,
        bath1, bath2,
        nurse1, nurse2,
        gate
    ]

    # Stage <-> Food
    stage1.neighbours = [food1]
    stage2.neighbours = [food1, food2]
    stage3.neighbours = [food2]

    food1.neighbours = [stage1, stage2]
    food2.neighbours = [stage2, stage3]

    # Bathrooms cluster A (Bathroom A <-> Food1, Nurse1)
    bath1.makeNeighbours([food1, nurse1])

    # Bathrooms cluster B (Bathroom B <-> Food2, Nurse2)
    bath2.makeNeighbours([food2, nurse2])

    # Nurse tents
    nurse1.neighbours = [food1]
    nurse2.neighbours = [food2]

    # Exit Gate -> Stages
    gate.neighbours = [stage1, stage2, stage3]

    # Stages -> Exit Gate  (bidirectional required!)
    stage1.neighbours.append(gate)
    stage2.neighbours.append(gate)
    stage3.neighbours.append(gate)
    
    dealers = [
        DrugDealer(stage1, 'Johnny Navajas'),
        DrugDealer(stage2, 'Mia Falcone'),
        DrugDealer(stage3, 'Snake? Snaaaaaaake!')
    ]

    locationList = {
        'stages': [stage1, stage2, stage3],
        'foodCarts': [food1, food2],
        'bathrooms': [bath1, bath2],
        'dealers': dealers,
        'nurse': [nurse1, nurse2],
        'all': all_locations,
        'exits': [gate]
    }

    clock = Clock(dayLength=1)
    clock.start()

    security = [
        SecurityGuard([stage1], locationList, clock, name='James Bond'),
        SecurityGuard([stage2], locationList, clock, name='Jason Bourne'),
        SecurityGuard([stage3], locationList, clock, name='OS Teacher'),
        SecurityGuard([food1, nurse1, bath1], locationList, clock, name='Big Boss'),
        SecurityGuard([food2, nurse2, bath2], locationList, clock, name='Lieutenant Dan')
    ]
    for guard in security:
        guard.start()

    for genre in musicStyles:
        artist = Artist(f'{genre}', random.randint(5, 10), genre, locationList, clock)
        artist.start()

    ID = 1
    while clock.getTime() < clock.dayLength/2:
        time.sleep(1)
        size = random.randint(0, 4) % 4  # group size 1–4
        group = []

        start = random.choice(locationList['stages'])

        for i in range(size + 1):
            ticket_price = random.randint(50, 150)
            metrics.log_ticket(ID, ticket_price)

            sp = Spectator(
                ID,
                random.choice(list(personalities.values())),
                locationList,
                start,
                clock
            )
            group.append(sp)
            ID += 1

        # Set friendships inside the group
        for sp in group:
            for friend in group:
                if sp != friend:
                    sp.relationships.append(friend)

        # Start spectator threads
        for sp in group:
            sp.start()


if __name__ == "__main__":
    main()
