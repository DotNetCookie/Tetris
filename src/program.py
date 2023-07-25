import pygame
import sys
import os


# get resource path for compiling:
# https://stackoverflow.com/questions/54210392/how-can-i-convert-pygame-to-exe#answer-54926684
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)


pygame.init()
pygame.display.set_caption("DotNetCookie's python tetris")
pygame.display.set_icon(pygame.image.load(resource_path("res/icon.png")))

_mixer = pygame.mixer
_mixer.init()

# Background music
_mixer.music.load(resource_path("res/sounds/music.mp3"))
_mixer.music.play(-1)

# Sound effects
SOUNDS = {
    'row_complete': _mixer.Sound(resource_path("res/sounds/cast_a_spell_sound.wav")),
    'tetromino_placed': _mixer.Sound(resource_path("res/sounds/wave_alert.wav")),
    'tetromino_moved': _mixer.Sound(resource_path("res/sounds/whoosh.wav")),
    'button_click': _mixer.Sound(resource_path("res/sounds/coin.wav")),
    'level_up': _mixer.Sound(resource_path("res/sounds/coin.wav")),
    'game_over': _mixer.Sound(resource_path("res/sounds/donk.wav"))
}


# Sound effect volume
def set_volume(muted):
    if muted:
        for sound in SOUNDS.values():
            sound.set_volume(0)
        _mixer.music.set_volume(0)
    else:
        _mixer.music.set_volume(0.1)
        for sound in SOUNDS.values():
            sound.set_volume(0.2)
        SOUNDS['tetromino_moved'].set_volume(0.05)


CELL_SIZE = 45  # the pixel size of on cell
FIELD_WIDTH = 10  # the amount of cells in width of the field
FIELD_HEIGHT = 20  # the amount of cells in height of the field
FIELD_OFFSET = 8  # the offset from the left side of the screen to the field
FONT = pygame.font.Font(resource_path('res/fonts/GamePlayed.ttf'), 30)
LARGE_FONT = pygame.font.Font(resource_path('res/fonts/GamePlayed.ttf'), 50)

MAX_VERTICAL_COOL_DOWN = 64
MAX_HORIZONTAL_COOL_DOWN = 5

COLORS = {
    'white': pygame.Color(223, 223, 223),
    'pure_white': pygame.Color(255, 255, 255),
    'black': pygame.Color(24, 24, 24),
    'pure_black': pygame.Color(0, 0, 0),
    "dark_grey": pygame.Color(32, 32, 32),
    "grey": pygame.Color(64, 64, 64),
    "light_grey": pygame.Color(96, 96, 96),

    'paste_blue': pygame.Color(128, 128, 223),
    'dark_paste_blue': pygame.Color(96, 96, 191),

    'yellow': pygame.Color(223, 223, 32),
    'orange': pygame.Color(223, 128, 32),
    'red': pygame.Color(223, 32, 32),
    'purple': pygame.Color(223, 32, 223),
    'blue': pygame.Color(32, 32, 223),
    'cyan': pygame.Color(32, 223, 223),
    'green': pygame.Color(32, 223, 32),
}

screen = pygame.display.set_mode((26 * CELL_SIZE, FIELD_HEIGHT * CELL_SIZE))
clock = pygame.time.Clock()
