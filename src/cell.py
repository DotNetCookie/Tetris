from src.program import pygame, screen, CELL_SIZE, COLORS


class Cell:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def drawBorders(self, borders):
        # borders
        if borders[0]:  # top
            pygame.draw.rect(screen, self.color, (
                self.x * CELL_SIZE,
                self.y * CELL_SIZE,
                CELL_SIZE,
                4
            ))
        if borders[1]:  # right
            pygame.draw.rect(screen, self.color, (
                self.x * CELL_SIZE + CELL_SIZE - 4,
                self.y * CELL_SIZE,
                4,
                CELL_SIZE
            ))
        if borders[2]:  # bottom
            pygame.draw.rect(screen, self.color, (
                self.x * CELL_SIZE,
                self.y * CELL_SIZE + CELL_SIZE - 4,
                CELL_SIZE,
                4
            ))
        if borders[3]:  # left
            pygame.draw.rect(screen, self.color, (
                self.x * CELL_SIZE,
                self.y * CELL_SIZE,
                4,
                CELL_SIZE
            ))

        # corners
        if self.color != COLORS['yellow']:
            if not borders[0] and not borders[3]:  # Top Left
                pygame.draw.rect(screen, self.color, (
                    self.x * CELL_SIZE,
                    self.y * CELL_SIZE,
                    4,
                    4
                ))
            if not borders[0] and not borders[1]:  # Top Right
                pygame.draw.rect(screen, self.color, (
                    self.x * CELL_SIZE + CELL_SIZE - 4,
                    self.y * CELL_SIZE,
                    4,
                    4
                ))
            if not borders[2] and not borders[1]:  # Bottom Right
                pygame.draw.rect(screen, self.color, (
                    self.x * CELL_SIZE + CELL_SIZE - 4,
                    self.y * CELL_SIZE + CELL_SIZE - 4,
                    4,
                    4
                ))
            if not borders[2] and not borders[3]:  # Bottom Left
                pygame.draw.rect(screen, self.color, (
                    self.x * CELL_SIZE,
                    self.y * CELL_SIZE + CELL_SIZE - 4,
                    4,
                    4
                ))

    def draw(self):
        tmp_color = self.color
        # dark
        pygame.draw.rect(screen, (self.color.r - 32, self.color.g - 32, self.color.b - 32), (
            self.x * CELL_SIZE,
            self.y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        ))
        # light
        pygame.draw.rect(screen, (self.color.r + 32, self.color.g + 32, self.color.b + 32), (
            self.x * CELL_SIZE,
            self.y * CELL_SIZE,
            CELL_SIZE - 4,
            CELL_SIZE - 4
        ))

        # normal
        pygame.draw.rect(screen, self.color, (
            self.x * CELL_SIZE + 4,
            self.y * CELL_SIZE + 4,
            CELL_SIZE - 8,
            CELL_SIZE - 8
        ))

        self.color = tmp_color

    def drop(self):
        self.y += 1

    def collidesWith(self, tetromino):
        for cell in tetromino.shape:
            if cell.x + tetromino.x == self.x and cell.y + tetromino.y == self.y:
                return True
        return False
