import turtle
import math
import tkinter as tk
import random


boid_count=300 #개체 개수
sep=10 #분리 강도
align = 1 #정렬 강도
coh= 0.1 #응집 강도
boidr=100 #시야각

screen = turtle.Screen()
screen.setup(width=800, height=800)
screen.title("Boids Simulation")
screen.bgcolor("white")
screen.tracer(False)
boid=turtle.Turtle() #창과 거북이 객체 생성
boid.penup()

boids = [[random.uniform(-500, 500), random.uniform(-500, 500)] for _ in range(boid_count)] #개체들의 좌표
v = [[random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)] for _ in range(boid_count)] #개체들의 속도
angles = [random.uniform(0, 360) for _ in range(boid_count)] #개체들의 방향

def limit_speed(vx, vy, max_speed):
    speed = math.sqrt(vx**2 + vy**2)
    if speed > max_speed:
        factor = max_speed / speed
        return vx * factor, vy * factor
    return vx, vy
def update():
    boid.clear()
    for i in range(boid_count):
        boidx, boidy = boids[i]
        if boidx < -400: boidx = 400
        if boidx > 400: boidx = -400
        if boidy < -400: boidy = 400
        if boidy > 400: boidy = -400
        vx, vy = v[i]
        Ncount = 0

        Fsep_x, Fsep_y = 0, 0
        Falignx, Faligny = 0, 0
        Fcohx, Fcohy = 0, 0

        for j in range(boid_count):
            if i == j:
                continue
            boidx2, boidy2 = boids[j]
            dx = boidx2 - boidx
            dy = boidy2 - boidy
            dist = math.hypot(dx, dy)
            

            if dist < boidr and dist > 0:
                Ncount += 1
                # Separation: 반대 방향으로 밀기
                Fsep_x -= dx / (dist**2 + 0.01)
                Fsep_y -= dy / (dist**2 + 0.01)


                # Alignment: 속도 차이
                Falignx += v[j][0] - vx
                Faligny += v[j][1] - vy

                # Cohesion: 중심점
                Fcohx += dx
                Fcohy += dy

        # 평균화
        if Ncount > 0:
            Falignx /= Ncount
            Faligny /= Ncount
            Fcohx /= Ncount
            Fcohy /= Ncount

        # 가속도 계산
        ax = Fsep_x * sep + Falignx * align + Fcohx * coh
        ay = Fsep_y * sep + Faligny * align + Fcohy * coh

        # 속도, 위치 업데이트
        vx += ax
        vy += ay
        vx, vy = limit_speed(vx, vy, max_speed=4.0)
        boidx += vx
        boidy += vy

        # 저장
        v[i] = [vx, vy]
        boids[i] = [boidx, boidy]
        angles[i] = math.degrees(math.atan2(vy, vx))

    for i in range(boid_count):
        boid.goto(boids[i][0], boids[i][1])
        boid.setheading(angles[i])
        boid.stamp()

    screen.update()
    screen.ontimer(update, 1)

    
update()

screen.mainloop()