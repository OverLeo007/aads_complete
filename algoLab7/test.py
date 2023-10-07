import pygame as pg
import pygame_menu as pgm


def button_handler():
    print("Button clicked!")


pg.init()
w, h = 500, 500
left_surf_w, left_surf_h = 300, h
menu_w, menu_h = 200, h

main_surface = pg.display.set_mode((w, h))
left_surface = main_surface.subsurface((0, 0, left_surf_w, left_surf_h))
menu_surface = main_surface.subsurface((300, 0, menu_w, menu_h))
menu = pgm.Menu("Bug menu", menu_w, menu_h,
                mouse_motion_selection=True,
                theme=pgm.themes.THEME_SOLARIZED,
                position=(0, 0),
                surface=menu_surface)
menu.add.button("Button1", button_handler)
menu.add.button("Button2", button_handler)
menu.add.button("Button3", button_handler)
menu.add.button("Button4", button_handler)
menu.add.button("Button5", button_handler)

while True:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            exit()
    menu.update(events)
    menu.draw()
    left_surface.fill((255, 255, 0))
    pg.display.flip()
