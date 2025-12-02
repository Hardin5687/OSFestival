import threading
import random
import time
from global_metrics import metrics
from Search import Search


class SecurityGuard(threading.Thread):
    def __init__(self, locations, locationList, clock, name=None):
        super().__init__()
        self.ID = name
        self.locations = locations
        self.locationList = locationList
        self.active = True
        self.nurse_history = {}
        self.clock=clock

    def run(self):
        while self.clock.active:
            while self.active:
                for loc in self.locations:
                    self.break_up_fights(loc)
                    self.handle_wasted(loc)
                    self.handle_drugged(loc)
                    time.sleep(1)
                if self.clock.getTime()>self.clock.dayLength:
                    self.active=False
                    exit=True
                time.sleep(1)
            if exit:
                self.nurse_history={}
                with self.clock.lock:
                    self.clock.comingBack.append(self)
                exit=False
            time.sleep(0.1)

    # -----------------------------------------
    # 1. Break up fights
    # -----------------------------------------
    def break_up_fights(self, location):
        fighters = location.getStateList("fighting")
        if not fighters:
            return

        spectator = random.choice(fighters)
        # Interrupt the fight
        spectator.is_fighting = False
        location.removeState(spectator, "fighting")
        print(f"Security {self.ID} Breaks up fight involving {spectator.attributes['ID']}")
        # LOG THE EVENT
        metrics.log_security_event("fight_break", spectator.attributes['ID'], self.ID)
        # 50%: escort out, 50%: warn
        if random.random() < 0.5:
            self.escort_out(spectator, location)
        else:
            print(f"Security {self.ID} Issues warning to {spectator.attributes['ID']}")

    def handle_wasted(self, location):
        wasted = location.getStateList("wasted")
        if not wasted:
            return
        for s in wasted:
            if random.random() < 0.3:
                print(f"Security {self.ID} Assists wasted spectator {s.attributes['ID']}")
                self.escort_to_nurse(s, location)

    def handle_drugged(self, location):
        drugged = location.getStateList("drugged")
        if not drugged:
            return

        for s in drugged:
            if random.random() < 0.2:
                print(f"Security {self.ID} DRUG EMERGENCY — {s.attributes['ID']}")
                self.escort_to_nurse(s, location)
                
    def escort_to_nurse(self, spectator, location):

        # Track how many times this spectator was sent to nurse
        if spectator not in self.nurse_history:
            self.nurse_history[spectator] = 0

        self.nurse_history[spectator] += 1

        # If the person has been sent twice → kick them out
        if self.nurse_history[spectator] >= 2:
            print(f"Security {self.ID} {spectator.attributes['ID']} has been sent to nurse twice → KICKING OUT.")
            
            # LOG THE EVENT
            metrics.log_security_event("kicked_out_repeat_offender", spectator.attributes['ID'], self.ID)

            self.escort_out(spectator, location)
            return

        # Regular nurse escort
        Search(spectator, self.locationList['nurse'], location)
        if spectator.location in self.locationList['nurse']:
            print(f"Security {self.ID} Delivered {spectator.attributes['ID']} to Nurse Tent")
            spectator.location.heal(spectator)
            # LOG THE EVENT
            metrics.log_security_event("sent_to_nurse", spectator.attributes['ID'], self.ID)

        else:
            print(f"Security {self.ID} Failed to move {spectator.attributes['ID']} to nurse")

        time.sleep(2)

    def escort_out(self, spectator, location):
        spectator.escorted=True
        Search(spectator, self.locationList['exits'], location)
        if spectator.location in self.locationList['exits']:
            print(f"Security {self.ID} Removes {spectator.attributes['ID']} from festival")
            # LOG THE EVENT
            try:
                metrics.log_security_event("kicked_out", spectator.attributes['ID'], self.ID)
            except:
                pass
            spectator.is_active = False
        else:
            print(f"Security {self.ID} Failed to escort {spectator.attributes['ID']} out")
        spectator.escorted=False
        time.sleep(3)

    def stop(self):
        self.active = False
        print(f"Security {self.ID} Going off duty.")
