"""
Файл с примитивами
Vec2 - двумерный вектор
Ball - класс шарика
Box - класс ограничивающего прямоугольника для ноды квадродерева
TextBlock - блок текст для отрисовки в pygame
"""
from typing import List

import pygame as pg
from pygame.math import Vector2

import quad_tree.consts as c


class Vec2(Vector2):
    def __init__(self, x, y) -> None:
        """
        Инициализация вектора
        """
        super(Vec2, self).__init__(x, y)

    def __len__(self) -> float:
        """
        Длина вектора в геометрическом смысле
        """
        return self.length()

    def __repr__(self) -> str:
        """
        Текстовое представление вектора
        """
        return f"Vec2(x={self.x}, y={self.y})"

    def invert_x(self) -> None:
        """
        Инвертирование вектора по оси x
        """
        self.x = -self.x

    def invert_y(self) -> None:
        """
        Инвертирование вектора по оси y
        """
        self.y = -self.y


class Ball:
    def __init__(self, screen: pg.display,
                 pos_x: float,
                 pos_y: float,
                 velocity: Vec2,
                 radius: int = c.BALL_RADIUS,
                 b_id=0) -> None:
        """
        Класс шарика, поддерживающего столкновения
        :param screen: экран, куда будет отрисован шарик
        :param pos_x: позиция центра по x
        :param pos_y: позиция центра по y
        :param velocity: вектор скорости (и направления)
        :param radius: радиус шарика
        :param b_id: айди шарика
        """
        self.screen = screen
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.velocity = velocity
        self.radius = radius
        self.max_x, self.max_y = self.screen.get_size()
        self.b_id = b_id
        self.mass = self.radius * 10
        self.text = pg.font.SysFont("Comic Sans", 12) \
            .render(str(self.b_id), True, (0, 0, 0))
        self.collisions_count = 0
        self.color_progress = .0

        self.is_collided = False

    def move(self) -> None:
        """
        Движения шарика с учетом глобальной скорости времени.
        Обрабатывает столкновения со стенками
        """
        self.pos_x += self.velocity.x * c.TIME_SPEED
        self.pos_y += self.velocity.y * c.TIME_SPEED

        if not self.radius <= self.pos_x <= self.max_x - self.radius:
            if (dif := self.pos_x - self.radius) < 0:
                self.pos_x -= dif
            elif self.pos_x + self.radius > self.max_x:
                self.pos_x -= self.radius - (self.max_x - self.pos_x)
            self.is_collided = not self.is_collided
            if c.TIME_SPEED > 0:
                self.collisions_count += 1
            else:
                self.collisions_count -= 1
            self.velocity.invert_x()

        if not self.radius <= self.pos_y <= self.max_y - self.radius:
            if (dif := self.pos_y - self.radius) < 0:
                self.pos_y -= dif
            elif self.pos_y + self.radius > self.max_y:
                self.pos_y -= self.radius - (self.max_y - self.pos_y)
            self.is_collided = not self.is_collided
            if c.TIME_SPEED > 0:
                self.collisions_count += 1
            else:
                self.collisions_count -= 1
            self.velocity.invert_y()
        self.render()

    def render(self) -> None:
        """
        Функция отрисовки шарика, изменяет его цвет
        в зависимости от кол-ва столкновений
        """
        if self.collisions_count < 0:
            self.collisions_count = 0
        if self.collisions_count > c.MAX_COLLISIONS:
            self.collisions_count = c.MAX_COLLISIONS

        self.color_progress = min(self.collisions_count / c.MAX_COLLISIONS, 1.0)

        r = int((1 - self.color_progress) * c.BALL_COLOR[0] +
                self.color_progress * c.BALL_COLOR_INV[0])
        g = int((1 - self.color_progress) * c.BALL_COLOR[1] +
                self.color_progress * c.BALL_COLOR_INV[1])
        b = int((1 - self.color_progress) * c.BALL_COLOR[2] +
                self.color_progress * c.BALL_COLOR_INV[2])

        color = (r, g, b)

        ball_rect = pg.draw.circle(self.screen, color, (self.pos_x, self.pos_y),
                                   self.radius)
        if c.IS_RENDER_NUMS:
            text_rect = self.text.get_rect(center=ball_rect.center)
            self.screen.blit(self.text, text_rect)

    def __repr__(self) -> str:
        """
        Тектовое представление шарика
        :return:
        """
        return f"Ball_{self.b_id}"

    def __eq__(self, other) -> bool:
        """
        Проверка двух шариков на эквивалентность
        :param other: другой шарик
        :return: True/False в зависимости от вердикта
        """
        if hasattr(other, "b_id") and self.b_id == other.b_id:
            return True
        return False

    def __hash__(self) -> int:
        """
        Вычисление хэша айди шарика для set()
        :return: хэш шарика
        """
        return hash(self.b_id)

    def collide(self, other: "Ball") -> None:
        """
        Метод обработки столкновения с другим шариком, производит столкновение
        с учетом закона сохранения импульса
        :param other: другой шарик
        """
        dist = ((self.pos_x - other.pos_x) ** 2 +
                (self.pos_y - other.pos_y) ** 2) ** 0.5
        if dist > self.radius + other.radius or dist == 0:
            return

        # remove_overlap
        overlap = (dist - self.radius - other.radius) * 0.5
        x_over = overlap * (self.pos_x - other.pos_x) / dist
        y_over = overlap * (self.pos_y - other.pos_y) / dist

        self.pos_x -= x_over
        self.pos_y -= y_over
        other.pos_x += x_over
        other.pos_y += y_over

        # recount_velocity
        dist = self.radius + other.radius

        norm_x = (other.pos_x - self.pos_x) / dist
        norm_y = (other.pos_y - self.pos_y) / dist

        tang_x = -norm_y
        tang_y = norm_x

        tang_scalar_self = self.velocity.x * tang_x + self.velocity.y * tang_y
        tang_scalar_other = other.velocity.x * tang_x + other.velocity.y * tang_y

        norm_scalar_self = self.velocity.x * norm_x + self.velocity.y * norm_y
        norm_scalar_other = other.velocity.x * norm_x + other.velocity.y * norm_y

        mass_scalar_self = (norm_scalar_self * (self.mass - other.mass) +
                            2 * other.mass * norm_scalar_other) / (
                                   self.mass + other.mass)
        mass_scalar_other = (norm_scalar_other * (other.mass - self.mass) +
                             2 * self.mass * norm_scalar_self) / (
                                    self.mass + other.mass)

        self.velocity = Vec2(tang_x * tang_scalar_self + norm_x * mass_scalar_self,
                             tang_y * tang_scalar_self + norm_y * mass_scalar_self)

        other.velocity = Vec2(
            tang_x * tang_scalar_other + norm_x * mass_scalar_other,
            tang_y * tang_scalar_other + norm_y * mass_scalar_other)

        self.is_collided = not self.is_collided
        other.is_collided = not other.is_collided
        if c.TIME_SPEED > 0:
            self.collisions_count += 1
            other.collisions_count += 1

        else:
            self.collisions_count -= 1
            other.collisions_count -= 1
        #
        # distance = ((self.pos_x - other.pos_x) ** 2 + (
        #         self.pos_y - other.pos_y) ** 2) ** 0.5
        # if distance < self.radius * 2 \
        #         and not self.is_collided \
        #         and not other.is_collided:
        #
        #     print(self, other, "Collided")
        #
        #     self.is_collided = True
        #     other.is_collided = True
        #
        #     norm = self.velocity - other.velocity
        #     self.velocity = self.velocity.reflect(norm)
        #     other.velocity = other.velocity.reflect(norm)
        #
        #     overlap = (self.radius * 2 - distance) / 2
        #
        #     if overlap > 2:
        #         dist_v = Vector2(abs(self.pos_x - other.pos_x),
        #                          abs(self.pos_y - other.pos_y))
        #         try:
        #             dist_v.normalize_ip()
        #         except ValueError:
        #             return
        #         x, y = dist_v.xy
        #         dist_v_len = dist_v.length()
        #         dif_x = overlap * (x / dist_v_len)
        #         dif_y = overlap * (y / dist_v_len)
        #         self.pos_x += dif_x
        #         self.pos_y += dif_y
        #         other.pos_x -= dif_x
        #         other.pos_y -= dif_y


class Box:
    def __init__(self, x, y, box_width, box_height) -> None:
        """
        Клас ограничивающего прямоугольника ноды квадродерева
        :param x: позиция левого верхнего угла по x
        :param y: позиция левого верхнего угла по y
        :param box_width: ширина
        :param box_height: высота
        """
        self.x, self.y = x, y
        self.width, self.height = box_width, box_height
        self.max_side = max(self.width, self.height)

    def __contains__(self, ball: Ball) -> bool:
        """
        Проверка на то, что шарик пересекается с боксом
        с учетом всей площади шарика
        :param ball: проверяемый шарик
        :return: True/False в зависимости от вердикта
        """
        x_dist = abs(ball.pos_x - (self.x + self.width / 2))
        y_dist = abs(ball.pos_y - (self.y + self.height / 2))
        if x_dist > (self.width / 2 + ball.radius):
            return False
        if y_dist > (self.height / 2 + ball.radius):
            return False
        if x_dist <= (self.width / 2):
            return True
        if y_dist <= (self.height / 2):
            return True
        corner_dist_sq = (x_dist - self.width / 2) ** 2 + (
                y_dist - self.height / 2) ** 2
        return corner_dist_sq <= (ball.radius ** 2)

    def render(self, screen: pg.display) -> None:
        """
        Рендер коробки
        :param screen:
        """
        box_rect = pg.Rect(self.x, self.y, self.width, self.height)
        pg.draw.rect(screen, (255, 255, 255), box_rect, 1)

    def __repr__(self) -> str:
        """
        Текстовое представление коробки
        """
        return f"Box({self.x}, {self.y}, {self.width}, {self.height})"


class TextBlock:
    def __init__(self) -> None:
        """
        Класс отрисовки многострочного текста
        """
        self.clock = pg.time.Clock()
        self.font_size = 20
        self.font = pg.font.SysFont("Comic Sans", self.font_size)

    def render(self, display, text: List[str]) -> None:
        """
        Рисует текст на определенный дисплей
        :param display: дисплей, куда рисуем
        :param text: рисуемый текст
        """
        rendered_text = [
            self.font.render("FPS: " + str(round(self.clock.get_fps(), 2)),
                             True,
                             (255, 255, 255))]
        for line in text:
            rendered_text.append(self.font.render(line, True, (255, 255, 255)))

        for pos_y, line in enumerate(rendered_text):
            display.blit(line, (10, (10 + self.font_size) * pos_y))

    def tick(self, fps) -> None:
        """
        Задержка для фпс
        :param fps: значение фпс
        """
        self.clock.tick(fps)
