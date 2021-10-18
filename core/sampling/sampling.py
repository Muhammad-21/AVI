from itertools import islice

from PIL import Image, ImageDraw

from core.helpers.helpers import white_color_by_mode
from core.math import math
from core.verification import verification


# TODO extract different scripts for different modes like RGB etc
def closest_neighbor_upsampling(image, factor):
    verification.verify_is_image_or_exception(image)

    if factor == 1:
        return image.copy()

    verification.verify_is_natural_or_exception(factor)

    result_width = image.width * factor
    result_height = image.height * factor
    result = Image.new(image.mode, (result_width, result_height))

    for x in range(result_width):
        x_nearest = int(x * image.width / result_width)
        for y in range(result_height):
            y_nearest = int(y * image.height / result_height)
            result.putpixel((x, y), image.getpixel((x_nearest, y_nearest)))

    return result


# TODO solve problem with black left and lower borders
def bilinear_interpolation_upsampling(image, factor):
    verification.verify_is_image_or_exception(image)

    if factor == 1:
        return image.copy()

    verification.verify_is_natural_or_exception(factor)

    result_width = image.width * factor
    result_height = image.height * factor
    result = Image.new(image.mode, (result_width, result_height))

    for x in range(result_width):
        for y in range(result_height):
            if (x % factor == 0) and (y % factor == 0):
                result.putpixel((x, y), image.getpixel((x // factor, y // factor)))
                continue

            prev_row_number = y // factor
            next_row_number = prev_row_number + 1
            prev_col_number = x // factor
            next_col_number = prev_col_number + 1

            if (next_row_number >= image.height) or (next_col_number >= image.width):
                result.putpixel((x, y), (0, 0, 0))
                continue

            prev_row_prev_col_pixel = image.getpixel((prev_col_number, prev_row_number))
            prev_row_next_col_pixel = image.getpixel((next_col_number, prev_row_number))
            next_row_prev_col_pixel = image.getpixel((prev_col_number, next_row_number))
            next_row_next_col_pixel = image.getpixel((next_col_number, next_row_number))

            upper_pseudo_pixel = math.rgb_color_lerp(prev_col_number, prev_row_prev_col_pixel, next_col_number, prev_row_next_col_pixel, x / factor)
            lower_pseudo_pixel = math.rgb_color_lerp(prev_col_number, next_row_prev_col_pixel, next_col_number, next_row_next_col_pixel, x / factor)

            result.putpixel((x, y), math.rgb_color_lerp(prev_row_number, upper_pseudo_pixel, next_row_number, lower_pseudo_pixel, y / factor))

    return result


# TODO solve problem with dropping factor - 1 pixels from right and lower borders
def decimation_downsampling(image, factor):
    verification.verify_is_image_or_exception(image)

    if factor == 1:
        return image.copy()

    verification.verify_is_natural_or_exception(factor)

    result_width = image.width // factor
    result_height = image.height // factor
    result = Image.new(image.mode, (result_width, result_height))

    for x in range(image.width - factor + 1):
        if x % factor != 0:
            continue

        for y in range(image.height - factor + 1):
            if y % factor != 0:
                continue

            result.putpixel((x // factor, y // factor), image.getpixel((x, y)))

    return result


def one_pass_resampling(image, upsample_factor, downsample_factor):
    verification.verify_is_image_or_exception(image)

    verification.verify_is_natural_or_exception(upsample_factor)
    verification.verify_is_natural_or_exception(downsample_factor)

    if upsample_factor == downsample_factor:
        return image.copy()

    result_width = image.width * upsample_factor // downsample_factor
    result_height = image.height * upsample_factor // downsample_factor
    result = Image.new(image.mode, (result_width, result_height))

    for x in range(result_width):
        for y in range(result_height):
            result.putpixel((x, y), image.getpixel((x * downsample_factor // upsample_factor, y * downsample_factor / upsample_factor)))

    return result


# Assumes that image has 'L' mode (grayscale)
def cut_empty_rows_and_cols(image):
    verification.verify_is_image_or_exception(image)

    empty_row_numbers = []
    empty_column_numbers = []

    for x in range(image.width):
        is_col_empty = True
        for y in range(image.height):
            if image.getpixel((x, y)) < 255:
                is_col_empty = False
                break

        if is_col_empty:
            empty_column_numbers.append(x)

    for y in range(image.height):
        is_row_empty = True
        for x in range(image.width):
            if image.getpixel((x, y)) < 255:
                is_row_empty = False
                break

        if is_row_empty:
            empty_row_numbers.append(y)

    def last_element_in_a_row(elements, start_element, step):
        prev_element = start_element

        for element in elements[::step]:
            if abs(element - prev_element) > 1:
                return prev_element + step

            prev_element = element

        return prev_element + step

    left_whitespace_end = last_element_in_a_row(empty_column_numbers, -1, 1)
    upper_whitespace_end = last_element_in_a_row(empty_row_numbers, -1, 1)
    right_whitespace_end = last_element_in_a_row(empty_column_numbers, image.width, -1)
    lower_whitespace_end = last_element_in_a_row(empty_row_numbers, image.height, -1)

    return image.crop(box=(left_whitespace_end, upper_whitespace_end, right_whitespace_end + 1, lower_whitespace_end + 1))


def expand_with_white(image: Image, where, size: int) -> Image:
    verification.verify_is_image_or_exception(image)

    fill = white_color_by_mode(image.mode)

    if where == 'to_left':
        result = Image.new(image.mode, (image.width + size, image.height))
        draw = ImageDraw.Draw(im=result, mode=result.mode)
        draw.rectangle(xy=[(0, 0), (size + 1, result.height + 1)], fill=fill)
        result.paste(im=image, box=(size + 1, 0))
    elif where == 'to_right':
        result = Image.new(image.mode, (image.width + size, image.height))
        draw = ImageDraw.Draw(im=result, mode=result.mode)
        draw.rectangle(xy=[(result.width - 1 - size, 0), (result.width + 1, result.height + 1)], fill=fill)
        result.paste(im=image, box=(0, 0))
    elif where == 'to_top':
        result = Image.new(image.mode, (image.width, image.height + size))
        draw = ImageDraw.Draw(im=result, mode=result.mode)
        draw.rectangle(xy=[(0, 0), (result.width + 1, size + 1)], fill=fill)
        result.paste(im=image, box=(0, size + 1))
    elif where == 'to_bottom':
        result = Image.new(image.mode, (image.width, image.height + size))
        draw = ImageDraw.Draw(im=result, mode=result.mode)
        draw.rectangle(xy=[(0, result.height - 1 - size), (result.width + 1, result.height + 1)], fill=fill)
        result.paste(im=image, box=(0, 0))
    else:
        raise ValueError(f'Where argument {where} is unsupported')

    return result
