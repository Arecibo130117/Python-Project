import tkinter as tk
import math

# 시뮬레이션 변수
m = 0
l = 0
g = 0
theta = 0
w = 0  # 각속도
c = 0
delta_t = 0.5

# Tkinter GUI 생성
window = tk.Tk()
window.title("Damped Pendulum")
window.geometry("900x800")
window.resizable(False, False)

canvas = tk.Canvas(window, width=800, height=800)
canvas.pack(side="right")

# Entry 생성 함수
def create_entry(x, y, info):
    e = tk.Entry(window, font=("Arial", 20))
    e.insert(0, info)
    e.place(x=x, y=y, width=180, height=30)
    return e

# Entry 위젯들
mass = create_entry(80, 130, "3.0")
leng = create_entry(80, 230, "500")
th = create_entry(80, 330, "30")     # 도
gra = create_entry(80, 430, "9.81")
c0 = create_entry(80, 530, "10000")
W0 = create_entry(80, 630, "0")      # 도

# Label
Label = tk.Label(window, text="Pendulum", fg="black", font=("Arial", 36))
Label.place(x=20, y=20)
info = tk.Label(window, text="M \n\n\nL \n\n\nθ \n\n\nG \n\n\nC \n\n\nW", fg="black", font=("Arial", 22))
info.place(x=20, y=125)

# 시뮬레이션 시작 함수
def get_data():
    global m, l, g, theta, c, w
    m = float(mass.get())
    l = float(leng.get())
    theta = math.radians(float(th.get()))
    g = float(gra.get())
    c = float(c0.get())
    w = math.radians(float(W0.get()))
    # Entry 비활성화
    for e in [mass, leng, th, gra, c0, W0]:
        e.config(state='disabled')
    update()

# 물리 계산 함수
def calculate():
    global w, theta
    a = - (g / l) * math.sin(theta) - (c / (m * l**2)) * w
    w += a * delta_t
    theta += w * delta_t

# 애니메이션 함수
def update():
    canvas.delete("all")
    calculate()

    # 원점 위치 (고정점)
    origin_x = 500
    origin_y = 100

    # 추의 위치 계산 (극좌표 -> 직교좌표)
    x = origin_x + l * math.sin(theta)
    y = origin_y + l * math.cos(theta)

    # 줄 그리기
    canvas.create_line(origin_x, origin_y, x, y, width=4, fill='black')

    # 추 그리기
    radius = m * 5 + 10
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill='black')

    window.after(16, update)  # 약 60 FPS

# 시작 버튼
start = tk.Button(window, text="Start", font=("Arial", 22), command=get_data)
start.place(x=80, y=700, width=140, height=50)

window.mainloop()