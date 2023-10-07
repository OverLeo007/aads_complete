"""
Файл с функцией рантайма пайгейма
"""

import sys
import cProfile

import pygame as pg
import random as rand

from quad_tree.gifer import GifSaver
import quad_tree.consts as c
from quad_tree.figures import Ball, Vec2, TextBlock
from quad_tree.tree import QuadTree
from quad_tree.balls_generator import generate_balls


# def set_consts_from_file()


def run():
    """
    Функция, в которой все и происходит
    """
    pg.init()
    screen = pg.display.set_mode((c.WIDTH, c.HEIGHT))
    pg.display.set_caption("Симуляция столкновений")
    gifer = GifSaver("images", c.WIDTH, c.HEIGHT)
    text_block = TextBlock()
    balls = []

    q_tree = QuadTree(screen)
    if c.IS_GEN:
        balls = generate_balls(screen,
                               c.BALLS_COUNT,
                               c.BALL_MIN_RADIUS,
                               c.BALL_MAX_RADIUS,
                               c.BALL_MIN_VELOCITY,
                               c.BALL_MAX_VELOCITY)

    is_recording = False
    is_tree_render = True

    start_pos = None, None
    finish_pos = None, None
    spawn_radius = c.BALL_RADIUS
    cur_pos = None

    none_point = None, None
    do_time = True

    while True:

        b_len = len(balls)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            left_butt, mid_butt, right_butt = pg.mouse.get_pressed(3)
            mods = pg.key.get_mods()

            if left_butt is True and start_pos != none_point and hasattr(event, "pos"):
                cur_pos = event.pos

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == pg.BUTTON_LEFT:
                    start_pos = event.pos

                if event.button == pg.BUTTON_RIGHT:
                    if balls:
                        balls.pop()

            if event.type == pg.MOUSEBUTTONUP:

                if left_butt is False and event.button == pg.BUTTON_LEFT:
                    finish_pos = event.pos

            if event.type == pg.MOUSEWHEEL:
                if start_pos == none_point:
                    if mods & pg.KMOD_SHIFT:
                        c.TIME_SPEED += event.y / 100
                    else:
                        c.TIME_SPEED += event.y / 10
                else:
                    spawn_radius += event.y * 1.5

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    is_recording = not is_recording
                if event.key == pg.K_SPACE:
                    do_time = not do_time

                if event.key == pg.K_t:
                    is_tree_render = not is_tree_render

                if event.key == pg.K_UP:
                    c.BALL_RADIUS += 5

                if event.key == pg.K_DOWN:
                    c.BALL_RADIUS -= 5

        if is_recording:
            gifer.add_img(pg.image.tostring(screen, "RGBA"))

        screen.fill((0, 0, 0))

        # Определяем новый шарик
        if start_pos != none_point and \
                finish_pos == none_point and \
                event.type != pg.WINDOWLEAVE:

            pg.draw.line(screen, c.BALL_COLOR_INV, start_pos,
                         event.pos if hasattr(event, "pos") else cur_pos)
            pg.draw.circle(screen,
                           color=c.BALL_COLOR,
                           center=start_pos,
                           radius=spawn_radius,
                           width=1)

        # запускаем шарик
        if start_pos != none_point and finish_pos != none_point:
            vel = Vec2((finish_pos[0] - start_pos[0]) / (c.WIDTH // 10),
                       (finish_pos[1] - start_pos[1]) / (c.HEIGHT // 10))
            b_x, b_y = start_pos
            balls.append(Ball(screen, b_x, b_y, vel, radius=spawn_radius, b_id=len(balls)))

            start_pos, finish_pos = none_point, none_point

        if do_time:
            for ball in balls:
                ball.move()
        else:
            for ball in balls:
                ball.render()

        if len(balls) != b_len:
            q_tree.upd(balls)
            # q_tree.print_nodes()

        if do_time:
            q_tree.upd(balls)
            q_tree.find_intersections()

        if is_tree_render:
            q_tree.render()

        text_block.render(screen, [f"Balls count: {len(balls)}",
                                   f"Time speed: {c.TIME_SPEED * 10:.1f}"])

        for ball in balls:
            if ball.color_progress == 1:
                ball.color_progress = .0

        pg.display.update()
        text_block.tick(c.FPS_LIMIT)


if __name__ == '__main__':
    run()
    # cProfile.run("main()")
