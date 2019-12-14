import math
from functools import cmp_to_key


def cross_product_magnitude(p, q):
    return p[0]*q[1] - p[1]*q[0]


def subtract_vectors(p, q):
    return (q[0]-p[0], q[1]-p[1])


def pseudo_distance(p, q):
    return (q[0]-p[0])**2 + (q[1]-p[1])**2


def on_segment(p, q, r):
    return (min(q[0], r[0]) <= p[0] <= max(q[0], r[0])) and (min(q[1], r[1]) <= p[1] <= max(q[1], r[1]))


def find_best_asteroid(asteroids):
    best_range = -1
    best = (-1, -1)
    for p in asteroids:
        num_of_reachable = 0
        for q in asteroids:
            is_colinear_with_any = False
            for r in asteroids:
                if ((p != q and q != r and p != r) and
                    cross_product_magnitude(subtract_vectors(p, q), subtract_vectors(p, r)) == 0 and
                        (not on_segment(p, q, r)) and
                        (pseudo_distance(p, q) > pseudo_distance(p, r))):
                    is_colinear_with_any = True
                    break
            if not is_colinear_with_any and p != q:
                num_of_reachable += 1
        if num_of_reachable > best_range:
            best_range = num_of_reachable
            best = p
    return (best, best_range)


def sort_by_angle(asteroids, reference_point):
    # moves vectors to a new coordinate system where reference_point is a center
    # and rotates them by 90 deg counterclockwise
    def prepare_vectors(x, y):
        _x = subtract_vectors(reference_point, x)
        _y = subtract_vectors(reference_point, y)
        return ((-_x[1], _x[0]), (-_y[1], _y[0]))

    def compare_vectors(x, y):
        (_x, _y) = prepare_vectors(x, y)
        if _x[1] == 0 and _x[0] > 0:
            return 1
        elif _y[1] == 0 and _y[0] > 0:
            return -1
        elif _x[1] > 0 and _y[1] < 0:
            return 1
        elif _x[1] < 0 and _y[1] > 0:
            return -1
        cpm = cross_product_magnitude(_x, _y)
        if cpm != 0:
            return cpm
        return pseudo_distance(reference_point, y) - pseudo_distance(reference_point, x)

    return sorted(asteroids, key=cmp_to_key(compare_vectors))


def find_nth_removed(asteroids, reference_point, n):
    _asteroids = sort_by_angle(asteroids, reference_point)
    i = 1
    j = 0
    while i < n:
        if j == len(_asteroids):
            j = 0
        el = _asteroids[len(_asteroids) - 1 - j]
        while cross_product_magnitude(subtract_vectors(reference_point, _asteroids[len(_asteroids) - 2 - j]), subtract_vectors(reference_point, _asteroids[len(_asteroids) - 1 - j])) == 0 and j != (len(_asteroids)-1):
            j += 1
        _asteroids.remove(el)
        i += 1
    return _asteroids[len(_asteroids) - 1 - j]


locations = """#.#................#..............#......#......
.......##..#..#....#.#.....##...#.........#.#...
.#...............#....#.##......................
......#..####.........#....#.......#..#.....#...
.....#............#......#................#.#...
....##...#.#.#.#.............#..#.#.......#.....
..#.#.........#....#..#.#.........####..........
....#...#.#...####..#..#..#.....#...............
.............#......#..........#...........#....
......#.#.........#...............#.............
..#......#..#.....##...##.....#....#.#......#...
...#.......##.........#.#..#......#........#.#..
#.............#..........#....#.#.....#.........
#......#.#................#.......#..#.#........
#..#.#.....#.....###..#.................#..#....
...............................#..........#.....
###.#.....#.....#.............#.......#....#....
.#.....#.........#.....#....#...................
........#....................#..#...............
.....#...#.##......#............#......#.....#..
..#..#..............#..#..#.##........#.........
..#.#...#.......#....##...#........#...#.#....#.
.....#.#..####...........#.##....#....#......#..
.....#..#..##...............................#...
.#....#..#......#.#............#........##...#..
.......#.....................#..#....#.....#....
#......#..###...........#.#....#......#.........
..............#..#.#...#.......#..#.#...#......#
.......#...........#.....#...#.............#.#..
..##..##.............#........#........#........
......#.............##..#.........#...#.#.#.....
#........#.........#...#.....#................#.
...#.#...........#.....#.........#......##......
..#..#...........#..........#...................
.........#..#.......................#.#.........
......#.#.#.....#...........#...............#...
......#.##...........#....#............#........
#...........##.#.#........##...........##.......
......#....#..#.......#.....#.#.......#.##......
.#....#......#..............#.......#...........
......##.#..........#..................#........
......##.##...#..#........#............#........
..#.....#.................###...#.....###.#..#..
....##...............#....#..................#..
.....#................#.#.#.......#..........#..
#........................#.##..........#....##..
.#.........#.#.#...#...#....#........#..#.......
...#..#.#......................#...............#"""

locations = list(map(list, locations.splitlines()))
asteroids = []

for i in range(len(locations)):
    for j in range(len(locations[i])):
        if locations[i][j] == '#':
            asteroids.append((j, i))

best = find_best_asteroid(asteroids)[0]
asteroids.remove(best)
print(find_nth_removed(asteroids, best, 200))
