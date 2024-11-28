import tkinter as tk
from game import Game
from copy import deepcopy

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
                    {"position": (2, 1), "color": "green"}
                ],
                "goals": [
                    {"position": (4, 4), "color": "green"}
                ]
            },


            {
                "walls": [
                    (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10),
                    (2, 2), (2, 3), (2, 10), (2, 11),
                    (3, 1), (3, 2), (3, 5), (3, 8), (3, 11), (3, 12),
                    (4, 1), (4, 4), (4, 9), (4, 12),
                    (5, 1), (5, 6), (5, 9), (5, 10), (5, 12),
                    (6, 1), (6, 3), (6, 5), (6, 6), (6, 10), (6, 12),
                    (7, 1), (7, 5), (7, 12),
                    (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), (8, 11), (8, 12)
                ],
                "players": [
                    {"position": (6, 11), "color": "green"},
                   {"position": (6, 2), "color": "red"}
                ],
                "goals": [
                    {"position": (3, 7), "color": "green"},
                    {"position": (4, 6), "color": "red"}
                ]
            },
            {
                "walls": [
                    (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
                    (1, 0), (1, 3), (1, 7),
                    (2, 0), (2, 7),
                    (3, 0), (3, 7),
                    (4, 0), (4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7),
                    (5, 3), (5, 4), (5, 5)
                ],
                "players": [
                    {"position": (2, 1), "color": "green"}
                ],
                "goals": [
                    {"position": (4, 4), "color": "green"}
                ]
            },                   
            {   
            "walls":[
                    (1,2),(1,3),(1,4),
                    (2,1),(2,2),(2,4),(2,5),(2,6),(2,7),(2,8),
                    (3,1),(3,8),
                    (4,1),(4,3),(4,5),(4,6),(4,7),(4,8),
                    (5,1),(5,2),(5,3),(5,4),(5,5),
            ],
            "players":[
                    {"position": (3,2), "color": "red"},
                    {"position": (3, 4), "color": "green"},
                    {"position": (3, 3), "color": "blue"}
            ],
            "goals":[
                {"position":(2,3),"color":"red"},
                {"position":(4,2),"color":"green"},
                {"position":(4,4),"color":"blue"}
        ],
            },
    
            {
                "walls":[
                    (1,9),(1,10),(1,11),(1,12),
                    (2,1),(2,2),(2,3),(2,4),(2,5),(2,8),(2,9),(2,12),
                    (3,1),(3,5),(3,6),(3,7),(3,8),(3,12),
                    (4,1),(4,12),
                    (5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),(5,8),(5,9),(5,10),(5,11),(5,12), 
                ],
                "players":[
                    {"position": (4, 5), "color": "blue"},
                    {"position": (4, 6), "color": "red"},
                    {"position": (4, 7), "color": "yellow"},
                    {"position": (4, 8), "color": "green"}
                    
                    ],
                "goals":[
                    {"position":(3,2),"color":"green"},
                    {"position":(3,3),"color":"blue"},
                    {"position":(3,4),"color":"yellow"},
                    {"position":(2,11),"color":"red"}
                ] 
                
            }
        ]

        self.current_board = 0
        self.game = Game(rows, cols, deepcopy(self.boards[self.current_board]))

        self.window = tk.Tk()
        self.window.title("DFS R")
        self.canvas = tk.Canvas(self.window, width=cols * 50, height=rows * 40)
        self.canvas.pack()

        self.switch_board_button = tk.Button(self.window, text="Switch Board", command=self.switch_board)
        self.switch_board_button.pack()

        self.auto_play_button = tk.Button(self.window, text="Play DFS R", command=self.auto_play)
        self.auto_play_button.pack()

        self.update_board()

    def switch_board(self):
        self.current_board = (self.current_board + 1) % len(self.boards)
        self.game = Game(self.rows, self.cols, deepcopy(self.boards[self.current_board]))
        self.update_board()

    def auto_play(self):
        solution_path, nodes_visited = self.game.dfs_r()
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
                fill="", outline=goal["color"], width=5
            )
        for player in self.game.players:
            row, col = player["position"]
            self.canvas.create_rectangle(
                col * 50 + 10, row * 50 + 10, (col + 1) * 50 - 10, (row + 1) * 50 - 10,
                fill=player["color"]
            )

    def next_state():
        print

    def run(self):
        self.window.mainloop()
