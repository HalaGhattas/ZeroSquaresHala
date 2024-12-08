from tkinter import Tk
from board import GameGUI


root = Tk()
rows, cols = 14, 14
board_details = {
    "walls": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
                (1, 0), (1, 3), (1, 7), (2, 0), (2, 7), (3, 0), (3, 7), (4, 0), (4, 1), (4, 2),
                (4, 3), (4, 5), (4, 6), (4, 7), (5, 3), (5, 4), (5, 5)],
    "players": [
        {"position": (2, 1), "color": "blue"}
    ],
    "goals": [
        {"position": (4, 4), "color": "blue"}
    ]
    }
gui = GameGUI(root, rows, cols, board_details)
root.mainloop()
