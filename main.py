import tkinter as tk
from tkinter import filedialog
import json
import random

GRID_WIDTH = 50
GRID_HEIGHT = 30
CELL_SIZE = 15

root = tk.Tk()
root.title("Conway's Game of Life")

canvas = tk.Canvas(root, width=GRID_WIDTH * CELL_SIZE, height=GRID_HEIGHT * CELL_SIZE, borderwidth=0, highlightthickness=0)
canvas.pack()

board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
next_board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

running = False
speed = 100

def render_grid():
    canvas.delete("all")
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            cell_color = "black" if board[y][x] else "white"
            canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE,
                                    (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                                    fill=cell_color, outline="gray")

def count_live_neighbors(y, x):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if 0 <= y + i < GRID_HEIGHT and 0 <= x + j < GRID_WIDTH:
                count += board[y + i][x + j]
    return count

def update_simulation():
    global running
    if running:
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                neighbors = count_live_neighbors(y, x)
                if board[y][x] == 1:
                    if neighbors < 2 or neighbors > 3:
                        next_board[y][x] = 0
                    else:
                        next_board[y][x] = 1
                else:
                    if neighbors == 3:
                        next_board[y][x] = 1
                    else:
                        next_board[y][x] = 0

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                board[y][x] = next_board[y][x]

        render_grid()
        root.after(speed, update_simulation)

def toggle_cell_state(event):
    x = event.x // CELL_SIZE
    y = event.y // CELL_SIZE
    board[y][x] = 1 - board[y][x]
    render_grid()

def start_game():
    global running
    running = True
    status_label.config(text="Running")
    update_simulation()

def stop_game():
    global running
    running = False
    status_label.config(text="Stopped")

def clear_board():
    global board, next_board
    board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    next_board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    render_grid()

def set_simulation_speed(val):
    global speed
    speed = int(val)

def save_board():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'w') as file:
            json.dump(board, file)

def load_board():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'r') as file:
            loaded_board = json.load(file)
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    board[y][x] = loaded_board[y][x]
            render_grid()

def randomize_board():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            board[y][x] = random.choice([0, 1])
    render_grid()

def load_pattern(pattern):
    clear_board()
    for (x, y) in pattern:
        board[y][x] = 1
    render_grid()

def load_glider():
    glider = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]
    load_pattern(glider)

def load_small_exploder():
    small_exploder = [(1, 0), (0, 1), (1, 1), (2, 1), (0, 2), (2, 2), (1, 3)]
    load_pattern(small_exploder)

def load_ten_cell_row():
    ten_cell_row = [(x, 1) for x in range(10)]
    load_pattern(ten_cell_row)

def load_lw_spaceship():
    lw_spaceship = [(1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (4, 1), (4, 2), (0, 3), (3, 3)]
    load_pattern(lw_spaceship)

def load_tumbler():
    tumbler = [(3, 0), (4, 0), (5, 0), (6, 0), (2, 1), (3, 1), (5, 1), (6, 1), (2, 2), (3, 2), (5, 2), (6, 2), 
               (0, 3), (2, 3), (6, 3), (8, 3), (0, 4), (1, 4), (7, 4), (8, 4), (0, 5), (8, 5), (1, 6), (7, 6), 
               (2, 6), (6, 6), (3, 6), (4, 6), (5, 6)]
    load_pattern(tumbler)

def load_gosper_glider_gun():
    gosper_glider_gun = [(24, 2), (22, 3), (24, 3), (12, 4), (13, 4), (20, 4), (21, 4), (34, 4), (35, 4), 
                         (11, 5), (15, 5), (20, 5), (21, 5), (34, 5), (35, 5), (0, 6), (1, 6), (10, 6), (16, 6), 
                         (20, 6), (21, 6), (0, 7), (1, 7), (10, 7), (14, 7), (16, 7), (17, 7), (22, 7), (24, 7), 
                         (10, 8), (16, 8), (24, 8), (11, 9), (15, 9), (12, 10), (13, 10)]
    load_pattern(gosper_glider_gun)

canvas.bind("<Button-1>", toggle_cell_state)

render_grid()

button_frame = tk.Frame(root)
button_frame.pack()

start_button = tk.Button(button_frame, text="Start", command=start_game)
start_button.grid(row=0, column=0)

stop_button = tk.Button(button_frame, text="Stop", command=stop_game)
stop_button.grid(row=0, column=1)

clear_button = tk.Button(button_frame, text="Clear", command=clear_board)
clear_button.grid(row=0, column=2)

save_button = tk.Button(button_frame, text="Save", command=save_board)
save_button.grid(row=0, column=3)

load_button = tk.Button(button_frame, text="Load", command=load_board)
load_button.grid(row=0, column=4)

random_button = tk.Button(button_frame, text="Randomize", command=randomize_board)
random_button.grid(row=0, column=5)

glider_button = tk.Button(button_frame, text="Glider", command=load_glider)
glider_button.grid(row=0, column=6)

small_exploder_button = tk.Button(button_frame, text="Small Exploder", command=load_small_exploder)
small_exploder_button.grid(row=0, column=7)

ten_cell_row_button = tk.Button(button_frame, text="10 Cell Row", command=load_ten_cell_row)
ten_cell_row_button.grid(row=0, column=8)

lw_spaceship_button = tk.Button(button_frame, text="Lightweight Spaceship", command=load_lw_spaceship)
lw_spaceship_button.grid(row=0, column=9)

tumbler_button = tk.Button(button_frame, text="Tumbler", command=load_tumbler)
tumbler_button.grid(row=0, column=10)

gosper_glider_gun_button = tk.Button(button_frame, text="Gosper Glider Gun", command=load_gosper_glider_gun)
gosper_glider_gun_button.grid(row=0, column=11)

speed_slider = tk.Scale(button_frame, from_=10, to=1000, orient="horizontal", label="Speed (ms)", command=set_simulation_speed)
speed_slider.set(speed)
speed_slider.grid(row=1, column=0, columnspan=6)

status_label = tk.Label(root, text="Stopped", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_label.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()
