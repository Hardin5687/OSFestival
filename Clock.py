import time
import threading

class Clock(threading.Thread):
    def __init__(self, dayLength=6):
        super().__init__()
        self.active = True
        self.startTime = None
        self.dayLength=dayLength
        self.lock=threading.Lock()
        self.comingBack=[]
        self.day=1
        
    def getTime(self):
        t=round((time.time()-self.startTime)/60, 2)
        return t

    def run(self):
        self.startTime=time.time()
        while self.getTime()<self.dayLength+1:
            time.sleep(0.1)
        print('DAY 1 ENDED')
        time.sleep(15)
        print('DAY 2 BEGINS')
        self.day=2
        self.startTime=time.time()
        for thing in self.comingBack:
            thing.active=True
        while round((time.time()-self.startTime)/60, 2)<self.dayLength+0.5:
            time.sleep(0.1)
        print('DAY 2 ENDED')
        time.sleep(5)
        print('DAY 3 BEGINS')
        self.day=3
        self.startTime=time.time()
        for thing in self.comingBack:
            thing.active=True
        while round((time.time()-self.startTime)/60, 2)<self.dayLength+0.5:
            time.sleep(0.1)
        print('DAY 3 ENDED')
        self.active=False
        
        


