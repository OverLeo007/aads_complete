"""
Модуль, реализующий поиск подстрок в строке,
при помощи алгоритма Бойера-Мура-Хорспула
"""

from typing import Union, Optional


def reverse_str(string: str) -> str:
    """
    Функция разворота строки
    :param string: строка
    :return: развернутая строка
    """
    return ''.join(reversed(string))


def find_offset(template: str) -> dict[str, int]:
    """
    Функция поиска таблицы сдвига для шаблона

    :param template: строка для которой создаем таблицу сдвигов
    :return: таблица сдвига
    """
    temp_len = len(template)
    res = {"*": temp_len}

    for i in range(temp_len - 2, -1, -1):
        if not res.get(template[i], False):
            res[template[i]] = temp_len - i - 1
    if not res.get(template[-1], False):
        res[template[-1]] = temp_len
    return res


def find_substr(string: str, sub_string: str) -> Optional[tuple[int, str]]:
    """
    Функция поиска первого вхождения шаблона в строку

    :param string: строка
    :param sub_string: шаблон
    :return: индекс вхождения
    """
    if len(sub_string) > len(string):
        return None
    offset_table = find_offset(sub_string)

    def compare(comp_str: str, inp_str: str) -> int:
        """
        Функция сравнения части строки с подстрокой

        :param comp_str: часть строки
        :param inp_str: шаблон
        :return: кол-во элементов на которые нужно сдвинуть шаблон
        """
        if comp_str[-1] != inp_str[-1]:
            return offset_table[comp_str[-1]] \
                if offset_table.get(comp_str[-1], False) \
                else offset_table["*"]

        ptr = -2
        while len(inp_str) >= abs(ptr):
            if comp_str[ptr] != inp_str[ptr]:
                return offset_table[inp_str[ptr]]
            ptr -= 1
        return 0

    index = 0
    while True:
        if len(sub_string) > len(string):
            return None
        next_sym = compare(string[:len(sub_string)], sub_string)
        index += next_sym
        string = string[next_sym:]
        # print(string)
        if next_sym == 0:
            if len(sub_string) == 1:
                string = string[offset_table["*"]:]
            else:
                string = string[1:]
            break

    return index, string


def search(string: str, sub_string: Union[str, list[str]],
           case_sensitivity: bool = False,
           method: str = 'first',
           count: Optional[int] = None) -> \
        Optional[Union[tuple[int, ...], dict[str, tuple[int, ...]]]]:
    """
    Функция поиска вхождений любого количества шаблонов в строку

    :param string: строка
    :param sub_string: шаблон(ы)
    :param case_sensitivity: чувствительность к регистру
    :param method: метод поиска (сначала либо с конца)
    :param count: количество найденных индексов подстрок для каждого шаблона
    :return: либо кортеж с индексами вхождений, если sub_string - str, либо словарь,
    где элементы (шаблон: кортеж с индексами вхождений), если sub_string - list
    """

    def get_all_indexes(substring: str):
        """
        Функция получения индексов всех вхождений шаблона в строку

        :param substring: шаблон
        :return: индексы вхождений
        """
        str_to_find = string
        indexes = []
        if not case_sensitivity:
            str_to_find = str_to_find.lower()
            substring = substring.lower()

        if method == "last":
            str_len = len(str_to_find)
            str_to_find = reverse_str(str_to_find)
            substring = reverse_str(substring)

        while str_to_find:
            if count is not None and len(indexes) >= count:
                break
            result = find_substr(str_to_find, substring)
            if result:
                index, str_to_find = result
                indexes.append(index + (indexes[-1] + 1 if indexes else 0))

            else:
                break
        if indexes:
            if method == "last":
                return tuple(map(lambda x: str_len - len(substring) - x, indexes))
            return tuple(indexes)
        return None

    if isinstance(sub_string, str):
        return get_all_indexes(sub_string)
    res = {subs: get_all_indexes(subs)
           for subs in sub_string}
    if (rvals := list(res.values())).count(None) == len(rvals):
        return None
    return res


if __name__ == '__main__':
    # print("apapapap", "apap")
    print(find_offset("зорро"))
    # print(compare("данные", "данные", find_offset("данные")))
