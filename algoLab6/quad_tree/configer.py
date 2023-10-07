"""
Файл с менеджером конфигов
"""


import os
from configparser import ConfigParser
from typing import Optional

from quad_tree import consts as c


def find_file(filename, search_path='.') -> Optional[str]:
    """
    Функция поиска файла в указанной и дочерних дерикториях
    :param filename: имя файла
    :param search_path: папка поиска
    :return: полный путь из search_path до файла
    """
    for root, _, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None


class ConfigManager:
    default_config = {
        'WIDTH': '800',
        'HEIGHT': '600',
        'BALL_RADIUS': '10',
        'FPS_LIMIT': '60',
        'TIME_SPEED': '1',
        'NODE_CAPACITY': '2',
        'IS_RENDER_NUMS': 'False',
        'BALL_COLOR': '(0, 0, 255)',
        'BALL_COLOR_INV': '(255, 0, 0)',
        'IS_GEN': 'True',
        'BALLS_COUNT': '50',
        'BALL_MIN_RADIUS': '1',
        'BALL_MAX_RADIUS': '50',
        'BALL_MIN_VELOCITY': '1',
        'BALL_MAX_VELOCITY': '5',
        'MAX_COLLISIONS': '50'
    }

    def __init__(self, config_path=find_file('config.ini')) -> None:
        """
        Инициализация
        :param config_path: путь до файла с конфигами
        """
        self.config = ConfigParser()
        self.file = config_path
        self.cur_config = ConfigManager.default_config

    def serialize(self) -> None:
        """
        Загрузка текущей конфигурации в парсер
        """
        self.config['DEFAULT'] = self.cur_config

    def deserialize(self) -> None:
        """
        Выгрузка конфигов из парсера в текущую конфигурацию
        """
        self.cur_config = {key.upper(): value for key, value in
                           self.config["DEFAULT"].items()}

    def load_from_file(self) -> None:
        """
        Загрузка конфигов из файла
        """
        self.config.read(self.file)
        self.deserialize()

    def set_consts(self) -> None:
        """
        Установка значений констант файла consts
        """
        c.WIDTH = self.config.getint('DEFAULT', 'WIDTH')
        c.HEIGHT = self.config.getint('DEFAULT', 'HEIGHT')
        c.BALL_RADIUS = self.config.getint('DEFAULT', 'BALL_RADIUS')
        c.FPS_LIMIT = self.config.getint('DEFAULT', 'FPS_LIMIT')
        c.TIME_SPEED = self.config.getfloat('DEFAULT', 'TIME_SPEED')
        c.NODE_CAPACITY = self.config.getint('DEFAULT', 'NODE_CAPACITY')
        c.IS_RENDER_NUMS = self.config.getboolean('DEFAULT', 'IS_RENDER_NUMS')
        c.BALL_COLOR = eval(self.config.get('DEFAULT', 'BALL_COLOR'))
        c.BALL_COLOR_INV = eval(self.config.get('DEFAULT', 'BALL_COLOR_INV'))
        c.IS_GEN = self.config.getboolean('DEFAULT', 'IS_GEN')
        c.BALLS_COUNT = self.config.getint('DEFAULT', 'BALLS_COUNT')
        c.BALL_MIN_RADIUS = self.config.getint('DEFAULT', 'BALL_MIN_RADIUS')
        c.BALL_MAX_RADIUS = self.config.getint('DEFAULT', 'BALL_MAX_RADIUS')
        c.BALL_MIN_VELOCITY = self.config.getint('DEFAULT', 'BALL_MIN_VELOCITY')
        c.BALL_MAX_VELOCITY = self.config.getint('DEFAULT', 'BALL_MAX_VELOCITY')
        c.MAX_COLLISIONS = self.config.getint('DEFAULT', 'MAX_COLLISIONS')

    def set_default(self) -> None:
        """
        Установка в парсер дефолтных значений конфигов
        """
        self.cur_config = ConfigManager.default_config
        self.config['DEFAULT'] = ConfigManager.default_config

    def update_from_dict(self, new_dict) -> None:
        """
        Обновление конфигурации новым словарем конфигов
        :param new_dict: словарь и изменениями в конфигах
        """
        self.cur_config.update(new_dict)
        self.serialize()

    def save_to_file(self) -> None:
        """
        Сохранение в файл конфигов
        """
        with open(self.file, 'w') as file:
            self.config.write(file)


if __name__ == '__main__':
    # config = ConfigParser()
    # config['DEFAULT'] = {
    #     'WIDTH': '800',
    #     'HEIGHT': '600',
    #     'BALL_RADIUS': '10',
    #     'FPS_LIMIT': '60',
    #     'TIME_SPEED': '1',
    #     'NODE_CAPACITY': '2',
    #     'IS_RENDER_NUMS': 'False',
    #     'BALL_COLOR': '(0, 0, 255)',
    #     'BALL_COLOR_INV': '(255, 0, 0)',
    #     'IS_GEN': 'True',
    #     'BALLS_COUNT': '50',
    #     'BALL_MIN_RADIUS': '1',
    #     'BALL_MAX_RADIUS': '50',
    #     'BALL_MIN_VELOCITY': '1',
    #     'BALL_MAX_VELOCITY': '5',
    #     'MAX_COLLISIONS': '50'
    # }
    #
    # with open('config.ini', 'w') as configfile:
    #     config.write(configfile)

    # config.read('config.ini')
    #
    # DEFAULT group

    # print()
    # # 'width, height, ball_radius, fps_limit, time_speed, node_capacity, is_render_nums, ball_color, ball_color_inv, is_gen, gen_count, min_radius, max_radius, min_velocity, max_velocity, max_collisions'
    manager = ConfigManager()
    manager.set_default()
    print(*manager.config["DEFAULT"].items())
