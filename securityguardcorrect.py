import threading
import random
import time
from global_metrics import metrics


class SecurityGuard(threading.Thread):
    def __init__(self, ID, locations, nurse_location, exit_location):
        super().__init__()
        self.ID = ID
        self.locations = locations
        self.nurse_location = nurse_location
        self.exit_location = exit_location
        self.active = True
        self.nurse_history = {}   # track nurse visits

    def run(self):
        while self.active:
            for loc in self.locations:
                self.break_up_fights(loc)
                self.handle_wasted(loc)
                self.handle_drugged(loc)
                time.sleep(1)
            time.sleep(1)

    # -----------------------------------------
    # 1. Break up fights
    # -----------------------------------------
    def break_up_fights(self, location):
        fighters = location.getStateList("fighting")
        if not fighters:
            return

        for spectator in fighters:
            # Interrupt the fight
            spectator.is_fighting = False
            location.removeState(spectator, "fighting")

            print(f"[Security {self.ID}] Breaks up fight involving {spectator.attributes['ID']}")

            # LOG THE EVENT
            metrics.log_security_event("fight_break", spectator.attributes['ID'], self.ID)

            # 50%: escort out, 50%: warn
            if random.random() < 0.5:
                self.escort_out(spectator, location)
            else:
                print(f"[Security {self.ID}] Issues warning to {spectator.attributes['ID']}")

    # -----------------------------------------
    # 2. Handle wasted spectators
    # -----------------------------------------
    def handle_wasted(self, location):
        wasted = location.getStateList("wasted")
        if not wasted:
            return

        for s in wasted:
            if random.random() < 0.3:
                print(f"[Security {self.ID}] Assists wasted spectator {s.attributes['ID']}")
                self.escort_to_nurse(s, location)

    # -----------------------------------------
    # 3. Handle drugged spectators
    # -----------------------------------------
    def handle_drugged(self, location):
        drugged = location.getStateList("drugged")
        if not drugged:
            return

        for s in drugged:
            if random.random() < 0.2:
                print(f"[Security {self.ID}] DRUG EMERGENCY — {s.attributes['ID']}")
                self.escort_to_nurse(s, location)

    # -----------------------------------------
    # ESCORT HELPERS
    # -----------------------------------------
    def escort_to_nurse(self, spectator, location):

        # Track how many times this spectator was sent to nurse
        if spectator not in self.nurse_history:
            self.nurse_history[spectator] = 0

        self.nurse_history[spectator] += 1

        # If the person has been sent twice → kick them out
        if self.nurse_history[spectator] >= 2:
            print(f"[Security {self.ID}] {spectator.attributes['ID']} has been sent to nurse twice → KICKING OUT.")
            
            # LOG THE EVENT
            metrics.log_security_event("kicked_out_repeat_offender", spectator.attributes['ID'], self.ID)

            self.escort_out(spectator, location)
            return

        # Regular nurse escort
        success = location.sendTo(spectator, self.nurse_location)
        if success:
            print(f"[Security {self.ID}] Delivered {spectator.attributes['ID']} to Nurse Tent")

            # LOG THE EVENT
            metrics.log_security_event("sent_to_nurse", spectator.attributes['ID'], self.ID)

        else:
            print(f"[Security {self.ID}] Failed to move {spectator.attributes['ID']} to nurse")

        time.sleep(2)

    def escort_out(self, spectator, location):
        success = location.sendTo(spectator, self.exit_location)
        if success:
            print(f"[Security {self.ID}] Removes {spectator.attributes['ID']} from festival")

            # LOG THE EVENT
            metrics.log_security_event("kicked_out", spectator.attributes['ID'], self.ID)

            spectator.is_active = False
        else:
            print(f"[Security {self.ID}] Failed to escort {spectator.attributes['ID']} out")

        time.sleep(3)

    def stop(self):
        self.active = False
        print(f"[Security {self.ID}] Going off duty.")
