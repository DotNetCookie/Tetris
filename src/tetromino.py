import time
import random

from src.cell import Cell
from src.program import pygame, FIELD_WIDTH, FIELD_HEIGHT, FIELD_OFFSET, SOUNDS, COLORS, screen, CELL_SIZE

TETROMINO_TEMPLATES = {
    # X -
    # X X X
    'lRight': {
        'cells': [
            [(0, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (2, 2)],
            [(1, 0), (1, 1), (1, 2), (0, 2)]
        ],
        'color': COLORS['blue']
    },
    #   - X
    # X X X
    'lLeft': {
        'cells': [
            [(0, 1), (1, 1), (2, 1), (2, 0)],
            [(1, 0), (1, 1), (1, 2), (2, 2)],
            [(0, 1), (1, 1), (2, 1), (0, 2)],
            [(0, 0), (1, 0), (1, 1), (1, 2)]
        ],
        'color': COLORS['orange']
    },
    # O X
    # X X
    'square': {
        'cells': [
            [(0, 0), (0, 1), (1, 0), (1, 1)],
            [(0, 0), (0, 1), (1, 0), (1, 1)],
            [(0, 0), (0, 1), (1, 0), (1, 1)],
            [(0, 0), (0, 1), (1, 0), (1, 1)]
        ],
        'color': COLORS['yellow']
    },
    # X O X X
    'line': {
        'cells': [
            [(0, 1), (1, 1), (2, 1), (3, 1)],
            [(1, 0), (1, 1), (1, 2), (1, 3)],
            [(-1, 1), (0, 1), (1, 1), (2, 1)],
            [(1, -1), (1, 0), (1, 1), (1, 2)]
        ],
        'color': COLORS['cyan']
    },
    #   X
    # X X O
    'pyramid': {
        'cells': [
            [(0, 1), (1, 1), (2, 1), (1, 0)],
            [(1, 0), (1, 1), (1, 2), (2, 1)],
            [(0, 1), (1, 1), (2, 1), (1, 2)],
            [(1, 0), (1, 1), (1, 2), (0, 1)]
        ],
        'color': COLORS['purple']
    },
    # X O
    #   X X
    'stairRight': {
        'cells': [
            [(0, 0), (1, 0), (1, 1), (2, 1)],
            [(2, 0), (2, 1), (1, 1), (1, 2)],
            [(0, 1), (1, 1), (1, 2), (2, 2)],
            [(1, 0), (1, 1), (0, 1), (0, 2)]
        ],
        'color': COLORS['green']
    },
    #   O X
    # X X
    'stairLeft': {
        'cells': [
            [(0, 1), (1, 0), (1, 1), (2, 0)],
            [(1, 0), (1, 1), (2, 1), (2, 2)],
            [(0, 2), (1, 2), (1, 1), (2, 1)],
            [(0, 0), (0, 1), (1, 1), (1, 2)]
        ],
        'color': COLORS['red']
    }
}


class Tetromino:
    def __init__(self, template):
        self.swap_enabled = True
        self.next_tetrominos = []

        self.x = FIELD_WIDTH / 2 - 1
        self.y = -1

        self.rotation = 0

        if template is None:
            template = random.choice(list(TETROMINO_TEMPLATES.values()))
            for i in range(3):
                self.next_tetrominos.append(random.choice(list(TETROMINO_TEMPLATES.values())))

        self.shape_rotations = []

        for i in range(len(template['cells'])):
            self.shape_rotations.append([])
            for cell in template['cells'][i]:
                self.shape_rotations[i].append(Cell(cell[0], cell[1], template['color']))

        self.shape = self.shape_rotations[self.rotation]

    def rotate(self, placed_cells):
        success = True
        tmp_x = self.x
        tmp_y = self.y
        tmp_rotation = self.rotation

        self.rotation += 1
        if self.rotation >= len(self.shape_rotations):
            self.rotation = 0

        self.shape = self.shape_rotations[self.rotation]

        SOUNDS['tetromino_moved'].play()

        for i in range(len(placed_cells)):
            if placed_cells[i].collidesWith(self):
                self.x += 1
                for j in range(len(placed_cells)):
                    if placed_cells[j].collidesWith(self):
                        self.x -= 2
                        for k in range(len(placed_cells)):
                            if placed_cells[k].collidesWith(self):
                                success = False

        for cell in self.shape:
            while cell.x + self.x < 0:
                self.x += 1
            while cell.x + self.x >= FIELD_WIDTH:
                self.x -= 1
            while cell.y + self.y >= FIELD_HEIGHT:
                self.y -= 1

        for cell in placed_cells:
            if cell.collidesWith(self):
                success = False

        if not success:
            self.rotation = tmp_rotation
            self.x = tmp_x
            self.y = tmp_y
            self.shape = self.shape_rotations[self.rotation]

    def move(self, amount, placed_cells):
        self.x += amount

        for cell in placed_cells:
            if cell.collidesWith(self):
                self.x -= amount

        for cell in self.shape:
            while cell.x + self.x < 0:
                self.x += 1
            while cell.x + self.x >= FIELD_WIDTH:
                self.x -= 1

        SOUNDS['tetromino_moved'].play()

    def showPreview(self, placed_cells):
        tmp_y = self.y

        testing = True
        while testing:
            self.y += 1
            for cell in placed_cells:
                if cell.collidesWith(self):
                    testing = False

            for cell in self.shape:
                if cell.y + self.y >= FIELD_HEIGHT:
                    testing = False
        self.y -= 1
        for cell in self.shape:
            borders = [True, True, True, True]  # Top, Right, Bottom, Left

            for otherCell in self.shape:
                if cell.y - 1 == otherCell.y and cell.x == otherCell.x:  # Top
                    borders[0] = False
                if cell.x + 1 == otherCell.x and cell.y == otherCell.y:  # Right
                    borders[1] = False
                if cell.y + 1 == otherCell.y and cell.x == otherCell.x:  # Bottom
                    borders[2] = False
                if cell.x - 1 == otherCell.x and cell.y == otherCell.y:  # Left
                    borders[3] = False

            cell.x += self.x + FIELD_OFFSET
            cell.y += self.y

            cell.drawBorders(borders)

            cell.x -= self.x + FIELD_OFFSET
            cell.y -= self.y
        self.y = tmp_y

    def draw(self):
        for cell in self.shape:
            cell.x += self.x + FIELD_OFFSET
            cell.y += self.y

            cell.draw()

            cell.x -= self.x + FIELD_OFFSET
            cell.y -= self.y

    def drop(self, placed_cells):
        self.y += 1
        for cell in placed_cells:
            if cell.collidesWith(self):
                return self._make_cells(placed_cells)

        for cell in self.shape:
            if cell.y + self.y >= FIELD_HEIGHT:
                return self._make_cells(placed_cells)

        SOUNDS['tetromino_moved'].play()

        return self

    def get_next(self):
        next_piece = Tetromino(self.next_tetrominos[0])

        for i in range(len(self.next_tetrominos)):
            if i + 1 < len(self.next_tetrominos):
                self.next_tetrominos[i] = self.next_tetrominos[i + 1]
            else:
                self.next_tetrominos[i] = random.choice(list(TETROMINO_TEMPLATES.values()))

        next_piece.next_tetrominos = self.next_tetrominos
        return next_piece

    def _make_cells(self, placed_cells):
        SOUNDS['tetromino_placed'].play()
        self.y -= 1

        tmp_color = self.shape[0].color

        for cell in self.shape:
            cell.color = COLORS['white']

        self.draw()
        pygame.display.update()
        time.sleep(0.1)

        for cell in self.shape:
            placed_cells.append(Cell(cell.x + self.x, cell.y + self.y, tmp_color))

        return self.get_next()
