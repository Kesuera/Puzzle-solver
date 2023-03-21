# Author: Samuel Hetteš, ID: 110968
# Subject: Artificial Intelligence
# Assignment: M x N Puzzle Solver using A* algorithm
# IDE: PyCharm 2021.2.3
# Programming language: Python 3.9
# Date: 20.10.2021

from timeit import default_timer as timer


# single node class
class Node:
    # constructor, table = M*N 2D array, parent = parent node, operator = action of parent node,
    # ending_positions = ending positions of values in a table, heuristic_to_use = which heuristic to be calculated
    def __init__(self, table, end_positions, heuristic_to_use, parent=None, operator=None):
        self.table = table
        self.parent = parent
        self.operator = operator
        if parent:  # not a root node -> depth = parents depth + 1
            self.depth = parent.depth + 1
        else:  # root node -> depth = 0
            self.depth = 0
        # combined heuristic calculation based on choice
        if heuristic_to_use == 1:
            self.heuristic = MisplacedHeuristic.misplaced_heuristic(table, end_positions) + self.depth
        elif heuristic_to_use == 2:
            self.heuristic = ManhattanHeuristic.manhattan_heuristic(table, end_positions) + self.depth
        else:
            self.heuristic = MisplacedHeuristic.misplaced_heuristic(table, end_positions) + self.depth +\
                             ManhattanHeuristic.manhattan_heuristic(table, end_positions)

    # function that recursively branches to the root node and returns the sequence of operators used
    def steps_sequence(self):
        node = self
        seq = []
        while node.parent:
            seq.append(node.operator)
            node = node.parent
        return reversed(seq)

    # method that calculates all the possible actions and returns them
    def possible_actions(self):
        actions = []
        # finding the position of space - '0'
        for y in range(len(self.table)):
            for x in range(len(self.table[0])):
                if self.table[y][x] == 0:
                    break
            else:
                continue
            break
        # checking all the possible actions
        if (x - 1) >= 0:
            actions.append(('R', x, y, x - 1, y))
        if (x + 1) < len(self.table[0]):
            actions.append(('L', x, y, x + 1, y))
        if (y - 1) >= 0:
            actions.append(('D', x, y, x, y - 1))
        if (y + 1) < len(self.table):
            actions.append(('U', x, y, x, y + 1))
        # returning actions as a list of tuples:
        # ('Operator', X, Y actual position of space, X, Y position of space after the operator is used)
        return actions

    # function that takes an action as an input and performs it on itself - creates a new table and returns it
    def perform_action(self, action):
        x_actual, y_actual, x_next, y_next = action[1], action[2], action[3], action[4]  # space position (at - to)
        new_table = [row[:] for row in self.table]  # deep copying the table
        new_table[y_actual][x_actual] = new_table[y_next][x_next]  # swapping value
        new_table[y_next][x_next] = 0  # swapping space
        return new_table


# class that solves the puzzle
class Solver:
    # constructor, start, end = M*N 2D starting/ending table array, heuristic = 1 (Misplaced Tiles), 2 (Manhattan)
    def __init__(self, start, end, heuristic):
        self.start_table = start
        self.end_table = end
        self.heuristic = heuristic
        self.end_positions = self.end_positions()  # ending positions of each number (indexes)

    # function to return ending positions of each number (indexes)
    def end_positions(self):
        end_positions = [None] * len(self.end_table) * len(self.end_table[0])
        for y in range(len(self.end_table)):
            for x in range(len(self.end_table[0])):
                end_positions[end_table[y][x]] = (x, y)  # index of array = number, tuple (x, y) = indexes
        return end_positions

    # function to check whether the table is solved
    def solved(self, table):
        if table == self.end_table:
            return 1
        else:
            return 0

    # function that perform the actual solving of a puzzle
    def solve(self, iter_limit, depth_limit):
        queue = []  # priority queue
        iterations = 0  # number of iterations - expanded nodes
        root = Node(self.start_table, self.end_positions, self.heuristic)  # root node
        queue.append(root)
        tables_set = set()  # set of unique tables created
        tables_set.add(tuple(map(tuple, root.table)))

        # branching
        while queue:
            # sorting the queue based on heuristic
            queue.sort(key=lambda x: x.heuristic)
            node = queue.pop(0)

            # checking whether the puzzle is solved -> returning the sequence of operators
            if self.solved(node.table):
                return node.steps_sequence(), node.depth, iterations

            # checking the limits
            if (iter_limit != 0) & (iter_limit == iterations):
                return None, None, iter_limit
            if (depth_limit != 0) & (depth_limit == node.depth):
                return None, depth_limit, None
            iterations += 1

            # performing all the possible actions and creating nodes
            for action in node.possible_actions():
                child = Node(node.perform_action(action), self.end_positions, self.heuristic, node, action[0])
                # checking whether the node created is unique -> pushing to queue and adding a new table to a set
                if tuple(map(tuple, child.table)) not in tables_set:
                    queue.append(child)
                    tables_set.add(tuple(map(tuple, child.table)))

        return None, None, None  # returning None if the solution was not found


# class to calculate the amount of misplaced tiles in a table - heuristic #1
class MisplacedHeuristic:
    # method takes a 2D array - table and ending positions as an input and returns the sum of misplaced tiles
    @staticmethod
    def misplaced_heuristic(table, end_positions):
        counter = 0
        for y in range(len(table)):
            for x in range(len(table[0])):
                x_final, y_final = end_positions[table[y][x]]
                # space not included, checking whether the indexes of a number match
                if (table[y][x] != 0) and (x_final != x or y_final != y):
                    counter += 1
        return counter


# class to calculate the Manhattan distance - heuristic #2
class ManhattanHeuristic:
    # takes a 2D array - table and ending positions as an input and returns the distance
    @staticmethod
    def manhattan_heuristic(table, end_positions):
        distance = 0
        for y in range(len(table)):
            for x in range(len(table[0])):
                if table[y][x] != 0:  # space not included
                    x_final, y_final = end_positions[table[y][x]]
                    distance += abs(x_final - x) + abs(y_final - y)
        return distance


print("*******************************")
print(">>>      PUZZLE SOLVER      <<<")
print("*******************************\n")
print("--- Heuristic configuration ---")
print("'1' - Misplaced tiles")
print("'2' - Manhattan")
print("'3' - Mix of both")
heuristic_choice = int(input("Enter the heuristic: "))  # heuristic choice input

print("\n--- Table configuration ---")
N = int(input("Enter the number of rows: "))  # number of rows input
M = int(input("Enter the number of columns: "))  # number of columns input

print("\n--- Starting table configuration ---")
print("Enter the entries separated by spaces ('0' for space):")
start_table, end_table = [], []
for i in range(N):  # starting table entries input
    print("Row #", i + 1, ":", sep='', end=' ')
    start_table.append(list(map(int, input().split())))

print("\n--- Ending table configuration ---")
print("Enter the entries separated by spaces ('0' for space):")
for i in range(N):  # ending table entries input
    print("Row #", i + 1, ":", sep='', end=' ')
    end_table.append(list(map(int, input().split())))

print("\n--- Solver limits configuration ---")
print("For no limit enter '0'")
iter_stop = int(input("Enter the iterations limit: "))  # iterations limit (number of expanded nodes) input
depth_stop = int(input("Enter the node depth limit: "))  # depth limit input

start_time = timer()  # starting time
solver = Solver(start_table, end_table, heuristic_choice)  # solver class initialization
sequence, depth, expanded_nodes = solver.solve(iter_stop, depth_stop)  # actual solving
end_time = timer()  # ending time

print("\n--- Summary ---")
if heuristic_choice == 1:
    print("Heuristic used: Misplaced tiles")
elif heuristic_choice == 2:
    print("Heuristic used: Manhattan")
else:
    print("Heuristic used: Mixed")
if sequence is None:  # no solution
    if (depth is not None) & (depth == depth_stop):
        print("Depth limit reached")
    if (expanded_nodes is not None) & (expanded_nodes == iter_stop):
        print("Iterations limit reached")
    print("Solution not found")
else:  # printing summary and solution
    print("Operators: L-Left, R-Right, U-Up, D-Down")
    print("Time taken:", round(end_time - start_time, 4), "sec")
    print("Depth:", depth)
    print("Expanded nodes:", expanded_nodes)
    print("Solution:", end=' ')
    steps = 0
    for op in sequence:
        steps += 1
        print(op, end=' ')
    print("\nNumber of steps:", steps)
