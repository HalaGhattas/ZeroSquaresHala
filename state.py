
from copy import deepcopy

class State:  # Game state
    def __init__(self, walls, goals, players, has_reached_goal):
        self.has_reached_goal = has_reached_goal
        self.walls = walls
        self.goals = goals
        self.players = players

    def copy(self):
        return deepcopy(self)
