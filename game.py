from copy import deepcopy
from collections import deque
from heapq import heappush, heappop


class GameState:
    def __init__(self, walls, goals, players, reached_goal):
        self.walls = walls
        self.goals = goals
        self.players = players
        self.reached_goal = reached_goal

    def copy(self):
        return deepcopy(self)

    def __lt__(self, other):
        return self.reached_goal.count(True) < other.reached_goal.count(True)
class Game:
    def __init__(self, rows, cols, board_details):
        self.rows = rows
        self.cols = cols
        self.state = GameState(
            walls=deepcopy(board_details["walls"]),
            goals=deepcopy(board_details["goals"]),
            players=deepcopy(board_details["players"]),
            reached_goal=[False] * len(board_details["players"])
        )

    def is_won(self):
        return all(self.state.reached_goal)

    def is_valid_move(self, row, col, player_i):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False
        if (row, col) in self.state.walls:
            return False
        for j, other_player in enumerate(self.state.players):
            if j != player_i and other_player["position"] == (row, col):
                return False
        if self.state.reached_goal[player_i] and (row, col) != self.state.goals[player_i]["position"]:
            return False
        return True


    def simulate_move(self, current_state, r_row, c_col):
        cloned_state = deepcopy(current_state)
        new_states = []
        for i, player in enumerate(cloned_state.players):
            if cloned_state.reached_goal[i]:
                continue
            current_row, current_col = player["position"]
            while True:
                next_row = current_row + r_row
                next_col = current_col + c_col
                if not self.is_valid_move(next_row, next_col, i):
                    break
                current_row, current_col = next_row, next_col
                if (current_row, current_col) == cloned_state.goals[i]["position"]:
                    cloned_state.reached_goal[i] = True
                    break
            if (current_row, current_col) != player["position"]:
                cloned_state.players[i]["position"] = (current_row, current_col)
                new_states.append(deepcopy(cloned_state))
        return new_states


    def get_state(self, state):
        players_positions = tuple(player["position"] for player in state.players)
        return (players_positions, tuple(state.reached_goal))

    def dfs(self):
        initial_state = self.state.copy()
        stack = [(initial_state, [])]
        visited = set()
        visited_states = []
        nodes_visited = 0
        while stack:
            current_state, path = stack.pop()
            nodes_visited += 1
            visited_states.append(deepcopy(current_state))
            if all(current_state.reached_goal):
                return path + [current_state], nodes_visited, visited_states
            state_hash = self.get_state(current_state)
            if state_hash in visited:
                continue
            visited.add(state_hash)
            for move_row, move_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_states = self.simulate_move(current_state, move_row, move_col)
                for new_state in new_states:
                    stack.append((new_state, path + [current_state]))
        return None, nodes_visited, visited_states

    def dfs_recursive(self, current_state, path, visited, visited_states):
        visited_states.append(deepcopy(current_state))
        if all(current_state.reached_goal):
            return path + [current_state], visited_states
        state_hash = self.get_state(current_state)
        if state_hash in visited:
            return None, visited_states
        visited.add(state_hash)
        for move_row, move_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_states = self.simulate_move(current_state, move_row, move_col)
            for new_state in new_states:
                solution, visited_states = self.dfs_recursive(new_state, path + [current_state], visited,
                                                              visited_states)
                if solution:
                    return solution, visited_states
        return None, visited_states

    def bfs(self):
        initial_state = self.state.copy()
        queue = deque([(initial_state, [])])
        visited = set()
        visited_states = []
        nodes_visited = 0
        while queue:
            current_state, path = queue.popleft()
            nodes_visited += 1
            visited_states.append(deepcopy(current_state))
            if all(current_state.reached_goal):
                return path + [current_state], nodes_visited, visited_states
            state_hash = self.get_state(current_state)
            if state_hash in visited:
                continue
            visited.add(state_hash)
            for move_row, move_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_states = self.simulate_move(current_state, move_row, move_col)
                for new_state in new_states:
                    queue.append((new_state, path + [current_state]))
        return None, nodes_visited, visited_states

    def ucs(self):
        initial_state = self.state.copy()
        priority_queue = [(0, initial_state, [])]
        visited = set()
        visited_states = []
        nodes_visited = 0
        while priority_queue:
            cost, current_state, path = heappop(priority_queue)
            nodes_visited += 1
            visited_states.append(deepcopy(current_state))
            if all(current_state.reached_goal):
                return path + [current_state], nodes_visited, visited_states
            state_hash = self.get_state(current_state)
            if state_hash in visited:
                continue
            visited.add(state_hash)
            for move_row, move_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_states = self.simulate_move(current_state, move_row, move_col)
                for new_state in new_states:
                    new_state_hash = self.get_state(new_state)
                    if new_state_hash not in visited:
                        heappush(priority_queue, (cost + 1, new_state, path + [current_state]))
        return None, nodes_visited, visited_states

    def hill_climbing(self):
        initial_state = self.state.copy()
        current_state = initial_state
        visited_states = []
        nodes_visited = 0
        while True:
            nodes_visited += 1
            visited_states.append(deepcopy(current_state))
            if all(current_state.reached_goal):
                return [current_state], nodes_visited, visited_states
            neighbors = []
            for move_row, move_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_states = self.simulate_move(current_state, move_row, move_col)
                neighbors.extend(new_states)
            if not neighbors:
                break
            best_neighbor = max(neighbors, key=lambda state: state.reached_goal.count(True))
            if best_neighbor.reached_goal.count(True) <= current_state.reached_goal.count(True):
                break
            current_state = best_neighbor
        return None, nodes_visited, visited_states

    def steepest_hill_climbing(self):
        initial_state = self.state.copy()
        current_state = initial_state
        visited_states = []
        nodes_visited = 0
        while True:
            nodes_visited += 1
            visited_states.append(deepcopy(current_state))
            if all(current_state.reached_goal):
                return [current_state], nodes_visited, visited_states
            neighbors = []
            for move_row, move_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_states = self.simulate_move(current_state, move_row, move_col)
                neighbors.extend(new_states)
            if not neighbors:
                break
            best_neighbor = max(neighbors, key=lambda state: state.reached_goal.count(True))
            if best_neighbor.reached_goal.count(True) <= current_state.reached_goal.count(True):
                break
            current_state = best_neighbor
        return None, nodes_visited, visited_states

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def a_star(self):
        initial_state = self.state.copy()
        priority_queue = [(0, 0, initial_state, [])]
        visited = set()
        visited_states = []
        nodes_visited = 0
        while priority_queue:
            total_cost, g_cost, current_state, path = heappop(priority_queue)
            nodes_visited += 1
            visited_states.append(deepcopy(current_state))
            if all(current_state.reached_goal):
                return path + [current_state], nodes_visited, visited_states
            state_hash = self.get_state(current_state)
            if state_hash in visited:
                continue
            visited.add(state_hash)
            for move_row, move_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_states = self.simulate_move(current_state, move_row, move_col)
                for new_state in new_states:
                    if self.get_state(new_state) not in visited:
                        h_cost = sum(
                            self.manhattan_distance(player["position"], goal["position"])
                            for player, goal in zip(new_state.players, new_state.goals)
                            if not new_state.reached_goal[new_state.players.index(player)]
                        )
                        heappush(priority_queue, (g_cost + 1 + h_cost, g_cost + 1, new_state, path + [current_state]))
        return None, nodes_visited, visited_states

    def advanced_heuristic(self, state):
        total_cost = 0
        for i, player in enumerate(state.players):
            if not state.reached_goal[i]:
                player_pos = player["position"]
                goal_pos = state.goals[i]["position"]
                dist = self.manhattan_distance(player_pos, goal_pos)
                obstacle_penalty = 0
                for other_player in state.players:
                    if other_player["position"] != player_pos:
                        other_pos = other_player["position"]
                        if abs(other_pos[0] - player_pos[0]) <= 1 and abs(other_pos[1] - player_pos[1]) <= 1:
                            obstacle_penalty += 2
                wall_penalty = sum(
                    1 for (r, c) in state.walls
                    if abs(r - player_pos[0]) <= 1 and abs(c - player_pos[1]) <= 1
                )
                total_cost += dist + obstacle_penalty + wall_penalty
        return total_cost

    def a_star_advanced(self):
        initial_state = self.state.copy()
        priority_queue = [(0, 0, initial_state, [])]
        visited = set()
        visited_states = []
        nodes_visited = 0
        while priority_queue:
            total_cost, g_cost, current_state, path = heappop(priority_queue)
            nodes_visited += 1
            visited_states.append(deepcopy(current_state))
            if all(current_state.reached_goal):
                return path + [current_state], nodes_visited, visited_states
            state_hash = self.get_state(current_state)
            if state_hash in visited:
                continue
            visited.add(state_hash)
            for move_row, move_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_states = self.simulate_move(current_state, move_row, move_col)
                for new_state in new_states:
                    if self.get_state(new_state) not in visited:
                        h_cost = self.advanced_heuristic(new_state)
                        heappush(priority_queue, (g_cost + 1 + h_cost, g_cost + 1, new_state, path + [current_state]))
        return None, nodes_visited, visited_states

