import tkinter as tk
import numpy as np
window = tk.Tk()
window.geometry("800x800")
window.resizable(False, False)
window.title("Heat Equation")
canvas=tk.Canvas(width=800, height=800)
canvas.pack()
heat = tk.Entry(window, font=("Arial", 10))
heat.insert(0, 1000)
heat.place(x=350, y=700,  width=100)
lable = tk.Label(window, text="Heat", font=("Arial", 15))
lable.place(x=375, y=670)



N = 45 #해상도
u = np.zeros((N + 2, N + 2))
u_new = np.zeros_like(u)
r = 0.2

def project():
    global u, u_new
    for i in range(1, N+1):
        for j in range(1, N+1):
            if j == 1:
                u[j-1][i] = u[j][i]      # 위쪽 경계
            if j == N:
                u[j+1][i] = u[j][i]      # 아래쪽 경계
            if i == 1:
                u[j][i-1] = u[j][i]      # 왼쪽 경계
            if i == N:
                u[j][i+1] = u[j][i]      # 오른쪽 경계
            
            u_new[j][i] = u[j][i] + r * (
                u[j+1][i] + u[j-1][i] + u[j][i+1] + u[j][i-1] - 4*u[j][i]
            )
    u[:, :] = u_new
    
def temperature_to_color(value, vmin=0, vmax=100): #색 변환은 gemini가 해줌
    ratio = (value - vmin) / (vmax - vmin)
    ratio = max(0.0, min(1.0, ratio)) 

    red = 0
    green = 0
    blue = 0

    if ratio < 0.25:
        segment_ratio = ratio / 0.25
        red = 0
        green = int(255 * segment_ratio)
        blue = 255
    elif ratio < 0.5:
        segment_ratio = (ratio - 0.25) / 0.25
        red = 0
        green = 255
        blue = int(255 * (1 - segment_ratio))
    elif ratio < 0.75:
        segment_ratio = (ratio - 0.5) / 0.25
        red = int(255 * segment_ratio)
        green = 255
        blue = 0
    else:
        segment_ratio = (ratio - 0.75) / 0.25
        red = 255
        green = int(255 * (1 - segment_ratio))
        blue = 0
    red = max(0, min(255, red))
    green = max(0, min(255, green))
    blue = max(0, min(255, blue))
    return f'#{red:02x}{green:02x}{blue:02x}'


def click(event):
    global u
    x, y = event.x, event.y
    u[int(x//(800/N))][int(y//(800/N))] += float(heat.get())


    
def update():
    canvas.bind("<Button-1>", click)
    canvas.bind("<B1-Motion>", click)
    canvas.delete("all")
    project()
    for i in range(1,N+1):
        for j in range(1, N+1):
            x1 = (j-1) * (800/N)
            x2 = (j) * (800/N)
            y1 = (i-1) * (800/N)
            y2 = (i) * (800/N)
            color = temperature_to_color(u[j][i]+50)
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
    window.after(20, update)
    
update()

window.mainloop()