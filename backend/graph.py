"""
Graph Layer — Navigation System
================================
Represents RUPP Campus 1 as a weighted undirected graph using an adjacency list.
Implements Dijkstra's Shortest Path Algorithm for finding optimal routes.
"""

import heapq


class Graph:
    """
    A weighted undirected graph using adjacency list representation.

    Attributes:
        vertices (dict): Adjacency list where each key is a vertex (str)
                         and value is a list of (neighbor, weight) tuples.
    """

    def __init__(self):
        """Initialise an empty graph."""
        self.vertices = {}

    def add_vertex(self, name):
        """Add a vertex to the graph if it does not already exist."""
        if name not in self.vertices:
            self.vertices[name] = []

    def add_edge(self, u, v, weight):
        """
        Add an undirected weighted edge between vertices u and v.
        Vertices are created automatically if they don't exist.
        """
        self.add_vertex(u)
        self.add_vertex(v)
        # Since the graph is undirected, add both directions.
        self.vertices[u].append((v, weight))
        self.vertices[v].append((u, weight))

    def dijkstra(self, start, end):
        """
        Find the shortest path between start and end using Dijkstra's algorithm.

        Args:
            start (str): Starting vertex name.
            end (str): Destination vertex name.

        Returns:
            tuple: (path list, total distance) or (None, float('inf')) if no path exists.

        Complexity:
            O((V + E) log V) where V = number of vertices, E = number of edges.
            Using a binary heap (priority queue) for efficient minimum extraction.
        """
        # Priority queue entries are (distance, vertex)
        pq = [(0, start)]
        # distances stores the shortest known distance to each vertex
        distances = {vertex: float('inf') for vertex in self.vertices}
        distances[start] = 0
        # predecessors stores the previous vertex on the shortest path
        predecessors = {vertex: None for vertex in self.vertices}

        while pq:
            current_distance, current_vertex = heapq.heappop(pq)

            # Skip if we've already found a better path to this vertex
            if current_distance > distances[current_vertex]:
                continue

            # Early exit: we've reached the destination
            if current_vertex == end:
                break

            # Explore neighbours
            for neighbour, weight in self.vertices[current_vertex]:
                distance = current_distance + weight
                if distance < distances[neighbour]:
                    distances[neighbour] = distance
                    predecessors[neighbour] = current_vertex
                    heapq.heappush(pq, (distance, neighbour))

        # Reconstruct the path from predecessors
        path = []
        current = end
        if distances[end] == float('inf'):
            # No path exists
            return None, float('inf')

        while current is not None:
            path.append(current)
            current = predecessors[current]
        path.reverse()

        return path, distances[end]

    def display_adjacency_list(self):
        """Print the adjacency list of the graph in a readable format."""
        print("\n=== CAMPUS GRAPH — ADJACENCY LIST ===\n")
        for vertex in sorted(self.vertices.keys()):
            print(f" {vertex}")
            for neighbour, weight in sorted(self.vertices[vertex], key=lambda x: x[0]):
                print(f"  -> {neighbour} ({weight})")
            print()

    @staticmethod
    def build_campus_graph():
        """
        Factory method: builds the RUPP Campus 1 graph with predefined vertices and edges.

        Returns:
            Graph: A fully constructed campus graph.
        """
        g = Graph()

        # Define all vertices explicitly (though add_edge handles this)
        buildings = [
            "Entrance", "Building A", "Building B", "Building C", "Building D",
            "Building Stem", "Building T", "Library", "NICC", "CKCC",
            "Study Office", "Canteen"
        ]
        for b in buildings:
            g.add_vertex(b)

        # Weighted undirected edges as specified
        g.add_edge("Entrance", "Building A", 90)
        g.add_edge("Building A", "Library", 60)
        g.add_edge("Building A", "Building Stem", 230)
        g.add_edge("Library", "NICC", 60)
        g.add_edge("Library", "CKCC", 100)
        g.add_edge("Library", "Building D", 240)
        g.add_edge("Library", "Building Stem", 240)
        g.add_edge("NICC", "CKCC", 80)
        g.add_edge("Building D", "CKCC", 64)
        g.add_edge("Building B", "Building D", 50)
        g.add_edge("Building B", "Building Stem", 50)
        g.add_edge("Building D", "Building Stem", 50)
        g.add_edge("Study Office", "Building Stem", 85)
        g.add_edge("Study Office", "Canteen", 60)
        g.add_edge("Building C", "Building T", 40)
        g.add_edge("Building C", "Canteen", 90)
        g.add_edge("Building T", "Canteen", 90)

        return g


# ----- Demonstration when run directly -----
if __name__ == "__main__":
    campus = Graph.build_campus_graph()
    campus.display_adjacency_list()

    # Test Case 1
    path, dist = campus.dijkstra("Library", "Building Stem")
    print(f"Library -> Building Stem: {path} (Distance = {dist})")

    # Test Case 2
    path, dist = campus.dijkstra("Entrance", "Building T")
    print(f"Entrance -> Building T: {path} (Distance = {dist})")

    # Test Case 3
    path, dist = campus.dijkstra("Building B", "Library")
    print(f"Building B -> Library: {path} (Distance = {dist})")

    # Test Case 4
    path, dist = campus.dijkstra("Entrance", "Building Stem")
    print(f"Entrance -> Building Stem: {path} (Distance = {dist})")