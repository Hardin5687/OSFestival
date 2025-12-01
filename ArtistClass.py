import threading
import random
import time

musicStyles = ['rock', 'reggaeton', 'techno', 'pop', 'hiphop', 'jazz']



class Artist(threading.Thread):
    def __init__(self, artist_id, skill, MusicStyle, prob_drink=0.3, prob_drugs=0.1):
        super().__init__()
        self.id = artist_id
        self.skill = skill
        self.prob_drink = prob_drink
        self.prob_drugs = prob_drugs
        self.health = 100
        self.on_stage = False
        self.lock = threading.Lock()

    def perform(self, stage):
        with self.lock:
            self.on_stage = True

            # Artist sets the stage music
            stage.setMusic(self.genre)

            print(f"Artist {self.id} starts performing {self.genre} on {stage.name}. Skill: {self.skill}/10")

            # Perform for 3 time units
            for _ in range(3):
                time.sleep(1)
                self.health -= random.randint(1, 5)
                print(f"Artist {self.id} performs... (health {self.health})")

                # Chance to drink or take drugs
                if random.random() < self.prob_drink:
                    self.drink_alcohol()

                if random.random() < self.prob_drugs:
                    self.take_drugs()

            print(f"Artist {self.id} ends performance on {stage.name} with health {self.health}.")
            self.on_stage = False

    def take_drugs(self):
        with self.lock:
            self.skill += 0.5
            self.health -= 10
            print(f"Artist {self.id} takes drugs! (skill {self.skill:.1f}, health {self.health})")

    def drink_alcohol(self):
        with self.lock:
            self.skill -= 0.2
            self.health -= 5
            print(f"Artist {self.id} drinks alcohol! (skill {self.skill:.1f}, health {self.health})")

    def run(self):
        while self.health > 0:
            # Rest between performances
            time.sleep(random.randint(5, 10))
            print(f"Artist {self.id} rests backstage...")
            self.health = min(100, self.health + 10)

        print(f"Artist {self.id} can no longer perform (health depleted).")
