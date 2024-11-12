
import tkinter as tk
from tkinter import messagebox
from game import Game
from copy import deepcopy

class BoardGUI:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.boards = [   {
                "walls": [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),
                          (2, 1), (2, 7), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7)],
                "players": [{"position": (2, 2), "color": "blue"}],
                "goals": [{"position": (2, 6), "color": "blue"}]
            },
            {
                "walls": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
                          (1, 0), (1, 3), (1, 7), (2, 0), (2, 7), (3, 0), (3, 7), (4, 0), (4, 1), (4, 2),
                          (4, 3), (4, 5), (4, 6), (4, 7), (5, 3), (5, 4), (5, 5)],
                "players": [{"position": (2, 1), "color": "green"}],
                "goals": [{"position": (4, 4), "color": "green"}]
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
     "players": [{"position": (6, 11), "color": "red"}, {"position": (6, 2), "color": "blue"}],
     "goals": [{"position": (3, 7), "color": "red"}, {"position": (4, 6), "color": "blue"}]
 },   {
     "walls":[
             (1,2),(1,3),(1,4),
             (2,1),(2,2),(2,4),(2,5),(2,6),(2,7),(2,8),
             (3,1),(3,8),
             (4,1),(4,3),(4,5),(4,6),(4,7),(4,8),
             (5,1),(5,2),(5,3),(5,4),(5,5),
             ],
     "players":[{"position":(3,2),"color":"yellow"},
             {"position":(3,4),"color":"blue"},
             {"position":(3,3),"color":"red"},],
     "goals":[{"position":(2,3),"color":"yellow"},
             {"position":(4,2),"color":"blue"},
             {"position":(4,4),"color":"red"},]
     },   {
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
      "players": [{"position": (6, 11), "color": "red"}, {"position": (6, 2), "color": "blue"}],
      "goals": [{"position": (3, 7), "color": "red"}, {"position": (4, 6), "color": "blue"}]
  },   {
      "walls":[
              (1,2),(1,3),(1,4),
              (2,1),(2,2),(2,4),(2,5),(2,6),(2,7),(2,8),
              (3,1),(3,8),
              (4,1),(4,3),(4,5),(4,6),(4,7),(4,8),
              (5,1),(5,2),(5,3),(5,4),(5,5),
              ],
      "players":[{"position":(3,2),"color":"yellow"},
              {"position":(3,4),"color":"blue"},
              {"position":(3,3),"color":"red"},],
      "goals":[{"position":(2,3),"color":"yellow"},
              {"position":(4,2),"color":"blue"},
              {"position":(4,4),"color":"red"},]
      }, 
  {
      "walls": [(1, 9), (1, 10), (1, 11), (1, 12),
              (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 8), (2, 9), (2, 12),
              (3, 1), (3, 5), (3, 6), (3, 7), (3, 8), (3, 12),
              (4, 1), (4, 12),
              (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5, 12)],
      "players": [{"position": (4, 5), "color": "blue"},
                  {"position": (4, 6), "color": "red"},
                  {"position": (4, 7), "color": "yellow"},
                  {"position": (4, 8), "color": "green"}],
      "goals": [{"position": (3, 2), "color": "green"},
              {"position": (3, 3), "color": "blue"},
              {"position": (3, 4), "color": "yellow"},
              {"position": (2, 11), "color": "red"}]
  },
  {
      "walls":[(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),
              (2,1),(2,7),
              (3,1),(3,5),(3,7),
              (4,1),(4,3),(4,5),(4,7),
              (5,1),(5,5),(5,7),
              (6,1),(6,4),(6,5),(6,7),
              (7,1),(7,7),
              (8,1),(8,6),(8,7),
              (9,1),(9,2),(9,3),(9,4),(9,7),
              (10,2),(10,7),
              (11,2),(11,3),(11,4),(11,5),(11,6),(11,7),
              ],
          "players":[{"position":(4,2),"color":"red"},
                      {"position":(3,4),"color":"blue"},],
          "goals":[{"position":(5,4),"color":"red"},
                  {"position":(2,6),"color":"blue"},],
  },
  {
          "walls":[(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),(1, 8), (1, 9), (1, 10), (1, 11),
                      (2,1),(2,11),
                      (3,1),(3,11),
                      (4,1),(4,2),(4,11),
                      (5,2),(5,7),(5,8),(5,9),(5,10),(5,11),
                      (6,2),(6,7),
                      (7,2),(7,3),(7,4),(7,5),(7,6),(7,7),
                      ],
          "players":[{"position":(2,2),"color":"yellow"},
                  {"position":(2,3),"color":"red"},
                  {"position":(2,4),"color":"blue"},
                  {"position":(2,5),"color":"green"},
                  ],
          "goals":[{"position":(3,7),"color":"yellow"},
                  {"position":(4,6),"color":"green"},
                  {"position":(5,5),"color":"blue"},
                  {"position":(6,4),"color":"red"},], 
  }     
               ] 

        self.root = tk.Tk()
        self.root.title("Zero Squares Game")
        self.canvas = tk.Canvas(self.root, width=700, height=700)
        self.canvas.pack()

        self.current_board = 0
        self.game_logic = Game(rows, cols, deepcopy(self.boards[self.current_board]))

        self.create_boardselect()
        self.canvas.bind("<KeyPress>", self.key_pressed)
        self.canvas.focus_set()
        self.draw_board()

    def create_boardselect(self):
        options = [f"Board {i + 1}" for i in range(len(self.boards))]
        self.selected_board = tk.StringVar(self.root)
        self.selected_board.set(options[0])
        board_selector = tk.OptionMenu(self.root, self.selected_board, *options, command=self.switchBoard)
        board_selector.pack()

    def switchBoard(self, selection):
        self.current_board = int(selection.split()[-1]) - 1
        self.game_logic = Game(self.rows, self.cols, deepcopy(self.boards[self.current_board]))
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        cellSize = 50
        for row in range(self.rows):
            for col in range(self.cols):
                x1, y1 = col * cellSize, row * cellSize
                x2, y2 = x1 + cellSize, y1 + cellSize
                if (row, col) in self.game_logic.state.walls:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")
                for goal in self.game_logic.state.goals:
                    if (row, col) == goal["position"]:
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill="", outline=goal["color"], width=8)
                for player in self.game_logic.state.players:
                    if (row, col) == player["position"]:
                        player_x1, player_y1 = x1 + cellSize * 0.1, y1 + cellSize * 0.1
                        player_x2, player_y2 = x2 - cellSize * 0.1, y2 - cellSize * 0.1
                        self.canvas.create_rectangle(player_x1, player_y1, player_x2, player_y2, fill=player["color"], outline="black")

    def key_pressed(self, event):
        if event.keysym == 'Left':
            next_state = self.game_logic.next_state(0, -1)
        elif event.keysym == 'Right':
            next_state = self.game_logic.next_state(0, 1)
        elif event.keysym == 'Up':
            next_state = self.game_logic.next_state(-1, 0)
        elif event.keysym == 'Down':
            next_state = self.game_logic.next_state(1, 0)
        self.game_logic.state = next_state
        if self.game_logic.check_win():
            messagebox.showinfo("Done!")
        self.draw_board()

    def run(self):
        self.root.mainloop()
