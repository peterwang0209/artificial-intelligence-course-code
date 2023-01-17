import copy
import random
import time
import statistics
import math
import numpy as np

FLAG = True
steps = []


# this function use to transfer a signle list into
# nested list, make it easy to check collision number
def transformer(pre_board):
    # initialize a 8*8 board filled with zero
    board = [[0 for i in range(8)] for j in range(8)]
    for i in range(8):
        board[pre_board[i]][i] = 1
    return board


def heuristic(board, cache):
    # h means the number of collision between queens
    h = 0
    # visited is used to store the queen who already get attacked,
    # the queen who get attack by a specific queen will not get attack
    # again.
    weight = 0
    visited = []
    for i in range(8):
        x_1, y_1 = cache["q" + str(i)]
        for j in range(i + 1, 8):
            x_2, y_2 = cache["q" + str(j)]
            if x_2 == x_1:
                weight += 1
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
            if x_2 - x_1 == j - i or x_2 - x_1 == i - j:
                weight += 1
    return h // 2, 28 - weight


def backtrace(board, cache):
    # print the matrix
    m = np.zeros((8, 8), dtype=int)
    for i in range(len(board)):
        row, column = cache["q" + str(i)]
        row, column = int(row), int(column)
        m[row][column] = 1
    return m


def random_adjust(board):
    temp = copy.deepcopy(board)
    random_row = random.randrange(0, 8)
    random_col = random.randrange(0, 8)
    temp["q" + str(random_col)] = [random_row, random_col]
    return temp


def simulated_annealing(board, cache, temperature, min_temperature, annealing_rate, local_round):
    # check temp
    while temperature > min_temperature:
        for i in range(local_round):
            # get collision
            old_collision, old_weight = heuristic(transformer(board), cache)
            # ascent
            if old_weight == 28:
                # track the step
                steps.append(i)
                # print the result
                print(backtrace(board, cache))
                return True
            new_board = random_adjust(cache)
            new_collision, new_weight = heuristic(transformer(board), new_board)
            # compare
            if new_weight >= old_weight:
                cache = new_board
            else:
                # random move
                if random.random() < math.exp((new_weight - old_weight) / temperature):
                    cache = new_board
        temperature = temperature * annealing_rate


def main():
    initial_temperature = 100
    min_temperature = 0.001
    annealing_factor = 0.95
    local_round = 150
    max_round = 50000
    f = open("simulated_annealing_test_cases.txt", "w")
    total_number = 1000
    board = ""
    while total_number > 0:
        total_number -= 1
        for col in range(0, 7):
            board += str(random.randint(0, 7)) + ' '
        board += str(random.randint(0, 7)) + '\n'
    f.write(board)
    f.close()
    successCase = 0
    totalCase = 0
    success_case = 0
    startTime = time.monotonic()
    with open("simulated_annealing_test_cases.txt", "r") as filehandler:
        for line in filehandler:
            board = []
            for col in line.split():
                board.append(int(col))
    for j in range(max_round):
        # these are maximum chance i could give
        totalCase += 1
        cache = {}
        m = np.zeros((8, 8), dtype=int)
        for i in range(0, 8):
            temp = random.randrange(0, 8)
            m[temp, i] = 1
            cache["q" + str(i)] = [temp, i]
        # call the function
        if simulated_annealing(board, cache, initial_temperature, min_temperature, annealing_factor,
                               local_round):
            success_case += 1
            print("Success")
        else:
            print("Failed")
    endTime = time.monotonic()
    print("\nSteps: " + str(statistics.mean(steps)))
    print("Total time: " + str(endTime - startTime) + '\n')
    print("Total case number: " + str(totalCase) + ", Success case number: " + str(successCase) + '\n')
    print("Success rate: " + str(successCase / float(totalCase)) + '\n')


if __name__ == "__main__":
    main()
