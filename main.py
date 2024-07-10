import tkinter as tk

GRID_WIDTH = 50
GRID_HEIGHT = 30
CELL_SIZE = 15

root = tk.Tk()
root.title("Conway's Game of Life")

canvas = tk.Canvas(root, width=GRID_WIDTH * CELL_SIZE, height=GRID_HEIGHT * CELL_SIZE, borderwidth=0, highlightthickness=0)
canvas.pack()

cells = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            cell_color = "white"
            canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE,
                                    (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                                    fill=cell_color, outline="gray")

draw_grid()

def toggle_cell(event):
    x = event.x // CELL_SIZE
    y = event.y // CELL_SIZE
    cells[y][x] = 1 - cells[y][x]
    draw_grid()

canvas.bind("<Button-1>", toggle_cell)

root.mainloop()
