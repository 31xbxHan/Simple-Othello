import pygame


pygame.init()
screen = pygame.display.set_mode((600, 600))
# board init
board = [[0 for i in range(8)] for i in range(8)]
board[3][4] = 1
board[4][3] = 1
board[4][4] = 2
board[3][3] = 2

# 8 directions
directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

# other
player = 1
color = ["#000000", "#FFFFFF"]
running = True

# function
def update_map(row, col):
    global player
    if isValid(row, col):
        board[col][row] = player
        flip_pieces()
        print(board)
        player = 2 if player == 1 else 1

    else:
        print("not available")
        return

def isOnTheBoard(row, col):
    """
    Detects if the coordinate point is on the board

    """
    if (0 <= row < 8) and (0 <= col < 8):
        return True
    else:
        return False

def isValid(row, col):
    """
    Check if placing a piece at the specified position (row, col) is a valid move.
    """
    global toFlip
    if board[col][row] != 0:
        return False

    toFlip = []
    for dr, dc in directions:
        check_row, check_col = row + dr, col + dc
        flipped = False
        temp_flip = []  # 用于暂时记录当前方向上的反转坐标
        while isOnTheBoard(check_row, check_col):
            if board[check_col][check_row] == 0:
                break
            elif board[check_col][check_row] == player:
                if flipped:
                    # 达到自己的棋的位置，记录反转坐标
                    toFlip.extend(temp_flip)
                    break  # 修改此处，使其继续检测其他方向
                else:
                    # 和自己的棋相邻
                    break
            else:
                # 对方的棋子，标记为可以翻转
                temp_flip.append([check_row, check_col])
                flipped = True
            check_row += dr
            check_col += dc
    else:
        return len(toFlip) > 0  # 如果 toFlip 不为空，则返回 True，否则返回 False



def flip_pieces():
    """
    flip the pieces
    """
    for (row, col) in toFlip:
        value = board[col][row]
        board[col][row] = 2 if value == 1 else 1


def getScoreOfBoard():
    """
    Get the number of pieces on the board for both black and white
    """
    player1 = 0
    player2 = 0
    for row in range(8):
        for col in range(8):
            if board[col][row] == 1:
                player1 += 1
            elif board[col][row] == 2:
                player2 += 1
            else:
                continue
    return player1, player2

def getAllValidMove():
    move = []
    for row in range(8):
        for col in range(8):
            if isValid(row, col):
                move.append([row, col])
    return move

def over():
    global board
    global player
    global valid_move
    player1, player2 = getScoreOfBoard()
    if player1 > player2:
        print("player1 win!")
    else:
        print("player2 win!")
    board = [[0 for i in range(8)] for i in range(8)]
    board[3][4] = 1
    board[4][3] = 1
    board[4][4] = 2
    board[3][3] = 2
    player = 1
    valid_move = getAllValidMove()

# main
valid_move = getAllValidMove()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            row = round((x - 55) / 70)
            col = round((y - 55) / 70)
            update_map(row, col)
            valid_move = getAllValidMove()
        font  = pygame.font.SysFont("Arial", 18)

    screen.fill("#89BF9B")

    # Draw the board
    for i in range(15):
        pygame.draw.line(screen, "#000000", [20 + 70 * i, 20], [20 + 70 * i, 580])
        pygame.draw.line(screen, "#000000", [20, 20 + 70 * i], [580, 20 + 70 * i])
    pygame.draw.circle(screen, "#000000", [300, 300], 4)

    # Show pending box
    x, y = pygame.mouse.get_pos()
    x = round((x - 55) / 70) * 70 + 55
    y = round((y - 55) / 70) * 70 + 55
    if (x > 0 and x < 600) and (y > 0 and y < 600):
        pygame.draw.circle(screen, color[player - 1], [x, y], 20)

    # update map
    for row in range(8):
        for col in range(8):
            if board[col][row] == 0:
                continue
            else:
                pygame.draw.circle(screen, color[board[col][row] - 1], [row * 70 + 55, col * 70 + 55], 20)

    # show all move
    no_valid_moves_count = 0
    no_valid_moves_player = 0
    if len(valid_move)>0:
        for (row, col) in valid_move:
            pygame.draw.circle(screen, color[player-1], [row * 70 + 55, col * 70 + 55], 20, 2)
    else:
        if (no_valid_moves_player != player):
            no_valid_moves_count += 1
            no_valid_moves_player = player
        player = 2 if player == 1 else 1
        if no_valid_moves_count >= 2:
            no_valid_moves_count = 0
            no_valid_moves_player = 0
            over()


    # update scores
    player1, player2 = getScoreOfBoard()
    if player1 + player2 == 64 or player1 ==0 or player2 == 0:
        over()
    txtsurf = font.render(str(player1)+':'+str(player2), True, color[1])
    screen.blit(txtsurf, (290, 0))


    pygame.display.update()

pygame.quit()



start_prompt = "一步合法的棋步包括：在一个空格新落下一个棋子，并且翻转对手一个或多个棋子。新落下的棋子与棋盘上已有的同色棋子间，对方被夹住的所有棋子都要翻转过来。可以是横着夹，竖着夹，或是斜着夹。夹住的位置上必须全部是对手的棋子，不能有空格。一步棋可以在数个方向上翻棋，任何被夹住的棋子都必须被翻转过来，棋手无权选择不去翻某个棋子。除非至少翻转了对手的一个棋子，否则就不能落子。如果一方没有合法棋步，也就是说不管他下到哪里，都不能至少翻转对手的一个棋子，那他这一轮只能弃权，而由他的对手继续落子直到他有合法棋步可下。如果一方至少有一步合法棋步可下，他就必须落子，不得弃权。棋局持续下去，直到棋盘填满或者双方都无合法棋步可下。"
