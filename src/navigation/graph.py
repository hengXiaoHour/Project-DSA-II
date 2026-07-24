import heapq
from collections import deque


class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_node(self, node):
        if node not in self.adjacency_list:
            self.adjacency_list[node] = {}

    def add_edge(self, node1, node2, weight=1):
        self.add_node(node1)
        self.add_node(node2)
        self.adjacency_list[node1][node2] = weight
        self.adjacency_list[node2][node1] = weight

    def get_neighbors(self, node):
        return list(self.adjacency_list.get(node, {}).items())

    def bfs(self, start, end):
        if start not in self.adjacency_list or end not in self.adjacency_list:
            return None, float('inf')

        queue = deque([(start, [start])])
        visited = {start}

        while queue:
            current, path = queue.popleft()
            if current == end:
                cost = sum(self.get_edge_weight(path[i], path[i+1]) for i in range(len(path)-1))
                return path, cost
            for neighbor in self.adjacency_list[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None, float('inf')

    def dfs(self, start, end):
        if start not in self.adjacency_list or end not in self.adjacency_list:
            return None, float('inf')

        stack = [(start, [start])]
        visited = set()

        while stack:
            current, path = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            if current == end:
                cost = sum(self.get_edge_weight(path[i], path[i+1]) for i in range(len(path)-1))
                return path, cost
            for neighbor in self.adjacency_list[current]:
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

        return None, float('inf')

    def get_edge_weight(self, node1, node2):
        return self.adjacency_list.get(node1, {}).get(node2, 0)

    def shortest_path(self, start, end):
        if start not in self.adjacency_list or end not in self.adjacency_list:
            return None, float('inf')

        pq = [(0, start, [start])]
        visited = set()

        while pq:
            cost, current, path = heapq.heappop(pq)
            if current in visited:
                continue
            visited.add(current)
            if current == end:
                return path, cost
            for neighbor, weight in self.get_neighbors(current):
                if neighbor not in visited:
                    heapq.heappush(pq, (cost + weight, neighbor, path + [neighbor]))

        return None, float('inf')

    def has_node(self, node):
        return node in self.adjacency_list

    def remove_node(self, node):
        if node in self.adjacency_list:
            for neighbor in self.adjacency_list[node]:
                self.adjacency_list[neighbor].pop(node, None)
            del self.adjacency_list[node]

    def remove_edge(self, node1, node2):
        self.adjacency_list.get(node1, {}).pop(node2, None)
        self.adjacency_list.get(node2, {}).pop(node1, None)

    def __len__(self):
        return len(self.adjacency_list)

    def __repr__(self):
        return f"Graph(nodes={list(self.adjacency_list.keys())})"
