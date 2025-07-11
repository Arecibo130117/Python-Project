import tkinter as tk
import math

g, m1, m2, l1, l2 = 0, 0, 0, 0, 0
theta1, theta2 = 0, 0
theta1_dot, theta2_dot = 0.0, 0.0

window = tk.Tk()
window.title("Double Pendulum")
window.geometry("1000x800")
window.resizable(False, False)

canvas = tk.Canvas(window, width=1000, height=800)
canvas.pack(side="right")

def create_entry(text, x, y):
    e = tk.Entry(window, font=("Arial", 20))
    e.insert(0, text)
    e.place(x=x, y=y, width=200, height=30)
    return e

Label = tk.Label(window, text="θ            M            L           G", font=("Arial", 38))
Label.place(x=180, y=550)

et1 = create_entry("180", 100, 650)
et2 = create_entry("120", 100, 700)
em1 = create_entry("1", 300, 650)
em2 = create_entry("1", 300, 700)
el1 = create_entry("100", 500, 650)
el2 = create_entry("80", 500, 700)
egravity = create_entry("9.81", 700, 650)

def start_simulation():
    global g, m1, m2, l1, l2, theta1, theta2, theta1_dot, theta2_dot
    theta1 = math.radians(float(et1.get()))
    theta2 = math.radians(float(et2.get()))
    m1 = float(em1.get())
    m2 = float(em2.get())
    l1 = float(el1.get())
    l2 = float(el2.get())
    g = float(egravity.get())
    for e in [et1, et2, em1, em2, el1, el2, egravity]:
        e.destroy()
    Label.destroy()
    start.place_forget()
    calculate()

def calculate():
    global g, m1, m2, l1, l2, theta1, theta2, theta1_dot, theta2_dot

    dt = 0.01
    delta = theta1 - theta2

    den1 = l1 * (2 * m1 + m2 - m2 * math.cos(2 * delta))
    theta1_ddot = (
        -g * (2 * m1 + m2) * math.sin(theta1)
        - m2 * g * math.sin(theta1 - 2 * theta2)
        - 2 * math.sin(delta) * m2 * (
            theta2_dot ** 2 * l2 + theta1_dot ** 2 * l1 * math.cos(delta)
        )
    ) / den1

    den2 = l2 * (2 * m1 + m2 - m2 * math.cos(2 * delta))
    theta2_ddot = (
        2 * math.sin(delta) * (
            theta1_dot ** 2 * l1 * (m1 + m2)
            + g * (m1 + m2) * math.cos(theta1)
            + theta2_dot ** 2 * l2 * m2 * math.cos(delta)
        )
    ) / den2

    theta1_dot += theta1_ddot * dt
    theta2_dot += theta2_ddot * dt
    theta1 += theta1_dot * dt
    theta2 += theta2_dot * dt

    x1 = l1 * math.sin(theta1)
    y1 = l1 * math.cos(theta1)
    x2 = x1 + l2 * math.sin(theta2)
    y2 = y1 + l2 * math.cos(theta2)

    scale = 1.5
    ox, oy = 500, 400

    canvas.delete("all")
    canvas.create_line(ox, oy, ox + x1 * scale, oy + y1 * scale, fill="blue", width=5)
    canvas.create_line(ox + x1 * scale, oy + y1 * scale, ox + x2 * scale, oy + y2 * scale, fill="red", width=5)
    canvas.create_oval(ox + x1 * scale - m1*10, oy + y1 * scale - m1*10, ox + x1 * scale + m1*10, oy + y1 * scale + m1*10, fill="blue")
    canvas.create_oval(ox + x2 * scale - m2*10, oy + y2 * scale - m2*10, ox + x2 * scale + m2*10, oy + y2 * scale + m2*10, fill="red")

    window.after(1, calculate)

start = tk.Button(window, text="start", font=("Arial", 20), background="red", command=start_simulation)
start.place(x=700, y=700, width=200, height=30)

window.mainloop()
