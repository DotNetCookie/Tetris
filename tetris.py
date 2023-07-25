import os.path
import time
from typing import List

from src.program import *
from src.tetromino import Tetromino
from src.cell import Cell
from src.button import start_button, quit_button, resume_button, restart_button, return_button, game_over_button, \
    mute_button

SCORE_TEMPLATES = [0, 100, 300, 500, 800]  # scores mapped to amount of rows completed

PANEL_OFFSET_X_RIGHT = FIELD_OFFSET + FIELD_WIDTH + 2  # Offset in cells for the stats and next tetrominos
PANEL_OFFSET_X_LEFT = 2  # Offset in cells for the storage
PANEL_OFFSET_Y_TOP = 2  # Offset for the upper most information panels from the top of the screen in cells
PANEL_OFFSET_Y_BOTTOM = 10  # Offset for the lower information panel in cells
PANEL_PADDING = 16  # padding for information panels in pixels
PANEL_BORDER_WIDTH = 8  # border of information panels in pixels
PANEL_WIDTH = 4  # width of information panel in cells

FIELD_BORDER_WIDTH = 5  # field border width in pixels
FIELD_DIVIDERS_WIDTH = 1  # width of the dividers in pixels
COOL_DOWN_BAR_HEIGHT = 2  # height of the top cool down bar in pixel

MENU_OFFSET_Y = 4  # the vertical offset of the pause and start menu to the top and bottom

score = 0
lines = 0
level = 0

tetromino: Tetromino = Tetromino(None)
stored_tetromino: Tetromino = Tetromino(None)
placed_cells: List[Cell] = []

horizontal_cool_down = 0
vertical_cool_down = 0

level_up_timer = 0

game_running = False
paused = False

muted = False


def reset():
    global score, lines, level, tetromino, stored_tetromino, placed_cells, horizontal_cool_down, vertical_cool_down
    global level_up_timer, game_running, paused

    score = 0
    lines = 0
    level = 1

    tetromino = Tetromino(None)

    stored_tetromino = None

    placed_cells = []

    horizontal_cool_down = 0
    vertical_cool_down = 0

    level_up_timer = 0

    game_running = False
    paused = False


def check_quit(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        exit(0)


def handle_high_score():
    dir_path = os.path.join(os.path.abspath('.'), "tetris_save")
    file_path = os.path.join(dir_path, "high_score.txt")
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    try:
        # read high score
        with open(file_path) as file:
            high_score = int(file.read())
    except FileNotFoundError:
        high_score = 0
    except ValueError:
        high_score = 0

    if score > high_score:
        high_score = score

        # write new high score
        with open(file_path, "w+") as file:
            file.write(str(high_score))

    return high_score


def show_level_up():
    global level_up_timer

    if level_up_timer > 0:
        # Level up background
        color = COLORS['red']
        pygame.draw.rect(screen, color, (
            PANEL_OFFSET_X_RIGHT * CELL_SIZE,
            PANEL_OFFSET_Y_TOP * CELL_SIZE,
            4 * CELL_SIZE,
            6 * CELL_SIZE
        ))

        # Level up text
        render = FONT.render("LEVEL UP!", True, COLORS['pure_white'])
        screen.blit(render, (
            (PANEL_OFFSET_X_RIGHT + 2) * CELL_SIZE - render.get_width() / 2,
            4 * CELL_SIZE
        ))

        # Level up number
        render = FONT.render(str(level), True, COLORS['pure_white'])
        screen.blit(render, (
            (PANEL_OFFSET_X_RIGHT + 2) * CELL_SIZE - render.get_width() / 2,
            5 * CELL_SIZE
        ))

        level_up_timer -= 1


def show_help():
    texts = [
        "MOVE PIECE LEFT:",
        "- LEFT-ARROW or A",
        "MOVE PIECE RIGHT:",
        "- RIGHT-ARROW or D",
        "ROTATE PIECE:",
        "- UP-ARROW or W",
        "SOFT DROP:",
        "- DOWN-ARROW or S",
        "HARD DROP:",
        "- SPACE or RETURN"
    ]

    for i in range(len(texts)):
        render = FONT.render(texts[i], True, COLORS['pure_white'])
        screen.blit(render, (
            0.5 * CELL_SIZE,
            (PANEL_OFFSET_Y_BOTTOM - 1 + i) * CELL_SIZE
        ))


def show_start_menu():
    global game_running, muted

    # Start background
    pygame.draw.rect(screen, COLORS['grey'], (
        FIELD_OFFSET * CELL_SIZE,
        MENU_OFFSET_Y * CELL_SIZE,
        FIELD_WIDTH * CELL_SIZE,
        (FIELD_HEIGHT - MENU_OFFSET_Y * 2) * CELL_SIZE
    ))

    # Start text
    render = FONT.render("DOTNETCOOKIE'S", True, COLORS['pure_white'])
    screen.blit(render, (
        screen.get_width() / 2 - render.get_width() / 2,
        (MENU_OFFSET_Y + 1) * CELL_SIZE
    ))

    render = LARGE_FONT.render("PYTHON TETRIS", True, COLORS['pure_white'])
    screen.blit(render, (
        screen.get_width() / 2 - render.get_width() / 2,
        (MENU_OFFSET_Y + 2) * CELL_SIZE
    ))

    # Start line
    pygame.draw.rect(screen, COLORS['pure_white'], (
        (FIELD_OFFSET + 1) * CELL_SIZE,
        8 * CELL_SIZE,
        (FIELD_WIDTH - 2) * CELL_SIZE,
        PANEL_BORDER_WIDTH
    ))

    # Start button
    start_button.draw()

    # Quit button
    quit_button.draw()

    # Mute button
    mute_button.draw()

    # Controls
    show_help()

    for event in pygame.event.get():
        check_quit(event)

        if start_button.check_click(event):
            reset()
            game_running = True
        if quit_button.check_click(event):
            pygame.quit()
            exit(0)
        if mute_button.check_click(event):
            muted = not muted
            set_volume(muted)

            button_text = ""
            if muted:
                button_text = "UN"
            button_text += "MUTE"

            mute_button.text = button_text

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                reset()
                game_running = True


def show_pause_menu():
    global paused, game_running

    # pause background
    pygame.draw.rect(screen, COLORS['grey'], (
        FIELD_OFFSET * CELL_SIZE,
        MENU_OFFSET_Y * CELL_SIZE,
        FIELD_WIDTH * CELL_SIZE,
        (FIELD_HEIGHT - MENU_OFFSET_Y * 2) * CELL_SIZE
    ))

    # pause menu text
    render = LARGE_FONT.render("PAUSED", True, COLORS['pure_white'])
    screen.blit(render, (
        screen.get_width() / 2 - render.get_width() / 2,
        (MENU_OFFSET_Y + 1) * CELL_SIZE
    ))

    # resume button
    resume_button.draw()

    # restart button
    restart_button.draw()

    # back to menu button
    return_button.draw()

    # Controls
    show_help()

    for event in pygame.event.get():
        check_quit(event)

        if resume_button.check_click(event):
            paused = not paused
        if restart_button.check_click(event):
            reset()
            game_running = True
        if return_button.check_click(event):
            paused = not paused
            game_running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused


def draw():
    # Background fill
    screen.fill(COLORS['black'])

    # Game field background
    pygame.draw.rect(screen, COLORS['pure_black'], (
        FIELD_OFFSET * CELL_SIZE,
        0,
        FIELD_WIDTH * CELL_SIZE,
        FIELD_HEIGHT * CELL_SIZE
    ))

    # Field cell dividers vertical
    for i in range(FIELD_HEIGHT - 1):
        pygame.draw.rect(screen, COLORS['grey'], (
            FIELD_OFFSET * CELL_SIZE,
            i * CELL_SIZE + CELL_SIZE,
            FIELD_WIDTH * CELL_SIZE,
            FIELD_DIVIDERS_WIDTH
        ))

    # Field cell dividers horizontal
    for i in range(FIELD_WIDTH - 1):
        pygame.draw.rect(screen, COLORS['grey'], (
            i * CELL_SIZE + CELL_SIZE + FIELD_OFFSET * CELL_SIZE,
            0,
            FIELD_DIVIDERS_WIDTH,
            FIELD_HEIGHT * CELL_SIZE
        ))

    # Field borders
    pygame.draw.rect(screen, COLORS['grey'], (
        FIELD_OFFSET * CELL_SIZE - FIELD_BORDER_WIDTH,
        0,
        FIELD_BORDER_WIDTH,
        FIELD_HEIGHT * CELL_SIZE
    ))
    pygame.draw.rect(screen, COLORS['grey'], (
        FIELD_OFFSET * CELL_SIZE + FIELD_WIDTH * CELL_SIZE,
        0,
        FIELD_BORDER_WIDTH,
        FIELD_HEIGHT * CELL_SIZE
    ))

    # Placed tiles
    for cell in placed_cells:
        cell.x += FIELD_OFFSET

        cell.draw()

        cell.x -= FIELD_OFFSET

    # preview
    tetromino.showPreview(placed_cells)

    # Active piece
    tetromino.draw()

    # Cool down
    pygame.draw.rect(screen, COLORS['paste_blue'], (
        FIELD_OFFSET * CELL_SIZE,
        0,
        (FIELD_WIDTH * CELL_SIZE) * (vertical_cool_down / MAX_VERTICAL_COOL_DOWN),
        COOL_DOWN_BAR_HEIGHT
    ))

    # Score background
    # border
    pygame.draw.rect(screen, COLORS['grey'], (
        PANEL_OFFSET_X_RIGHT * CELL_SIZE - PANEL_PADDING,
        PANEL_OFFSET_Y_TOP * CELL_SIZE - PANEL_PADDING,
        PANEL_WIDTH * CELL_SIZE + PANEL_PADDING * 2,
        6 * CELL_SIZE + PANEL_PADDING * 2
    ))
    # background
    pygame.draw.rect(screen, COLORS['light_grey'], (
        PANEL_OFFSET_X_RIGHT * CELL_SIZE - PANEL_PADDING + PANEL_BORDER_WIDTH,
        PANEL_OFFSET_Y_TOP * CELL_SIZE - PANEL_PADDING + PANEL_BORDER_WIDTH,
        PANEL_WIDTH * CELL_SIZE + PANEL_PADDING * 2 - PANEL_BORDER_WIDTH * 2,
        6 * CELL_SIZE + PANEL_PADDING * 2 - PANEL_BORDER_WIDTH * 2
    ))

    # High score label text
    render = FONT.render("TOP SCORE", True, COLORS['pure_white'])
    screen.blit(render, (
        PANEL_OFFSET_X_RIGHT * CELL_SIZE,
        PANEL_OFFSET_Y_TOP * CELL_SIZE
    ))

    # High score text
    high_score = handle_high_score()
    render = FONT.render("0" * (7 - len(str(high_score))) + str(high_score), True, COLORS['pure_white'])
    screen.blit(render, (
        PANEL_OFFSET_X_RIGHT * CELL_SIZE,
        (PANEL_OFFSET_Y_TOP + 1) * CELL_SIZE
    ))

    # Score label text
    render = FONT.render("SCORE", True, COLORS['pure_white'])
    screen.blit(render, (
        PANEL_OFFSET_X_RIGHT * CELL_SIZE,
        (PANEL_OFFSET_Y_TOP + 2) * CELL_SIZE
    ))

    # Score text
    render = FONT.render("0" * (7 - len(str(score))) + str(score), True, COLORS['pure_white'])
    screen.blit(render, (
        PANEL_OFFSET_X_RIGHT * CELL_SIZE,
        (PANEL_OFFSET_Y_TOP + 3) * CELL_SIZE
    ))

    # Level text
    render = FONT.render("LEVEL: " + "0" * (2 - len(str(level))) + str(level), True, COLORS['pure_white'])
    screen.blit(render, (
        (PANEL_OFFSET_X_RIGHT + PANEL_WIDTH / 2) * CELL_SIZE - render.get_width() / 2,
        (PANEL_OFFSET_Y_TOP + 5) * CELL_SIZE
    ))

    # Level up
    show_level_up()

    # Next pieces background
    # border
    pygame.draw.rect(screen, COLORS['light_grey'], (
        PANEL_OFFSET_X_RIGHT * CELL_SIZE - PANEL_PADDING,
        PANEL_OFFSET_Y_BOTTOM * CELL_SIZE - PANEL_PADDING,
        PANEL_WIDTH * CELL_SIZE + PANEL_PADDING * 2,
        8 * CELL_SIZE + PANEL_PADDING * 2
    ))
    # background
    pygame.draw.rect(screen, COLORS['grey'], (
        PANEL_OFFSET_X_RIGHT * CELL_SIZE - PANEL_PADDING + PANEL_BORDER_WIDTH,
        PANEL_OFFSET_Y_BOTTOM * CELL_SIZE - PANEL_PADDING + PANEL_BORDER_WIDTH,
        PANEL_WIDTH * CELL_SIZE + PANEL_PADDING * 2 - PANEL_BORDER_WIDTH * 2,
        8 * CELL_SIZE + PANEL_PADDING * 2 - PANEL_BORDER_WIDTH * 2
    ))

    # Next pieces
    for i in range(len(tetromino.next_tetrominos)):
        for cellTemplate in tetromino.next_tetrominos[i]['cells'][0]:
            cell = Cell(
                cellTemplate[0] + PANEL_OFFSET_X_RIGHT,
                cellTemplate[1] + PANEL_OFFSET_Y_BOTTOM + i * 3,
                tetromino.next_tetrominos[i]['color']
            )

            cell.draw()

    # Next pieces text
    render = FONT.render("NEXT", True, COLORS['pure_white'])
    screen.blit(render, (
        PANEL_OFFSET_X_RIGHT * CELL_SIZE - PANEL_PADDING - 0,
        PANEL_OFFSET_Y_BOTTOM * CELL_SIZE - PANEL_PADDING - render.get_height(),
    ))

    # Storage background
    # border
    pygame.draw.rect(screen, COLORS['light_grey'], (
        PANEL_OFFSET_X_LEFT * CELL_SIZE - PANEL_PADDING,
        PANEL_OFFSET_Y_TOP * CELL_SIZE - PANEL_PADDING,
        PANEL_WIDTH * CELL_SIZE + PANEL_PADDING * 2,
        2 * CELL_SIZE + PANEL_PADDING * 2
    ))
    # background
    pygame.draw.rect(screen, COLORS['grey'], (
        PANEL_OFFSET_X_LEFT * CELL_SIZE - PANEL_PADDING + PANEL_BORDER_WIDTH,
        PANEL_OFFSET_Y_TOP * CELL_SIZE - PANEL_PADDING + PANEL_BORDER_WIDTH,
        PANEL_WIDTH * CELL_SIZE + PANEL_PADDING * 2 - PANEL_BORDER_WIDTH * 2,
        2 * CELL_SIZE + PANEL_PADDING * 2 - PANEL_BORDER_WIDTH * 2
    ))

    # Storage piece
    if stored_tetromino is not None:
        for cell in stored_tetromino.shape:
            cell.x += 2
            cell.y += 2

            cell.draw()

            cell.x -= 2
            cell.y -= 2

    # Storage text
    render = FONT.render("STORED (C)", True, COLORS['pure_white'])
    screen.blit(render, (
        PANEL_OFFSET_X_LEFT * CELL_SIZE - PANEL_PADDING,
        PANEL_OFFSET_Y_TOP * CELL_SIZE - PANEL_PADDING - render.get_height()
    ))


def handleEvents():
    global score, level, tetromino, stored_tetromino, placed_cells, horizontal_cool_down, vertical_cool_down, paused

    for event in pygame.event.get():
        check_quit(event)
        if game_running:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_r or event.key == pygame.K_w:  # rotate
                    tetromino.rotate(placed_cells)

                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:  # hard drop
                    new_tetromino = tetromino
                    while new_tetromino == tetromino:
                        score += 2
                        new_tetromino = tetromino.drop(placed_cells)
                    tetromino = new_tetromino
                    vertical_cool_down = MAX_VERTICAL_COOL_DOWN

                if event.key == pygame.K_c:  # switch storage with active piece

                    if tetromino.swap_enabled:
                        SOUNDS['button_click'].play()
                        tetromino.swap_enabled = False

                        if stored_tetromino is not None:
                            tmp_piece = stored_tetromino
                            tmp_piece.y = -1
                            tmp_piece.x = FIELD_WIDTH / 2 - 1
                        else:
                            tmp_piece = tetromino.get_next()

                        tetromino.shape = tetromino.shape_rotations[0]
                        stored_tetromino = tetromino
                        tetromino = tmp_piece
                if event.key == pygame.K_ESCAPE:
                    paused = not paused

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # move piece left
        if horizontal_cool_down < 0:
            tetromino.move(-1, placed_cells)
            horizontal_cool_down = MAX_HORIZONTAL_COOL_DOWN

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # move piece right
        if horizontal_cool_down < 0:
            tetromino.move(1, placed_cells)
            horizontal_cool_down = MAX_HORIZONTAL_COOL_DOWN

    if keys[pygame.K_DOWN] or keys[pygame.K_s]:  # slow drop
        vertical_cool_down -= 20
        if vertical_cool_down < 0:
            score += 1


def update():
    global score, level, tetromino, stored_tetromino, placed_cells, horizontal_cool_down, vertical_cool_down, game_running, lines, level_up_timer

    handleEvents()

    vertical_cool_down -= level
    horizontal_cool_down -= 1

    if vertical_cool_down < 0:  # move piece down
        vertical_cool_down = MAX_VERTICAL_COOL_DOWN
        tetromino = tetromino.drop(placed_cells)

    rows = []
    completed_rows = 0
    for i in range(FIELD_HEIGHT):
        rows.append(0)
    for cell in placed_cells:
        if cell.y <= 0:
            # Game over
            waiting = True
            SOUNDS['game_over'].play()
            while waiting:
                # Game over background
                pygame.draw.rect(screen, COLORS['grey'], (
                    FIELD_OFFSET * CELL_SIZE,
                    6 * CELL_SIZE,
                    FIELD_WIDTH * CELL_SIZE,
                    6 * CELL_SIZE
                ))

                # Game over text
                render = LARGE_FONT.render("GAME OVER", True, COLORS['pure_white'])
                screen.blit(render, (
                    FIELD_OFFSET * CELL_SIZE + FIELD_WIDTH / 2 * CELL_SIZE - render.get_width() / 2,
                    7 * CELL_SIZE
                ))

                # Game over button
                game_over_button.draw()
                pygame.display.update()

                for event in pygame.event.get():
                    check_quit(event)
                    if game_over_button.check_click(event):
                        waiting = False
            game_running = False
            return

        rows[cell.y] += 1

    for i in reversed(range(len(rows))):
        if rows[i] >= FIELD_WIDTH:
            for cell in placed_cells:
                if cell.y == i:
                    cell.color = COLORS['white']
                    draw()
                    pygame.display.update()
            SOUNDS['row_complete'].play()
            time.sleep(0.1)
            placed_cells = [cell for cell in placed_cells if not (cell.y == i)]

    for i in reversed(range(len(rows))):
        if rows[i] >= FIELD_WIDTH:
            completed_rows += 1
            for tile in placed_cells:
                if tile.y - (completed_rows - 1) < i:
                    tile.y += 1

    score += SCORE_TEMPLATES[completed_rows] * level
    lines += completed_rows
    if lines > level * 10 + 10:
        level += 1
        level_up_timer = 100
        SOUNDS['level_up'].play()


if __name__ == '__main__':
    set_volume(muted)
    draw()
    while True:
        clock.tick(60)

        if paused:
            show_pause_menu()
        elif game_running:
            draw()
            update()
        else:
            show_start_menu()

        pygame.display.update()
