# -*- coding: cp1252 -*-
import pygame, sys
from pygame.locals import *
import time

# ----------------------------------------------------------------------
# --------------------------DESCRIZIONE BREVE---------------------------
# ----------------------------------------------------------------------
# 
# Tutto il gioco si basa su una matrice 8x8 in cui ogni elemento
# e' una tripla (x,y,z):
# "x" rappresenta il colore della casella
# "y" rappresenta il giocatore. -1 per G2, 1 per G1, 0 per casella vuota
# "z" indica se la pedina è una dama (True) oppure no (False)
# 
# ----------------------------------------------------------------------
# ----------------------INIZIO FUNZIONI "LOGICHE"-----------------------
# ----------------------------------------------------------------------

# crea scacchiera
def crea_sc():
    mat = []
    x = 0
    dama = False
    col_num = row_num = 8

    for row_i in range(row_num):
        row = []
        x = 1 - x
        for i in range(col_num):
            x = 1 - x

            if (0 <= row_i <= 2) and (x == 0):
                pezzo = 1  # giocatore 1
            elif 5 <= row_i <= 7 and x == 0:
                pezzo = -1  # giocatore 2
            else:
                pezzo = 0  # casella vuota

            row.append([x, pezzo, dama])
        mat.append(row)
    return mat

# funzione che restituisce, date le coordinate della pedina (x,y) e la matrice(scacchiera),
# una lista contenente tuple di coord matriciali di possibili mosse.
def validMoves(cell, mat):
    x = cell[0]
    y = cell[1]
    dama = mat[y][x][2]
    validMoves = []

    if 0 <= x <= 7:
        if mat[y][x][1] == 0:
            return []

        player = mat[y][x][1]

        # mosse da 1 casella
        if 0 <= y + 1 * player <= 7:
            if (0 <= x + 1 <= 7) and mat[y + 1 * player][x + 1][1] == 0:
                validMoves.append((x + 1, y + 1 * player))
            if (0 <= x - 1 <= 7) and mat[y + 1 * player][x - 1][1] == 0:
                validMoves.append((x - 1, y + 1 * player))

        # mosse da 2 caselle
        if 0 <= y + 2 * player <= 7:
            if (0 <= x + 2 <= 7) and mat[y + 2 * player][x + 2][1] == 0  and mat[y + 1 * player][x + 1][
                                                                             1] == -1 * player:
                validMoves.append((x + 2, y + 2 * player))
            if (0 <= x - 2 <= 7) and mat[y + 2 * player][x - 2][1] == 0  and mat[y + 1 * player][x - 1][
                                                                             1] == -1 * player:
                validMoves.append((x - 2, y + 2 * player))

        if dama:  # aggiungo le altre mosse (copio quelle dell'altro player...)

            player *= -1

            if 0 <= y + 1 * player <= 7:
                if (0 <= x + 1 <= 7) and mat[y + 1 * player][x + 1][1] == 0:
                    validMoves.append((x + 1, y + 1 * player))
                if (0 <= x - 1 <= 7) and mat[y + 1 * player][x - 1][1] == 0:
                    validMoves.append((x - 1, y + 1 * player))

            if 0 <= y + 2 * player <= 7:
                if (0 <= x + 2 <= 7) and mat[y + 2 * player][x + 2][1] == 0  and mat[y + 1 * player][x + 1][
                                                                                 1] == 1 * player:  # qua
                    validMoves.append((x + 2, y + 2 * player))
                if (0 <= x - 2 <= 7) and mat[y + 2 * player][x - 2][1] == 0  and mat[y + 1 * player][x - 1][
                                                                                 1] == 1 * player:  # e qua non va
                # messo (ovviamente) -1*player ma
                # 1*player,
                # in quanto e' gia stato invertito
                # il segno
                    validMoves.append((x - 2, y + 2 * player))

        else:
            pass

    return validMoves

# Riceve una tupla di coordinate (x,y) e ritorna Falso/Vero in base al turno
def isClickable(cell):
    global turn
    if scacc[cell[1]][cell[0]][1] == turn:
        return True
    else:
        return False

# Trasforma una pedina in dama se raggiunge "l'altra sponda". Se è già una dama lascia invariato
def isDama(cell):
    player = scacc[cell[1]][cell[0]][1]
    dama = scacc[cell[1]][cell[0]][2]
    if dama:
        return True
    else:
        if player == 1 and cell[1] == 7:
            return True
        elif player == -1 and cell[1] == 0:
            return True
        else:
            return False

# Riceve due tuple di coordinate matriciali e sposta la pedina. Nel caso cancella anche la pedina mangiata
def move(startCell, endCell):
    global turn, pieces
    player = scacc[startCell[1]][startCell[0]][1]

    if endCell in validMoves(startCell, scacc):
        if abs(startCell[1] - endCell[1]) > 1 or abs(startCell[0] - endCell[0]) > 1:  # ovvero mossa di presa
            delCell = [abs((startCell[0] + endCell[0]) // 2),
                       abs((startCell[1] + endCell[1]) // 2)]  # calcolo cella presa
            scacc[delCell[1]][delCell[0]][1], scacc[delCell[1]][delCell[0]][
                                              2] = 0, False  # rimozione pedina della cella presa
            pieces[-player] -= 1  # calcolo pedina mangiata

        scacc[endCell[1]][endCell[0]][1] = scacc[startCell[1]][startCell[0]][1]
        scacc[endCell[1]][endCell[0]][2] = scacc[startCell[1]][startCell[0]][
                                           2]  # "copia" la pedina nella cella di destinazione
        scacc[startCell[1]][startCell[0]][1], scacc[startCell[1]][startCell[0]][
                                              2] = 0, False  # toglie la pedina dalla cella di partenza

        turn *= -1
    else:
        pass

    scacc[endCell[1]][endCell[0]][2] = isDama(endCell)
    showTurn()
    drawScacc(scacc)
    checkScore(pieces)

# ritorna una tupla (x,y) di coordinate matriciali. Inoltre gestisce la "memoria" dei click
def selectedCell():
    click = tuple(x // 50 for x in pygame.mouse.get_pos())
    if len(clickMem) <= 1:
        clickMem.append(click)
    elif len(clickMem) == 2:
        clickMem.pop(0)
        clickMem.append(click)
    return click

# Prende in input il dizionario pieces e controlla che ci siano le condizioni di vittoria o meno
def checkScore(pieces):
    if pieces[1] == 0:
        showWin(-1)
    elif pieces[-1] == 0:
        showWin(1)

# ----------------------------------------------------------------------
# ------------------------FINE FUNZIONI "LOGICHE"-----------------------
# ----------------------------------------------------------------------
# ------------------------INIZIO FUNZIONI "PYGAME"----------------------
# ----------------------------------------------------------------------

# disegna la scacchiera partendo dalla matrice (scacc)
def drawScacc(scacc):
    square = pygame.Rect(0, 0, 50, 50)
    for row in scacc:
        for element in row:
            sq_color = GRAY if element[0] == 1 else MAROON
            ped_color = WHITE if element[1] == 1 else BLACK if element[1] == -1 else False
            pygame.draw.rect(mainW, sq_color, square)
            if ped_color:
                pygame.draw.circle(mainW, ped_color, (square.centerx, square.centery), 20, 0)
                if element[2]:
                    dama = font_dama.render("D", True, RED)
                    dama_rect = dama.get_rect()
                    dama_rect.topleft = (square.centerx - 2.5, square.centery - 2.5)
                    mainW.blit(dama, dama_rect)
            square.left += 50
        square.top += 50
        square.left = 0
    square.top = 0
    pygame.display.update()

# Riceve una tupla (x,y) e disegna un puntino verde sulle caselle su cui e' possibile spostare la pedina selezionata
# (tramite la tupla).
def showValidCell(cell):
    for move in validMoves(cell, scacc):
        x = move[0] * 50 + 25
        y = move[1] * 50 + 25
        pygame.draw.circle(mainW, GREEN, (x, y), 10)
    pygame.display.update()

# Riceve una tupla di coord matriciali (cella selezionata) e disegna un cerchietto blu attorno al pezzo
def showSelected(cell):
    center_x = cell[0] * 50 + 25
    center_y = cell[1] * 50 + 25
    if scacc[cell[1]][cell[0]][1]:
        center_x = cell[0] * 50 + 25
        center_y = cell[1] * 50 + 25
        pygame.draw.circle(mainW, BLUE, (center_x, center_y), 21, 3)

    pygame.display.update()


def showTurn():
    msg = "Turno bianco" if turn == 1 else "Turno nero"
    text = font.render(str(msg), True, WHITE, BLUE)
    text_rect = text.get_rect()
    text_rect.topleft = (8 * 50 + 15, 25)
    pygame.draw.rect(mainW, BLACK, (text_rect.left, text_rect.top, text_rect.width + 100, text_rect.height))
    mainW.blit(text, text_rect)


def showWin(player):
    winner = "bianchi" if player == 1 else "neri"
    msg = "I " + winner + " hanno vinto! Bye!"
    font = pygame.font.SysFont(None, 50)
    text = font.render(msg, True, RED, BLACK)
    rect = pygame.rect.Rect(0, height / 2 - 50, 50 * 8, 50)
    pygame.draw.rect(mainW, BLACK, rect)
    mainW.blit(text, rect)
    pygame.display.update()

    time.sleep(3)
    pygame.quit()
    sys.exit()

# ----------------------------------------------------------------------
# ----------------------FINE FUNZIONI "PYGAME"--------------------------
# ----------------------------------------------------------------------

pygame.init()

# colori...ma va??
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAROON = (152, 76, 0)
GRAY = (180, 180, 180)

clickMem = []  # tiene in memoria i click dell'utente
turn = 1  # turno del giocatore
pieces = {1: 12, -1: 12}  # sarebbe da sostituire con una funzione che li calcoli man mano...

font = pygame.font.SysFont(None, 32)  # font generale usato
font_dama = pygame.font.SysFont(None, 20)  # font della "D" che appare sulle Dame

width, height = 50 * 8 + 225, 50 * 8
mainW = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("Dama")

# crea la matrice iniziale
scacc = crea_sc()

# disegna-scacchiera
drawScacc(scacc)
# mostra a video una stringa "Turno bianco" o "Turno nero"
showTurn()

pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if 0 < pygame.mouse.get_pos()[
                   0] < 50 * 8:  # evita spiacevoli effetti collaterali (list of index nella matrice)

                if event.button == 1:
                    drawScacc(scacc)
                    cell = selectedCell()

                    if scacc[cell[1]][cell[0]][1] != 0:  # ovvero cella in cui è presente una pedina

                        if isClickable(cell) == 1:
                            showValidCell(cell)
                            showSelected(cell)

                    elif scacc[cell[1]][cell[0]][1] == 0 and isClickable(
                        clickMem[0]):  # ovvero cella vuota (possibile mossa) AND precedente click "buono".
                        if len(clickMem) == 2:
                            move(clickMem[0], clickMem[1])

                    else:
                        pass
