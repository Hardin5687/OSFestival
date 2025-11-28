# artist class

import threading 
import random
import time

class Artist:
    def __init__(self, id, skill, genre, prob_drink = 0.3, prob_drugs = 0.1 ):
        threading.Thread.__init__(self)
        self.id = id
        self.skill = skill
        self.genre = genre
        self.prob_drink = prob_drink    
        self.prob__drugs = prob_drugs   
        self.health = 100
        self.on_stage = False
        self.lock = threading.Lock()    
    def perform(self, stage):
        # Artist goes on stage and performs
        with self.lock:
            self.on_stage = True
            print(f"{self.name} starts performing {self.music_type} on {stage.name}. Skill: {self.skill}/10")
            # Health slowly decreases during performance
            for _ in range(3): #assume 3 time units of performance
                time.sleep(1)
                self.health -= random.randint(1, 5)
                print(f"{self.name} performs... (health {self.health})")
                # Chance to drink or take drugs mid-show
                if random.random() < self.drink_prob:
                    self.drink()
                if random.random() < self.drug_prob:
                    self.take_drugs()
            print(f"{self.name} finishes their set on {stage.name} with health {self.health}.")
            self.on_stage = False
    def take_drug(self):
        # Taking drugs boosts performance but reduces health
        with self.lock:
            self.skill += 0.5
            self.health -= 10
            print(f"{self.name} takes drugs! (skill {self.skill:.1f}, health {self.health})")

    def drink_alcohol(self):
        # Drinking alcohol slightly decreases performance but reduces health
        with self.lock:
            self.skill -= 0.2
            self.health -= 5
            print(f"{self.name} drinks alcohol! (skill {self.skill:.1f}, health {self.health})")
    def run(self):
        while self.health > 0:
            time.sleep(random.randint(5, 10))
            print(f"{self.name} is getting ready for a new performance...")
            # Choose a random stage if you later give them one
            # For now, just simulate rest between shows
            self.health = min(100, self.health + 10)
        print(f"{self.name} can no longer perform (health depleted).")

        