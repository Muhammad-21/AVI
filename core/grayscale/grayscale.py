from PIL import Image
from core.verification.verification import verify_is_image_or_exception

GRAYSCALE_MODE = 'L'


def mean_grayscale(image):
    verify_is_image_or_exception(image)

    result = Image.new(GRAYSCALE_MODE, (image.width, image.height))

    for x in range(result.width):
        for y in range(result.height):
            result.putpixel((x, y), pixel_mean_value_grayscale(image.getpixel((x, y))))

    return result


def photoshop_grayscale(image):
    verify_is_image_or_exception(image)

    result = Image.new(GRAYSCALE_MODE, (image.width, image.height))

    for x in range(result.width):
        for y in range(result.height):
            result.putpixel((x, y), pixel_photoshop_grayscale(image.getpixel((x, y))))

    return result


# Assumes that pixel is RGB tuple
def pixel_mean_value_grayscale(pixel):
    return int(round((pixel[0] + pixel[1] + pixel[2]) / 3))


# Assumes that pixel is RGB tuple
def pixel_photoshop_grayscale(pixel):
    return int(round(pixel[0] * 0.3 + pixel[1] * 0.59 + pixel[2] * 0.11))
