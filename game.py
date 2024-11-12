
from state import State
from copy import deepcopy

class Game:
    def __init__(self, rows, cols, board_details):
        self.cols = cols
        self.rows = rows
        self.state = State(
            players=deepcopy(board_details["players"]),
            goals=deepcopy(board_details["goals"]),
            walls=deepcopy(board_details["walls"]),
            has_reached_goal=[False] * len(board_details["players"])
        )

    def check_win(self):
        return all(self.state.has_reached_goal)

    def move_players(self, _row, _col):
        new_state = self.state.copy()
        for i, player in enumerate(new_state.players):
            if new_state.has_reached_goal[i]:
                continue
            new_row_step, new_col_step = player["position"]
            while True:
                next_row, next_col = new_row_step + _row, new_col_step + _col
                if not self.move_valid(next_row, next_col, i):
                    break
                new_row_step, new_col_step = next_row, next_col
                if (new_row_step, new_col_step) == new_state.goals[i]["position"]:
                    new_state.has_reached_goal[i] = True
                    break
            if (new_row_step, new_col_step) != player["position"]:
                new_state.players[i]["position"] = (new_row_step, new_col_step)

        return new_state, self.check_win()

    def move_valid(self, row, col, current_player):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False
        if (row, col) in self.state.walls:
            return False
        for j, other_player in enumerate(self.state.players):
            if j != current_player and other_player["position"] == (row, col):
                return False
        if self.state.has_reached_goal[current_player] and (row, col) != self.state.goals[current_player]["position"]:
            return False
        return True

    def next_state(self, _row, _col):
        new_state, _ = self.move_players(_row, _col)
        return new_state
