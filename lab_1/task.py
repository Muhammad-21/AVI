import os

from PIL import Image
from mdutils import MdUtils

from core.helpers import folder_helper
from core.constants import constants
from core.grayscale import grayscale
from core.sampling import sampling
from core.thresholding import thresholding

IMAGES = [
    'cat.png',
    'colors.jpg',
    'cool.jpg'
]

UPSAMPLE_FACTOR = 3
DOWNSAMPLE_FACTOR = 4


def generate_report():
    report = MdUtils(file_name='./report.md')
    report.new_header(level=1, title='Лабораторная работа №1. Передискретизация, обесцвечивание и бинаризация растровых изображений')
    report.new_line(text='Выполнил Махмудов Мухаммад Б18-504')

    for im in IMAGES:
        image_path = f'{folder_helper.IMAGES_FOLDER_PATH}/{im}'

        processed_image_folder_path = f'{image_path}_processed'
        os.makedirs(processed_image_folder_path, exist_ok=True)

        image = Image.open(image_path).convert(constants.RGB_MODE)

        # Sampling
        upsampled_integer_number_of_times_image_path = f'{processed_image_folder_path}/{im}_upsampled_m.png'
        downsampled_integer_number_of_times_image_path = f'{processed_image_folder_path}/{im}_downsampled_n.png'
        oversampled_two_pass_image_path = f'{processed_image_folder_path}/{im}_oversampled_two_pass.png'
        oversampled_one_pass_image_path = f'{processed_image_folder_path}/{im}_oversampled_one_pass.png'

        sampling.bilinear_interpolation_upsampling(image, UPSAMPLE_FACTOR).save(
            upsampled_integer_number_of_times_image_path)
        sampling.decimation_downsampling(image, DOWNSAMPLE_FACTOR).save(downsampled_integer_number_of_times_image_path)
        sampling.decimation_downsampling(sampling.bilinear_interpolation_upsampling(image, UPSAMPLE_FACTOR),
                                         DOWNSAMPLE_FACTOR).save(oversampled_two_pass_image_path)
        sampling.one_pass_resampling(image, UPSAMPLE_FACTOR, DOWNSAMPLE_FACTOR).save(oversampled_one_pass_image_path)

        # Grayscale
        mean_grayscaled_image_path = f'{processed_image_folder_path}/{im}_mean_grayscaled.png'
        photoshop_grayscaled_image_path = f'{processed_image_folder_path}/{im}_photoshop_grayscaled.png'

        grayscale.mean_grayscale(image).save(mean_grayscaled_image_path)
        grayscale.photoshop_grayscale(image).save(photoshop_grayscaled_image_path)

        # Threshold
        balansed_hist_thresholded_image_path = f'{processed_image_folder_path}/{im}_balansed_hist_thresholded.png'

        thresholding.balansed_histogram_method(grayscale.mean_grayscale(image)).save(
            balansed_hist_thresholded_image_path)

        # Report
        report.new_header(level=2, title=f'{im}')
        report.new_header(level=3, title='Исходная картинка')
        report.new_line(report.new_inline_image(text='Исходная картинка', path=image_path))

        report.new_header(level=3, title=f'Интерполяция с коэффициентом {UPSAMPLE_FACTOR}')
        report.new_line(report.new_inline_image(text=f'Интерполяция с коэффициентом {UPSAMPLE_FACTOR}',
                                                path=upsampled_integer_number_of_times_image_path))

        report.new_header(level=3, title=f'Децимация с коэффициентом {DOWNSAMPLE_FACTOR}')
        report.new_line(report.new_inline_image(text=f'Децимация с коэффициентом {DOWNSAMPLE_FACTOR}',
                                                path=downsampled_integer_number_of_times_image_path))

        report.new_header(level=3, title=f'Двухпроходная передескритизация с коэффициентом {UPSAMPLE_FACTOR}/{DOWNSAMPLE_FACTOR}')
        report.new_line(report.new_inline_image(text=f'Двухпроходная передескритизация с коэффициентом {UPSAMPLE_FACTOR}/{DOWNSAMPLE_FACTOR}',
                                                path=oversampled_two_pass_image_path))

        report.new_header(level=3, title=f'Однопроходная передескритизация с коэффициентом {UPSAMPLE_FACTOR}/{DOWNSAMPLE_FACTOR}')
        report.new_line(report.new_inline_image(text=f'Однопроходная передескритизация с коэффициентом {UPSAMPLE_FACTOR}/{DOWNSAMPLE_FACTOR}',
                                                path=oversampled_two_pass_image_path))

        report.new_header(level=3, title=f'Оттенки серого')
        report.new_line(report.new_inline_image(text=f'Оттенки серого', path=mean_grayscaled_image_path))

        report.new_header(level=3, title=f'Оттенки серого (как в Photoshop)')
        report.new_line(report.new_inline_image(text=f'Оттенки серого (как в Photoshop)',
                                                path=photoshop_grayscaled_image_path))

        report.new_header(level=3, title=f'Бинаризация (балансировка гистограммы)')
        report.new_line(report.new_inline_image(text=f'Бинаризация (балансировка гистограммы)', path=balansed_hist_thresholded_image_path))

    report.create_md_file()


def main():
    generate_report()


if __name__ == '__main__':
    main()
