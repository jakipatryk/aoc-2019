import math


class Obj:
    def __init__(self):
        self.orbiting_around = None
        self.orbiters = []


obj_map = {}


def create_map(list_of_pairs):
    for pair in list_of_pairs:
        obj, orbiter = pair.split(")")
        if not (obj in obj_map):
            obj_map[obj] = Obj()
        if not (orbiter in obj_map):
            obj_map[orbiter] = Obj()
        obj_map[obj].orbiters.append(orbiter)
        obj_map[orbiter].orbiting_around = obj


def count_orbits(start_obj, curr_len=0):
    level_sum = 0
    if len(start_obj.orbiters) == 0:
        return 0
    for orbiter in start_obj.orbiters:
        level_sum += count_orbits(obj_map[orbiter],
                                  curr_len + 1) + 1 + curr_len
    return level_sum


def calculate_shortest_path(start, dest):
    distance = {}
    q = [start]
    distance[start] = 0
    while len(q) > 0:
        current = q.pop(0)
        if dest in obj_map[current].orbiters:
            return distance[current]
        if obj_map[current].orbiting_around is not None and not obj_map[current].orbiting_around in distance:
            distance[obj_map[current].orbiting_around] = distance[current]+1
            q.append(obj_map[current].orbiting_around)
        for orbiter in obj_map[current].orbiters:
            if not orbiter in distance:
                distance[orbiter] = distance[current]+1
                q.append(orbiter)


mp = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN""".split("\n")
create_map(mp)
# print(count_orbits(obj_map["COM"]))
print(calculate_shortest_path(obj_map["YOU"].orbiting_around, "SAN"))
