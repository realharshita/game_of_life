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
    root.after(10, update_grid)  # Update every 100 milliseconds

def toggle_cell(event):
    x = event.x // CELL_SIZE
    y = event.y // CELL_SIZE
    cells[y][x] = 1 - cells[y][x]
    draw_grid()

canvas.bind("<Button-1>", toggle_cell)

draw_grid()
update_grid()

root.mainloop()
