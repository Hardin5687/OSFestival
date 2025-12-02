import threading
from LocationClass import Location

class Stage(Location):
    def __init__(self, name=None):
        super().__init__()
        self.name = name
        self.music = None
        self.quality=0
        self.states['dancing']={'list': [], 'lock': threading.Lock()}

    def setMusic(self, genre):
        # Artist sets the current music playing on this stage
        self.music = genre
        print(f"Stage {self.name}: Music changed to {self.music}")

