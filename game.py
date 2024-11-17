from copy import deepcopy
from collections import deque


class Game:
    def __init__(self, rows, cols, board_data):
        self.rows = rows
        self.cols = cols
        self.walls = deepcopy(board_data["walls"])
        self.goals = deepcopy(board_data["goals"])
        self.players = deepcopy(board_data["players"])
        self.reach_goal = [False] * len(board_data["players"])

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
        cloned_game = deepcopy(self)
        new_states = []

        for idx, player in enumerate(cloned_game.players):
            if cloned_game.reach_goal[idx]:
                continue

            current_row, current_col = player["position"]

            while True:
                next_row = current_row + _row
                next_col = current_col + _col

                if not cloned_game.is_valid_move(next_row, next_col, idx):
                    break

                current_row, current_col = next_row, next_col

                if (current_row, current_col) == cloned_game.goals[idx]["position"]:
                    cloned_game.reach_goal[idx] = True
                    break

            if (current_row, current_col) != player["position"]:
                cloned_game.players[idx]["position"] = (current_row, current_col)
                new_states.append(deepcopy(cloned_game))

        return new_states

    def solve_with_bfs(self):
        initial_game = deepcopy(self)
        queue = deque([(initial_game, [])])
        visited = set()
        nodes_visited = 0

        while queue:
            current_game, path = queue.popleft()
            nodes_visited += 1

            if all(current_game.reach_goal):
                return path + [current_game], nodes_visited

            state_hash = self.get_state_hash(current_game)
            if state_hash in visited:
                continue
            visited.add(state_hash)

            for move_row, move_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_states = current_game.simulate_move(move_row, move_col)
                for new_state in new_states:
                    queue.append((new_state, path + [current_game]))

        return None, nodes_visited

    def get_state_hash(self, game):
        players_positions = tuple(player["position"] for player in game.players)
        return (players_positions, tuple(game.reach_goal))

