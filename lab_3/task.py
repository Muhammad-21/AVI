import os

from PIL import Image
from mdutils import MdUtils

from core.helpers import folder_helper
from core.constants import constants
from core.filtration import filtration
from core.grayscale import grayscale

IMAGES = [
    'pict.jpg',
    'picture3.png',
    'text.jpg'
]


def generate_report():
    report = MdUtils(file_name='./report.md')
    report.new_header(level=1, title='Лабораторная работа №3. Выделение контуров на изображении')
    report.new_line(text='Выполнил Махмудов Мухаммад Б18-504')

    for im in IMAGES:
        image_path = f'{folder_helper.IMAGES_FOLDER_PATH}/{im}'

        processed_image_folder_path = f'{image_path}_processed'
        os.makedirs(processed_image_folder_path, exist_ok=True)

        image = Image.open(image_path).convert(constants.RGB_MODE)

        # Outline
        smoothed_image_path = f'{processed_image_folder_path}/{im}_grayscaled.png'
        roberts_cross_x_image_path = f'{processed_image_folder_path}/{im}_roberts_cross_x.png'
        roberts_cross_y_image_path = f'{processed_image_folder_path}/{im}_roberts_cross_y.png'
        roberts_cross_image_path = f'{processed_image_folder_path}/{im}_roberts_cross.png'
        roberts_cross_normalized_image_path = f'{processed_image_folder_path}/{im}_roberts_cross_normalized_#.png'

        grayscaled = grayscale.mean_grayscale(image)
        smoothed = filtration.spatial_smoothing(grayscaled)
        smoothed.save(smoothed_image_path)

        filtration.roberts_cross_x(smoothed).save(roberts_cross_x_image_path)
        filtration.roberts_cross_y(smoothed).save(roberts_cross_y_image_path)
        filtration.roberts_cross(smoothed).save(roberts_cross_image_path)

        for i in range(10, 31):
            filtration.roberts_cross_threshold(smoothed, i).save(
                roberts_cross_normalized_image_path.replace('#', f'{i}'))

        # Report
        report.new_header(level=2, title=f'{im}')
        report.new_header(level=3, title='Исходная картинка')
        report.new_line(report.new_inline_image(text='Исходная картинка', path=image_path))

        report.new_header(level=3, title='Сглаженные оттенки серого')
        report.new_line(report.new_inline_image(text='Сглаженные оттенки серого', path=smoothed_image_path))

        report.new_header(level=3, title='Оператор Робертса 2x2 (x)')
        report.new_line(
            report.new_inline_image(text='Оператор Робертса 2x2 (x)', path=roberts_cross_x_image_path))

        report.new_header(level=3, title='Оператор Робертса 2x2 (y)')
        report.new_line(
            report.new_inline_image(text='Оператор Робертса 2x2 (y)', path=roberts_cross_y_image_path))

        report.new_header(level=3, title='Оператор Робертса 2x2')
        report.new_line(
            report.new_inline_image(text='Оператор Робертса 2x2', path=roberts_cross_image_path))

        report.new_header(level=3, title='Оператор Робертса 2x2 (нормализованная)')
        for i in range(10, 31):
            report.new_header(level=4, title=f'Порог {i}')
            report.new_line(
                report.new_inline_image(text=f'Порог {i}',
                                        path=roberts_cross_normalized_image_path.replace('#', f'{i}')))

    report.create_md_file()


def main():
    generate_report()


if __name__ == '__main__':
    main()
