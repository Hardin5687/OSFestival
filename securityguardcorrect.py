import threading
import random
import time

class SecurityGuard(threading.Thread):
    def __init__(self, ID, locations, nurse_location, exit_location):
        super().__init__()
        self.ID = ID
        self.locations = locations              # list of Location objects
        self.nurse_location = nurse_location
        self.exit_location = exit_location
        self.active = True

    def run(self):
        # Simple patrol loop
        while self.active:
            for loc in self.locations:
                self.break_up_fights(loc)
                self.handle_wasted(loc)
                self.handle_drugged(loc)
                time.sleep(1)  # patrol speed
            time.sleep(1)

    # 1. Fight handling — interrupts fights
    def break_up_fights(self, location):
        fighters = location.getStateList("fighting")
        if not fighters:
            return

        for spectator in fighters:
            # Interrupt fight
            spectator.is_fighting = False                   # <<< CRITICAL
            location.removeState(spectator, "fighting")

            print(f"[Security {self.ID}] Breaks up fight involving {spectator.attributes['ID']}")

            # 50%: escort out, 50%: warn
            if random.random() < 0.5:
                self.escort_out(spectator, location)
            else:
                print(f"[Security {self.ID}] Issues warning to {spectator.attributes['ID']}")

    # 2. Drunk / wasted handling
    def handle_wasted(self, location):
        wasted = location.getStateList("wasted")
        if not wasted:
            return

        for s in wasted:
            # 30% chance to help
            if random.random() < 0.3:
                print(f"[Security {self.ID}] Assists wasted spectator {s.attributes['ID']}")
                self.escort_to_nurse(s, location)

    # 3. Drugged emergency handling
    def handle_drugged(self, location):
        drugged = location.getStateList("drugged")
        if not drugged:
            return

        for s in drugged:
            # 20% chance for medical emergency
            if random.random() < 0.2:
                print(f"[Security {self.ID}] DRUG EMERGENCY — {s.attributes['ID']}")
                self.escort_to_nurse(s, location)

    # ESCORT HELPERS
    def escort_to_nurse(self, spectator, location):
        success = location.sendTo(spectator, self.nurse_location)
        if success:
            print(f"[Security {self.ID}] Delivered {spectator.attributes['ID']} to Nurse Tent")
        else:
            print(f"[Security {self.ID}] Failed to move {spectator.attributes['ID']} to nurse")

        time.sleep(2)

    def escort_out(self, spectator, location):
        success = location.sendTo(spectator, self.exit_location)
        if success:
            print(f"[Security {self.ID}] Removes {spectator.attributes['ID']} from festival")
            # Optionally disable spectator actions
            spectator.is_active = False
        else:
            print(f"[Security {self.ID}] Failed to escort {spectator.attributes['ID']} out")

        time.sleep(3)

    # Stop the guard thread
    def stop(self):
        self.active = False
        print(f"[Security {self.ID}] Going off duty.")
