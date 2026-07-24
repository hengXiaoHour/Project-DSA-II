class Room:
    def __init__(self, room_id, name, floor, room_type="classroom", capacity=0):
        self.room_id = room_id
        self.name = name
        self.floor = floor
        self.room_type = room_type
        self.capacity = capacity

    def __repr__(self):
        return f"Room({self.room_id}, {self.name})"


class Floor:
    def __init__(self, floor_id, name, level):
        self.floor_id = floor_id
        self.name = name
        self.level = level
        self.rooms = {}

    def add_room(self, room):
        self.rooms[room.room_id] = room

    def get_room(self, room_id):
        return self.rooms.get(room_id)

    def __repr__(self):
        return f"Floor({self.name}, level={self.level})"


class Building:
    def __init__(self, building_id, name, floors=None):
        self.building_id = building_id
        self.name = name
        self.floors = floors or {}

    def add_floor(self, floor):
        self.floors[floor.floor_id] = floor

    def get_floor(self, floor_id):
        return self.floors.get(floor_id)

    def __repr__(self):
        return f"Building({self.name})"
