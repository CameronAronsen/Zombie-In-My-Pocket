import shelve
import cmd
import sys
import tkinter as tk

class FinishScreen():

    def __init__(self, win, game):
        self.game = game
        self.window = tk.Tk()
        self.window.geometry("400x400")
        if win:
            self.won_game()
        else:
            self.lost_game()

    def won_game(self):
        self.create_title("You Won The Game!", self.window)
        self.create_frame()
        self.create_label(self.game.get_time(), self.frame)

    def lost_game(self):
        self.create_title("You Lost The Game!", self.window)
        self.create_frame()
        self.create_label("Stats", self.frame)
        self.create_label(f"The time is: {self.game.get_time()}pm",
                          self.frame)
        self.create_label(f"Holding Totem: {self.game.player.get_totem()}",
                          self.frame)

        self.create_label(f"You lost with: {self.game.player.get_health()} health",
                          self.frame)

        self.create_label(f"You had: {self.game.player.get_attack()} health",
                          self.frame)

        self.create_label(f"Your items were: {self.game.player.get_items()}",
                          self.frame)

        self.create_label(f"You moved {self.game.get_player_moves()} times",
                          self.frame)

        self.create_label(f"You placed {self.game.get_tiles_placed()} tiles",
                          self.frame)

        self.create_label(f"You used {self.game.get_dev_cards_used()} development cards",
                          self.frame)

        self.create_label(f"You attacked {self.game.get_attacks_completed()} times",
                          self.frame)

    def start(self):
        self.window.mainloop()

    def create_frame(self):
        self.frame = tk.Frame(self.window)
        self.frame.pack()

    def create_label(self, text, frame):
        self.label = tk.Label(frame, text=text)
        self.label.pack()

    def create_title(self, text, frame):
        self.label = tk.Label(frame, text=text, font='bold')
        self.label.pack()
