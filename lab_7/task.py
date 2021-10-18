import os
from pprint import pprint

from PIL import Image
from mdutils import MdUtils

from core import helpers, constants, draw, grayscale, texturing

IMAGES = [
    'white.png',
    'cloth.jpg',
    'cloth_2.jpg',
    'oak_wood.jpg',
    'opal.jpg'
]


def generate_report():
    report = MdUtils(file_name=f'./report.md')
    report.new_header(level=1, title='Лабораторная работа №7. Текстурный анализ')
    report.new_line(text='Выполнил Махмудов Мухаммад Б18-504')

    for im in IMAGES:
        image_path = f'{helpers.folder_helper.IMAGES_FOLDER_PATH}/{im}'

        processed_image_folder_path = f'{image_path}_processed'
        os.makedirs(processed_image_folder_path, exist_ok=True)

        series_length_matrix_image_path = f'{processed_image_folder_path}/{im}_series_length_matrix.png'

        image = Image.open(image_path).convert(constants.constants.RGB_MODE)
        grayscaled = grayscale.grayscale.mean_grayscale(image)

        # Series length matrix
        draw.draw.draw_series_length_matrix(grayscale.grayscale.mean_grayscale(image)).save(series_length_matrix_image_path)

        # SRE
        sre = texturing.texturing.sre_coefficient(grayscaled)

        # Report
        report.new_header(level=2, title=f'{im} (SRE = {sre})')

        report.new_header(level=3, title='Исходная картинка')
        report.new_line(report.new_inline_image(text='Исходная картинка', path=image_path))

        report.new_header(level=3, title='Матрица длин серий')
        report.new_line(report.new_inline_image(text='Матрица длин серий', path=series_length_matrix_image_path))

    report.create_md_file()


def main():
    generate_report()


if __name__ == '__main__':
    main()
