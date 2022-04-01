import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class FinishScreen():

    def __init__(self, win, game_stats):
        self.game = game_stats
        with open(self.game) as stats:
            self.lines = stats.readlines()
            stats.close()
        self.lines = [line.strip() for line in self.lines]
        self.window = tk.Tk()
        self.window.geometry("1000x800")
        if win:
            self.won_game()
        else:
            self.lost_game()

        self.list_stats()

    def won_game(self):
        self.create_title("You Won The Game!", self.window)

    def lost_game(self):
        self.create_title("You Lost The Game!", self.window)

    def list_stats(self):
        self.create_frame()
        self.create_label("", self.frame)
        self.create_sub_title("Stats", self.frame)
        self.create_label("", self.frame)
        self.create_label(f"The time is: {self.lines[0]}pm",
                          self.frame)
        self.create_label(f"Holding Totem: {self.lines[1]}",
                          self.frame)

        self.create_label(f"You had: {self.lines[2]} health",
                          self.frame)

        self.create_label(f"You had: {self.lines[3]} attack",
                          self.frame)

        self.create_label(f"Your items were: {self.lines[4]}",
                          self.frame)

        self.create_label(f"You moved {self.lines[5]} times",
                          self.frame)

        self.create_label(f"You placed {self.lines[6]} tiles",
                          self.frame)

        self.create_label(f"You used {self.lines[7]} development cards",
                          self.frame)

        self.create_label(f"You attacked {self.lines[8]} times",
                          self.frame)

        self.create_label("", self.frame)

        self.create_graph()

    def start(self):
        self.window.mainloop()

    def create_frame(self):
        self.frame = tk.Frame(self.window)
        self.frame.pack()

    def create_label(self, text, frame):
        self.label = tk.Label(frame, text=text)
        self.label.pack()

    def create_title(self, text, frame):
        self.label = tk.Label(frame, text=text, font=(None, 24, 'bold'))
        self.label.pack()

    def create_sub_title(self, text, frame):
        self.label = tk.Label(frame, text=text, font=(None, 18, 'bold'))
        self.label.pack()

    def create_graph(self):
        self.stats = self.lines
        self.titles = ["Health", "Attack", "Moves",
                       "Tiles Placed", "Development Cards", "Attacks"]
        self.data = [self.stats[2], self.stats[3], self.stats[5],
                     self.stats[6], self.stats[7], self.stats[8]]
        self.data = [float(point) for point in self.data]
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.fig.add_axes([0.1, 0.1, 0.8, 0.8])
        self.ax.bar(self.titles, self.data)
        self.ax.set_title("Player Stats")
        self.ax.set_xlabel("Stats")
        self.ax.set_ylabel("Value")

        self.canvas = FigureCanvasTkAgg(self.fig, self.window)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
