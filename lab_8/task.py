import os

import numpy
from PIL import Image
from mdutils import MdUtils

from core import helpers, enhancement
from core.constants import constants
from core.grayscale import grayscale

IMAGES = [
    'old_paris.jpg',
    'old_saratov.jpg',
    'old_serpukhov.jpg'
]

START_GAMMA = 0.25
STOP_GAMMA = 2.25
STEP_GAMMA = 0.25
GAMMA_ROUND_SIGNS = 2


def generate_report():
    report = MdUtils(file_name=f'./report.md')
    report.new_header(level=1, title='Лабораторная работа №8. Улучшение изображений. Контрастирование')
    report.new_line(text='Выполнил Махмудов Мухаммад Б18-504')

    for im in IMAGES:
        image_path = f'{helpers.folder_helper.IMAGES_FOLDER_PATH}/{im}'

        processed_image_folder_path = f'{image_path}_processed'
        os.makedirs(processed_image_folder_path, exist_ok=True)

        grayscaled_image_path = f'{processed_image_folder_path}/{im}_grayscaled.png'
        linear_contrasted_image_path = f'{processed_image_folder_path}/{im}_linear_contrasted.png'
        power_transformed_image_path = f'{processed_image_folder_path}/{im}_power_transformed_gamma=#.png'

        image = Image.open(fp=image_path).convert(constants.RGB_MODE)
        grayscaled = grayscale.mean_grayscale(image)

        grayscaled.save(grayscaled_image_path)

        # Contrasting
        enhancement.contrasting.linear_contrasting(grayscaled).save(linear_contrasted_image_path)
        for gamma in numpy.arange(START_GAMMA, STOP_GAMMA, STEP_GAMMA):
            gamma = round(gamma, GAMMA_ROUND_SIGNS)
            enhancement.contrasting.power_transformation(grayscaled, gamma=gamma)\
                .save(power_transformed_image_path.replace('#', str(gamma)))

        # Report
        report.new_header(level=2, title=f'{im}')

        report.new_header(level=3, title='Исходная картинка')
        report.new_line(report.new_inline_image(text='Исходная картинка', path=image_path))

        report.new_header(level=3, title='Оттенки серого')
        report.new_line(report.new_inline_image(text='Оттенки серого', path=grayscaled_image_path))

        report.new_header(level=3, title='Линейное контрастирование')
        report.new_line(report.new_inline_image(text='Линейное контрастирование', path=linear_contrasted_image_path))

        report.new_header(level=3, title='Степенное преобразование')
        for gamma in numpy.arange(START_GAMMA, STOP_GAMMA, STEP_GAMMA):
            gamma = round(gamma, GAMMA_ROUND_SIGNS)
            report.new_header(level=4, title=f'Gamma = {gamma}')
            report.new_line(report.new_inline_image(text='Степенное преобразование', path=power_transformed_image_path
                                                    .replace('#', str(gamma))))

    report.create_md_file()


def main():
    generate_report()


if __name__ == '__main__':
    main()
