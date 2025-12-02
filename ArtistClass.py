import threading
import random
import time

class Artist(threading.Thread):
    def __init__(self, artist_id, skill, MusicStyle, locationList, prob_drink=0.3, prob_drugs=0.1):
        super().__init__()
        self.id = artist_id
        self.skill = skill
        self.prob_drink = prob_drink
        self.prob_drugs = prob_drugs
        self.health = 10
        self.on_stage = False
        self.genre=MusicStyle
        self.locationList=locationList

    def perform(self, stage):
        print(f'{self.genre} artist performs in {stage.name}')
        self.on_stage = True
        # Artist sets the stage music
        stage.setMusic(self.genre)

        # Perform for 3 time units
        for _ in range(20):
            stage.quality=int((self.skill+self.health))
            time.sleep(1)
            self.health -= random.randint(1, 5)

            # Chance to drink or take drugs
            if random.random() < self.prob_drink:
                self.drink_alcohol()

            if random.random() < self.prob_drugs:
                self.take_drugs()
        
        stage.setMusic(None)
        stage.quality=0
        self.on_stage = False

    def take_drugs(self):
        self.skill += 0.5
        self.health -= 1

    def drink_alcohol(self):
        self.skill -= 0.2
        self.health -= 0.5

    def run(self):
        time.sleep(random.randint(5, 15))
        while self.health > 0:
            for stage in self.locationList['stages']:
                if stage.music==None:
                    self.perform(stage)
                    break
            if random.random() < self.prob_drink:
                self.drink_alcohol()
            if random.random() < self.prob_drugs:
                self.take_drugs()
            # Rest between performances
            siesta = random.randint(5, 10)
            time.sleep(siesta)
            self.health+=siesta
        print('Overdose')
