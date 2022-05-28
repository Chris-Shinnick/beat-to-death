import pygame as pg
import intro
import menu


def main():
    state = {}
    state["clock"] = pg.time.Clock()
    state["screen"] = pg.display.set_mode((1600, 900))
    state["screen"].fill((30, 30, 30))
    state["screen_width"], state["screen_height"] = state["screen"].get_size()
    state["scene"] = intro.intro()
    state["next_scene"] = None
    state["depressed_keys"] = {}
    state["controls"] = {
        "up" : pg.K_UP,
        "down" : pg.K_DOWN,
        "left" : pg.K_LEFT,
        "right" : pg.K_RIGHT,
        "hihat" : pg.K_q,
        "snare" : pg.K_w,
        "tom_one" : pg.K_e,
        "tom_two" : pg.K_r,
        "floor_tom" : pg.K_d,
        "cymbal" : pg.K_f,
        "gather_bones" : pg.K_1,
        "hurl_femur" : pg.K_2,
        "summon_archer" : pg.K_3,
        "summon_zombie" : pg.K_4,
        "build_catapult" : pg.K_5,
        "deep_freeze" : pg.K_6,
        "frenzy" : pg.K_7,
    }

    while True:
        state["depressed_keys"] = handle_input(state["depressed_keys"])
        state["screen"].fill((30, 30, 30))
        state = update(state)
        pg.display.update()
        state["clock"].tick(30)

def scene_change(state):
    if state["next_scene"] == "INTRO":
        state["scene"] = intro.intro()
    elif state["next_scene"] == "MAIN_MENU":
        state["scene"] = menu.main_menu(state)
    elif state["next_scene"] == "CONTROLS_MENU":
        state["scene"] = menu.controls_menu(state)
    else:
        pg.quit()
    state["next_scene"] = None
    return state

def handle_input(depressed_keys):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.KEYDOWN:
            depressed_keys[event.key] = True
        if event.type == pg.KEYUP:
            depressed_keys[event.key] = False
    return depressed_keys


def update(state):
    if state["next_scene"] is not None:
        state = scene_change(state)
    new_state = state["scene"].main(state)
    return new_state




if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()