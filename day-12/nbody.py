import operator
from functools import reduce
import math


class Moon:
    def __init__(self, position, velocity=None):
        self.position = position
        if velocity is None:
            self.velocity = [0, 0, 0]
        else:
            self.velocity = velocity

    def update_position(self):
        self.position = list(
            map(operator.add, self.position, self.velocity))

    def calculate_energy(self):
        def e(source): return reduce(lambda acc, x: abs(x)+acc, source, 0)
        return e(self.position) * e(self.velocity)


def pair_update_velocity(m1, m2):
    for i in range(3):
        if(m1.position[i] > m2.position[i]):
            m1.velocity[i] -= 1
            m2.velocity[i] += 1
        elif(m1.position[i] < m2.position[i]):
            m1.velocity[i] += 1
            m2.velocity[i] -= 1


def all_update_velocity(moons):
    for i in range(len(moons)):
        for j in range(i+1, len(moons)):
            pair_update_velocity(moons[i], moons[j])


def simulate_step(moons):
    all_update_velocity(moons)
    for m in moons:
        m.update_position()


def calculate_total_energy(moons):
    return reduce(lambda acc, m: acc + m.calculate_energy(), moons, 0)


def find_period_for_one_coordinate(moons, i):
    j = 0
    start_p = list(map(lambda m: m.position[i], moons))
    start_v = list(map(lambda m: m.velocity[i], moons))
    while True:
        j += 1
        simulate_step(moons)
        is_start = True
        for l in range(len(moons)):
            if start_p[l] != moons[l].position[i] or start_v[l] != moons[l].velocity[i]:
                is_start = False
                break
        if is_start:
            return j


ms = [Moon([0, 6, 1]), Moon([4, 4, 19]), Moon([-11, 1, 8]), Moon([2, 19, 15])]

# PART 1
# for i in range(1000):
#     simulate_step(ms)
# print(calculate_total_energy(ms))

# PART 2
peroids = [find_period_for_one_coordinate(ms, i) for i in range(3)]
temp = peroids[0]
for i in range(1, len(peroids)):
    temp = (temp * peroids[i]) // math.gcd(temp, peroids[i])

print(temp)
