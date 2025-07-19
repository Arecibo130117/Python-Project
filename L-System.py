import turtle
import time

# L-System 설정
axiom = "F"
rule = {"F": "F[+F]F[-F]F"}
iterations = 5
angle = 25

# L-System 문자열 생성
def generate_lsystem(axiom, rule, iterations):
    result = axiom
    for _ in range(iterations):
        next_result = ""
        for char in result:
            next_result += rule.get(char, char)
        result = next_result
    return result

# Turtle 설정
t = turtle.Turtle()
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("L-System")
t.speed(0)
t.hideturtle()

# 생성된 코드
code = generate_lsystem(axiom, rule, iterations)

# 시작 위치와 방향
t.penup()
t.goto(0, -250)
t.setheading(90)
t.pendown()
t.pencolor("green")

# 위치 저장용 스택
stack = []

# 코드 해석 및 그리기
for char in code:
    if char == "F":
        t.forward(5)
    elif char == "+":
        t.right(angle)
    elif char == "-":
        t.left(angle)
    elif char == "[":
        stack.append((t.pos(), t.heading()))
    elif char == "]":
        pos, heading = stack.pop()
        t.penup()
        t.goto(pos)
        t.setheading(heading)
        t.pendown()

# 클릭하면 종료
screen.exitonclick()
