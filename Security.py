''''''
import threading
import random
import time


class SecurityGuard(threading.Thread):
    def __init__(self, ID, assigned_locations, nurse_location, exit_location):
        super().__init__()
        self.ID = ID
        self.assigned_locations = assigned_locations
        self.nurse_location = nurse_location
        self.exit_location = exit_location
        self.current_location = assigned_locations[0] if assigned_locations else None
        self.detained_spectators = []  # This would be the list of spectators currently being escorted out
        self.is_active = True

    def run(self):
        # This will be the main loop for security guard behavior
        while self.is_active:
            # patrol all assigned locations
            for location in self.assigned_locations:
                self.current_location = location
                self.check_for_fights()
                self.check_for_wasted_spectators()
                self.check_for_drugged_spectators()

                # Time to check the location (patrol speed)
                time.sleep(2)
            # Small pause between patrol cycles
            time.sleep(1)

    def check_for_fights(self):
        # Check current location for fighting spectators
        fighting_list = self.current_location.getStateList('fighting')
        if fighting_list and len(fighting_list) > 0:
            # Security intervenes in fights
            for spectator in fighting_list[:]:  # Copy the list to avoid modification during iteration
                self.intervene_fight(spectator)

    def check_for_wasted_spectators(self):
        # Check for heavily intoxicated spectators
        wasted_list = self.current_location.getStateList('wasted')

        if wasted_list and len(wasted_list) > 0:
            for spectator in wasted_list[:]:
                # Random chance to notice and help wasted spectators
                if random.random() < 0.3:  # 30% chance per check
                    self.help_wasted_spectator(spectator)

    def check_for_drugged_spectators(self):
        drugged_list = self.current_location.getStateList('drugged')

        if drugged_list and len(drugged_list) > 0:
            for spectator in drugged_list[:]:
                # Check if spectator needs medical attention
                # You can add more conditions here based on spectator's state
                if random.random() < 0.2:  # 20% chance - serious reaction
                    self.emergency_medical_response(spectator)

    def intervene_fight(self, spectator):
        print(f"Security Guard {self.ID}: Intervening in fight with Spectator {spectator.attributes['ID']}")

        # Remove fighting state
        self.current_location.removeState(spectator, 'fighting')

        # Determine action based on random severity or could be based on spectator's fight history
        action = random.choice(['warning', 'warning', 'escort_out', 'escort_out', 'nurse'])

        if action == 'warning':
            print(f"Security Guard {self.ID}: Warning issued to Spectator {spectator.attributes['ID']}")
            # Could add a warning counter to spectator's attributes
            time.sleep(1)

        elif action == 'escort_out':
            print(f"Security Guard {self.ID}: Escorting Spectator {spectator.attributes['ID']} out of festival")
            self.escort_to_exit(spectator)

        elif action == 'nurse':
            print(f"Security Guard {self.ID}: Taking injured Spectator {spectator.attributes['ID']} to nurse")
            self.escort_to_nurse(spectator)

    def help_wasted_spectator(self, spectator):
        print(f"Security Guard {self.ID}: Found wasted Spectator {spectator.attributes['ID']}")

        # Decide based on severity
        if random.random() < 0.5:
            # Take to medical tent
            print(f"Security Guard {self.ID}: Taking Spectator {spectator.attributes['ID']} to nurse")
            self.escort_to_nurse(spectator)
        else:
            # Just monitoring, let them be
            print(f"Security Guard {self.ID}: Monitoring Spectator {spectator.attributes['ID']}")

    def emergency_medical_response(self, spectator):
        print(f"Security Guard {self.ID}: MEDICAL EMERGENCY - Spectator {spectator.attributes['ID']}")
        self.escort_to_nurse(spectator)

    def escort_to_nurse(self, spectator):
        # Add spectator to detained list
        self.detained_spectators.append(spectator)

        # Move spectator to nurse
        success = self.current_location.sendTo(spectator, self.nurse_location)

        if success:
            print(f"Security Guard {self.ID}: Delivered Spectator {spectator.attributes['ID']} to nurse")
            # Spectator is now at nurse location
            # The nurse location should handle recovery
        else:
            print(f"Security Guard {self.ID}: Failed to escort Spectator {spectator.attributes['ID']}")

        # Remove from detained list after delivery
        if spectator in self.detained_spectators:
            self.detained_spectators.remove(spectator)

        # Time to escort
        time.sleep(3)

    def escort_to_exit(self, spectator):
        # Add spectator to detained list
        self.detained_spectators.append(spectator)

        # Move spectator to exit
        success = self.current_location.sendTo(spectator, self.exit_location)

        if success:
            print(f"Security Guard {self.ID}: Removed Spectator {spectator.attributes['ID']} from festival")
            # Optionally: stop the spectator's thread
            spectator.is_active = False
        else:
            print(f"Security Guard {self.ID}: Failed to remove Spectator {spectator.attributes['ID']}")

        # Remove from detained list
        if spectator in self.detained_spectators:
            self.detained_spectators.remove(spectator)

        # Time to escort
        time.sleep(5)

    def stop(self):
        self.is_active = False
        print(f"Security Guard {self.ID}: Going off duty")


# Example usage:
if __name__ == "__main__":
    # Create locations (using your Location class, put these ones of what I remember)
    stage1 = Location()
    stage2 = Location()
    bathroom = Location()
    food_area = Location()
    nurse_tent = Location()
    exit_gate = Location()

    # Create security guard assigned to patrol stage areas and bathroom
    guard1 = SecurityGuard(
        ID=1,
        assigned_locations=[stage1, stage2, bathroom],
        nurse_location=nurse_tent,
        exit_location=exit_gate
    )

    # Create another guard for food area
    guard2 = SecurityGuard(
        ID=2,
        assigned_locations=[food_area],
        nurse_location=nurse_tent,
        exit_location=exit_gate
    )

    # Start security guards
    guard1.start()
    guard2.start()

    # Stop guards when simulation ends
    guard1.stop()
    guard2.stop()

''''''  