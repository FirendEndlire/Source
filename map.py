from settings import *
import pygame
from random import randint
map_now = ["shop"]
with open(F'data/map1.txt', 'rt') as f:
    matrix_map1 = f.readlines()
print(f.closed)
with open(F'data/map2.txt', 'rt') as f:
    matrix_map2 = f.readlines()
print(f.closed)


def generation_map(x, y):
    matrix = []
    for i in range(x):
        matrix.append([])
        for j in range(y):
            if (i == 0 or i == x - 1) != (j == 0 or j == y - 1):
                matrix[i].append("W")
            else:
                matrix[i].append("_")
    matrix[0][0] = "W"
    matrix[0][y - 1] = "W"
    matrix[x - 1][0] = "W"
    matrix[x - 1][y - 1] = "W"
    for i in range(1, len(matrix) - 1):
        for j in range(1, len(matrix[i]) - 1):
            if j == 1:
                key = f"{matrix[i][j - 2]}{matrix[i][j - 1]}{matrix[i - 1][j - 1]}{matrix[i - 1][j]}{matrix[i - 1][j + 1]}"
            else:
                key = f"W{matrix[i][j - 1]}{matrix[i - 1][j - 1]}{matrix[i - 1][j]}{matrix[i - 1][j + 1]}"
            if TABEl[key] == -1:
                a = randint(0, 1)
            else:
                a = TABEl[key]
            if a == 1:
                matrix[i][j] = "W"
            else:
                matrix[i][j] = "_"

    return matrix
labirynth = generation_map(15, 15)
with open(F'labyrinth.txt', 'w') as f:
    for i in labirynth:
        #print(i)
        f.write(str(i)+"\n")
labirynth = list(map(lambda x: str(x), labirynth))
labirynth = list(map(lambda x: x.replace("W", "5"), labirynth))
labirynth = list(map(lambda x: x.replace(",", ""), labirynth))
labirynth = list(map(lambda x: x.replace(" ", ""), labirynth))
labirynth = list(map(lambda x: x.replace("\n", ""), labirynth))
labirynth = list(map(lambda x: x.replace("'", ""), labirynth))
labirynth = list(map(lambda x: x.replace("[", ""), labirynth))
labirynth = list(map(lambda x: x.replace("]", ""), labirynth))
labirynth = list(map(lambda x: list(x), labirynth))
labirynth[1][2] = "_"
labirynth[2][1] = "_"
labirynth[2][2] = "_"
labirynth[1][1] = "_"
labirynth[13][13] = "_"
labirynth[12][13] = "_"
labirynth[11][13] = "_"
labirynth[12][12] = "_"
labirynth[13][12] = "_"
labirynth[11][12] = "_"
labirynth[13][11] = "_"
labirynth[12][11] = "_"
labirynth[11][11] = "_"

_ = False
matrix_map1 = list(map(lambda x: x.replace(" ", ""), matrix_map1))
matrix_map1 = list(map(lambda x: x.replace(",", ""), matrix_map1))
matrix_map1 = list(map(lambda x: x.replace("\n", ""), matrix_map1))
matrix_map1 = list(map(lambda x: list(x), matrix_map1))
print(matrix_map2[1])
matrix_map2 = list(map(lambda x: str(x), matrix_map2))
matrix_map2 = list(map(lambda x: x.replace(" ", ""), matrix_map2))
matrix_map2 = list(map(lambda x: x.replace(",", ""), matrix_map2))
matrix_map2 = list(map(lambda x: x.replace("\n", ""), matrix_map2))
matrix_map2 = list(map(lambda x: list(x), matrix_map2))

# карта в таком формате будет
for i in range(len(matrix_map1)):
    matrix_map1[i] = matrix_map1[i] + labirynth[i] + matrix_map2[i]

with open(F'TEST.txt', 'w') as f:
    for i in matrix_map1:
        #print(i)
        f.write(str(i)+"\n")
WORLD_WIDTH = len(matrix_map1[0]) * TILE
WORLD_HEIGHT = len(matrix_map1) * TILE
world_map = {}# здесь инфа о стенах хранится
collision_walls = []
for j, row in enumerate(matrix_map1):# здесь инфа о стенах добавляется
    for i, char in enumerate(row):
        if char != "_":
            char = int(char)
            collision_walls.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
            if char:
                world_map[(i * TILE, j * TILE)] = char
            
            
