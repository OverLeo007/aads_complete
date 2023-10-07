"""
Модуль реализации консольного интерфейса для алгоритма поиска

"""

import argparse

from search import search

BLACK = 40
RED = 101
GREEN = 102
YELLOW = 103
BLUE = 104
PURPLE = 105
CYAN = 106
WHITE = 107

col_seq = [RED, YELLOW, GREEN, BLUE, CYAN, PURPLE]


class ExtendedChar:  # pylint: disable=R0903
    """
    Класс символа, содержащего дополнительно его цвет
    """

    def __init__(self, char: str, color: int = 0):
        """
        Инициализация экземпляра раскрашенного символа
        :param char: символ
        :param color: цвет раскраски
        """
        self.char = char
        self.color = color

    def colored(self):
        """
        Представления символа с добавлением ANSI раскраски текущего цвета
        :return: раскрашенный в color символ
        """
        return f"\033[{self.color};{30 if self.color else 0}m{self.char}\033[0;0m"


def colorize(string: str, indexes: dict[str: tuple[int, ...]]):
    """
    Функция раскраски строки
    :param string: строка
    :param indexes: словарь из найденных подстрок и их индексов в строке
    :return: раскрашенная строка
    """
    if indexes is None:
        return string
    subs = sorted(list(indexes.items()), key=lambda x: len(x[0]), reverse=True)
    str_list = [ExtendedChar(char) for char in string]
    for i, sub in enumerate(subs):
        cur_sub, cur_indexes = sub
        if cur_indexes is None:
            continue
        color = col_seq[i % len(col_seq)]
        for index in cur_indexes:
            for j in range(index, index + len(cur_sub)):
                str_list[j].color = color

    return "".join(map(lambda x: x.colored(), str_list))


def main():
    """
    Точка входа
    """
    parser = argparse.ArgumentParser(description="Моя реализация поиска подстроки в строке "
                                                 "при помощи алгоритма Бойера-Мура-Хорспула")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--string", "-s", dest="string",
                       type=str, help="Строка, где будет производиться поиск")
    group.add_argument("--file_path", "-fp", dest="path",
                       type=str, help="Файл, с текстом где будет производиться поиск")

    parser.add_argument("--sub_string", "-ss", dest="sub_string",
                        type=str, nargs="+", help="шаблон(ы) для поиска в строке")
    parser.add_argument("--case_sensitivity", "-cs", dest="case_sensitivity",
                        type=bool, default=False, help="Чувствительность поиска к регистру")
    parser.add_argument("--method", "-m", dest="method",
                        type=str, default="first", help="Метод поиска - с начала или с конца")
    parser.add_argument("--count", "-c", dest="count",
                        type=int, default=None,
                        help="Максимальное кол-во найденных подстрок для каждого шаблона")

    args = parser.parse_args()

    if (args.string is None and args.path is None) or args.sub_string is None:
        raise parser.error("Строка или шаблон(ы) не указан(ы)")  # pylint: disable=E0702
    if len(args.sub_string) > 6:
        raise parser.error(  # pylint: disable=E0702
            f"Слишком большое количество шаблонов "
            f"({len(args.sub_string)} > 6)")

    if args.path is not None:
        try:
            with open(args.path, "r", encoding="utf-8") as file:
                args.string = file.read()
        except FileNotFoundError as exc:
            raise parser.error(f"Файл с именем {exc.filename} не найден")  # pylint: disable=E0702

    indexes = search(args.string,
                     args.sub_string,
                     args.case_sensitivity,
                     args.method, args.count)

    print(f'Текст: "{args.string}"')
    print(f'Шаблон(ы): {args.sub_string}')

    print(f'Индексы: {str(indexes)}')
    print(f"Раскрашенная строка:\n{colorize(args.string, indexes)}")


if __name__ == '__main__':
    main()
