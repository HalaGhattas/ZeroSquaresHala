import heapq
from copy import deepcopy

class Game:
    def __init__(self, rows, cols, board_data):
        self.rows = rows
        self.cols = cols
        self.walls = deepcopy(board_data["walls"])
        self.goals = deepcopy(board_data["goals"])
        self.players = deepcopy(board_data["players"])
        self.reach_goal = [False] * len(board_data["players"])

    def __lt__(self, other):
        return self.get_cost() < other.get_cost()

    def get_cost(self):
        return sum(1 for player in self.players if not self.reach_goal[self.players.index(player)])

    def is_won(self):
        return all(self.reach_goal)

    def is_valid_move(self, row, col, player_idx):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False
        if (row, col) in self.walls:
            return False
        for j, other_player in enumerate(self.players):
            if j != player_idx and other_player["position"] == (row, col):
                return False
        if self.reach_goal[player_idx] and (row, col) != self.goals[player_idx]["position"]:
            return False
        return True

    def simulate_move(self, _row, _col):
        new_states = []
        for idx, player in enumerate(self.players):
            if self.reach_goal[idx]:
                continue
            current_row, current_col = player["position"]
            while True:
                next_row = current_row + _row
                next_col = current_col + _col
                if not self.is_valid_move(next_row, next_col, idx):
                    break
                current_row, current_col = next_row, next_col
                if (current_row, current_col) == self.goals[idx]["position"]:
                    self.reach_goal[idx] = True
                    break
            if (current_row, current_col) != player["position"]:
                cloned_game = deepcopy(self)
                cloned_game.players[idx]["position"] = (current_row, current_col)
                new_states.append(cloned_game)
        return new_states

    
    
    def heuristic(self):
        for i in self.players:
            for j in self.goals:
                if self.players[i]["color"] == self.goals[j]["color"]:
                    return abs(self.player["position"] - self.goals["position"]) 
