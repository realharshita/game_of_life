import tkinter as tk
from tkinter import filedialog, messagebox
import json
import random

GRID_WIDTH = 50
GRID_HEIGHT = 30
CELL_SIZE = 15

root = tk.Tk()
root.title("Conway's Game of Life")

root.configure(bg="black")

canvas = tk.Canvas(root, width=GRID_WIDTH * CELL_SIZE, height=GRID_HEIGHT * CELL_SIZE, borderwidth=0, highlightthickness=0, bg="black")
canvas.pack(pady=20)

board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
next_board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

running = False
drawing_mode = False
speed = 100

def render_grid():
    canvas.delete("all")
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            cell_color = "red" if board[y][x] else "black"
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

def add_cell(event):
    x = event.x // CELL_SIZE
    y = event.y // CELL_SIZE
    board[y][x] = 1
    render_grid()

def remove_cell(event):
    x = event.x // CELL_SIZE
    y = event.y // CELL_SIZE
    board[y][x] = 0
    render_grid()

def draw_cell(event):
    if drawing_mode and event.num == 1:  # Left click
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        board[y][x] = 1
        render_grid()

def erase_cell(event):
    if drawing_mode and event.num == 3:  # Right click
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        board[y][x] = 0
        render_grid()

def start_game():
    global running
    running = True
    status_label.config(text="Running", fg="red")
    update_simulation()

def stop_game():
    global running
    running = False
    status_label.config(text="Stopped", fg="red")

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

def toggle_drawing_mode():
    global drawing_mode
    drawing_mode = not drawing_mode
    if drawing_mode:
        draw_button.config(text="Drawing Mode: ON", bg="red", fg="black")
    else:
        draw_button.config(text="Drawing Mode: OFF", bg="black", fg="red")

def show_help():
    help_text = (
        "Conway's Game of Life Instructions:\n\n"
        "- Left click on cells to add them.\n"
        "- Right click on cells to remove them.\n"
        "- Drag with the left mouse button to draw cells in drawing mode.\n"
        "- Use the right mouse button to erase cells in drawing mode.\n"
        "- Use the Start button to start the simulation.\n"
        "- Use the Stop button to stop the simulation.\n"
        "- Use the Clear button to clear the grid.\n"
        "- Use the Save button to save the current grid to a file.\n"
        "- Use the Load button to load a grid from a file.\n"
        "- Use the Randomize button to randomize the grid.\n"
        "- Use the pattern buttons to load predefined patterns.\n"
        "- Adjust the simulation speed with the speed slider.\n"
        "- Toggle drawing mode with the Drawing Mode button."
    )
    messagebox.showinfo("Help", help_text)

canvas.bind("<Button-1>", add_cell)
canvas.bind("<B1-Motion>", draw_cell)
canvas.bind("<Button-3>", remove_cell)
canvas.bind("<B3-Motion>", erase_cell)

# Create menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Save", command=save_board)
file_menu.add_command(label="Load", command=load_board)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

pattern_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Patterns", menu=pattern_menu)
pattern_menu.add_command(label="Glider", command=load_glider)
pattern_menu.add_command(label="Small Exploder", command=load_small_exploder)
pattern_menu.add_command(label="Ten Cell Row", command=load_ten_cell_row)
pattern_menu.add_command(label="Lightweight Spaceship", command=load_lw_spaceship)
pattern_menu.add_command(label="Tumbler", command=load_tumbler)
pattern_menu.add_command(label="Gosper Glider Gun", command=load_gosper_glider_gun)

help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Instructions", command=show_help)

# Control buttons
controls_frame = tk.Frame(root, bg="black")
controls_frame.pack()

start_button = tk.Button(controls_frame, text="Start", command=start_game, bg="black", fg="red")
start_button.grid(row=0, column=0, padx=5, pady=10)

stop_button = tk.Button(controls_frame, text="Stop", command=stop_game, bg="black", fg="red")
stop_button.grid(row=0, column=1, padx=5, pady=10)

clear_button = tk.Button(controls_frame, text="Clear", command=clear_board, bg="black", fg="red")
clear_button.grid(row=0, column=2, padx=5, pady=10)

draw_button = tk.Button(controls_frame, text="Drawing Mode: OFF", command=toggle_drawing_mode, bg="black", fg="red")
draw_button.grid(row=0, column=3, padx=5, pady=10)

speed_scale = tk.Scale(controls_frame, from_=1, to=200, orient=tk.HORIZONTAL, label="Speed", bg="black", fg="red", command=set_simulation_speed)
speed_scale.set(speed)
speed_scale.grid(row=0, column=4, padx=5, pady=10)

status_label = tk.Label(controls_frame, text="Stopped", bg="black", fg="red")
status_label.grid(row=0, column=5, padx=5, pady=10)

randomize_button = tk.Button(controls_frame, text="Randomize", command=randomize_board, bg="black", fg="red")
randomize_button.grid(row=0, column=6, padx=5, pady=10)

root.mainloop()
