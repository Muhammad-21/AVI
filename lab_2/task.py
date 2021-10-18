import os

from PIL import Image
from mdutils import MdUtils

from core.helpers import folder_helper
from core.constants import constants
from core.filtration import filtration
from core.grayscale import grayscale

IMAGES = [
    'monah.jpg',
    'colors.jpg',
    'old_text_2.jpg'
]


def generate_report():
    report = MdUtils(file_name='./report.md')
    report.new_header(level=1, title='Лабораторная работа №2. Фильтрация изображений и морфологические операции')
    report.new_line(text='Выполнил Махмудов Мухаммад Б18-504')

    for im in IMAGES:
        image_path = f'{folder_helper.IMAGES_FOLDER_PATH}/{im}'

        processed_image_folder_path = f'{image_path}_processed'
        os.makedirs(processed_image_folder_path, exist_ok=True)

        image = Image.open(image_path).convert(constants.RGB_MODE)

        # Smoothing
        spatial_smoothed_image_path = f'{processed_image_folder_path}/{im}_spatial_smoothed.png'
        spatial_smoothed_difference_image_path = f'{processed_image_folder_path}/{im}_spatial_smoothed_difference.png'

        grayscaled = grayscale.mean_grayscale(image)
        filtration.spatial_smoothing(grayscaled).save(spatial_smoothed_image_path)
        filtration.spatial_smoothing_difference(grayscaled).save(spatial_smoothed_difference_image_path)

        # Report
        report.new_header(level=2, title=f'{im}')
        report.new_header(level=3, title='Исходная картинка')
        report.new_line(report.new_inline_image(text='Исходная картинка', path=image_path))

        report.new_header(level=3, title='Пространственное сглаживание')
        report.new_line(report.new_inline_image(text='Пространственное сглаживание', path=spatial_smoothed_image_path))

        report.new_header(level=3, title='Разница сглаженной и исходной')
        report.new_line(report.new_inline_image(text='Разница сглаженной и исходной',
                                                path=spatial_smoothed_difference_image_path))

    report.create_md_file()


def main():
    generate_report()


if __name__ == '__main__':
    main()
