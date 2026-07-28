"""
Hash Table Layer — Information System
======================================
Uses a Python dictionary as a hash table to store building information.
Provides O(1) average-case lookup for searching building details by name.
"""


class BuildingInfo:
    """
    Stores metadata about a single campus building.

    Attributes:
        name (str): Building name.
        category (str): Category (e.g. Academic, Service, Administration, etc.).
        description (str): Brief description of the building.
        services (list): List of services / facilities available.
    """

    def __init__(self, name, category, description, services):
        self.name = name
        self.category = category
        self.description = description
        self.services = services if isinstance(services, list) else [services]

    def __str__(self):
        """Return a formatted string of the building information."""
        svc = ", ".join(self.services) if self.services else "None"
        return (
            f"{'=' * 50}\n"
            f"  Building    : {self.name}\n"
            f"  Category    : {self.category}\n"
            f"  Description : {self.description}\n"
            f"  Services    : {svc}\n"
            f"{'=' * 50}"
        )


class BuildingHashTable:
    """
    Hash table (dictionary) mapping building names to BuildingInfo objects.

    Why a dictionary?
    -----------------
    Python's dict is implemented as a hash table with O(1) average
    lookup, insert, and delete. The key (building name) is hashed
    to determine the bucket where the value is stored.

    This simulates a real hash table with:
      - Hash function  : Python's built-in hash() on the string key
      - Collision      : handled internally by CPython (open addressing /
                          quadratic probing in modern CPython)

    Attributes:
        table (dict): The underlying dictionary acting as the hash table.
    """

    def __init__(self):
        """Initialise the hash table and populate with campus data."""
        self.table = {}
        self._populate()

    def _populate(self):
        """Insert all building information into the hash table."""
        data = [
            BuildingInfo("Building A", "Academic", "Teaching building with classrooms and lecture rooms",
                         ["Classes", "Lectures"]),
            BuildingInfo("Building B", "Academic", "Academic building for teaching activities",
                         ["Classes"]),
            BuildingInfo("Building C", "Academic", "Academic building",
                         ["Classes"]),
            BuildingInfo("Building D", "Academic", "Academic building close to CKCC",
                         ["Classes", "Lecture Rooms"]),
            BuildingInfo("Building Stem", "Academic", "Science, Technology, Engineering Building",
                         ["Faculty Offices", "Labs", "Classrooms", "Events"]),
            BuildingInfo("Building T", "Academic", "Teaching building",
                         ["Classes"]),
            BuildingInfo("Library", "Service", "University library and student study area",
                         ["Books", "Reading Area", "Research"]),
            BuildingInfo("NICC", "Service", "Academic cooperation and conference center",
                         ["Training", "Events", "Programs"]),
            BuildingInfo("CKCC", "Academic", "Academic international cooperation center for international programs",
                         ["Cultural Exchange", "Education", "Training"]),
            BuildingInfo("Study Office", "Administration","Student academic support office",
                         ["Student Services", "Academic Records"]),
            BuildingInfo("Canteen", "Service", "Food court and dining area",
                         ["Food", "Drinks", "Rest Area"]),
            BuildingInfo("Entrance", "Access Point", "Main campus entrance",
                         ["Campus Access"]),
        ]
        for info in data:
            self.insert(info)

    def insert(self, info):
        """
        Insert a BuildingInfo object into the hash table.

        Stores the key in lowercase for case-insensitive lookups.
        The original name is preserved inside the BuildingInfo object.

        Time complexity: O(1) average.
        """
        self.table[info.name.lower()] = info

    def search(self, name):
        """
        Look up a building by name.

        Time complexity: O(1) average — direct hash table lookup.

        Args:
            name (str): Building name (case-insensitive).

        Returns:
            BuildingInfo or None: The building info if found, else None.
        """
        # Normalise to lowercase for case-insensitive O(1) lookup
        key = name.strip().lower()
        return self.table.get(key, None)

    def get_all_buildings(self):
        """Return a list of all BuildingInfo objects in the table."""
        return list(self.table.values())

    def display_all(self):
        """Print all building information entries."""
        print("\n=== ALL BUILDING INFORMATION ===\n")
        for info in self.get_all_buildings():
            print(info)


# ----- Demonstration when run directly -----
if __name__ == "__main__":
    ht = BuildingHashTable()

    # Search example
    result = ht.search("Library")
    if result:
        print(result)
    else:
        print("Building not found.")

    # Demonstrate O(1) lookup
    print("\n--- Quick lookups (O(1) each) ---")
    for name in ["Building A", "Canteen", "STEM"]:  # "STEM" should miss
        info = ht.search(name)
        if info:
            print(f"  Found: {info.name}")
        else:
            print(f"  NOT FOUND: {name}")
