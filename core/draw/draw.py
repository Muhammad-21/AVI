from PIL import Image, ImageDraw

from core import texturing, constants, math
from core.feature_extraction.feature_extraction import horizontal_projection,\
    inverted_vertical_projection, symbol_segments
from core.math.math import lerp
from core.sampling.sampling import expand_with_white
from core.verification import verification


# Assumes that image has 'L' mode
def draw_projections(image: Image) -> Image:
    verification.verify_is_image_or_exception(image)

    x_expand_size = 30
    y_expand_size = 30

    result = expand_with_white(image=expand_with_white(image=image, where='to_left', size=x_expand_size), where='to_bottom', size=y_expand_size).convert('RGB')
    result_draw = ImageDraw.Draw(im=result)

    h_color = (44, 176, 62)
    h_levels, h_projections = horizontal_projection(image)
    max_h_projection = max(h_projections)

    for y in range(image.height):
        x_projection_coord = int(round(lerp(0, 0, max_h_projection, 30, h_projections[y]))) + 1
        result_draw.rectangle(xy=[(0, y), (x_projection_coord, y + 1)], fill=h_color)

    v_color = (166, 29, 5)
    v_levels, v_projections = inverted_vertical_projection(image)
    max_v_projection = max(v_projections)

    for x in range(image.width):
        y_projection_coord = result.height - int(round(lerp(0, 0, max_v_projection, 30, v_projections[x])))
        result_draw.rectangle(xy=[(x + x_expand_size, y_projection_coord), (x + x_expand_size + 1, result.height + 1)], fill=v_color)

    return result


# Assumes that image is symbolic string and has 'L' mode
def draw_symbol_segments(image: Image, diff_threshold: float) -> Image:
    verification.verify_is_image_or_exception(image)

    start_color = (66, 218, 245)
    stop_color = (204, 87, 247)

    segments = symbol_segments(image, diff_threshold)
    result = image.copy().convert('RGB')
    result_draw = ImageDraw.Draw(im=result)

    for segment in segments:
        result_draw.rectangle(xy=[(segment[0], 0), (segment[0], result.height)], fill=start_color)
        result_draw.rectangle(xy=[(segment[1], 0), (segment[1], result.height)], fill=stop_color)

    return result


# Assumes that image has 'L' mode
def draw_series_length_matrix(image: Image) -> Image:
    verification.verify_is_image_or_exception(image)

    series_length_matrix = texturing.texturing.series_length_matrix(image)

    result = Image.new(mode=constants.constants.GRAYSCALE_MODE, size=(len(series_length_matrix[0]), len(series_length_matrix)))

    max_series_length = max([max(row) for row in series_length_matrix])

    for x in range(result.width):
        for y in range(result.height):
            result.putpixel((x, y), int(round(math.math.lerp(x1=0, f1=0, x2=max_series_length, f2=255, x=series_length_matrix[y][x]))))

    return result
