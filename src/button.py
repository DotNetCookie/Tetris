from src.program import pygame, FONT, screen, CELL_SIZE, FIELD_WIDTH, FIELD_OFFSET, COLORS, SOUNDS


class Button:
    def __init__(self, text, rect):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.color = COLORS['paste_blue']

    def draw(self):
        # dark
        pygame.draw.rect(screen, (self.color.r - 32, self.color.g - 32, self.color.b - 32), self.rect)
        # light
        pygame.draw.rect(screen, (self.color.r + 32, self.color.g + 32, self.color.b + 32), (
            self.rect.x, self.rect.y, self.rect.w - 8, self.rect.h - 8
        ))
        # normal
        pygame.draw.rect(screen, self.color, (
            self.rect.x + 8, self.rect.y + 8, self.rect.w - 16, self.rect.h - 16
        ))

        render = FONT.render(self.text, True, (255, 255, 255))
        screen.blit(render, (
            self.rect.x + self.rect.w / 2 - render.get_width() / 2,
            self.rect.y + self.rect.h / 2 - render.get_height() / 2
        ))

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = self.rect.collidepoint(pygame.mouse.get_pos()) and self.color == COLORS['dark_paste_blue']

            if clicked:
                SOUNDS['button_click'].play()

            self.color = COLORS['paste_blue']
            return clicked

        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color = COLORS['dark_paste_blue']

        return False


start_button = Button("START", (
    FIELD_OFFSET * CELL_SIZE + CELL_SIZE,
    10 * CELL_SIZE,
    (FIELD_WIDTH - 2) * CELL_SIZE,
    2 * CELL_SIZE
))

quit_button = Button("QUIT", (
    FIELD_OFFSET * CELL_SIZE + CELL_SIZE,
    13 * CELL_SIZE,
    (FIELD_WIDTH - 2) * CELL_SIZE,
    2 * CELL_SIZE
))

resume_button = Button("RESUME", (
    FIELD_OFFSET * CELL_SIZE + CELL_SIZE,
    7 * CELL_SIZE,
    (FIELD_WIDTH - 2) * CELL_SIZE,
    2 * CELL_SIZE
))

restart_button = Button("RESTART", (
    FIELD_OFFSET * CELL_SIZE + CELL_SIZE,
    10 * CELL_SIZE,
    (FIELD_WIDTH - 2) * CELL_SIZE,
    2 * CELL_SIZE
))

return_button = Button("RETURN TO MENU", (
    FIELD_OFFSET * CELL_SIZE + CELL_SIZE,
    13 * CELL_SIZE,
    (FIELD_WIDTH - 2) * CELL_SIZE,
    2 * CELL_SIZE
))

game_over_button = Button("CONTINUE", (
    FIELD_OFFSET * CELL_SIZE + CELL_SIZE,
    8 * CELL_SIZE + CELL_SIZE,
    (FIELD_WIDTH - 2) * CELL_SIZE,
    2 * CELL_SIZE
))

mute_button = Button("MUTE", (
    2 * CELL_SIZE,
    2 * CELL_SIZE,
    4 * CELL_SIZE,
    2 * CELL_SIZE
))
