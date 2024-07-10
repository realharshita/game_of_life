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

speed_slider = tk.Scale(button_frame, from_=10, to=1000, orient="horizontal", label="Speed (ms)", command=set_simulation_speed)
speed_slider.set(speed)
speed_slider.grid(row=0, column=6)

status_label = tk.Label(button_frame, text="Stopped")
status_label.grid(row=0, column=7)

root.mainloop()
