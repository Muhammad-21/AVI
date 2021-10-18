import os
import matplotlib.pyplot as pyplot

from PIL import Image, ImageFont, ImageDraw

from core.constants import constants
from core.helpers import folder_helper
from core.sampling.sampling import cut_empty_rows_and_cols
from mdutils.mdutils import MdUtils

from core.thresholding.thresholding import simple_threshold
from core.feature_extraction.feature_extraction import black_weight, normalized_black_weight, gravity_center,\
    normalized_gravity_center, central_horizontal_axial_moment, central_vertical_axial_moment,\
    normalized_central_horizontal_axial_moment, normalized_central_vertical_axial_moment, vertical_projection,\
    horizontal_projection


ALPHABET = 'AΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ'
WHITE = 255
FONT_SIZE = 52
FONT = ImageFont.truetype(font=f'{folder_helper.FONTS_FOLDER_PATH}/times.ttf', size=FONT_SIZE)


def generate_report():
    report = MdUtils(file_name=f'./report.md')
    report.new_header(level=1, title='Лабораторная работа №4. Выделение признаков символов')
    report.new_line(text='Выполнил Махмудов Мухаммад Б18-504')
    report.new_line(text=f'Алфавит - {ALPHABET}')

    for letter in ALPHABET:
        letter_folder_path = f'./{folder_helper.IMAGES_FOLDER_PATH}/letter_{letter}'
        os.makedirs(letter_folder_path, exist_ok=True)
        letter_image_path = f'{letter_folder_path}/{letter}.png'
        letter_image = Image.new(mode=constants.GRAYSCALE_MODE, size=(FONT_SIZE, FONT_SIZE), color=WHITE)
        result = ImageDraw.Draw(im=letter_image, mode=constants.GRAYSCALE_MODE)
        result.text(xy=(0, 0), text=letter, font=FONT, fill=0, anchor='lt')
        letter_image = cut_empty_rows_and_cols(letter_image)
        letter_image.save(letter_image_path)
        report.new_header(level=2, title=f'Буква {letter}')
        report.new_line(report.new_inline_image(text=letter, path=letter_image_path))
        thresholded = simple_threshold(letter_image, 100)
        report.new_line(text=f'Вес черного - {black_weight(thresholded)}')
        report.new_line(text=f'Удельный вес черного - {normalized_black_weight(thresholded)}')
        center = gravity_center(thresholded)
        report.new_line(text=f'Координаты центра масс - ({center[0]}, {center[1]})')
        normalized_center = normalized_gravity_center(thresholded)
        report.new_line(text=f'Нормированные координаты центра масс - ({normalized_center[0]}, {normalized_center[1]})')
        report.new_line(text=f'Центральный горизонтальный осевой момент - {central_horizontal_axial_moment(thresholded)}')
        report.new_line(text=f'Центральный вертикальный осевой момент - {central_vertical_axial_moment(thresholded)}')
        report.new_line(text=f'Нормированный центральный горизонтальный осевой момент -'
                             f'{normalized_central_horizontal_axial_moment(thresholded)}')
        report.new_line(text=f'Нормированный центральный вертикальный осевой момент -'
                             f'{normalized_central_vertical_axial_moment(thresholded)}')

        h_levels, h_projections = horizontal_projection(thresholded)
        pyplot.plot(h_levels, h_projections)
        pyplot.title(f'Horizontal projection {letter}')
        path = f'{letter_folder_path}/horizontal_projection_{letter}.png'
        pyplot.savefig(path)
        pyplot.close()

        report.new_line(report.new_inline_image(text=letter, path=path))

        v_levels, v_projections = vertical_projection(thresholded)
        pyplot.plot(v_levels, v_projections)
        pyplot.title(f'Vertical projection {letter}')
        path = f'{letter_folder_path}/vertical_projection_{letter}.png'
        pyplot.savefig(path)
        pyplot.close()

        report.new_line(report.new_inline_image(text=letter, path=path))

        report.new_line()

    report.create_md_file()


def main():
    generate_report()


if __name__ == '__main__':
    main()
