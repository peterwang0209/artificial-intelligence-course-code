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

    return h // 2


def first_choice(board):
    old_collision = heuristic(transformer(board))
    maxRound = 200  # the expected number to find a better choice
    count = 0
    while True:
        count += 1
        if count >= maxRound:
            # if count is bigger, then we change the global variable to True
            # it will trigger the fail for the report.txt
            global FLAG
            FLAG = True
            return board
        random_row = random.randint(0, len(board) - 1)
        random_col = random.randint(0, len(board) - 1)
        # if these two numbers are the same as current location
        if board[random_col] == random_row:
            # exit and continuou generate another pair of location
            continue
        origin_row = board[random_col]
        board[random_col] = random_row
        # if the new find board heuristic number is smaller than the previous collision number
        # then we return this result as the first choice result
        if heuristic(transformer(board)) <= old_collision:
            # break from here, and return the board
            return board
        # keep going
        board[random_col] = origin_row


def first_choice_helper(board):
    # the expected number to find a solution
    max_choice = 200
    choice_count = 0
    while True:
        collisionNum = heuristic(transformer(board))
        # if the number is zero, then we get the result
        if collisionNum == 0:
            steps.append(choice_count)
            return board
        # call the function
        board = first_choice(board)
        # recall the global variable
        global FLAG
        # if FLAG is true, then we give up
        if FLAG:
            return board
        choice_count += 1
        # if the count is exceeding the maxRound then we give up too
        if choice_count >= max_choice:
            FLAG = True
            return board


def main():
    f = open("first_choice_test_cases.txt", "w")
    total_number = 1000
    board = ""
    while total_number > 0:
        total_number -= 1
        for col in range(0, 7):
            # append the test case to the file
            board += str(random.randint(0, 7)) + ' '
        board += str(random.randint(0, 7)) + '\n'
    f.write(board)
    f.close()
    startTime = time.monotonic()
    successCase = 0
    totalCase = 0
    with open("first_choice_test_cases.txt", "r") as filehandler:
        for line in filehandler:
            global FLAG
            FLAG = False
            totalCase += 1
            board = []
            for col in line.split():
                board.append(int(col))
            board = first_choice_helper(board)
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
