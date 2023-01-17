import time
from queue import PriorityQueue


# Using pq take advantage on compareing multiple object
# because priority queue is implemented by heapq

# The Node class contain the current state, its parent, the operator
# the depth, the heuristic cost and the total final cost
class Node:
    def __init__(self, state, parent, operator, depth, cost, f_cost):
        self.state = state
        self.parent = parent
        self.operator = operator
        self.depth = depth
        self.cost = cost
        self.f_cost = f_cost

    # get method
    def get_state(self):
        return self.state

    def get_parent(self):
        return self.parent

    def get_operator(self):
        return self.operator

    def get_depth(self):
        return self.depth

    def get_cost(self):
        return self.cost

    def get_f_cost(self):
        return self.f_cost

    # set method
    def set_state(self, state):
        self.state = state

    def set_parent(self, parent):
        self.parent = parent

    def set_operator(self, operator):
        self.operator = operator

    def set_depth(self, depth):
        self.depth = depth

    def set_operator(self, operator):
        self.operator = operator

    def set_cost(self, cost):
        self.cost = cost

    def set_f_cost(self, f_cost):
        self.f_cost = f_cost

    # I need this for priority queue, comparator
    def __lt__(self, other):
        return self.f_cost < other.f_cost


# debug checking graph
def display_board(state):
    print("-------------")
    print("| %i | %i | %i |" % (state[0], state[1], state[2]))
    print("-------------")
    print("| %i | %i | %i |" % (state[3], state[4], state[5]))
    print("-------------")
    print("| %i | %i | %i |" % (state[6], state[7], state[8]))
    print("-------------")


# move up
def move_up(state):
    # retriving the position of the blank
    # blank is the one need to move
    new_state = state[:]
    blank_index = new_state.index(0)
    # check if blank is on the top row
    if blank_index not in [0, 1, 2]:
        temp = new_state[blank_index - 3]
        new_state[blank_index - 3] = new_state[blank_index]
        new_state[blank_index] = temp
        return new_state
    else:
        # can't move
        return None


# move down
def move_down(state):
    # retriving the position of the blank
    # blank is the one need to move
    new_state = state[:]
    blank_index = new_state.index(0)
    # check if blank is on the bottom row
    if blank_index not in [6, 7, 8]:
        temp = new_state[blank_index + 3]
        new_state[blank_index + 3] = new_state[blank_index]
        new_state[blank_index] = temp
        return new_state
    else:
        # can't move
        return None


# move right
def move_right(state):
    # retriving the position of the blank
    # blank is the one need to move
    new_state = state[:]
    blank_index = new_state.index(0)
    # check if blank is on the right most column
    if blank_index not in [2, 5, 8]:
        temp = new_state[blank_index + 1]
        new_state[blank_index + 1] = new_state[blank_index]
        new_state[blank_index] = temp
        return new_state
    else:
        # can't move
        return None


# move left
def move_left(state):
    # retriving the position of the blank
    # blank is the one need to move
    new_state = state[:]
    blank_index = new_state.index(0)
    # check if blank is on the left most column
    if blank_index not in [0, 3, 6]:
        temp = new_state[blank_index - 1]
        new_state[blank_index - 1] = new_state[blank_index]
        new_state[blank_index] = temp
        return new_state
    else:
        # can't move
        return None


# function to create node
def create_node(state, parent, operator, depth, cost, f_cost):
    return Node(state, parent, operator, depth, cost, f_cost)


# expand neighbor funtion
# take a node and expand to all four directions
# everytime it expand, the depth will increment
# it produce a list of actions
def generate_child(node):
    # retuen all possible move, and set the current node as their parent
    children = \
        [create_node(move_up(node.get_state()), node, "up", node.get_depth() + 1, node.get_cost(), node.get_f_cost()),
         create_node(move_down(node.get_state()), node, "down", node.get_depth() + 1, node.get_cost(),
                     node.get_f_cost()),
         create_node(move_left(node.get_state()), node, "left", node.get_depth() + 1, node.get_cost(),
                     node.get_f_cost()),
         create_node(move_right(node.get_state()), node, "right", node.get_depth() + 1, node.get_cost(),
                     node.get_f_cost())]
    offspring = [node for node in children if node.get_state() is not None]
    return offspring


# depth limit search
# I found it difficult to implement dls in recrusive function,
# thus I use the iterative method

def dls(start, goal, limit):
    frontier = [create_node(start, None, None, 0, 0, 0)]
    # set is great for checking if it contains certain element
    explored = set()
    while frontier:
        parent = frontier.pop()
        # set doesnt take list but it takes tuple
        explored.add(tuple(parent.state))
        if parent.state == goal:
            moves = []
            temp = parent
            while True:
                moves.insert(0, temp.get_operator())
                if temp.get_depth() <= 1:
                    break
                temp = temp.get_parent()
            return moves
        if parent.depth <= limit:
            for child in generate_child(parent):
                if tuple(child.state) not in explored:
                    frontier.append(child)
                    explored.add(tuple(child.state))


# Iterative Deepening
# inspired from the book
def ids(start, goal, depth_limit):
    for i in range(depth_limit):
        result = dls(start, goal, i)
        if result is not None:
            return result


# Heuristics
# calculating the difference between the current states and goal states
def num_wrong_tiles(state, goal):
    score = 0
    for i in range(len(state)):
        if state[i] != goal[i]:
            score = score + 1
    return score


# manhattan distance,
# use mod and div to find the column and row
def manhattan_distance(state, goal):
    # abs of b % 3 - g % 3 will get the column
    # abs of b // 3 - g // 3 will get the row
    # find them from two list and sum them up
    return sum(abs(b % 3 - g % 3) + abs(b // 3 - g // 3)
               for b, g in ((state.index(i), goal.index(i))
                            for i in range(1, 9)))


# A* search
# inspire by best first search provided by professor
def astar_wrong_tiles(start, goal):
    explore = set()
    first_node_h = num_wrong_tiles(start, goal)
    first_node = create_node(start, None, None, 0, first_node_h, first_node_h)
    frontier = PriorityQueue()
    # using () could make the queue take them as one object, and I could access them individually
    frontier.put((first_node.get_f_cost(), first_node))

    while not frontier.empty():
        node = frontier.get()
        parent = node[1]
        explore.add(tuple(parent.get_state()))
        # print the result
        if parent.get_state() == goal:
            moves = []
            temp = parent
            while True:
                moves.insert(0, temp.get_operator())
                if temp.get_depth() <= 1:
                    break
                temp = temp.get_parent()
            return moves

        children = generate_child(parent)
        for child in children:
            if tuple(child.get_state()) not in explore:
                child.set_cost(num_wrong_tiles(child.get_state(), goal))
                child.set_f_cost(child.get_depth() + child.get_cost())
                # when I put the object in, the comparator I set before will do the work
                # make sure the lowest value will come up front
                frontier.put((child.get_f_cost(), child))


def astar_manhattan(start, goal):
    explore = set()
    first_node_h = manhattan_distance(start, goal)
    first_node = create_node(start, None, None, 0, first_node_h, first_node_h)
    frontier = PriorityQueue()
    frontier.put((first_node.get_f_cost(), first_node))

    while not frontier.empty():
        node = frontier.get()
        parent = node[1]
        explore.add(tuple(parent.get_state()))
        if parent.get_state() == goal:
            moves = []
            temp = parent
            while True:
                moves.insert(0, temp.get_operator())
                if temp.get_depth() <= 1:
                    break
                temp = temp.get_parent()
            return moves

        children = generate_child(parent)
        for child in children:
            if tuple(child.get_state()) not in explore:
                child.set_cost(manhattan_distance(child.get_state(), goal))
                child.set_f_cost(child.get_depth() + child.get_cost())
                frontier.put((child.get_f_cost(), child))


# This is the main function, it will ask user for a input and algorithm to use.
def main():
    # The goal state is the state I want to achieve
    goal_state = [1, 2, 3, 8, 0, 4, 7, 6, 5]
    depth_limit = 40
    input_number = input("\nEnter the numbers : ")
    input_state = [int(x) for x in str(input_number)]
    print(input_state)

    # run the ids search
    ids_start = time.monotonic()
    result_ids = ids(input_state, goal_state, depth_limit)
    ids_end = time.monotonic()

    # run the astar with num_wrong_tiles as heuristic function
    aster_wrong_start = time.monotonic()
    result_astar_wrong_tiles = astar_wrong_tiles(input_state, goal_state)
    aster_wrong_end = time.monotonic()

    # run the astar with num_wrong_tiles as heuristic function
    aster_manhattan_start = time.monotonic()
    result_astar_manhattan = astar_manhattan(input_state, goal_state)
    aster_manhattan_end = time.monotonic()

    # ids output
    if result_ids is None:
        print("No solution found for ids_search")
    elif not result_ids:
        print("The start node is the goal for ids_search")
    else:
        print(result_ids)
        print(len(result_ids), "moves")
        print("the ids search use", ids_end - ids_start, "seconds")

    # astar wrong tiles output
    if result_astar_wrong_tiles is None:
        print("No solution found for result_astar_wrong_tiles")
    elif not result_astar_wrong_tiles:
        print("The start node is the goal for result_astar_wrong_tiles")
    else:
        print(result_astar_wrong_tiles)
        print(len(result_astar_wrong_tiles), "moves")
        print("the astar wrong tiles search use", aster_wrong_end - aster_wrong_start, "seconds")

    # astar manhattan output
    if result_astar_manhattan is None:
        print("No solution found for astar_manhattan")
    elif result_astar_manhattan is [None]:
        print("The start node is the goal for astar_manhattan")
    else:
        print(result_astar_manhattan)
        print(len(result_astar_manhattan), "moves")
        print("the astar manhattan search use", aster_manhattan_end - aster_manhattan_start, "seconds")


# Need this statement to make the python project run
if __name__ == "__main__":
    main()
