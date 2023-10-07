"""
Файл, содержащий функцию - генератор шариков
"""

from typing import List

from quad_tree.figures import Ball, Vec2
import random as rand
from math import pi, sin, cos


def generate_balls(screen, ball_count: int,
                   min_size: int, max_size: int,
                   min_velocity: int, max_velocity: int) -> List[Ball]:
    """
    Функция генерации списка шарика с заданными параметрами
    :param screen: экран, на который рисуются шарики
    :param ball_count: кол-во шариков
    :param min_size: минимальный радиус шарика
    :param max_size: максимальный радиус шарика
    :param min_velocity: минимальная скорость шарика
    :param max_velocity: максимальная скорость шарика
    :return: список сгенерированных шариков
    """
    def generate_random_ball(b_id):
        """
        Внутренняя функция генерации шарика, генерирует шарик с заданными параметрами
        :param b_id: айди шарика
        :return: готовый шарик
        """
        width, height = screen.get_size()
        radius = rand.randint(min_size, max_size)
        b_x = rand.randint(radius, width - radius)
        b_y = rand.randint(radius, height - radius)
        r_angle = rand.uniform(0, 2 * pi)
        d_x = cos(r_angle) * rand.uniform(min_velocity, max_velocity)
        d_y = sin(r_angle) * rand.uniform(min_velocity, max_velocity)
        vel = Vec2(d_x, d_y)
        return Ball(screen, b_x, b_y, vel, radius, b_id)

    return [generate_random_ball(i) for i in range(ball_count)]
