import tkinter as tk

GRID_WIDTH = 50
GRID_HEIGHT = 30
CELL_SIZE = 15

root = tk.Tk()
root.title("Conway's Game of Life")

canvas = tk.Canvas(root, width=GRID_WIDTH * CELL_SIZE, height=GRID_HEIGHT * CELL_SIZE, borderwidth=0, highlightthickness=0)
canvas.pack()

cells = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
next_cells = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

running = False
speed = 100

def draw_grid():
    canvas.delete("all")
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            cell_color = "black" if cells[y][x] else "white"
            canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE,
                                    (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                                    fill=cell_color, outline="gray")

def count_neighbors(y, x):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if 0 <= y + i < GRID_HEIGHT and 0 <= x + j < GRID_WIDTH:
                count += cells[y + i][x + j]
    return count

def update_grid():
    global running
    if running:
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                neighbors = count_neighbors(y, x)
                if cells[y][x] == 1:
                    if neighbors < 2 or neighbors > 3:
                        next_cells[y][x] = 0
                    else:
                        next_cells[y][x] = 1
                else:
                    if neighbors == 3:
                        next_cells[y][x] = 1
                    else:
                        next_cells[y][x] = 0

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                cells[y][x] = next_cells[y][x]

        draw_grid()
        root.after(speed, update_grid)

def toggle_cell(event):
    x = event.x // CELL_SIZE
    y = event.y // CELL_SIZE
    cells[y][x] = 1 - cells[y][x]
    draw_grid()

def start_simulation():
    global running
    running = True
    update_grid()

def stop_simulation():
    global running
    running = False

def clear_grid():
    global cells, next_cells
    cells = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    next_cells = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    draw_grid()

def change_speed(val):
    global speed
    speed = int(val)

canvas.bind("<Button-1>", toggle_cell)

draw_grid()

button_frame = tk.Frame(root)
button_frame.pack()

start_button = tk.Button(button_frame, text="Start", command=start_simulation)
start_button.grid(row=0, column=0)

stop_button = tk.Button(button_frame, text="Stop", command=stop_simulation)
stop_button.grid(row=0, column=1)

clear_button = tk.Button(button_frame, text="Clear", command=clear_grid)
clear_button.grid(row=0, column=2)

speed_slider = tk.Scale(button_frame, from_=10, to=1000, orient="horizontal", label="Speed (ms)", command=change_speed)
speed_slider.set(speed)
speed_slider.grid(row=0, column=3)

root.mainloop()
