from PIL import Image, ImageFont, ImageDraw
from mdutils import MdUtils

from core.helpers import folder_helper
from core.feature_extraction.feature_extraction import proximity_assessment
from core.sampling.sampling import cut_empty_rows_and_cols

ALPHABET = 'AΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ'
PHRASE = 'ΨΟΜΓΤΗ ΛΙΟΣΡΦΔΔΦΗ ΦΓΤΩΖΦΥ ΚΜΙΞ ΒΞ'
SYMBOLS_DIFF_THRESHOLD = 0.03
GRAYSCALE_MODE = 'L'
WHITE = 255
FONT_SIZE = 52
SMALL_FONT_SIZE = 46
FONT_PATH = f'{folder_helper.FONTS_FOLDER_PATH}/times.ttf'


def generate_report():
    def generate_phrase_image(width: int, font: ImageFont) -> Image:
        result = Image.new(mode=GRAYSCALE_MODE, size=(width, font.size), color=WHITE)
        result_draw = ImageDraw.Draw(im=result, mode=GRAYSCALE_MODE)
        result_draw.text(xy=(0, 0), text=PHRASE, font=font, fill=0, anchor='lt')
        return cut_empty_rows_and_cols(result)

    def p_ass_for_table(p_ass):
        result = []
        for row in p_ass:
            for element in row:
                result.append(str(element))

        return result

    report = MdUtils(file_name=f'./report.md')
    report.new_header(level=1, title='Лабораторная работа №6. Классификация на основе признаков, анализ профилей')
    report.new_line(text='Выполнил Махмудов Мухаммад Б18-504')
    report.new_line(text=f'Алфавит - {ALPHABET}')
    report.new_line(text=f'Исходная фраза - {PHRASE}')
    report.new_line(text=f'Размер шрифта - {FONT_SIZE}')

    # Phrase
    phrase_image = generate_phrase_image(1200, ImageFont.truetype(font=FONT_PATH, size=FONT_SIZE))
    phrase_image_small_font = generate_phrase_image(1200, ImageFont.truetype(font=FONT_PATH, size=SMALL_FONT_SIZE))

    # Proximity assessment
    p_assessment = proximity_assessment(image=phrase_image, diff_threshold=SYMBOLS_DIFF_THRESHOLD, phrase=PHRASE)
    p_assessment_small_font = proximity_assessment(image=phrase_image_small_font, diff_threshold=SYMBOLS_DIFF_THRESHOLD,
                                                   phrase=PHRASE)

    p_assessment_for_table = p_ass_for_table(p_assessment)
    p_assessment_small_font_for_table = p_ass_for_table(p_assessment_small_font)

    # Report
    report.new_header(level=2, title=f'Оценка близости для размера шрифта {FONT_SIZE}')

    rows = len(p_assessment)
    columns = len(p_assessment[0]) if len(p_assessment) > 0 else 0
    report.new_table(columns=columns, rows=rows, text=p_assessment_for_table)

    report.new_header(level=2, title=f'Оценка близости для размера шрифта {SMALL_FONT_SIZE}')

    rows = len(p_assessment_small_font)
    columns = len(p_assessment_small_font[0]) if len(p_assessment_small_font) > 0 else 0
    report.new_table(columns=columns, rows=rows, text=p_assessment_small_font_for_table)

    report.new_line(text='Так как были использованы нормализованные параметры для оценки близости символов, размер шрифта не влияет на результат')

    report.create_md_file()


def main():
    generate_report()


if __name__ == '__main__':
    main()
