import math
import re

current_chemicals = {}


def find_minimum_needed_ORE(reactions, fuel=1):

    def go(doing, amount_needed):
        if doing == "ORE":
            return amount_needed
        will_produce = reactions[doing][0]
        needed = reactions[doing][1]
        ores = 0
        times = math.ceil(
            (amount_needed - current_chemicals[doing]) / will_produce)
        for ch in needed:
            if current_chemicals[ch[1]] >= (times * ch[0]):
                current_chemicals[ch[1]] -= (times * ch[0])
                continue
            else:
                ch_needed = (times * ch[0]) - current_chemicals[ch[1]]
                current_chemicals[ch[1]] = 0
            ores += go(ch[1], ch_needed)
        current_chemicals[doing] += (times * will_produce) - amount_needed
        return ores

    return go("FUEL", fuel)


lines = """157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT""".splitlines()
reactions = {}
for line in lines:
    splitted = line.split("=>")
    needed = re.findall("(\d+) (\w+)", splitted[0])
    will_produce = re.search("(\d+) (\w+)", splitted[1])
    reactions[will_produce[2]] = (
        int(will_produce[1]), [(int(x[0]), x[1]) for x in needed])

current_chemicals["ORE"] = 0
for r in reactions:
    current_chemicals[r] = 0

# minimum_ORE = find_minimum_needed_ORE(reactions, 1)

# # PART 1
# print(minimum_ORE)

# PART 2
ores = 1000000000000
l = 1
r = 100000000
while l + 1 < r:
    m = (l+r) // 2
    print(m)
    if(find_minimum_needed_ORE(reactions, m) < ores):
        l = m+1
    else:
        r = m

print(l-1)
