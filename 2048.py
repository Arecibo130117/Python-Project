import tkinter as tk
import copy
import random

N = 4
Score = 0
MoveCnt = 0

Game = [[-1] + [0] * N + [-1] for _ in range(N)] #-1로 패딩
Game.insert(0, [-1] * (N + 2)) 
Game.append([-1] * (N + 2))
Pgame = copy.deepcopy(Game)

def PlaceTile(): #타일 배치 함수
    whitePlace = []
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if Game[i][j] == 0:
                whitePlace.append((i, j))
    
    if len(whitePlace) == 0:
        return
    
    ni, nj = whitePlace[random.randint(0, len(whitePlace) - 1)]
    Game[ni][nj] = 2 if random.randint(0, 9) < 9 else 4 

def move(mode: str): #타일 움직이기 함수
    global MoveCnt, Score, Pgame
    
    '''
    탐색 인덱스 저장용 변수들
    '''
    si, ei, vi = 0, 0, 0
    sj, ej, vj = 0, 0, 0
    
    if mode == 'up' or mode == 'left': #탐색 순서 정하기
        si, ei, vi = 1, N + 1, 1
        sj, ej, vj = 1, N + 1, 1
    elif mode == 'down' or mode == 'right':
        si, ei, vi = N, 0, -1
        sj, ej, vj = N, 0, -1

    for i in range(si, ei, vi):
        for j in range(sj, ej, vj):
            preY, preX, nY, nX = 0, 0, 0, 0 #좌표 가중치
            if Game[i][j] != 0:
                myCell = Game[i][j]
                Game[i][j] = 0
                
                while True:
                    y, x = i + nY, j + nX
                    
                    if not Game[y][x] == 0:
                        if Game[y][x] == myCell: #같은 수끼리 만나면 점수 더하고 셀 바꾸기
                            Score += myCell * 2 
                            Game[y][x] = myCell * 2
                        else:
                            Game[i + preY][j + preX] = myCell #아니면 이전 자리로 되돌아가기
                        break
                    
                    if mode == 'up':
                        preY = nY
                        nY -= 1
                    elif mode == 'down':
                        preY = nY
                        nY += 1
                    elif mode == 'left':
                        preX = nX
                        nX -= 1
                    else:
                        preX = nX
                        nX += 1
    if Pgame != Game:
        MoveCnt += 1
        PlaceTile()
        Pgame = copy.deepcopy(Game)

def CheckGameOver() -> bool: #게임오버 판별
    dx = [0, 0, 1, -1]
    dy = [1, -1, 0, 0]
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if Game[i][j] == 0:
                return False
    
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            myCell = Game[i][j]
            for k in range(4):
                if Game[i + dy[k]][j + dx[k]] == myCell:
                    return False
    
    return True

colors = {
    "background": "#FAF8EF",
    "grid": "#BBADA0",
    "0": "#CDC1b4",
    "2": "#EEE4DA",
    "4": "#EDE0C8",
    "8": "#F2B179",
    "16": "#F59563",
    "32": "#F67C5F",
    "64": "#F65E3B",
    "128": "#EDCF72",
    "256": "#EDCC61",
    "512": "#EDC850",
    "1024": "#EDC53F",
    "2048": "#EDC22E",
    "4096": "#3C3A32"
}

window = tk.Tk()
window.resizable(False, False)
window.geometry('500x550')
window.title('2048')
window.config(background= colors["background"])
LabelScore = tk.Label(window, text= 'Move : 0', fg= "#776e65", bg= colors["background"], font=("Helvetica", 26, "bold"))
LabelScore.place(x = 30, y = 20)
LabelMove = tk.Label(window, text= 'Move : 0', fg= "#776e65", bg= colors["background"], font=("Helvetica", 26, "bold"))
LabelMove.place(x = 280, y = 20)
canvas = tk.Canvas(window, width= 440, height= 440, background= colors["grid"])
canvas.place(x= 29, y= 70)

def Game2048_ui():
    canvas.delete('all')
    k = 12
    nx, ny = 0, k
    d = 107.5
    w = 96
    for i in range(1, N + 1):
        nx = k
        for j in range(1, N + 1):
            canvas.create_rectangle(nx, ny, nx + w, ny + w, fill= colors[str(min(4096, Game[i][j]))], outline= colors[str(min(4096, Game[i][j]))])
            if Game[i][j] != 0:
                canvas.create_text(nx + w/2, ny + w/2, text= Game[i][j], font= ("Helvetica", 36 if Game[i][j] < 1000 else 26, "bold"), fill= "#776e65" if Game[i][j] in [2, 4] else "#f9f6f2")
            nx += d
        ny += d

PlaceTile()
PlaceTile()
def main():
    LabelScore.config(text= f'Score : {Score}')
    LabelMove.config(text= f'Move : {MoveCnt}')
    window.bind("<w>", lambda e: move('up'))
    window.bind("<s>", lambda e: move('down'))
    window.bind("<a>", lambda e: move('left'))
    window.bind("<d>", lambda e: move('right'))
    Game2048_ui()
    if CheckGameOver():
        canvas.create_rectangle(0, 0, 500, 550, fill='black', stipple='gray50')
        canvas.create_text(220, 160, text= 'Game Over', font= ("Helvetica", 36, "bold"), fill= "#FFFFFF")
        canvas.create_text(220, 250, text= f'Score : {Score}  Move : {MoveCnt}', font= ("Helvetica", 17, "bold"), fill= "#FFFFFF")
        return
        
    
    window.after(20, main)

main()
window.mainloop()