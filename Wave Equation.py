import tkinter as tk
import math
import copy

window = tk.Tk()
window.geometry("800x800")
window.resizable(False, False)
window.title("Wave Equation")
window.config(background="black")
canvas = tk.Canvas(width=600, height=600, background="black")
canvas.place(x=100, y=100)

N = 50
clickR = 10
dt = 0.01
c = 300
h = 600/(N-1)
u = [[0 for _ in range(N+2)]for _ in range(N+2)]
u_new=copy.deepcopy(u)
u_prev=copy.deepcopy(u)
mx, my = 0, 0
mode1 = 1
step=0
rotX, rotY = 0, 0
perspective = 385

def temperature_to_color(value, vmin=0, vmax=100):
    ratio = (value+50 - vmin) / (vmax - vmin)
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

def edit(event):
    mx, my = event.x, event.y
    j = int(my // (600 / N))
    i = int(mx // (600 / N))
    
    # 범위 체크: j, i가 1 이상 N 이하인지 확인
    if 1 <= i <= N and 1 <= j <= N:
        for j_index in range(max(1, j - clickR), min(N, j + clickR) + 1):
            for i_index in range(max(1, i - clickR), min(N, i + clickR) + 1):
                d = math.sqrt((j - j_index) ** 2 + (i - i_index) ** 2)
                u[i_index][j_index] += mode1*max(0, (clickR-d))

def rotate_m(event):
    global rotX, rotY
    rotX, rotY = (event.x - 400) / 80, (event.y - 400) / 80

def mode_change():
    global mode1
    if mode1 == 1:
        mode1 = -1
        mode.config(fg="blue", bg="black", text="Cold")
    else:
        mode1 = 1
        mode.config(fg="red", bg="black", text="Hot")

def starting():
    global step, u_prev
    step = 1
    u_prev = copy.deepcopy(u)
    canvas.config(width=800, height=800)
    canvas.place(x=0, y=0)
    mode.destroy()
    start_button.destroy()

def draw():
    canvas.bind("<Button-1>", edit)
    canvas.bind("<B1-Motion>", edit)
    canvas.delete("all")
    for j in range(1, N+1):
        for i in range(1, N+1):
            x0 = (i-1)*(600/N)
            y0 = (j-1)*(600/N)
            x1 = i*(600/N)
            y1 = j*(600/N)
            value = u[i][j]  # 진폭을 하나 선택
            color = temperature_to_color(value)
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=0)
    if step == 0:
        window.after(20, draw)

def rotate(i,j,z):
    x = (i - N/2) * 800/(N-1)
    y = (j - N/2) * 800/(N-1)
    Xrot = (math.cos(rotX) * x) - (math.sin(rotX) * z)
    Zrot = (math.sin(rotX) * x) + (math.cos(rotX) * z)
    Yrot = (math.cos(rotY) * y) - (math.sin(rotY) * Zrot)
    Zrot = (math.sin(rotY) * y) + (math.cos(rotY) * Zrot)
    return Xrot+400, Yrot+400, Zrot+400

def wave_calculate():
    global u_new, u, u_prev
    for j in range(1, N+1):
        for i in range(1, N+1):
            u_new[i][j] = 2*u[i][j] - u_prev[i][j] + ((c*dt)/h)**2 * (u[i+1][j] + u[i-1][j] + u[i][j+1] + u[i][j-1] - 4*u[i][j])
    u_prev = copy.deepcopy(u)
    u = copy.deepcopy(u_new)

def draw3D():
    if step == 1:
        global rotX, rotY
        canvas.delete("all")
        wave_calculate()
        canvas.bind("<B1- Motion>", rotate_m)
        for j in range(1, N+1):
            for i in range(1, N+1):
                x0, y0, z0 = rotate(i, j, u[i][j])
                x1, y1, z1 = rotate(i+1, j, u[i+1][j])
                x2, y2, z2 = rotate(i+1, j+1, u[i+1][j+1])
                x3, y3, z3 = rotate(i, j+1, u[i][j+1])
                if min(z0, z1, z2, z3) > 0:
                    pts = [
                        (perspective*(x0/z0), perspective*(y0/z0)),
                        (perspective*(x1/z1), perspective*(y1/z1)),
                        (perspective*(x2/z2), perspective*(y2/z2)),
                        (perspective*(x3/z3), perspective*(y3/z3)),
                    ]
                    color = temperature_to_color((u[i][j] + u[i+1][j] + u[i+1][j+1] + u[i][j+1])/4)
                    canvas.create_polygon(pts, outline=color, fill='')
    window.after(20, draw3D)

mode = tk.Button(window, text="Hot", font=("Arial",30), command=mode_change, fg="red", background="black")
mode.place(x=250, y=5)
start_button = tk.Button(window, text="Start", font=("Arial", 30), command=starting)
start_button.place(x=500, y=5)
draw()
draw3D()
window.mainloop()
