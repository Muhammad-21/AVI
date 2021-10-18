from PIL import Image

from core.math import math
from core.verification import verification


# Assumes that image has 'L' mode
def linear_contrasting(image: Image, min_brightness: int = 0, max_brightness: int = 255) -> Image:
    def calculate_brightness(f, f_min, f_max, g_min, g_max):
        return round(int((f - f_min) / (f_max - f_min) * (g_max - g_min) + g_min))

    verification.verify_is_image_or_exception(image)

    image_pixels = list(image.getdata())

    image_min_brightness = min(image_pixels)
    image_max_brightness = max(image_pixels)

    result = image.copy()

    for x in range(result.width):
        for y in range(result.height):
            brightness = calculate_brightness(result.getpixel((x, y)), image_min_brightness, image_max_brightness,
                                              min_brightness, max_brightness)
            result.putpixel((x, y), brightness)

    return result


# Assumes that image has 'L' mode and other arguments >= 0
def power_transformation(image: Image, c: float = 1, f_zero: float = 0, gamma: float = 0.5) -> Image:
    def calculate_brightness(pixel_brightness: int) -> int:
        normalized_pixel_brightness = math.lerp(x1=0, f1=0, x2=255, f2=1, x=pixel_brightness)
        result_brightness = c * pow(normalized_pixel_brightness + f_zero, gamma)
        return int(round(math.lerp(x1=0, f1=0, x2=1, f2=255, x=result_brightness)))

    verification.verify_is_image_or_exception(image)

    assert c >= 0
    assert f_zero >= 0
    assert gamma >= 0

    result = image.copy()

    for x in range(result.width):
        for y in range(result.height):
            brightness = calculate_brightness(result.getpixel((x, y)))
            result.putpixel((x, y), brightness)

    return result



