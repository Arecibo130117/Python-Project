import tkinter as tk
import random

grid = [[random.randint(0, 1) for _ in range(80)] for _ in range(80)]
window = tk.Tk()
window.geometry("800x800")
window.resizable(False, False)
window.title("Game of Life")
canvas = tk.Canvas(window, width=800, height=800, bg="white")
canvas.pack()

def draw_grid():
    canvas.delete("all")
    for i in range(80):
        for j in range(80):
            x1 = j * 10
            y1 = i * 10
            x2 = x1 + 10
            y2 = y1 + 10
            color = "black" if grid[i][j] == 1 else "white"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

def update_grid():
    global grid
    case = [(-1, 1), (0, 1), (1, 1), (-1,0), (1, 0), (-1, -1), (0, -1), (1, -1)]
    new_grid = [[0 for _ in range(80)] for _ in range(80)]
    for i in range(80):
        for j in range(80):
            neighbor = 0
            for dx, dy in case:
                ni = (i + dy) % 80
                nj = (j + dx) % 80
                if grid[ni][nj] == 1:
                    neighbor += 1
            if grid[i][j] == 1:
                if neighbor == 2 or neighbor == 3:
                    new_grid[i][j] = 1
                else:
                    new_grid[i][j] = 0
            else:
                if neighbor == 3:
                    new_grid[i][j] = 1
                else:
                    new_grid[i][j] = 0
    grid = new_grid
    draw_grid()
    window.after(40, update_grid)

draw_grid()
window.after(40, update_grid)
window.mainloop()