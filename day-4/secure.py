def is_good(password):
    sequence = []
    current = password
    for i in range(6):
        sequence.insert(0, current % 10)
        current = current // 10
    was_two_consecutive = False
    many_in_row = False
    for i in range(1, 6):
        if sequence[i] < sequence[i-1]:
            return False
        if sequence[i] == sequence[i-1] and not many_in_row:
            if i+1 >= 6 or (i+1 < 6 and sequence[i+1] != sequence[i]):
                was_two_consecutive = True
                many_in_row = False
            else:
                many_in_row = True
        elif sequence[i] != sequence[i-1]:
            many_in_row = False
    return was_two_consecutive


def count_num_of_possible_passwords(start, end):
    sum = 0
    for i in range(start, end+1):
        if is_good(i):
            sum += 1
    return sum


print(count_num_of_possible_passwords(265275, 781584))
