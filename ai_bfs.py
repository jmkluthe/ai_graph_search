#!/usr/bin/python3
from node_state import NodeState


class GraphSearch(object):

    def __init__(self, initial, goals, search_type):
        self.initial_state = initial
        self.goal_states = goals
        self.frontier = [initial]
        self.explored = []
        self.total_explored = 0
        if search_type == "bfs":
            self.solution_path = self.graph_search(0)
        elif search_type == "dfs":
            self.solution_path = self.graph_search(-1)
        elif search_type == "iddfs":
            self.solution_path = self.iddfs_search()
        elif search_type == "astar":
            self.solution_path = self.astar_search()

    def graph_search(self, pop):
        while len(self.frontier) > 0:
            self.total_explored += 1
            node = self.frontier.pop(pop)
            #print("node explored number {}".format(self.total_explored))
            #node.print_state()
            if self.has_state(node, self.goal_states):
                return self.solution(node)
            if not self.has_state(node, self.explored):
                self.explored.append(node)
            self.expand(node)

    def iddfs_search(self):
        for i in range(1000):
            self.frontier = [self.initial_state]
            self.explored = []
            attempt = self.dl_search(i)
            if attempt is not None and attempt is True:
                return attempt

    def dl_search(self, limit):
        while len(self.frontier) > 0:
            if limit == 0:
                return False
            self.total_explored += 1
            node = self.frontier.pop(-1)
            # print("node explored number {}".format(self.total_explored))
            # node.print_state()
            if self.has_state(node, self.goal_states):
                return self.solution(node)
            if not self.has_state(node, self.explored):
                self.explored.append(node)
            self.expand(node)
            limit -= 1

    def astar_search(self):
        while len(self.frontier) > 0:
            self.total_explored += 1
            self.frontier.sort(key=self.order_by_cost)
            node = self.frontier.pop(0)
            #print("node explored number {}".format(self.total_explored))
            #node.print_state()
            if self.has_state(node, self.goal_states):
                return self.solution(node)
            if not self.has_state(node, self.explored):
                self.explored.append(node)
            self.expand(node)

    def order_by_cost(self, node):
        min_cost = 0
        for i in range(3):
            min_cost += abs(node.left[i] - self.goal_states[0].left[i])
        for i in range(1, len(self.goal_states)):
            temp_cost = 0
            for j in range(3):
                temp_cost += abs(node.left[j] - self.goal_states[i].left[j])
            if temp_cost < min_cost:
                min_cost = temp_cost
        return min_cost

    def expand(self, node):
        children = node.get_children()
        for child in children:
            if not self.has_state(child, self.explored) and not self.has_state(child, self.frontier):
                self.frontier.append(child)

    def solution(self, node):
        solution = []
        while (node):
            solution.insert(0, node)
            node = node.parent
        return solution

    def has_state(self, test_node, node_list):
        for node in node_list:
            if test_node == node:
                return True
        return False


goal = NodeState(None, "goal3.txt")
start = NodeState(None, "start3.txt")
print("goal:")
goal.print_state()
print("start:")
start.print_state()
sol = GraphSearch(start, [goal], "astar")
print("length of solution: {}".format(len(sol.solution_path)))
i = 0
for node in sol.solution_path:
    print("state number {}".format(i))
    node.print_state()
    i += 1
print("Total explored: {}".format(sol.total_explored))

