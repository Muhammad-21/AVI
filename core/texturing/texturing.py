from PIL import Image

from core import verification


# Assumes that image has 'L' mode
def series_length_matrix(image: Image):
    verification.verification.verify_is_image_or_exception(image)

    series_matrix = [[0 for _ in range(max(image.width, image.height) + 1)] for _ in range(256)]

    # Vertical series
    for x in range(image.width):
        count = 1
        prev_pixel = -1

        for y in range(image.height):
            pixel = image.getpixel((x, y))

            if pixel != prev_pixel:
                if count >= 2:
                    series_matrix[prev_pixel][count] += 1

                count = 1
                prev_pixel = pixel
            else:
                count += 1

        if count >= 2:
            series_matrix[prev_pixel][count] += 1

    # Horizontal series
    for y in range(image.height):
        count = 1
        prev_pixel = -1

        for x in range(image.width):
            pixel = image.getpixel((x, y))

            if pixel != prev_pixel:
                if count >= 2:
                    series_matrix[prev_pixel][count] += 1

                count = 1
                prev_pixel = pixel
            else:
                count += 1

        if count >= 2:
            series_matrix[prev_pixel][count] += 1

    # Rising diagonal series
    for y in range(image.height):
        prev_pixel = image.getpixel((0, y))
        count = 1
        current_y = y

        for x in range(1, image.width):
            current_y -= 1

            if current_y < 0:
                break

            pixel = image.getpixel((x, current_y))

            if pixel != prev_pixel:
                if count >= 2:
                    series_matrix[prev_pixel][count] += 1

                count = 1
                prev_pixel = pixel
            else:
                count += 1

        if count >= 2:
            series_matrix[prev_pixel][count] += 1

    for x in range(1, image.width):
        prev_pixel = image.getpixel((x, image.height - 1))
        count = 1
        current_x = x

        for y in range(image.height - 2, -1, -1):
            current_x += 1

            if current_x >= image.width:
                break

            pixel = image.getpixel((current_x, y))

            if pixel != prev_pixel:
                if count >= 2:
                    series_matrix[prev_pixel][count] += 1

                count = 1
                prev_pixel = pixel
            else:
                count += 1

        if count >= 2:
            series_matrix[prev_pixel][count] += 1

    # Falling diagonal series
    for y in range(image.height):
        prev_pixel = image.getpixel((0, y))
        count = 1
        current_y = y

        for x in range(1, image.width):
            current_y += 1

            if current_y >= image.height:
                break

            pixel = image.getpixel((x, current_y))

            if pixel != prev_pixel:
                if count >= 2:
                    series_matrix[prev_pixel][count] += 1

                count = 1
                prev_pixel = pixel
            else:
                count += 1

        if count >= 2:
            series_matrix[prev_pixel][count] += 1

    for x in range(1, image.width):
        prev_pixel = image.getpixel((x, 0))
        count = 1
        current_x = x

        for y in range(1, image.height):
            current_x += 1

            if current_x >= image.width:
                break

            pixel = image.getpixel((current_x, y))

            if pixel != prev_pixel:
                if count >= 2:
                    series_matrix[prev_pixel][count] += 1

                count = 1
                prev_pixel = pixel
            else:
                count += 1

        if count >= 2:
            series_matrix[prev_pixel][count] += 1

    return series_matrix


# Assumes that image has 'L' mode
def sre_coefficient(image: Image) -> float:
    verification.verification.verify_is_image_or_exception(image)
    s_length_matrix = series_length_matrix(image)

    s_length_matrix_sum = sum([sum(row) for row in s_length_matrix])
    sre = 0

    for i in range(len(s_length_matrix[0])):
        tmp = 0

        for j in range(256):
            tmp += s_length_matrix[j][i]

        sre += tmp / ((i + 2) ** 2)

    return sre / s_length_matrix_sum
