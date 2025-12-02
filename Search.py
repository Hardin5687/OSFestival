class Search:
    def __init__(self, spectator, request, start):
        self.spectator = spectator
        self.request = request
        self.start = start
        self.run()

    def run(self):
        # If already at destination → do nothing (but return True so caller knows)
        if self.start in self.request:
            return True
        # BFS
        from collections import deque
        queue = deque()
        queue.append((self.start, []))
        visited = set()
        while queue:
            current, path = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            # Found target
            if current in self.request:
                self.start.sendTo(self.spectator, path)
                return True

            # Expand neighbors
            for neigh in current.neighbours:
                if neigh not in visited:
                    queue.append((neigh, path + [neigh]))

        # No path found
        return False
