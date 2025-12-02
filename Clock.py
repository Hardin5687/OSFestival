import time

class Clock():
    def __init__(self):
        self.start = time.time()
        
    def getTime(self):
        t=round((time.time()-self.start)/60, 2)
        return t
