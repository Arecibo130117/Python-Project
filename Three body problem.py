import tkinter as tk
import math

# 윈도우 생성
window = tk.Tk()
window.title("Three-body problem")
window.geometry("1280x800")
window.resizable(False, False)

# 데이터 저장 리스트
xdata = []
ydata = []
vxdata = []
vydata = []

# 캔버스 생성
canvas = tk.Canvas(window, width=1280, height=650, bg="black")

# 텍스트 라벨
text_1 = tk.Label(window, text="x_1\n\ny_1\n\nvx_1\n\nvy_1", fg="black", font=("Arial", 20))
text_1.place(x=30, y=300)

text_2 = tk.Label(window, text="x_2\n\ny_2\n\nvx_2\n\nvy_2", fg="black", font=("Arial", 20))
text_2.place(x=470, y=300)

text_3 = tk.Label(window, text="x_3\n\ny_3\n\nvx_3\n\nvy_3", fg="black", font=("Arial", 20))
text_3.place(x=910, y=300)

title = tk.Label(window, text="Settings", fg="black", font=("Arial", 50))
title.place(x=540, y=20)

# Entry 생성 함수
def create_entry(x, y):
    e = tk.Entry(window, font=("Arial", 20))
    e.insert(0, "")
    e.place(x=x, y=y, width=250, height=25)
    return e

# planet_1
x_1 = create_entry(100, 310)
y_1 = create_entry(100, 370)
vx_1 = create_entry(100, 435)
vy_1 = create_entry(100, 500)

# planet_2
x_2 = create_entry(540, 310)
y_2 = create_entry(540, 370)
vx_2 = create_entry(540, 435)
vy_2 = create_entry(540, 500)

# planet_3
x_3 = create_entry(980, 310)
y_3 = create_entry(980, 370)
vx_3 = create_entry(980, 435)
vy_3 = create_entry(980, 500)

# planet 움직임 계산
def move_planet():
    for j in range(3):
        for i in range(3):
            if j != i:
                r = math.sqrt((xdata[j] - xdata[i])**2 + (ydata[j] - ydata[i])**2)
                if r > 10:
                    Fx = 0.2 * ((200**2) * (xdata[i] - xdata[j])) / r**3
                    Fy = 0.2 * ((200**2) * (ydata[i] - ydata[j])) / r**3
                    a1x = Fx / 200
                    a1y = Fy / 200
                    a2x = -Fx / 200
                    a2y = -Fy / 200

                    vxdata[j] += a1x * 0.2
                    vydata[j] += a1y * 0.2
                    xdata[j] += vxdata[j]
                    ydata[j] += vydata[j]

                    vxdata[i] += a2x * 0.2
                    vydata[i] += a2y * 0.2
                    xdata[i] += vxdata[i]
                    ydata[i] += vydata[i]

# 시뮬레이션 반복
def update():
    canvas.delete("all")
    move_planet()

    # 행성 그리기
    canvas.create_oval(xdata[0]-15, ydata[0]-15, xdata[0]+15, ydata[0]+15, fill="red")
    canvas.create_oval(xdata[1]-15, ydata[1]-15, xdata[1]+15, ydata[1]+15, fill="blue")
    canvas.create_oval(xdata[2]-15, ydata[2]-15, xdata[2]+15, ydata[2]+15, fill="yellow")

    window.after(20, update)  # 50ms마다 반복

# 데이터 가져오기 + UI 전환
def get_all_data():
    # 행성 1
    xdata.append(float(x_1.get()))
    ydata.append(float(y_1.get()))
    vxdata.append(float(vx_1.get()))
    vydata.append(float(vy_1.get()))
    # 행성 2
    xdata.append(float(x_2.get()))
    ydata.append(float(y_2.get()))
    vxdata.append(float(vx_2.get()))
    vydata.append(float(vy_2.get()))
    # 행성 3
    xdata.append(float(x_3.get()))
    ydata.append(float(y_3.get()))
    vxdata.append(float(vx_3.get()))
    vydata.append(float(vy_3.get()))

    # Entry와 Label 숨기기
    for widget in [x_1, y_1, vx_1, vy_1, x_2, y_2, vx_2, vy_2, x_3, y_3, vx_3, vy_3, text_1, text_2, text_3, ok]:
        widget.place_forget()

    title.config(text="Three-body problem")
    title.place(x=375, y=20)

    canvas.pack(side="bottom")

    # 시뮬레이션 시작
    update()

# OK 버튼
ok = tk.Button(window, text="ok", font=("Arial", 24), command=get_all_data)
ok.place(x=640, y=700, width=60, height=40)

window.mainloop()