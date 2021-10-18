from PIL import Image

from core.helpers.helpers import white_color_by_mode
from core.math.math import euclidean_metric
from core.verification.verification import verify_is_image_or_exception


# Assumes that image in '1' mode
def black_weight(image):
    verify_is_image_or_exception(image)

    result = 0

    for x in range(image.width):
        for y in range(image.height):
            result += image.getpixel((x, y))

    return result


# Assumes that image in '1' mode
def normalized_black_weight(image):
    verify_is_image_or_exception(image)

    return black_weight(image) / (image.width * image.height)


# Assumes that image in '1' mode
def gravity_center(image):
    verify_is_image_or_exception(image)

    x_coord = 0
    y_coord = 0

    for x in range(image.width):
        for y in range(image.height):
            pixel = image.getpixel((x, y))
            x_coord += x * pixel
            y_coord += y * pixel

    weight = black_weight(image)
    return int(round(x_coord / weight)), int(round(y_coord / weight))


# Assumes that image in '1' mode
def normalized_gravity_center(image):
    verify_is_image_or_exception(image)

    x, y = gravity_center(image)

    return (x - 1) / (image.width - 1), (y - 1) / (image.height - 1)


# Assumes that image in '1' mode
def central_horizontal_axial_moment(image):
    verify_is_image_or_exception(image)

    center = gravity_center(image)
    result = 0

    for x in range(image.width):
        for y in range(image.height):
            result += (y - center[1]) ** 2 * image.getpixel((x, y))

    return result


# Assumes that image in '1' mode
def normalized_central_horizontal_axial_moment(image):
    verify_is_image_or_exception(image)

    return central_horizontal_axial_moment(image) / (image.width ** 2 + image.height ** 2)


# Assumes that image in '1' mode
def central_vertical_axial_moment(image):
    verify_is_image_or_exception(image)

    center = gravity_center(image)
    result = 0

    for x in range(image.width):
        for y in range(image.height):
            result += (x - center[0]) ** 2 * image.getpixel((x, y))

    return result


# Assumes that image in '1' mode
def normalized_central_vertical_axial_moment(image):
    verify_is_image_or_exception(image)

    return central_vertical_axial_moment(image) / (image.width ** 2 + image.height ** 2)


# Assumes that image in '1' mode
def horizontal_projection(image):
    verify_is_image_or_exception(image)

    levels = []
    projections = []

    for y in range(image.height):
        y_projection = 0
        for x in range(image.width):
            y_projection += image.getpixel((x, y))

        levels.append(y)
        projections.append(y_projection)

    return levels, projections


# Assumes that image in '1' mode
def vertical_projection(image):
    verify_is_image_or_exception(image)

    levels = []
    projections = []

    for x in range(image.width):
        x_projection = 0
        for y in range(image.height):
            x_projection += image.getpixel((x, y))

        levels.append(x)
        projections.append(x_projection)

    return levels, projections


# Assumes that image in '1' mode
def inverted_vertical_projection(image):
    verify_is_image_or_exception(image)

    levels = []
    projections = []

    for x in range(image.width):
        x_projection = 0
        for y in range(image.height):
            x_projection += white_color_by_mode(image.mode) - image.getpixel((x, y))

        levels.append(x)
        projections.append(x_projection)

    return levels, projections


# Assumes that image is symbolic string and has 'L' mode
def symbol_segments(image: Image, diff_threshold: float):
    verify_is_image_or_exception(image)

    v_levels, v_projections = inverted_vertical_projection(image)
    max_v_projection = max(v_projections)
    min_v_projection = min(v_projections)

    diff = (max_v_projection - min_v_projection) * diff_threshold

    start = 0

    prev_v_projection = 0
    result = []

    for i in range(len(v_projections) - 1):
        if prev_v_projection - diff <= 0 < v_projections[i] - diff:
            start = i
        elif prev_v_projection - diff > 0 >= v_projections[i] - diff:
            result.append((start, i))
            start = -1

        prev_v_projection = v_projections[i]

    if start != -1:
        result.append((start, len(v_projections) - 1))

    return result


# Assumes that image_a and image_b has '1' mode:
def proximity_measure(image_a: Image, image_b: Image) -> float:
    verify_is_image_or_exception(image_a)
    verify_is_image_or_exception(image_b)

    signs = [(normalized_black_weight(image_a), normalized_black_weight(image_b))]

    normalized_center_a = normalized_gravity_center(image_a)
    normalized_center_b = normalized_gravity_center(image_b)

    signs.append((normalized_center_a[0], normalized_center_b[0]))
    signs.append((normalized_center_a[1], normalized_center_b[1]))

    signs.append((normalized_central_horizontal_axial_moment(image_a), normalized_central_horizontal_axial_moment(image_b)))

    signs.append((normalized_central_vertical_axial_moment(image_a), normalized_central_vertical_axial_moment(image_b)))

    return euclidean_metric(signs)


# Assumes that image has 'L' mode
def proximity_assessment(image: Image, diff_threshold: float, phrase: str):
    phrase_symbols = phrase.replace(' ', '')
    segments = symbol_segments(image, diff_threshold)

    result = []

    for segment in segments:
        test_start = segment[0]
        test_stop = segment[1]
        test_segment_image = image.crop(box=(test_start, 0, test_stop, image.height))

        tmp = []
        result.append(tmp)

        for j in range(len(segments)):
            start = segments[j][0]
            stop = segments[j][1]
            segment_image = image.crop(box=(start, 0, stop, image.height))

            measure = proximity_measure(test_segment_image, segment_image)
            tmp.append((phrase_symbols[j], measure))

        tmp.sort(key=lambda m: m[1])

    return result
