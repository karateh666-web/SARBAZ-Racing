import pygame
import random
import os

pygame.init()

WIDTH, HEIGHT = 480, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SARBAZ Racing")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 58)
small_font = pygame.font.Font(None, 25)
sign_font = pygame.font.Font(None, 19)
button_font = pygame.font.Font(None, 38)

GREEN = (35, 145, 55)
DARK_GREEN = (25, 115, 40)
ROAD = (65, 65, 70)
WHITE = (245, 245, 245)
YELLOW = (255, 220, 30)
RED = (230, 45, 45)
BLUE = (30, 130, 255)
BLACK = (20, 20, 20)

ROAD_LEFT = 65
ROAD_RIGHT = 415
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT

# موسیقی
music_file = os.path.expanduser(
    "~/car-game/My_Life_Be_Like.mp3"
)

try:
    pygame.mixer.init()
    if os.path.exists(music_file):
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)
except pygame.error:
    pass


def draw_car(surface, x, y, color, player=False):
    x, y = int(x), int(y)

    for wx in (x - 4, x + 26):
        pygame.draw.rect(
            surface, (15, 15, 15),
            (wx, y + 9, 8, 20), border_radius=3
        )
        pygame.draw.rect(
            surface, (15, 15, 15),
            (wx, y + 43, 8, 20), border_radius=3
        )

    pygame.draw.rect(
        surface, color, (x, y, 30, 70),
        border_radius=7
    )

    pygame.draw.rect(
        surface, (100, 210, 240),
        (x + 5, y + 12, 20, 17), border_radius=4
    )
    pygame.draw.rect(
        surface, (35, 55, 70),
        (x + 5, y + 38, 20, 14), border_radius=3
    )

    pygame.draw.rect(
        surface, (255, 255, 180),
        (x + 3, y + 2, 7, 5), border_radius=2
    )
    pygame.draw.rect(
        surface, (255, 255, 180),
        (x + 20, y + 2, 7, 5), border_radius=2
    )

    if player:
        pygame.draw.rect(
            surface, WHITE, (x + 13, y + 31, 4, 5)
        )


def draw_sign(x, y):
    pygame.draw.rect(
        screen, (105, 70, 35),
        (x + 27, y + 35, 6, 65)
    )

    pygame.draw.rect(
        screen, (20, 90, 45),
        (x, y, 60, 38), border_radius=5
    )
    pygame.draw.rect(
        screen, (240, 220, 150),
        (x, y, 60, 38), 2, border_radius=5
    )

    text = sign_font.render("SARBAZ", True, WHITE)
    screen.blit(
        text, text.get_rect(center=(x + 30, y + 19))
    )


def new_game():
    return {
        "player_x": WIDTH // 2 - 15,
        "player_y": HEIGHT - 120,
        "obstacles": [],
        "score": 0.0,
        "level": 1,
        "road_offset": 0.0,
        "spawn_timer": 0.0,
        "game_over": False,
        "won": False,
    }


def draw_touch_controls(game_over):
    button_y = HEIGHT - 76

    left_rect = pygame.Rect(24, button_y, 118, 58)
    right_rect = pygame.Rect(WIDTH - 142, button_y, 118, 58)

    for rect in (left_rect, right_rect):
        pygame.draw.rect(
            screen, BLACK, rect, border_radius=14
        )
        pygame.draw.rect(
            screen, WHITE, rect, 2, border_radius=14
        )

    left_text = button_font.render("<", True, WHITE)
    right_text = button_font.render(">", True, WHITE)

    screen.blit(
        left_text, left_text.get_rect(center=left_rect.center)
    )
    screen.blit(
        right_text, right_text.get_rect(center=right_rect.center)
    )

    restart_rect = pygame.Rect(
        WIDTH // 2 - 105,
        HEIGHT // 2 + 75,
        210,
        58
    )

    if game_over:
        pygame.draw.rect(
            screen, (20, 115, 45),
            restart_rect, border_radius=14
        )
        pygame.draw.rect(
            screen, WHITE, restart_rect,
            2, border_radius=14
        )

        text = small_font.render(
            "TAP TO RESTART", True, WHITE
        )
        screen.blit(
            text, text.get_rect(center=restart_rect.center)
        )

    return left_rect, right_rect, restart_rect


game = new_game()
running = True

# نگهداری محل انگشت‌ها برای حرکت با نگه داشتن دکمه
finger_positions = {}

while running:
    dt = min(clock.tick(60) / 1000, 0.04)
    state = game

    left_button = pygame.Rect(
        24, HEIGHT - 76, 118, 58
    )
    right_button = pygame.Rect(
        WIDTH - 142, HEIGHT - 76, 118, 58
    )
    restart_button = pygame.Rect(
        WIDTH // 2 - 105,
        HEIGHT // 2 + 75,
        210,
        58
    )

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif state["game_over"] and event.key in (
                pygame.K_r,
                pygame.K_SPACE,
                pygame.K_RETURN
            ):
                game = new_game()
                state = game

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if (
                    state["game_over"]
                    and restart_button.collidepoint(event.pos)
                ):
                    game = new_game()
                    state = game

        elif event.type == pygame.FINGERDOWN:
            pos = (
                int(event.x * WIDTH),
                int(event.y * HEIGHT)
            )
            finger_positions[event.finger_id] = pos

            if (
                state["game_over"]
                and restart_button.collidepoint(pos)
            ):
                game = new_game()
                state = game
                finger_positions.clear()

        elif event.type == pygame.FINGERMOTION:
            finger_positions[event.finger_id] = (
                int(event.x * WIDTH),
                int(event.y * HEIGHT)
            )

        elif event.type == pygame.FINGERUP:
            finger_positions.pop(event.finger_id, None)

    # تشخیص نگه داشتن انگشت روی دکمه‌ها
    touch_left = any(
        left_button.collidepoint(pos)
        for pos in finger_positions.values()
    )
    touch_right = any(
        right_button.collidepoint(pos)
        for pos in finger_positions.values()
    )

    mouse_down = pygame.mouse.get_pressed()[0]
    mouse_pos = pygame.mouse.get_pos()

    if mouse_down:
        if left_button.collidepoint(mouse_pos):
            touch_left = True
        if right_button.collidepoint(mouse_pos):
            touch_right = True

    keys = pygame.key.get_pressed()

    # چمن
    screen.fill(GREEN)

    grass_offset = int(state["road_offset"]) % 50

    for y in range(-50, HEIGHT, 50):
        yy = y + grass_offset

        pygame.draw.rect(
            screen, DARK_GREEN, (10, yy, 35, 22)
        )
        pygame.draw.rect(
            screen, DARK_GREEN,
            (WIDTH - 45, yy + 15, 35, 22)
        )

    # تابلوها
    draw_sign(2, 250)
    draw_sign(418, 450)

    # جاده
    pygame.draw.rect(
        screen, ROAD,
        (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT)
    )

    pygame.draw.rect(
        screen, WHITE,
        (ROAD_LEFT, 0, 5, HEIGHT)
    )
    pygame.draw.rect(
        screen, WHITE,
        (ROAD_RIGHT - 5, 0, 5, HEIGHT)
    )

    speed = 240 + (state["level"] - 1) * 25

    if not state["game_over"]:

        state["road_offset"] += speed * dt
        state["score"] += dt * 5

        # کنترل با کیبورد یا لمس صفحه
        if (
            keys[pygame.K_LEFT]
            or keys[pygame.K_a]
            or touch_left
        ):
            state["player_x"] -= 280 * dt

        if (
            keys[pygame.K_RIGHT]
            or keys[pygame.K_d]
            or touch_right
        ):
            state["player_x"] += 280 * dt

        state["player_x"] = max(
            ROAD_LEFT + 12,
            min(ROAD_RIGHT - 42, state["player_x"])
        )

        # ده مرحله
        state["level"] = min(
            10, int(state["score"] // 100) + 1
        )

        if state["score"] >= 1000:
            state["won"] = True
            state["game_over"] = True

        # خط‌کشی جاده
        for lane_x in (
            ROAD_LEFT + ROAD_WIDTH // 3,
            ROAD_LEFT + 2 * ROAD_WIDTH // 3
        ):
            for y in range(-80, HEIGHT, 100):
                yy = int(
                    (y + state["road_offset"])
                    % (HEIGHT + 100) - 50
                )

                pygame.draw.rect(
                    screen, YELLOW,
                    (lane_x - 3, yy, 6, 48)
                )

        # ساخت ماشین‌های مانع
        state["spawn_timer"] += dt
        spawn_delay = max(
            0.48, 1.15 - state["level"] * 0.055
        )

        if state["spawn_timer"] >= spawn_delay:
            state["spawn_timer"] = 0

            lanes = [
                ROAD_LEFT + ROAD_WIDTH // 6 - 15,
                ROAD_LEFT + ROAD_WIDTH // 2 - 15,
                ROAD_LEFT + 5 * ROAD_WIDTH // 6 - 15,
            ]

            available = [
                lane for lane in lanes
                if all(
                    abs(lane - obs["x"]) > 55
                    for obs in state["obstacles"]
                    if obs["y"] < 150
                )
            ]

            if available:
                state["obstacles"].append({
                    "x": random.choice(available),
                    "y": -80.0,
                    "color": random.choice([
                        RED,
                        BLUE,
                        (255, 150, 20),
                        (180, 60, 220),
                        (240, 240, 240)
                    ])
                })

        # حرکت موانع و تشخیص تصادف
        player_rect = pygame.Rect(
            int(state["player_x"]) + 2,
            state["player_y"] + 3,
            26,
            64
        )

        for obs in state["obstacles"][:]:
            obs["y"] += speed * dt

            draw_car(
                screen, obs["x"], obs["y"], obs["color"]
            )

            obstacle_rect = pygame.Rect(
                obs["x"] + 2,
                int(obs["y"]) + 3,
                26,
                64
            )

            if player_rect.colliderect(obstacle_rect):
                state["game_over"] = True
                break

            if obs["y"] > HEIGHT:
                state["obstacles"].remove(obs)
                state["score"] += 10

    else:
        for obs in state["obstacles"]:
            draw_car(
                screen, obs["x"], obs["y"], obs["color"]
            )

    # ماشین بازیکن
    draw_car(
        screen,
        state["player_x"],
        state["player_y"],
        BLUE,
        player=True
    )

    # امتیاز و مرحله
    screen.blit(
        font.render(
            f"Score: {int(state['score'])}", True, WHITE
        ),
        (15, 15)
    )

    screen.blit(
        font.render(
            f"Level: {state['level']}/10", True, WHITE
        ),
        (330, 15)
    )

    # صفحه پایان و شروع مجدد لمسی
    if state["game_over"]:
        shade = pygame.Surface(
            (WIDTH, HEIGHT), pygame.SRCALPHA
        )
        shade.fill((0, 0, 0, 180))
        screen.blit(shade, (0, 0))

        if state["won"]:
            title = big_font.render(
                "YOU WIN!", True, YELLOW
            )
            message = "All 10 levels completed!"
        else:
            title = big_font.render(
                "CRASH!", True, RED
            )
            message = "Your car hit an obstacle!"

        screen.blit(
            title,
            title.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 - 65)
            )
        )

        screen.blit(
            small_font.render(message, True, WHITE),
            (65, HEIGHT // 2)
        )

        restart_text = font.render(
            "Tap the green button", True, YELLOW
        )
        screen.blit(
            restart_text,
            restart_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 55)
            )
        )

        quit_text = small_font.render(
            "ESC: Quit", True, WHITE
        )
        screen.blit(
            quit_text,
            quit_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 145)
            )
        )

    draw_touch_controls(state["game_over"])
    pygame.display.flip()

pygame.quit()
