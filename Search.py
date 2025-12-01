

class Search:
    def __init__(self, spectator, request, start):
        self.spectator=spectator
        self.request=request
        self.visited=[]
        self.pending=[(start, [])]
        self.startSearch(start)
    
    def startSearch(self, start):
        #This is a breadth first search
        #It gets the nearest location that fulfills requirements and the path to it
        #Then it starts the movement sequence
        if start in self.request:
            return
        while len(self.pending)>0:
            l = self.pending.pop(0)
            location, path = l[0], l[1]
            if location in self.request:
                start.sendTo(self.spectator, path)
                break
            elif location in self.visited:
                continue
            else:
                self.visited.append(location)
                for neigh in location.neighbours():
                    self.pending.append((neigh, path+[neigh]))
                    
