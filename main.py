from src.navigation import Navigator


def main():
    nav = Navigator()

    print("=" * 50)
    print("  RUPP Campus 1 - Smart Building Navigation System")
    print("=" * 50)

    print("\nCampus Hierarchy:")
    print(nav.show_campus_hierarchy())

    print("\nFind Room A101:", nav.find_room("A101"))
    print("Find Building B:", nav.find_building("B"))

    path, cost = nav.shortest_path("A101", "B103")
    if path:
        print(f"\nShortest path from A101 to B103: {' -> '.join(path)} (distance: {cost})")
    else:
        print("\nNo path found from A101 to B103")


if __name__ == "__main__":
    main()
