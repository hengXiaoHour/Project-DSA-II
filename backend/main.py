"""
Smart Building Mapping and Navigation System for RUPP Campus 1
==============================================================
Integrates three data structures:
  1. Graph          — Navigation layer (Dijkstra's shortest path)
  2. Hash Table     — Information layer (O(1) building lookup)
  3. Tree           — Categorization layer (hierarchical browsing)

Run this file to start the CLI menu-driven program.
"""

import sys
from graph import Graph
from hash_table import BuildingHashTable
from tree import CategoryTree


class CampusNavigationSystem:
    """
    Main application class that ties together the three data structure layers.
    Provides a CLI menu for user interaction.
    """

    def __init__(self):
        """Initialise all three data layers."""
        print("\nInitialising RUPP Campus Navigation System...")

        # Layer 1: Graph
        print("  [✓] Building campus graph (adjacency list)...")
        self.campus_graph = Graph.build_campus_graph()

        # Layer 2: Hash Table
        print("  [✓] Loading building information (hash table)...")
        self.building_info = BuildingHashTable()

        # Layer 3: Tree
        print("  [✓] Building category tree...")
        self.category_tree = CategoryTree()

        print("  System ready!\n")

    def search_building_info(self):
        """Menu option 1: Look up building information by name or number."""
        buildings = self.building_info.get_all_buildings()
        buildings.sort(key=lambda b: b.name)

        print("\n--- SEARCH BUILDING INFORMATION ---")
        print("  Select a building:\n")
        for i, b in enumerate(buildings, 1):
            print(f"  {i:>2}.  {b.name}")
        print()

        choice = input("  Enter number (1-{}) or type a name: ".format(len(buildings))).strip()
        if not choice:
            print("  No input entered.\n")
            return

        # Try number first
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(buildings):
                info = buildings[idx - 1]
                print(f"\n{info}\n")
                print("  [Hash Table] O(1) lookup complete.\n")
                return

        # Otherwise treat as a name search
        info = self.building_info.search(choice)
        if info:
            print(f"\n{info}\n")
            print("  [Hash Table] O(1) lookup complete.\n")
        else:
            print(f"\n  Building '{choice}' not found.\n")

    def browse_by_category(self):
        """Menu option 2: Browse buildings by category using the tree."""
        print("\n--- BROWSE BUILDINGS BY CATEGORY ---")
        self.category_tree.browse_by_category()
        print("  [Tree] Category browsing uses pre-order traversal.\n")

    def _select_building(self, prompt):
        """Show a numbered list and let the user pick by number or type a name."""
        buildings = sorted(self.campus_graph.vertices.keys())
        print(f"  {prompt}")
        print()
        for i, b in enumerate(buildings, 1):
            print(f"  {i:>2}.  {b}")
        print()
        choice = input("  Enter number (1-{}) or type a name: ".format(len(buildings))).strip()
        if not choice:
            return None
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(buildings):
                return buildings[idx - 1]
        # Normalise for case-insensitive match
        choice_lower = choice.strip().lower()
        for b in buildings:
            if b.lower() == choice_lower:
                return b
        return None

    def find_shortest_path(self):
        """Menu option 3: Find shortest path between two buildings using Dijkstra."""
        print("\n--- FIND SHORTEST PATH ---")
        start = self._select_building("Select starting building:")
        if start is None:
            print("  Invalid selection.\n")
            return
        end = self._select_building("Select destination building:")
        if end is None:
            print("  Invalid selection.\n")
            return

        path, distance = self.campus_graph.dijkstra(start, end)

        if path is None:
            print(f"  No path found between '{start}' and '{end}'.\n")
            return

        print(f"\n  Shortest route from {start} to {end}:")
        print(f"  {'─' * 40}")
        for i, location in enumerate(path):
            arrow = "  → " if i > 0 else "    "
            print(f"{arrow}{location}")
        print(f"\n  Total Distance = {distance}")
        print(f"  [Graph] Dijkstra's algorithm computed this path in "
              f"O((V+E) log V) time.\n")

    def display_campus_graph(self):
        """Menu option 4: Show the full adjacency list of the campus graph."""
        self.campus_graph.display_adjacency_list()

    def show_menu(self):
        """Print the main menu options."""
        print("=" * 43)
        print("  SMART RUPP CAMPUS NAVIGATION SYSTEM")
        print("=" * 43)
        print("  1. Search Building Information")
        print("  2. Browse Buildings by Category")
        print("  3. Find Shortest Path")
        print("  4. Display Campus Graph")
        print("  5. Exit")
        print("=" * 43)

    def run(self):
        """Main program loop with the interactive CLI menu."""
        while True:
            self.show_menu()
            choice = input("  Enter your choice (1-5): ").strip()

            if choice == "1":
                self.search_building_info()
            elif choice == "2":
                self.browse_by_category()
            elif choice == "3":
                self.find_shortest_path()
            elif choice == "4":
                self.display_campus_graph()
            elif choice == "5":
                print("\n  Thank you for using the RUPP Campus Navigation System!")
                print("  Goodbye!\n")
                sys.exit(0)
            else:
                print(f"\n  Invalid choice '{choice}'. Please enter 1-5.\n")

            input("  Press Enter to continue...")


# ========================================
# Entry Point
# ========================================
if __name__ == "__main__":
    app = CampusNavigationSystem()
    app.run()
