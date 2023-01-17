import copy
import random
import math

WHITE = 1
BLACK = -1
EMPTY = 0
SIZE = 8
SKIP = "SKIP"


# random player class

class RandomPlayer:
    def __init__(self, mycolor):
        self.color = mycolor

    def get_color(self):
        return self.color

    def make_move(self, state):
        curr_move = None
        legals = actions(state)
        while curr_move is None:
            display(state)
            if self.color == 1:
                print("White ", end='')
            else:
                print("Black ", end='')
            print(" to play.")
            print("Legal moves are " + str(legals))
            # random pick a move
            curr_move = random.choice(legals)
            return curr_move


# minimax player

class MinimaxPlayer:

    def __init__(self, color, max_depth=math.inf):
        self.color = color
        self.max_depth = max_depth

    def get_color(self):
        return self.color

    # adapt to the play function
    def make_move(self, state):
        return self.minimax(state, self.max_depth)

    # here is the utility function
    def utility(self, state, player_color):
        # early_weights matrix will have greater portion
        early_weights = [
            [5, -4, 2, 2, 2, 2, -4, 5],
            [-4, -5, -1, -1, -1, -1, -5, -4],
            [2, -1, 1, 0, 0, 1, -1, 2],
            [2, -1, 0, 1, 1, 0, -1, 2],
            [2, -1, 0, 1, 1, 0, -1, 2],
            [2, -1, 1, 0, 0, 1, -1, 2],
            [-4, -5, -1, -1, -1, -1, -5, -4],
            [5, -4, 2, 2, 2, 2, -4, 5]
        ]
        # this will count the piece of each player
        late_weights = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1]
        ]

        op_color = -player_color
        e_score, l_score = 0, 0
        empty = 0.0
        # for loop to count
        for i in range(8):
            for j in range(8):
                if player_color == state.board_array[i][j]:
                    e_score += early_weights[i][j]
                    l_score += late_weights[i][j]
                elif op_color == state.board_array[i][j]:
                    e_score -= early_weights[i][j]
                    l_score -= late_weights[i][j]
                else:
                    empty += 1
        # hash the value
        return (e_score * ((64.0 - empty) / 64.0)) + (l_score * (empty / 64.0)) + len(actions(state)) * (empty / 64.0)

    def minimax(self, state, max_depth):
        def max_value(state, depth):
            action = None
            if depth >= self.max_depth or terminal_test(state):
                return action, self.utility(state, self.color)
            value = -math.inf
            for action in actions(state):
                resulting_state = result(state, action)
                value = max(value, min_value(resulting_state, depth + 1)[1])
            return action, value

        def min_value(state, depth):
            action = None
            if depth >= self.max_depth or terminal_test(state):
                return action, self.utility(state, self.color)
            value = math.inf
            for action in actions(state):
                resulting_state = result(state, action)
                value = min(value, max_value(resulting_state, depth + 1)[1])
            return action, value
        # display the result for each term
        display(state)
        if self.color == 1:
            print("White ", end='')
        else:
            print("Black ", end='')
        print(" to play.")
        return max_value(state, 0)[0]


# alpha beta
class AlphabetaPlayer:

    def __init__(self, color, max_depth=math.inf):
        self.color = color
        self.max_depth = max_depth

    def get_color(self):
        return self.color

    def make_move(self, state):
        return self.alphabeta(state, self.max_depth)

    def utility(self, state, player_color):

        early_weights = [
            [5, -4, 2, 2, 2, 2, -4, 5],
            [-4, -5, -1, -1, -1, -1, -5, -4],
            [2, -1, 1, 0, 0, 1, -1, 2],
            [2, -1, 0, 1, 1, 0, -1, 2],
            [2, -1, 0, 1, 1, 0, -1, 2],
            [2, -1, 1, 0, 0, 1, -1, 2],
            [-4, -5, -1, -1, -1, -1, -5, -4],
            [5, -4, 2, 2, 2, 2, -4, 5]
        ]

        late_weights = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1]
        ]

        op_color = -player_color
        e_score, l_score = 0, 0
        piece = 0
        empty = 0.0

        for i in range(8):
            for j in range(8):
                if player_color == state.board_array[i][j]:
                    e_score += early_weights[i][j]
                    l_score += late_weights[i][j]
                elif op_color == state.board_array[i][j]:
                    e_score -= early_weights[i][j]
                    l_score -= late_weights[i][j]
                else:
                    empty += 1

        return e_score * ((64.0 - empty) / 64.0) + l_score * (empty / 64.0) + len(actions(state)) * (empty / 64.0)

    # implement alphabeta minimax, using the code from the book
    def alphabeta(self, state, max_depth):
        def max_value(state, alpha, beta, depth):
            action = None
            if depth >= self.max_depth or terminal_test(state):
                return action, self.utility(state, self.color)
            value = -math.inf
            for action in actions(state):
                resulting_state = result(state, action)
                value = max(value, min_value(resulting_state, alpha, beta, depth + 1)[1])
                if value >= beta:
                    return action, value
                alpha = max(alpha, value)
            return action, value

        def min_value(state, alpha, beta, depth):
            action = None
            if depth >= self.max_depth or terminal_test(state):
                return action, self.utility(state, self.color)
            value = math.inf
            for action in actions(state):
                resulting_state = result(state, action)
                value = min(value, max_value(resulting_state, alpha, beta, depth + 1)[1])
                if value <= alpha:
                    return action, value
                beta = min(beta, value)
            return action, value

        display(state)
        if self.color == 1:
            print("White ", end='')
        else:
            print("Black ", end='')
        print(" to play.")
        return max_value(state, -math.inf, math.inf, 0)[0]


class HumanPlayer:
    def __init__(self, mycolor):
        self.color = mycolor

    def get_color(self):
        return self.color

    def make_move(self, state):
        curr_move = None
        legals = actions(state)
        while curr_move is None:
            display(state)
            if self.color == 1:
                print("White ", end='')
            else:
                print("Black ", end='')
            print(" to play.")
            print("Legal moves are " + str(legals))
            move = input("Enter your move as a r,c pair:")
            if move == "":
                return legals[0]

            if move == SKIP and SKIP in legals:
                return move

            try:
                movetup = int(move.split(',')[0]), int(move.split(',')[1])
            except Exception:
                movetup = None
            if movetup in legals:
                curr_move = movetup
            else:
                print("That doesn't look like a legal action to me")
        return curr_move


class OthelloState:
    """A class to represent an othello game state"""

    def __init__(self, currentplayer, otherplayer, board_array=None, num_skips=0):
        if board_array is not None:
            self.board_array = board_array
        else:
            self.board_array = [[EMPTY] * SIZE for i in range(SIZE)]
            self.board_array[3][3] = WHITE
            self.board_array[4][4] = WHITE
            self.board_array[3][4] = BLACK
            self.board_array[4][3] = BLACK
        self.num_skips = num_skips
        self.current = currentplayer
        self.other = otherplayer


def player(state):
    return state.current


def actions(state):
    """Return a list of possible actions given the current state
    """
    legal_actions = []
    for i in range(SIZE):
        for j in range(SIZE):
            if result(state, (i, j)) is not None:
                legal_actions.append((i, j))
    if len(legal_actions) == 0:
        legal_actions.append(SKIP)
    return legal_actions


def result(state, action):
    """Returns the resulting state after taking the given action

    (This is the workhorse function for checking legal moves as well as making moves)

    If the given action is not legal, returns None

    """
    # first, special case! an action of SKIP is allowed if the current agent has no legal moves
    # in this case, we just skip to the other player's turn but keep the same board
    if action == SKIP:
        newstate = OthelloState(state.other, state.current, copy.deepcopy(state.board_array), state.num_skips + 1)
        return newstate

    if state.board_array[action[0]][action[1]] != EMPTY:
        return None

    color = state.current.get_color()
    # create new state with players swapped and a copy of the current board
    newstate = OthelloState(state.other, state.current, copy.deepcopy(state.board_array))

    newstate.board_array[action[0]][action[1]] = color

    flipped = False
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for d in directions:
        i = 1
        count = 0
        while i <= SIZE:
            x = action[0] + i * d[0]
            y = action[1] + i * d[1]
            if x < 0 or x >= SIZE or y < 0 or y >= SIZE:
                count = 0
                break
            elif newstate.board_array[x][y] == -1 * color:
                count += 1
            elif newstate.board_array[x][y] == color:
                break
            else:
                count = 0
                break
            i += 1

        if count > 0:
            flipped = True

        for i in range(count):
            x = action[0] + (i + 1) * d[0]
            y = action[1] + (i + 1) * d[1]
            newstate.board_array[x][y] = color

    if flipped:
        return newstate
    else:
        # if no pieces are flipped, it's not a legal move
        return None


def terminal_test(state):
    """Simple terminal test
    """
    # if both players have skipped
    if state.num_skips == 2:
        return True

    # if there are no empty spaces
    empty_count = 0
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board_array[i][j] == EMPTY:
                empty_count += 1
    if empty_count == 0:
        return True
    return False


def display(state):
    """Displays the current state in the terminal window
    """
    print('  ', end='')
    for i in range(SIZE):
        print(i, end='')
    print()
    for i in range(SIZE):
        print(i, '', end='')
        for j in range(SIZE):
            if state.board_array[j][i] == WHITE:
                print('W', end='')
            elif state.board_array[j][i] == BLACK:
                print('B', end='')
            else:
                print('-', end='')
        print()


def display_final(state):
    """Displays the score and declares a winner (or tie)
    """
    wcount = 0
    bcount = 0
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board_array[i][j] == WHITE:
                wcount += 1
            elif state.board_array[i][j] == BLACK:
                bcount += 1

    print("Black: " + str(bcount))
    print("White: " + str(wcount))
    if wcount > bcount:
        print("White wins")
    elif wcount < bcount:
        print("Black wins")
    else:
        print("Tie")


def play_game(p1=None, p2=None):
    """Plays a game with two players. By default, uses two humans
    """
    if p1 is None:
        p1 = RandomPlayer(BLACK)
    if p2 is None:
        p2 = AlphabetaPlayer(WHITE, 4)
        # p2 = RandomPlayer(WHITE)

    s = OthelloState(p1, p2)
    while True:
        action = p1.make_move(s)
        if action not in actions(s):
            print("Illegal move made by Black")
            print("White wins!")
            return
        s = result(s, action)
        if terminal_test(s):
            print("Game Over")
            display(s)
            display_final(s)
            return
        action = p2.make_move(s)
        list_action = actions(s)
        if action not in actions(s):
            print("Illegal move made by White")
            print("Black wins!")
            return
        s = result(s, action)
        if terminal_test(s):
            print("Game Over")
            display(s)
            display_final(s)
            return


def main():
    play_game()


if __name__ == '__main__':
    main()
