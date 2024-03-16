import heapq
import heapq
from Pieces import Piece

class AStar:
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal
        self.open_set = []
        self.closed_set = set()
        self.came_from = {}
        self.g_score = {start: 0}
        self.f_score = {start: self.heuristic(start)}

    def run(self):
        heapq.heappush(self.open_set, (self.f_score[self.start], self.start))

        while self.open_set:
            current = heapq.heappop(self.open_set)[1]

            if current == self.goal:
                return self.reconstruct_path(current)

            self.closed_set.add(current)

            for neighbor in self.get_neighbors(current):
                tentative_g_score = self.g_score[current] + self.distance(current, neighbor)

                if neighbor in self.closed_set and tentative_g_score >= self.g_score.get(neighbor, float('inf')):
                    continue

                if tentative_g_score < self.g_score.get(neighbor, float('inf')):
                    self.came_from[neighbor] = current
                    self.g_score[neighbor] = tentative_g_score
                    self.f_score[neighbor] = tentative_g_score + self.heuristic(neighbor)

                    if neighbor not in self.open_set:
                        heapq.heappush(self.open_set, (self.f_score[neighbor], neighbor))

        return None

    def get_neighbors(self, node):
        # Implement your logic to get the neighbors of a given node here
        pass

    def distance(self, node1, node2):
        # Implement your logic to calculate the distance between two nodes here
        pass

    def heuristic(self, node):
        # Implement your heuristic function here
        pass

    def reconstruct_path(self, current):
        path = [current]

        while current in self.came_from:
            current = self.came_from[current]
            path.append(current)

        return path[::-1]
    



class UCS:
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal
        self.open_set = []
        self.closed_set = set()
        self.came_from = {}
        self.g_score = {start: 0}

    def run(self):
        heapq.heappush(self.open_set, (self.g_score[self.start], self.start))

        while self.open_set:
            current = heapq.heappop(self.open_set)[1]

            if current == self.goal:
                return self.reconstruct_path(current)

            self.closed_set.add(current)

            for neighbor in self.get_neighbors(current):
                tentative_g_score = self.g_score[current] + self.distance(current, neighbor)

                if neighbor in self.closed_set and tentative_g_score >= self.g_score.get(neighbor, float('inf')):
                    continue

                if tentative_g_score < self.g_score.get(neighbor, float('inf')):
                    self.came_from[neighbor] = current
                    self.g_score[neighbor] = tentative_g_score

                    if neighbor not in self.open_set:
                        heapq.heappush(self.open_set, (self.g_score[neighbor], neighbor))

        return None

    def get_neighbors(self, node):
        # Implement your logic to get the neighbors of a given node here
        pass

    def distance(self, node1, node2):
        # Implement your logic to calculate the distance between two nodes here
        pass

    def reconstruct_path(self, current):
        path = [current]

        while current in self.came_from:
            current = self.came_from[current]
            path.append(current)

        return path[::-1]
    





class Node:
    def __init__(self, piece: Piece, heuristics, ASheuristic):
        self.piece = piece
        self.heuristics = heuristics
        self.ASheuristic = ASheuristic