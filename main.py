from SpectatorClass import Spectator
from LocationClass import Location
from StageClass import Stage
from bathroomClass import Bathroom
from FoodCart import FoodCart
from drugdealerClass import DrugDealer
from Clock import Clock
import threading
import concurrent.futures
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
    locationList = {
        'all':[],
        'exits': [Location()],
        'stages': [Stage()],
        'foodCarts': [FoodCart()],
        'bathrooms': [Bathroom()]
        }
    for key in locationList.keys():
        if key != 'all':
            for location in locationList[key]:
                locationList['all'].append(location)
    for location in locationList['all']:
        for neigh in locationList['all']:
            if location != neigh:
                location.makeNeighbours(neigh)
    locationList['dealers']=[DrugDealer(locationList['stages'][0])]
    clock = Clock()
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        while clock.getTime()<5:
            time.sleep(0.1)
            executor.submit(Spectator, personalities[random.choice(list(personalities.keys()))], locationList, clock)
    #Make locations
    #Connect locations
    #Make clock
    #Start generating spectators
        #Make number
        #Make that number of spectators
        #Add them all to each other's friends list
    
main()



