import math


def find_fewest_zeros_layer(data, width, height):
    min_layer = 0
    min_zeros = math.inf
    ones_on_min_layer = 0
    twos_on_min_layer = 0
    pixels_per_layer = width*height
    for i in range(len(data)//pixels_per_layer):
        zeros = 0
        ones = 0
        twos = 0
        for j in range(pixels_per_layer):
            pixel = data[i*pixels_per_layer+j]
            if pixel == '0':
                zeros += 1
            elif pixel == '1':
                ones += 1
            elif pixel == '2':
                twos += 1
        if zeros < min_zeros:
            min_zeros = zeros
            min_layer = i
            ones_on_min_layer = ones
            twos_on_min_layer = twos
    return (min_layer, min_zeros, ones_on_min_layer, twos_on_min_layer)


def flatten_image(data, width, height):
    pixels_per_layer = width*height
    flat_image = []
    for i in range(height):
        flat_image.append([])
    for i in range(pixels_per_layer):
        j = 0
        while data[j*pixels_per_layer+i] == '2':
            j += 1
        pixel = data[j*pixels_per_layer+i]
        if pixel == '0':
            pixel = ' '
        elif pixel == '1':
            pixel = '#'
        flat_image[i//width].append(pixel)
    return flat_image


def print_flat_image(image):
    for line in image:
        print("".join(line))


data = "0222112222120000"
(layer, zeros, ones, twos) = find_fewest_zeros_layer(data, 2, 2)
# print(ones*twos)

flat_image = flatten_image(data, 2, 2)
print_flat_image(flat_image)
