import turtle
import math

# --- 전역 설정 ---
t = turtle.Turtle()
t.hideturtle()
t.speed(0)
screen = turtle.Screen()
screen.bgcolor("black")
screen.tracer(False)

Rx = 0  # X축 회전 각도
Ry = 0  # Y축 회전 각도

X = 0
Y = 0
Z = 0

# --- 회전 함수 ---
def rotate(x, y, z):
    global X, Y, Z

    # X축 회전 (Rx)
    tempX = math.cos(math.radians(Rx)) * x - math.sin(math.radians(Rx)) * z
    tempZ1 = math.sin(math.radians(Rx)) * x + math.cos(math.radians(Rx)) * z

    # Y축 회전 (Ry)
    tempY = math.cos(math.radians(Ry)) * y - math.sin(math.radians(Ry)) * tempZ1
    tempZ2 = math.sin(math.radians(Ry)) * y + math.cos(math.radians(Ry)) * tempZ1

    X = tempX
    Y = tempY
    Z = tempZ2+400

def triangle_color_xyz(color, x0, y0, z0, x1, y1, z1, x2, y2, z2):
    rotate(x0, y0, z0)
    saveX0 = 200*X/Z
    saveY0 = 200*Y/Z

    rotate(x1, y1, z1)
    saveX1 = 200*X/Z
    saveY1 = 200*Y/Z

    rotate(x2, y2, z2)
    saveX2 = 200*X/Z
    saveY2 = 200*Y/Z

    # 뒤집히지 않은 면만 그리기
    if ((saveX1 - saveX0)*(saveY2 - saveY0) - (saveX2 - saveX0)*(saveY1 - saveY0)) <= 0:
        t.penup()
        t.goto(saveX0, saveY0)
        t.pendown()
        t.fillcolor(color)
        t.begin_fill()
        t.goto(saveX1, saveY1)
        t.goto(saveX2, saveY2)
        t.goto(saveX0, saveY0)
        t.end_fill()


def redraw():
    t.clear()

    # 앞면 (Z = +150)
    triangle_color_xyz("red", -150, -150, 150,  150, -150, 150,  150, 150, 150)
    triangle_color_xyz("red", -150, -150, 150,  150, 150, 150,  -150, 150, 150)

    # 뒷면 (Z = -150)
    triangle_color_xyz("orange", -150, -150, -150,  150, 150, -150,  150, -150, -150)
    triangle_color_xyz("orange", -150, -150, -150,  -150, 150, -150,  150, 150, -150)

    # 오른쪽 면 (X = +150)
    triangle_color_xyz("yellow", 150, -150, -150,  150, 150, 150,  150, -150, 150)
    triangle_color_xyz("yellow", 150, -150, -150,  150, 150, -150,  150, 150, 150)

    # 왼쪽 면 (X = -150)
    triangle_color_xyz("green", -150, -150, -150,  -150, -150, 150,  -150, 150, 150)
    triangle_color_xyz("green", -150, -150, -150,  -150, 150, 150,  -150, 150, -150)

    # 윗면 (Y = +150)
    triangle_color_xyz("blue", -150, 150, -150,  -150, 150, 150,  150, 150, 150)
    triangle_color_xyz("blue", -150, 150, -150,  150, 150, 150,  150, 150, -150)

    # 아랫면 (Y = -150)
    triangle_color_xyz("white", -150, -150, -150,  150, -150, -150,  150, -150, 150)
    triangle_color_xyz("white", -150, -150, -150,  150, -150, 150,  -150, -150, 150)

    screen.update()
    screen.ontimer(redraw, 1) 


def increase_rx():
    global Rx
    Rx += 5

def decrease_rx():
    global Rx
    Rx -= 5

def increase_ry():
    global Ry
    Ry += 5

def decrease_ry():
    global Ry
    Ry -= 5

def setup_key_controls():
    screen.onkeypress(increase_rx, "a")
    screen.onkeypress(decrease_rx, "d")
    screen.onkeypress(increase_ry, "s")
    screen.onkeypress(decrease_ry, "w")

# --- 실행 ---
setup_key_controls()
screen.listen()
redraw()
screen.mainloop()