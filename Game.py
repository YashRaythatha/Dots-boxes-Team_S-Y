# This Game is developed by Saurabh and Yash
import pygame
import os
import constants
import DBNode
import DotsAndBoxes
import MCTS
import copy

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

WIDTH = 800
HEIGHT = 600
GAME_WIDTH = 500
GAME_HEIGHT = 500
DOT_RADIUS = 10
DOT_SPACING = 100
DOT_CENTER_HEIGHT = 300
DOT_CENTER_WIDTH = 400

# you can adjust the power of AI to think from 0 to 2
# On the basis of BRAIN_POWER value our AI will explore more depth in tree and it will cause AI more powerfull
# suggested BRAIN_POWER value for
# beginner mode = 0.1
# Intermidiate mode = 0.4
# Hard mode = 1.0
# Pro mode = 2.0
BRAIN_POWER = 0.1


def endGame(board):
    print("Game Over!")
    print("AI Score:", board.P1Score)
    print("Human Score", board.P2Score)
    if board.P1Score > board.P2Score:
        print("AI Won!")
    else:
        print("Human Won!")
    quit()


def setup(screen):
    pygame.display.set_caption("Dots and Boxes Using MCTS")
    font = pygame.font.Font(constants.title, 40)
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (WIDTH/2 - GAME_WIDTH/2 + 10,
                                     HEIGHT/2 - GAME_HEIGHT/2, GAME_WIDTH, GAME_HEIGHT))
    pygame.draw.rect(screen, WHITE, (WIDTH/2 - GAME_WIDTH/2 + 15,
                                     HEIGHT/2 - GAME_HEIGHT/2 + 5, GAME_WIDTH - 10, GAME_HEIGHT - 10))
    text = font.render('Dots and Boxes', True, BLACK, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH/2, 20)
    screen.blit(text, text_rect)

    font = pygame.font.Font(constants.title, 25)
    text = font.render('Player: 0', True, BLACK, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH-49, 10)
    screen.blit(text, text_rect)

    text = font.render('AI: 0', True, BLACK, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH-70, 40)
    screen.blit(text, text_rect)

    text = font.render('Playing Now: ', True, BLACK, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (100, 10)
    screen.blit(text, text_rect)

    text = font.render('AI', True, BLACK, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (100, 40)
    screen.blit(text, text_rect)

    pygame.display.update()

    rows = 4
    cols = 4

    if (rows % 2 != 0 and cols % 2 != 0):
        for i in range(-(rows-rows//2)+1, rows-rows//2):
            for j in range(-(cols-cols//2)+1, cols-cols//2):
                pygame.draw.circle(screen, BLACK, (DOT_CENTER_WIDTH + (i*DOT_SPACING),
                                                   DOT_CENTER_HEIGHT + (j*DOT_SPACING)), DOT_RADIUS)

    if (rows % 2 == 0 and cols % 2 == 0):
        for i in range(-(rows-rows//2), rows-rows//2):
            for j in range(-(cols-cols//2), cols-cols//2):
                pygame.draw.circle(screen, BLACK, (DOT_CENTER_WIDTH + ((2*i+1)*DOT_SPACING//2),
                                                   DOT_CENTER_HEIGHT + ((2*j+1)*DOT_SPACING//2)), DOT_RADIUS)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    setup(screen)
    running = True

    tempGame = DotsAndBoxes.DotsAndBoxes()
    currentId = 0
    root = DBNode.DBNode(tempGame, currentId, -1, (-1, 0, 0))
    currentId += 1
    tree = dict()
    tree[root.id] = root

    playing = True
    row_borders = copy.deepcopy(tempGame.rows)
    col_borders = copy.deepcopy(tempGame.cols)
    boxes = copy.deepcopy(tempGame.boxes)

    for i in range(len(row_borders)):
        for j in range(len(row_borders[i])):
            row_borders[i][j] = pygame.Rect(
                (260+j*DOT_SPACING, 145+i*DOT_SPACING, DOT_SPACING - 2*DOT_RADIUS, DOT_RADIUS))

    for i in range(len(col_borders)):
        for j in range(len(col_borders[i])):
            col_borders[i][j] = pygame.Rect(
                (245+i*DOT_SPACING, 160+j*DOT_SPACING, DOT_RADIUS, DOT_SPACING - 2*DOT_RADIUS))

    for i in range(len(boxes)):
        for j in range(len(boxes[i])):
            boxes[i][j] = pygame.Rect(
                (250+i*DOT_SPACING, 150+j*DOT_SPACING, 100, 100))

    pygame.display.update()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

        if not tempGame.player:
            pos = None
            move = None

            while move == None:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()

                        for i in range(len(row_borders)):
                            for j in range(len(row_borders[i])):
                                if row_borders[i][j].collidepoint(pos):
                                    move = (0, i, j)
                                    pygame.draw.rect(
                                        screen, BLUE, row_borders[i][j])
                                    pygame.display.update()

                        for i in range(len(col_borders)):
                            for j in range(len(col_borders[i])):
                                if col_borders[i][j].collidepoint(pos):
                                    move = (1, i, j)
                                    pygame.draw.rect(
                                        screen, BLUE, col_borders[i][j])
                                    pygame.display.update()

                        if move:
                            if tempGame.addLine(*move):
                                nextNode = root.id
                                foundNextNode = False
                                for node in root.children:
                                    if tree[node].newMove == move:
                                        nextNode = node
                                        foundNextNode = True

                                if not foundNextNode:
                                    newNode = DBNode.DBNode(
                                        tempGame, currentId, -1, move)
                                    newNode.board.addLine(*move)
                                    nextNode = newNode.id
                                    currentId += 1
                                    tree[newNode.id] = newNode

                                root = tree[nextNode]
        else:
            # determine how many rollouts should be done based on depth into game
            if len(root.board.moves) < 12:
                rollouts = 13000
            elif len(root.board.moves) < 16:
                rollouts = 11000
            elif len(root.board.moves) < 22:
                rollouts = 8000
            else:
                rollouts = 3500
            # modify the number of rollouts by the power given by the user
            rollouts *= BRAIN_POWER
            nextComputerId, currentId = MCTS.MCTS(
                tree, currentId, root.id, rollouts)
            root = tree[nextComputerId]

        tempGame = root.board

        if tempGame.checkEnd():
            endGame(tempGame)

        (direction, i, j) = root.newMove
        if direction == 0:
            pygame.draw.rect(
                screen, RED if tempGame.player else BLUE, row_borders[i][j])
        else:
            pygame.draw.rect(
                screen, RED if tempGame.player else BLUE, col_borders[i][j])

        for i in range(len(tempGame.boxes)):
            for j in range(len(tempGame.boxes[i])):
                if tempGame.boxes[j][i]:
                    pygame.draw.rect(screen, WHITE, boxes[i][j])
                    font = pygame.font.Font(constants.title, 20)
                    text = font.render(
                        'AI' if tempGame.boxesOwners[j][i] == 1 else 'P', True, BLACK, WHITE)
                    text_rect = text.get_rect()
                    text_rect.center = (
                        250 + i * DOT_SPACING + 50, 150 + j * DOT_SPACING + 50)
                    screen.blit(text, text_rect)

        font = pygame.font.Font(constants.title, 25)
        text = font.render('Player: %d' % tempGame.P2Score, True, BLACK, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH-47, 10)
        screen.blit(text, text_rect)

        text = font.render('AI: %d' %
                           tempGame.P1Score, True, BLACK, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH-70, 40)
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, WHITE, (0, 0, 200, 50))
        text = font.render('Playing Now: ', True, BLACK, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (100, 10)
        screen.blit(text, text_rect)

        if tempGame.player:
            text = font.render('AI', True, BLACK, WHITE)
        else:
            text = font.render('Player', True, BLACK, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (100, 40)
        screen.blit(text, text_rect)

        pygame.display.update()


if __name__ == "__main__":
    main()
