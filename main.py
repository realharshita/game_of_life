import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import json
import random

GRID_WIDTH = 50
GRID_HEIGHT = 30
CELL_SIZE = 15

live_cell_color = "red"
dead_cell_color = "black"
grid_line_color = "gray"
background_color = "black"

root = tk.Tk()
root.title("Conway's Game of Life")
root.configure(bg=background_color)

canvas = tk.Canvas(root, width=GRID_WIDTH * CELL_SIZE, height=GRID_HEIGHT * CELL_SIZE, borderwidth=0, highlightthickness=0, bg=background_color)
canvas.pack(pady=20)

board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
next_board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

running = False
drawing_mode = False
speed = 100

generation_count = 0
live_cells_count = 0

def render_grid():
    canvas.delete("all")
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            cell_color = live_cell_color if board[y][x] else dead_cell_color
            canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE,
                                    (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                                    fill=cell_color, outline=grid_line_color)

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
    global running, generation_count, live_cells_count
    if running:
        generation_count += 1
        live_cells_count = sum(sum(row) for row in board)

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
        update_statistics()

        if running:
            root.after(speed, update_simulation)

def update_statistics():
    stats_label.config(text=f"Generation: {generation_count} | Live Cells: {live_cells_count}")

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
    stats_label.config(text="Running", fg="red")
    update_simulation()

def stop_game():
    global running
    running = False
    stats_label.config(text="Stopped", fg="red")
    
def step_game():
    global running
    if not running:
        running = True
        stats_label.config(text="Stepping", fg="red")
        update_simulation()
        running = False 


def reset_speed():
    global speed
    speed = 100
    speed_scale.set(speed)

def clear_board():
    global board, next_board, generation_count, live_cells_count
    board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    next_board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    generation_count = 0
    live_cells_count = 0
    render_grid()
    update_statistics()

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
            update_statistics()

def randomize_board():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            board[y][x] = random.choice([0, 1])
    render_grid()
    update_statistics()

def load_pattern(pattern):
    clear_board()
    for (x, y) in pattern:
        board[y][x] = 1
    render_grid()
    update_statistics()

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

def choose_color(color_type):
    color = colorchooser.askcolor()[1]
    if color:
        global live_cell_color, dead_cell_color, grid_line_color, background_color
        if color_type == "Live Cell":
            live_cell_color = color
        elif color_type == "Dead Cell":
            dead_cell_color = color
        elif color_type == "Grid Line":
            grid_line_color = color
        elif color_type == "Background":
            background_color = color
            root.configure(bg=background_color)
            canvas.configure(bg=background_color)
        render_grid()

def create_pattern_preview(pattern):
    preview_window = tk.Toplevel(root)
    preview_window.title("Pattern Preview")
    preview_canvas = tk.Canvas(preview_window, width=100, height=100, bg=background_color)
    preview_canvas.pack()

    for (x, y) in pattern:
        preview_canvas.create_rectangle(x * 10, y * 10, (x + 1) * 10, (y + 1) * 10, fill=live_cell_color, outline=grid_line_color)

def preview_glider():
    glider = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]
    create_pattern_preview(glider)

def preview_small_exploder():
    small_exploder = [(1, 0), (0, 1), (1, 1), (2, 1), (0, 2), (2, 2), (1, 3)]
    create_pattern_preview(small_exploder)

def preview_ten_cell_row():
    ten_cell_row = [(x, 1) for x in range(10)]
    create_pattern_preview(ten_cell_row)

def preview_lw_spaceship():
    lw_spaceship = [(1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (4, 1), (4, 2), (0, 3), (3, 3)]
    create_pattern_preview(lw_spaceship)

def preview_tumbler():
    tumbler = [(3, 0), (4, 0), (5, 0), (6, 0), (2, 1), (3, 1), (5, 1), (6, 1), (2, 2), (3, 2), (5, 2), (6, 2), 
               (0, 3), (2, 3), (6, 3), (8, 3), (0, 4), (1, 4), (7, 4), (8, 4), (0, 5), (8, 5), (1, 6), (7, 6), 
               (2, 6), (6, 6), (3, 6), (4, 6), (5, 6)]
    create_pattern_preview(tumbler)

def preview_gosper_glider_gun():
    gosper_glider_gun = [(24, 2), (22, 3), (24, 3), (12, 4), (13, 4), (20, 4), (21, 4), (34, 4), (35, 4), 
                         (11, 5), (15, 5), (20, 5), (21, 5), (34, 5), (35, 5), (0, 6), (1, 6), (10, 6), (16, 6), 
                         (20, 6), (21, 6), (0, 7), (1, 7), (10, 7), (14, 7), (16, 7), (17, 7), (22, 7), (24, 7), 
                         (10, 8), (16, 8), (24, 8), (11, 9), (15, 9), (12, 10), (13, 10)]
    create_pattern_preview(gosper_glider_gun)

canvas.bind("<Button-1>", add_cell)
canvas.bind("<B1-Motion>", draw_cell)
canvas.bind("<Button-3>", remove_cell)
canvas.bind("<B3-Motion>", erase_cell)

root.bind("<space>", start_game)
root.bind("<Escape>", stop_game)
root.bind("c", clear_board)
root.bind("r", randomize_board)

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

preview_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Previews", menu=preview_menu)
preview_menu.add_command(label="Glider", command=preview_glider)
preview_menu.add_command(label="Small Exploder", command=preview_small_exploder)
preview_menu.add_command(label="Ten Cell Row", command=preview_ten_cell_row)
preview_menu.add_command(label="Lightweight Spaceship", command=preview_lw_spaceship)
preview_menu.add_command(label="Tumbler", command=preview_tumbler)
preview_menu.add_command(label="Gosper Glider Gun", command=preview_gosper_glider_gun)

color_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Colors", menu=color_menu)
color_menu.add_command(label="Live Cell Color", command=lambda: choose_color("Live Cell"))
color_menu.add_command(label="Dead Cell Color", command=lambda: choose_color("Dead Cell"))
color_menu.add_command(label="Grid Line Color", command=lambda: choose_color("Grid Line"))
color_menu.add_command(label="Background Color", command=lambda: choose_color("Background"))

help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Instructions", command=show_help)

# Control buttons
controls_frame = tk.Frame(root, bg=background_color)
controls_frame.pack()

start_button = tk.Button(controls_frame, text="Start Simulation", command=start_game, bg="black", fg="red", padx=10, pady=5)
start_button.grid(row=0, column=0, padx=5, pady=10)
start_button.config(cursor="hand2", relief=tk.RAISED, bd=2, highlightbackground="red")

stop_button = tk.Button(controls_frame, text="Stop Simulation", command=stop_game, bg="black", fg="red", padx=10, pady=5)
stop_button.grid(row=0, column=1, padx=5, pady=10)
stop_button.config(cursor="hand2", relief=tk.RAISED, bd=2, highlightbackground="red")

step_button = tk.Button(controls_frame, text="Step", command=step_game, bg="black", fg="red", padx=10, pady=5)
step_button.grid(row=0, column=2, padx=5, pady=10)
step_button.config(cursor="hand2", relief=tk.RAISED, bd=2, highlightbackground="red")

reset_speed_button = tk.Button(controls_frame, text="Reset Speed", command=reset_speed, bg="black", fg="red", padx=10, pady=5)
reset_speed_button.grid(row=0, column=3, padx=5, pady=10)
reset_speed_button.config(cursor="hand2", relief=tk.RAISED, bd=2, highlightbackground="red")

clear_button = tk.Button(controls_frame, text="Clear Grid", command=clear_board, bg="black", fg="red", padx=10, pady=5)
clear_button.grid(row=0, column=4, padx=5, pady=10)
clear_button.config(cursor="hand2", relief=tk.RAISED, bd=2, highlightbackground="red")

random_button = tk.Button(controls_frame, text="Randomize Grid", command=randomize_board, bg="black", fg="red", padx=10, pady=5)
random_button.grid(row=0, column=5, padx=5, pady=10)
random_button.config(cursor="hand2", relief=tk.RAISED, bd=2, highlightbackground="red")

draw_button = tk.Button(controls_frame, text="Drawing Mode: OFF", command=toggle_drawing_mode, bg="black", fg="red", padx=10, pady=5)
draw_button.grid(row=0, column=6, padx=5, pady=10)
draw_button.config(cursor="hand2", relief=tk.RAISED, bd=2, highlightbackground="red")

# Simulation speed control
speed_scale = tk.Scale(root, from_=10, to=1000, orient=tk.HORIZONTAL, label="Simulation Speed (ms)", command=set_simulation_speed, bg="black", fg="red", troughcolor="gray", highlightbackground="red")
speed_scale.set(speed)
speed_scale.pack(pady=20)

# Statistics display
stats_label = tk.Label(root, text="Generation: 0 | Live Cells: 0", fg="red", bg="black")
stats_label.pack(pady=10)

root.mainloop()
