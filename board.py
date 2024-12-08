import tkinter as tk
from tkinter import messagebox
import time
from game import Game

class GameGUI:
    def __init__(self, root, rows, cols, board_details):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.cell_size = 50
        self.game = Game(rows, cols, board_details)

        self.canvas = tk.Canvas(root, width=self.cols * self.cell_size, height=self.rows * self.cell_size)
        self.canvas.pack()

        self.status_label = tk.Label(root, text="Choose option from  menu", font=("bold", 14))
        self.status_label.pack()

        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        game_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="Play Manually", command=self.play_manually)
        game_menu.add_command(label="DFS", command=lambda: self.solve_with_algorithm("DFS"))
        game_menu.add_command(label="Recursive DFS", command=lambda: self.solve_with_algorithm("Recursive DFS"))
        game_menu.add_command(label="BFS", command=lambda: self.solve_with_algorithm("BFS"))
        game_menu.add_command(label="UCS", command=lambda: self.solve_with_algorithm("UCS"))
        game_menu.add_command(label="Hill Climbing", command=lambda: self.solve_with_algorithm("Hill Climbing"))
        game_menu.add_command(label="Steepest Hill Climbing",
                              command=lambda: self.solve_with_algorithm("Steepest Hill Climbing"))
        game_menu.add_command(label="A*", command=lambda: self.solve_with_algorithm("A*"))
        game_menu.add_command(label="A* Advanced", command=lambda: self.solve_with_algorithm("A* Advanced"))
        game_menu.add_command(label="Exit", command=root.quit)

        self.draw_board()

    def draw_board(self, state=None):
        self.canvas.delete("all")
        if state is None:
            state = self.game.state
        for row in range(self.rows):
            for col in range(self.cols):
                x1, y1 = col * self.cell_size, row * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                if (row, col) in state.walls:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="black")
                elif any((row, col) == goal["position"] for goal in state.goals):
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="blue" , width=5)
                elif any((row, col) == player["position"] for player in state.players):
                    self.canvas.create_rectangle(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="blue", outline="black")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")


    def play_manually(self):
        self.status_label.config(text="Use WASD")
        self.root.bind("<Key>", self.manual_keypress)

    def manual_keypress(self, event):
        move_map = {
            "w": (-1, 0),
            "s": (1, 0),
            "a": (0, -1),
            "d": (0, 1),
        }
        move = move_map.get(event.keysym.lower())
        if move:
            new_states = self.game.simulate_move(self.game.state, *move)
            if new_states:
                self.game.state = new_states[0]
                self.draw_board()
            if self.game.is_won():
                self.status_label.config(text="You won!")
                messagebox.showinfo(" You won!")
                self.root.unbind("<Key>")


    def solve_with_algorithm(self, algorithm):
        start_time = time.time()
        if algorithm == "DFS":
            solution, nodes_visited, _ = self.game.dfs()
        elif algorithm == "Recursive DFS":
            solution, visited_states = self.game.dfs_recursive(self.game.state, [], set(), [])
            nodes_visited = len(visited_states)
        elif algorithm == "BFS":
            solution, nodes_visited, _ = self.game.bfs()
        elif algorithm == "UCS":
            solution, nodes_visited, _ = self.game.ucs()
        elif algorithm == "Hill Climbing":
            solution, nodes_visited, _ = self.game.hill_climbing()
        elif algorithm == "Steepest Hill Climbing":
            solution, nodes_visited, _ = self.game.steepest_hill_climbing()
        elif algorithm == "A*":
            solution, nodes_visited, _ = self.game.a_star()
        elif algorithm == "A* Advanced":
            solution, nodes_visited, _ = self.game.a_star_advanced()
        else:
            messagebox.showerror("Error", "Invalid algorithm")
            return
        end_time = time.time()
        #
        if solution:
            self.animate_solution(solution)
            self.status_label.config(
                text=f"Solution found! Nodes visited: {nodes_visited}, Time: {end_time - start_time:.2f}s")
        else:
            self.status_label.config(text="No solution found.")


    def animate_solution(self, solution):
        for state in solution:
            self.draw_board(state)
            self.root.update()
            time.sleep(0.5)

