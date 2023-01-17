import random
import time
import statistics

FLAG = True
steps = []


def transformer(pre_board):
    # initialize a 8*8 board filled with zero
    board = [[0 for i in range(8)] for j in range(8)]
    for i in range(8):
        board[pre_board[i]][i] = 1
    return board


def heuristic(board):
    # h means the number of collision between queens
    h = 0
    # visited is used to store the queen who already get attacked,
    # the queen who get attack by a specific queen will not get attack
    # again.
    visited = []
    for i in range(8):
        for j in range(8):
            if board[i][j]:

                # horizontal
                for k in range(8):
                    if board[i][k] == 1 and k != j and (i, j, i, k) not in visited:
                        visited.append((i, j, i, k))
                        h += 1

                # vertical
                for k in range(8):
                    if board[k][j] == 1 and k != i and (i, j, i, k) not in visited:
                        visited.append((i, j, i, k))
                        h += 1

                # upper-left diagonal
                n = i - 1
                m = j - 1
                while n >= 0 and m >= 0:
                    if board[n][m] == 1 and (i, j, n, m) not in visited:
                        visited.append((i, j, i, k))
                        h += 1
                    n, m = n - 1, m - 1

                # upper-right diagonal
                n = i - 1
                m = j + 1
                while n >= 0 and m < 8:
                    if board[n][m] == 1 and (i, j, n, m) not in visited:
                        visited.append((i, j, i, k))
                        h += 1
                    n, m = n - 1, m + 1

                # lower-left diagonal
                n = i + 1
                m = j - 1
                while n < 8 and m >= 0:
                    if board[n][m] == 1 and (i, j, n, m) not in visited:
                        visited.append((i, j, i, k))
                        h += 1
                    n, m = n + 1, m - 1

                # lower-right diagonal
                n = i + 1
                m = j + 1
                while n < 8 and m < 8:
                    if board[n][m] == 1 and (i, j, n, m) not in visited:
                        visited.append((i, j, i, k))
                        h += 1
                    n, m = n + 1, m + 1
    # 28 is the worst case when 8 queen laying together
    # doing this subtraction, we could see the higher the value is
    # the better the result can be
    return 28 - h // 2


# for each column, calculate the collision number
# if the queen is moved to the other rows
# find the smallest one and move to it.
def step_steepestHillClimbing(board):
    visited = {}
    current_collision = heuristic(transformer(board))
    # expand the matrix, get the row and column
    for column in range(len(board)):
        for row in range(len(board)):
            # if the coordinate has queen, continue
            if board[column] == row:
                continue
            original_row = board[column]
            board[column] = row
            visited[(row, column)] = heuristic(transformer(board))
            # return to the original form
            # we want to measure all possible move so we move, document then go back to
            # the original form
            board[column] = original_row

    for coordinate, collision in visited.items():
        # ascent means if the collision number bigger, then it is better
        if collision > current_collision:
            # this will guarantte the best result
            current_collision = collision

    # welcome to the winner pool, every best choice will be here
    winner_pool = []
    for coordinate, collision in visited.items():
        if collision == current_collision:
            winner_pool.append(coordinate)

    if len(winner_pool) == 0:
        # reach to the peateu
        global FLAG
        FLAG = True
        return board

    # shuffle the pool, pick the lucky one
    random.shuffle(winner_pool)
    board[winner_pool[0][1]] = winner_pool[0][0]
    return board


def steepest_helper(board):
    maxRound = 100
    count = 0
    while True:
        collisionNum = heuristic(transformer(board))
        # becuase this is ascent, so when collision is 0, the output should be 28-0
        if collisionNum == 28:
            # update the average step
            steps.append(count)
            return board
        board = step_steepestHillClimbing(board)
        count += 1
        if count >= maxRound:
            global FLAG
            FLAG = True
            return board


def main():
    f = open("steepest_test_cases.txt", "w")
    total_number = 1000
    board = ""
    while total_number > 0:
        total_number -= 1
        for col in range(0, 7):
            board += str(random.randint(0, 7)) + ' '
        board += str(random.randint(0, 7)) + '\n'
    f.write(board)
    f.close()
    startTime = time.monotonic()
    successCase = 0
    totalCase = 0
    with open("steepest_test_cases.txt", "r") as filehandler:
        for line in filehandler:
            global FLAG
            FLAG = False
            totalCase += 1
            board = []
            for col in line.split():
                board.append(int(col))
            board = steepest_helper(board)
            if FLAG:
                print("Failed")
            else:
                successCase += 1
                print(*transformer(board), sep='\n')

    endTime = time.monotonic()
    print("\nSteps: " + str(statistics.mean(steps)))
    print("Total time: " + str(endTime - startTime) + '\n')
    print("Total case number: " + str(totalCase) + ", Success case number: " + str(successCase) + '\n')
    print("Success rate: " + str(successCase / float(totalCase)) + '\n')


if __name__ == "__main__":
    main()
