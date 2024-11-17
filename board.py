import tkinter as tk
from copy import deepcopy
from game import Game


class GameUI:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.boards = [
            {
                "walls": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
                          (1, 0), (1, 3), (1, 7), (2, 0), (2, 7), (3, 0), (3, 7), (4, 0), (4, 1), (4, 2),
                          (4, 3), (4, 5), (4, 6), (4, 7), (5, 3), (5, 4), (5, 5)],
                "players": [
                    {"position": (2, 1), "color": "blue"}
                ],
                "goals": [
                    {"position": (4, 4), "color": "blue"}
                ]
            },
        ]

        self.current_board = 0
        self.game = Game(rows, cols, deepcopy(self.boards[self.current_board]))

        self.window = tk.Tk()
        self.window.title("Bfs")
        self.canvas = tk.Canvas(self.window, width=cols * 50, height=rows * 50)
        self.canvas.pack()

        self.auto_play_button = tk.Button(self.window, text="Play bfs", command=self.auto_play)
        self.auto_play_button.pack()

        self.update_board()

    def auto_play(self):
        solution_path, nodes_visited = self.game.solve_with_bfs()
        if not solution_path:
            print("Wrong")
            return

        for state in solution_path:
            self.game = state
            self.update_board()
            self.window.update_idletasks()
            self.window.after(500)

            self.print_board(state)

        print(f"Total node: {nodes_visited}")

    def print_board(self, state):
        for row in range(self.game.rows):
            row_str = ""
            for col in range(self.game.cols):
                if (row, col) in state.walls:
                    row_str += "W "
                elif any(goal["position"] == (row, col) for goal in state.goals):
                    row_str += "G "
                elif any(player["position"] == (row, col) for player in state.players):
                    row_str += "P "
                else:
                    row_str += ". "
            print(row_str)
        print()

    def update_board(self):
        self.canvas.delete("all")
        for (row, col) in self.game.walls:
            self.canvas.create_rectangle(
                col * 50, row * 50, (col + 1) * 50, (row + 1) * 50,
                fill="gray",
                outline="gray"
            )
        for goal in self.game.goals:
            row, col = goal["position"]
            self.canvas.create_rectangle(
                col * 50 + 5, row * 50 + 5, (col + 1) * 50 - 5, (row + 1) * 50 - 5,
                fill="", outline=goal["color"], width=8
            )
        for player in self.game.players:
            row, col = player["position"]
            self.canvas.create_rectangle(
                col * 50 + 10, row * 50 + 10, (col + 1) * 50 - 10, (row + 1) * 50 - 10,
                fill=player["color"]
            )

    def run(self):
        self.window.mainloop()