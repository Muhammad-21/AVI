# Assumes that all parameters are numeric
def lerp(x1, f1, x2, f2, x):
    return (f1 * (x - x2) - f2 * (x - x1)) / (x1 - x2)


def rgb_color_lerp(x1, c1, x2, c2, x):
    r = int(lerp(x1, c1[0], x2, c2[0], x))
    g = int(lerp(x1, c1[1], x2, c2[1], x))
    b = int(lerp(x1, c1[2], x2, c2[2], x))

    return r, g, b


def euclidean_metric(array_of_pairs) -> float:
    result = 0

    for pair in array_of_pairs:
        result += pow(pair[0] - pair[1], 2)

    return pow(result, 0.5)

