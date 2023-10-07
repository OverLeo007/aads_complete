"""
Файл в котором реализовано квадродерево
"""


from typing import List
from itertools import combinations

from quad_tree.figures import Ball, Box
import quad_tree.consts as c
import pygame as pg


class QuadTree:
    class Node:
        def __init__(self, box: Box, parent: "QuadTree.Node" = None) -> None:
            """
            Класс ноды квадродерева
            :param box: ограничивающий прямоугольник
            :param parent: родительская нода
            """
            self.box = box
            self.children: List["QuadTree.Node"] = []
            self.balls: List[Ball] = []
            self.parent = parent

        def compute_children(self):
            """
            Метод рассчета дочерних нод для текущей
            """
            x, y, w, h = self.box.x, self.box.y, self.box.width, self.box.height
            w_2 = w // 2
            h_2 = h // 2
            self.children.append(QuadTree.Node(
                Box(x, y, w_2, h_2), self
            ))
            self.children.append(QuadTree.Node(
                Box(x + w_2, y, w_2, h_2), self
            ))
            self.children.append(QuadTree.Node(
                Box(x, y + h_2, w_2, h_2), self
            ))
            self.children.append(QuadTree.Node(
                Box(x + w_2, y + h_2, w_2, h_2), self
            ))

        def find_children(self, ball: Ball):
            """
            Метод поиска того, в каких дочерних нодах лежит шарик
            :param ball: искомый шарик
            :return: массив из нод
            """
            intersections = []
            for i, child in enumerate(self.children):
                if ball in child:
                    intersections.append(i)

            if not intersections:
                return False
            return intersections

        def __contains__(self, item: Ball) -> bool:
            """
            Проверка на вхождение шарика в ноду
            :param item: шарик
            :return: True/False в зависимости от вердикта
            """
            return item in self.box

        def append(self, ball: Ball) -> None:
            """
            Метод добавления шарика в ноду
            :param ball:
            """
            self.balls.append(ball)

        def is_leaf(self) -> bool:
            """
            Проверка на то имеет ли нода дочерние
            :return: True/False в зависимости от вердикта
            """
            if self.children:
                return False
            return True

        def __repr__(self) -> str:
            """
            Текстовое представление ноды
            """
            return f"Node(" \
                   f"parent={self.parent}," \
                   f"box={self.box}, " \
                   f"balls={len(self.balls)}" \
                   f")"

    def __init__(self, screen: pg.display):
        self.root_node = QuadTree.Node(Box(0, 0, c.WIDTH, c.HEIGHT))
        self.screen = screen
        self.node_capacity = c.NODE_CAPACITY

    def insert(self, ball: Ball):
        """
        Метод вставки шарика в нужную ноду
        :param ball: вставляемый шарик
        """
        def insert_inner(node: "QuadTree.Node", inner_ball: Ball):
            """
            внутренняя рекурсивная функция вставки
            :param node: текущая нода
            :param inner_ball: шарик
            """
            if inner_ball not in node:
                return False

            if len(node.balls) < self.node_capacity or \
                    node.box.max_side < c.BALL_RADIUS:
                node.append(inner_ball)
            else:
                if not node.children:
                    node.compute_children()
                child_nums = node.find_children(inner_ball)
                if child_nums is not False:
                    for child_num in child_nums:
                        insert_inner(node.children[child_num],
                                     inner_ball)
                else:
                    return False

        insert_inner(self.root_node, ball)

    # def find_intersections(self):
    #
    #     def collide(balls: List[Ball], collided=None):
    #         if collided is None:
    #             collided = []
    #
    #
    #         for ball1, ball2 in combinations(balls, 2):
    #             ball1.collide(ball2)
    #             collided.append((ball1, ball2))
    #         return collided
    #
    #
    #     def find_inner(cur_node: "QuadTree.Node" = self.root_node):
    #         cur_node_balls = cur_node.balls
    #
    #
    #         if cur_node.is_leaf():
    #
    #     find_inner()

    def find_leaves(self):
        """
        Метод поиска всех нод без дочерних нод
        :return: список таковых
        """
        def find_leaves_inner(cur_node: "QuadTree.Node"):
            """
            Внутренняя рекурсивная функция
            :param cur_node: текущая нода
            :return: список листьев текущей ноды
            """
            if cur_node.is_leaf():
                if len(cur_node.balls) > 0:
                    return [cur_node]
                else:
                    return []
            else:
                leaves = []
                for child in cur_node.children:
                    leaves.extend(find_leaves_inner(child))
                return leaves

        return find_leaves_inner(self.root_node)

    def find_intersections(self):
        """
        Метод поиска возможных пересечений, отбирает шарики
        на проверку пересечений исходя из их положения в дереве
        :return:
        """
        def find_balls_to_intersect(leaf_to_find: "QuadTree.Node"):
            """
            Функция, проходящаяся от листка корню,
            собирающая все шарики по пути
            :param leaf_to_find: лист из которого идем
            :return: кортеж из шариков
            """
            balls = []
            while leaf_to_find is not None:
                balls.extend(leaf_to_find.balls)
                leaf_to_find = leaf_to_find.parent
            return tuple(balls)

        leaves = self.find_leaves()
        to_check_collides = []
        for leaf in leaves:
            inter_list = find_balls_to_intersect(leaf)
            # for ball1, ball2 in itertools.combinations(inter_list, 2):
            #     ball1.collide(ball2)
            to_check_collides.append(inter_list)

        to_check_collides = list(set(to_check_collides))

        for ball_seq in to_check_collides:
            for ball1, ball2 in combinations(ball_seq, 2):
                ball1.collide(ball2)
        return to_check_collides

    def render(self, cur_node: "QuadTree.Node" = None):
        """
        Рекурсивный метод отрисовки дерева
        :param cur_node: текущая нода для отрисовки
        """
        if cur_node is None:
            cur_node = self.root_node
        cur_node.box.render(self.screen)
        if cur_node.children:
            for child in cur_node.children:
                self.render(child)

    def print_nodes(self):

        def _print_nodes(node: "QuadTree.Node", depth=0):
            print("\t" * depth, node)
            for child in node.children:
                _print_nodes(child, depth + 1)

        _print_nodes(self.root_node)
        print("#" * 20)

    def upd(self, balls: List[Ball]):
        """
        Метод обновления дерева списком шаров
        :param balls:
        """
        self.root_node = QuadTree.Node(Box(0, 0, c.WIDTH, c.HEIGHT))
        for ball in balls:
            self.insert(ball)
