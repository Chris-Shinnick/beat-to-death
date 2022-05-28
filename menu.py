import pygame as pg
pg.font.init()
from collections import OrderedDict

class menu:
    button_color = pg.Color('ivory4')
    active_button_color = pg.Color('ivory3')
    button_height = pg.font.Font(None, 64).size("TEST")[1]
    button_offset = 20
    menu_delay = 6
    action_ready_in = 0
    def __init__(self,menu_top,menu_center,button_odict):
        self.menu_top = menu_top
        self.menu_center = menu_center
        self.buttons = []
        self.button_center = [menu_center,menu_top+self.button_height/2]
        self.active_button = None
        for label, destination in button_odict.items():
            next_button = menu_button(label,destination,self.button_center,self.button_color)
            self.button_center = [self.button_center[0],self.button_center[1]+self.button_height+self.button_offset]
            self.buttons.append(next_button)
        self.active_button = self.buttons[0]
        


    def main(self,state):
        self.action_ready_in = max(self.action_ready_in - 1, 0)
        for key in state["depressed_keys"]:
            if key == pg.K_RETURN:
                if state["depressed_keys"][key] == True:
                    state["depressed_keys"][key] = False
                    state = self.active_button.press(state)
            elif self.action_ready_in == 0 and key == pg.K_DOWN:
                 if state["depressed_keys"][key] == True:
                    button_index = min(
                        self.buttons.index(self.active_button)+1,
                        len(self.buttons)-1,
                        )
                    self.active_button = self.buttons[button_index]
                    self.action_ready_in += self.menu_delay
            elif self.action_ready_in == 0 and key == pg.K_UP:
                 if state["depressed_keys"][key] == True:
                    button_index = max(
                        self.buttons.index(self.active_button)-1,
                        0
                        )
                    self.active_button = self.buttons[button_index]
                    self.action_ready_in += self.menu_delay
        for button in self.buttons:
            if button == self.active_button:
                button.set_color(self.active_button_color)
            else:
                button.set_color(self.button_color)
            button.draw(state)
        return state

class controls_menu(menu):
    menu_title = pg.font.Font(None,128).render("CONTROLS",True,pg.Color('ivory3'))
    button_odict = OrderedDict()
    button_odict['Change controls'] = ['CONTROLS_UPDATE']
    button_odict['Return To Main Menu'] = 'MAIN_MENU'
    def __init__(self,state):
    #layout: control list is centered vertically, with title offset slightly above and menu options slightly below
        control_font = pg.font.Font(None,64)
        control_color = pg.Color('darkslategray4')
        self.drum_list = [
            control_font.render("Move Up(Bass): " + pg.key.name(state["controls"]["up"]),True,control_color),
            control_font.render("Move Down(Bass): " + pg.key.name(state["controls"]["down"]),True,control_color),
            control_font.render("Move Left(Bass): " + pg.key.name(state["controls"]["left"]),True,control_color),
            control_font.render("Move Right(Bass): " + pg.key.name(state["controls"]["right"]),True,control_color),
            control_font.render("Hi-Hat: " + pg.key.name(state["controls"]["hihat"]),True,control_color),
            control_font.render("Snare: " + pg.key.name(state["controls"]["snare"]),True,control_color),
            control_font.render("Tom Drum One: " + pg.key.name(state["controls"]["tom_one"]),True,control_color),
            control_font.render("Tom Drum Two: " + pg.key.name(state["controls"]["tom_two"]),True,control_color),
            control_font.render("Floor Tom: " + pg.key.name(state["controls"]["floor_tom"]),True,control_color),
            control_font.render("Crash Cymbal: " + pg.key.name(state["controls"]["cymbal"]),True,control_color)
        ]
        self.pattern_list = [
            control_font.render("Gather Bones: " + pg.key.name(state["controls"]["gather_bones"]),True,control_color),
            control_font.render("Hurl Femur: " + pg.key.name(state["controls"]["hurl_femur"]),True,control_color),
            control_font.render("Summon Archer: " + pg.key.name(state["controls"]["summon_archer"]),True,control_color),
            control_font.render("Summon Zombie: " + pg.key.name(state["controls"]["summon_zombie"]),True,control_color),
            control_font.render("Build Skull Catapult: " + pg.key.name(state["controls"]["build_catapult"]),True,control_color),
            control_font.render("Cast Deep Freeze: " + pg.key.name(state["controls"]["deep_freeze"]),True,control_color),
            control_font.render("Cast Skeletal Frenzy: " + pg.key.name(state["controls"]["frenzy"]),True,control_color)
        ]
        self.control_line_height = pg.font.Font(None, 64).size("LINE HEIGHT TEST")[1]
        self.control_line_offset = 10
        control_box_height = max((self.control_line_height+self.control_line_offset)*len(self.drum_list)-self.control_line_offset,
                                (self.control_line_height+self.control_line_offset)*len(self.pattern_list)-self.control_line_offset)
        self.control_box_top = state["screen_height"]/2 - control_box_height/2
        self.menu_center = state["screen_width"]/2
        self.menu_top = self.control_box_top + control_box_height + 20
        self.title_center_y = self.control_box_top - self.menu_title.get_height() - 20
        menu.__init__(self,self.menu_top,self.menu_center,self.button_odict)

    def draw_text_boxes(self,state,boxes,center_x):
        next_box_top = self.control_box_top
        for text in boxes:
            state["screen"].blit(text,text.get_rect(center = [center_x,next_box_top]))
            next_box_top += (self.control_line_height + self.control_line_offset)

    def main(self,state):
        state["screen"].blit(self.menu_title,self.menu_title.get_rect(center = [self.menu_center,self.title_center_y]))
        self.draw_text_boxes(state,self.drum_list,state["screen_width"]/4)
        self.draw_text_boxes(state,self.pattern_list,state["screen_width"]*3/4)
        return menu.main(self,state)



class main_menu(menu):
    menu_title =  pg.font.Font(None, 192).render("BEAT TO DEATH", True,pg.Color('coral4'))
    button_odict = OrderedDict()
    button_odict['Start Game'] = 'QUIT'
    button_odict['Controls'] = 'CONTROLS_MENU'
    button_odict['Replay Intro'] = 'INTRO'
    button_odict['Credits'] = 'QUIT'
    button_odict['Exit Game'] = 'QUIT'
    def __init__(self,state):
        self.menu_center = state["screen_width"]/2
        self.menu_top = state["screen_height"]/2 - 50
        menu.__init__(self,self.menu_top,self.menu_center,self.button_odict)
    
    def main(self,state):
        state["screen"].blit(self.menu_title,self.menu_title.get_rect(center = [self.menu_center,200]))
        return menu.main(self,state)




class menu_button:
    def __init__(self,text,scene_name,center,color):
        self.display_text = text
        self.target_scene = scene_name
        self.center = center
        self.color = color
        self.txt_surf = pg.font.Font(None, 64).render(self.display_text, True, self.color)
        pass

    def get_text(self):
        return self.display_text
    
    def get_color(self):
        return self.color

    def set_color(self,color):
        self.color = color
        self.txt_surf = pg.font.Font(None, 64).render(self.display_text, True, self.color)

    def draw(self,state):
        state["screen"].blit(self.txt_surf, self.txt_surf.get_rect(center=(self.center)))

    def press(self,state):
        state["next_scene"] = self.target_scene
        return state



