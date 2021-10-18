from PIL import Image
from core.verification.verification import verify_is_image_or_exception
from statistics import mean

THRESHOLDING_MODE = '1'


# Assumes that image has 'L' mode (grayscale)
def spatial_smoothing(image):
    verify_is_image_or_exception(image)

    result = Image.new(image.mode, (image.width, image.height))

    for x in range(1, result.width - 1):
        for y in range(1, result.height - 1):
            window = list()
            for i in range(3):
                for j in range(3):
                    window.append(image.getpixel((x + i - 1, y + j - 1)))

            result.putpixel((x, y), int(round(mean(window))))

    return result


# Assumes that image has 'L' mode (grayscale)
def spatial_smoothing_difference(image):
    verify_is_image_or_exception(image)

    spatial_smoothed = spatial_smoothing(image)
    result = Image.new(image.mode, (image.width, image.height))

    for x in range(result.width):
        for y in range(result.height):
            result.putpixel((x, y), abs(image.getpixel((x, y)) - spatial_smoothed.getpixel((x, y))))

    return result


def roberts_cross_gradient_x(image, x, y):
    return abs(image.getpixel((x, y)) - image.getpixel((x + 1, y + 1)))


def roberts_cross_gradient_y(image, x, y):
    return abs(image.getpixel((x + 1, y)) - image.getpixel((x, y + 1)))


def roberts_cross_gradient(gradient_x, gradient_y):
    return int(round((gradient_x ** 2 + gradient_y ** 2) ** 0.5))


# Assumes that image has 'L' mode (grayscale)
def roberts_cross_threshold(image, threshold=128):
    verify_is_image_or_exception(image)

    result = Image.new('1', (image.width, image.height))
    gradient_max = 0
    gradient_matrix = list()

    for x in range(result.width - 1):
        gradient_matrix.append(list())
        for y in range(result.height - 1):
            gradient_x = roberts_cross_gradient_x(image, x, y)
            gradient_y = roberts_cross_gradient_y(image, x, y)
            gradient = roberts_cross_gradient(gradient_x, gradient_y)

            if gradient > gradient_max:
                gradient_max = gradient

            gradient_matrix[x].append(gradient)

    for x in range(result.width - 1):
        for y in range(result.height - 1):
            gradient_normalized = int(round(gradient_matrix[x][y] * 255 / gradient_max))
            result.putpixel((x, y), gradient_normalized > threshold)

    return result


# Assumes that image has 'L' mode (grayscale)
def roberts_cross(image):
    verify_is_image_or_exception(image)

    result = Image.new(image.mode, (image.width, image.height))
    gradient_max = 0
    gradient_matrix = list()

    for x in range(result.width - 1):
        gradient_matrix.append(list())
        for y in range(result.height - 1):
            gradient_x = roberts_cross_gradient_x(image, x, y)
            gradient_y = roberts_cross_gradient_y(image, x, y)
            gradient = roberts_cross_gradient(gradient_x, gradient_y)

            if gradient > gradient_max:
                gradient_max = gradient

            gradient_matrix[x].append(gradient)

    for x in range(result.width - 1):
        for y in range(result.height - 1):
            result.putpixel((x, y), int(round(gradient_matrix[x][y] * 255 / gradient_max)))

    return result


# Assumes that image has 'L' mode (grayscale)
def roberts_cross_x(image):
    verify_is_image_or_exception(image)

    result = Image.new(image.mode, (image.width, image.height))
    gradient_x_max = 0
    gradient_x_matrix = list()

    for x in range(result.width - 1):
        gradient_x_matrix.append(list())
        for y in range(result.height - 1):
            gradient_x = roberts_cross_gradient_x(image, x, y)

            if gradient_x > gradient_x_max:
                gradient_x_max = gradient_x

            gradient_x_matrix[x].append(gradient_x)

    for x in range(result.width - 1):
        for y in range(result.height - 1):
            result.putpixel((x, y), int(round(gradient_x_matrix[x][y] * 255 / gradient_x_max)))

    return result


# Assumes that image has 'L' mode (grayscale)
def roberts_cross_y(image):
    verify_is_image_or_exception(image)

    result = Image.new(image.mode, (image.width, image.height))
    gradient_y_max = 0
    gradient_y_matrix = list()

    for x in range(result.width - 1):
        gradient_y_matrix.append(list())
        for y in range(result.height - 1):
            gradient_x = roberts_cross_gradient_y(image, x, y)

            if gradient_x > gradient_y_max:
                gradient_y_max = gradient_x

            gradient_y_matrix[x].append(gradient_x)

    for x in range(result.width - 1):
        for y in range(result.height - 1):
            result.putpixel((x, y), int(round(gradient_y_matrix[x][y] * 255 / gradient_y_max)))

    return result

