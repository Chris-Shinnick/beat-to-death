import pygame as pg


def main():
    clock = pg.time.Clock()
    screen = pg.display.set_mode((1600, 900))
    intro_text = [
        "The village executed you for the crime of necromancy",
        "They thought that would be the end of it...",
        "killing... a necromancer",
        "This town sucks. Exact your revenge!"
    ]
    title = "BEAT TO DEATH"
    intro_played = False
    # This surface is used to adjust the alpha of the txt_surf.

    alpha = 255  # The current alpha value of the surface.

    while not intro_played:
        quit_check()
        intro_played = play_intro(screen,clock,intro_text,title)

def fade_text_in(screen,clock,text,loc):
    fade_text(screen,clock,text,loc,0,6)

def fade_text_out(screen,clock,text,loc):
    fade_text(screen,clock,text,loc,255,-4)
def fade_text(screen,clock,orig_surf,loc,alpha,fade_rate):
    
    txt_surf = orig_surf.copy()
    alpha_surf = pg.Surface(txt_surf.get_size(), pg.SRCALPHA)
    while alpha >= 0 and alpha <= 255:
            quit_check()
            # Reduce alpha each frame, but make sure it doesn't get below 0.
            alpha = alpha+fade_rate
            display_alpha = max(0, min(alpha, 255))
            txt_surf = orig_surf.copy()
            # Fill alpha_surf with this color to set its alpha value.
            alpha_surf.fill((255, 255, 255, display_alpha))
            # To make the text surface transparent, blit the transparent
            # alpha_surf onto it with the BLEND_RGBA_MULT flag.
            txt_surf.blit(alpha_surf, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
            screen.fill((30, 30, 30))
            screen.blit(txt_surf, loc)
            pg.display.flip()
            clock.tick(30)

def play_intro(screen,clock,text_array,title):
    w, h = screen.get_size()
    font = pg.font.Font(None, 64)
    color = pg.Color('royalblue')
    title_font = pg.font.Font(None,256)
    title_color = pg.Color('coral4')
    for text in text_array:
        surf = font.render(text, True, color)
        surf_rect = surf.get_rect(center=(w/2,h/2))
        fade_text_in(screen,clock,surf,surf_rect)
        clock.tick(60)
        fade_text_out(screen,clock,surf,surf_rect)
        clock.tick(60)
    surf = title_font.render(title, True, title_color)
    surf_rect = surf.get_rect(center=(w/2,h/2))
    fade_text_in(screen,clock,surf,surf_rect)
    clock.tick(60)
    fade_text_out(screen,clock,surf,surf_rect)
    clock.tick(60)
    return True

def quit_check():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()



if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()