from PIL import Image


def verify_is_image_or_exception(image):
    is_image = isinstance(image, Image.Image)

    if not is_image:
        raise TypeError(f"Object passed to function has type {image.__class__}."
                        "Expected that it will be subclass of Image.")


def verify_is_natural_or_exception(number):
    is_natural = isinstance(number, int) and number > 0

    if not is_natural:
        raise ValueError(f"Passed upsampling factor {number} is not natural but natural expected.")
