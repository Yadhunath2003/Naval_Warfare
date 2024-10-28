import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)

bg = pygame.image.load("images/bg.png")
bg2 = pygame.image.load("images/bg2.png")
bg3 = pygame.image.load("images/bg3.png")
bg4 = pygame.image.load("images/bg4.png")

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


class UIElement(Sprite):
    """ An user interface element that can be added to a surface """

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        """
        Args:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            bg_rgb (background colour) - tuple (r, g, b)
            text_rgb (text colour) - tuple (r, g, b)
            action - the gamestate change associated with this button
        """
        self.mouse_over = False

        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        self.images = [default_image, highlighted_image]

        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        self.action = action

        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        """ Updates the mouse_over variable and returns the button's
            action value when clicked.
        """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draws element onto a surface """
        surface.blit(self.image, self.rect)


def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.NEWGAME:
            game_state = game_mode(screen)
            
        if game_state == GameState.AIMODE:
            game_state = ai_mode(screen)
        
        if game_state == GameState.HUMAN:
            game_state = human_mode(screen)

        if game_state == GameState.QUIT:
            pygame.quit()
            return


def title_screen(screen):
    start_btn = UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Start",
        action=GameState.NEWGAME,
    )
    quit_btn = UIElement(
        center_position=(400, 440),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,
    )

    buttons = [start_btn, quit_btn]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.blit(bg, (0, 0))

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()


def game_mode(screen):
    return_btn = UIElement(
        center_position=(80, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="RETURN",
        action=GameState.TITLE,
    )
    
    ai_btn = UIElement(
        center_position=(400, 370),
        font_size=40,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="AI",
        action=GameState.AIMODE,
    )
    human_btn = UIElement(
        center_position=(400, 410),
        font_size=40,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="HUMAN",
        action=GameState.HUMAN,
    )

    buttons = [ai_btn, human_btn]


    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.blit(bg2, (0, 0))

        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action
        return_btn.draw(screen)
        
        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()

def ai_mode(screen):
    return_btn = UIElement(
        center_position=(80, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="RETURN",
        action=GameState.NEWGAME, 
    )
    
    easy_btn = UIElement(
        center_position=(400, 340),
        font_size=40,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="EASY",
        action=GameState.HUMAN, #need to be update
    )
    medium_btn = UIElement(
        center_position=(400, 380),
        font_size=40,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="MEDIUM",
        action=GameState.HUMAN, #need to be update
    )
    hard_btn = UIElement(
        center_position=(400, 420),
        font_size=40,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="HARD",
        action=GameState.HUMAN, #need to be update
    )
    
    buttons = [easy_btn, medium_btn, hard_btn]
    
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.blit(bg3, (0, 0))
        
        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action
        return_btn.draw(screen)
        
        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)
        
        pygame.display.flip()

def human_mode(screen):
    return_btn = UIElement(
        center_position=(80, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="RETURN",
        action=GameState.NEWGAME, 
    )
    
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.blit(bg4, (0, 0))
        
        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action
        return_btn.draw(screen)
        
        pygame.display.flip()

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    AIMODE = 2
    HUMAN = 3


if __name__ == "__main__":
    main()