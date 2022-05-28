import pygame as pg
pg.font.init()

class intro:
    intro_text = [
        "The village executed you for the crime of necromancy",
        "They thought that would be the end of it...",
        "killing... a necromancer",
        "This town sucks. Exact your revenge!",
        "BEAT TO DEATH"
    ]
    intro_colors = [
        pg.Color('royalblue'),
        pg.Color('royalblue'),
        pg.Color('royalblue'),
        pg.Color('royalblue'),
        pg.Color('coral4')
    ]

    intro_fonts = [
        pg.font.Font(None, 64),
        pg.font.Font(None, 64),
        pg.font.Font(None, 64),
        pg.font.Font(None, 64),
        pg.font.Font(None, 256)
    ]

    intro_surfaces = [
        intro_fonts[0].render(intro_text[0], True, intro_colors[0]),
        intro_fonts[1].render(intro_text[1], True, intro_colors[1]),
        intro_fonts[2].render(intro_text[2], True, intro_colors[2]),
        intro_fonts[3].render(intro_text[3], True, intro_colors[3]),
        intro_fonts[4].render(intro_text[4], True, intro_colors[4])
    ]

    min_alpha = 0
    max_alpha = 255

    def __init__(self):
        self.intro_played = False
        self.current_line = 0
        self.alpha = 0
        self.fade_dir = 1
        self.fade_rate = 6
    def fade_text(self,state):
        self.alpha += (self.fade_dir*self.fade_rate)
        display_alpha = max(0, min(self.alpha, 255))
        txt_surf = self.intro_surfaces[self.current_line].copy()
        #transparency surface
        alpha_surf = pg.Surface(self.intro_surfaces[self.current_line].get_size(), pg.SRCALPHA)
        # Fill alpha_surf with this color to set its alpha value.
        alpha_surf.fill((255, 255, 255, display_alpha))
        txt_surf.blit(alpha_surf, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        state["screen"].blit(txt_surf, txt_surf.get_rect(center=(state["screen_width"]/2,state["screen_height"]/2)))

    def main(self,state):
        for key in state["depressed_keys"]:
            if key == pg.K_ESCAPE:
                if state["depressed_keys"][key] == True:
                    self.intro_played = True
        if self.intro_played:
            state["next_scene"] = 'MAIN_MENU'
        else:
            #fade text one step
            self.fade_text(state)
            #when text is fully faded in, switch to fading out
            if self.alpha > 255:
                self.alpha = 255
                self.fade_dir = -1
            #when text has fully faded out, go to next line
            if self.alpha < 0:
                self.alpha = 0
                self.fade_dir = 1
                self.current_line += 1
                #If there's no line to switch to, tell the game the intro has finished playing
                if self.current_line >= len(self.intro_text):
                    self.intro_played = True
        return state    