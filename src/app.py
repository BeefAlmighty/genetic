# Application wrapper for viewing evolution

import random
from numpy.random import choice
import config as cfg
from tkinter import ttk, Tk, StringVar, \
    Button, Frame, Label, W, IntVar, Canvas
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import numpy as np
from src.objects.chromosome import Chromosome, Codon
from src.objects.individual import Individual, Population
from src.objects.experiment import VisualSimpleExperiment, number_ones


def draw_data(data, color_array, canvas, window):
    canvas.delete("all")
    canvas_width = 800
    canvas_height = 400
    x_width = canvas_width / (len(data) + 1)
    offset = 4
    spacing = 2
    normalized_data = [i / max(data) for i in data]

    for i, height in enumerate(normalized_data):
        x0 = i * x_width + offset + spacing
        y0 = canvas_height - height * 390
        x1 = (i + 1) * x_width + offset
        y1 = canvas_height
        canvas.create_rectangle(
            x0,
            y0,
            x1,
            y1,
            fill=color_array[i]
        )

    window.update_idletasks()
    return None


def generate(canvas, window):
    global data

    data = []
    for i in range(0, 100):
        random_value = random.randint(1, 150)
        data.append(random_value)

    draw_data(data,
              [cfg.COLORS["BLUE"] for _ in range(len(data))],
              canvas,
              window)
    return None


def set_speed(speed_menu):
    if speed_menu.get() == 'Slow':
        return 0.3
    elif speed_menu.get() == 'Medium':
        return 0.1
    else:
        return 0.001


def evolve(ax, canvas, time_interval, pop_size, gens):
    # Initialize the population

    nums = choice(range(256), pop_size)
    pop = Population()
    fit = lambda x: number_ones(x)
    for item in nums:
        person = Individual([Chromosome([Codon(item)])])
        person.apply(fit)
        pop.add(person)

    VisualSimpleExperiment(
        ax,
        canvas,
        time_interval,
        population=pop,
        generations=gens,
        p_cross=.9,
        p_mutate=.001,
        fitness_func=fit
    ).run()
    return None

# def matrix():
#     import numpy as np
#     import matplotlib.pyplot as plt
#     import tkinter as tk
#     # ~from board import Board
#     from PIL import Image, ImageTk
#     from matplotlib.backends.backend_tkagg import (
#         FigureCanvasTkAgg, NavigationToolbar2Tk)

    # def num():
    #     n1 = int(t1.get())
    #     n2 = int(t2.get())
    #     n3 = int(t3.get()) / 100.00
    #     top.destroy()  # close dialog
    #     initBoard = np.zeros((n1, n2))
    #     for row in range(0, n1):
    #         for column in range(0, n2):
    #             initBoard[row][column] = np.random.choice(
    #                 np.arange(0, 2), p=[1 - n3, n3])
    #     # game_board = Board(n1, n2, initBoard)
    #     ax.imshow(initBoard)  # draw board
    #     canvas.draw_idle()  # update matplotlib figure
    #
    # root = Tk()
    # root.title('Game of Life')
    # root.geometry('800x600')
    # # create matplotlib figure
    # fig = plt.figure()
    # ax = fig.add_subplot(111)  # create axis
    # ax.axis('off')
    # canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    # canvas.get_tk_widget().grid(row=4, column=0)
    #
    # # toplevel to choose parameters
    # top = tk.Toplevel(root)
    # Label(top, text="How many rows?: ").grid(row=0)
    # Label(top, text="How many columns?: ").grid(row=1)
    # Label(top, text="Probability of spawn (between 0 and 100): ").grid(
    #     row=2)
    #
    # t1 = tk.Entry(top)
    # t2 = tk.Entry(top)
    # t3 = tk.Entry(top)
    #
    # t1.grid(row=0, column=1)
    # t2.grid(row=1, column=1)
    # t3.grid(row=2, column=1)
    #
    # Button(top, text='Generate', command=num).grid(row=3, column=1,
    #                                                sticky=tk.W, pady=4)
    #
    # tk.mainloop()


def main():
    # Create basic window
    window = Tk()
    window.title("Simple genetic algorithm")
    window.maxsize(1000, 700)
    window.config(bg=cfg.COLORS["WHITE"])

    fig = plt.figure()
    ax = fig.add_subplot(111)  # create axis
    ax.axis('off')
    canvas = FigureCanvasTkAgg(fig, master=window)

    population_size = IntVar()
    size_list = [2, 10, 25, 100]

    speed_name = StringVar()
    speed_list = ["Fast", "Medium", "Slow"]

    # Create the basic UI frame, i.e. the frame surrounding the widgets
    UI_frame = Frame(
        window,
        width=900,
        height=300,
        bg=cfg.COLORS["LIGHT_GRAY"]
    )
    UI_frame.grid(row=0, column=0, padx=10, pady=5)

    # dropdown to select population size
    l1 = Label(UI_frame,
               text="Population Size: ",
               bg=cfg.COLORS["DARK_GRAY"])
    l1.grid(row=0, column=0, padx=10, pady=5, sticky=W)
    size_menu = ttk.Combobox(UI_frame,
                             textvariable=population_size,
                             values=size_list)
    size_menu.grid(row=0, column=1, padx=5, pady=5)
    size_menu.current(0)
    pop_size = size_menu.get()

    # dropdown to select evolution speed
    l2 = Label(
        UI_frame,
        text="Evolution Speed: ",
        bg=cfg.COLORS["DARK_GRAY"]
        )
    l2.grid(row=1, column=0, padx=10, pady=5, sticky=W)
    speed_menu = ttk.Combobox(
        UI_frame,
        textvariable=speed_name,
        values=speed_list
    )
    speed_menu.grid(row=1, column=1, padx=5, pady=5)
    speed_menu.current(0)
    time_interval = set_speed(speed_menu)

    # canvas to draw our population
    canvas = Canvas(
        window,
        width=800,
        height=400,
        bg=cfg.COLORS["LIGHT_GREEN"]
    )
    canvas.grid(row=1, column=0, padx=10, pady=5)

    # button for generating array
    b3 = Button(
        UI_frame,
        text="Generate Population",
        command=lambda: generate(canvas, window),
        bg=cfg.COLORS["BLACK"]
    )
    b3.grid(row=2, column=0, padx=5, pady=5)

    # run button
    b1 = Button(
        UI_frame,
        text="Evolve",
        command=lambda: evolve(ax, canvas, .3, 10, 10),
        bg=cfg.COLORS["LIGHT_GREEN"]
    )
    b1.grid(row=2, column=1, padx=5, pady=5)

    window.mainloop()

if __name__ == "__main__":
    main()
