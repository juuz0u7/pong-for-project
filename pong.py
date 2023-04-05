import random
from button import *
from other_variables import *
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

ball_dx, ball_dy = -5, 5
state_menu = True
state_1 = False
state_2 = False
is_over = False


def move_player():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT


def move_player2():
    bot.y += player2_speed
    if bot.top <= 0:
        bot.top = 0
    if bot.bottom >= SCREEN_HEIGHT:
        bot.bottom = SCREEN_HEIGHT


def move_ball(dx, dy):
    global pause_len
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        dy = -dy

    if ball.colliderect(player) and dx < 0:
        pong.play()
        if abs(ball.left - player.right) < 10:
            dx = -dx
        elif abs(ball.top - player.bottom) < 10 and dy < 0:
            dy = -dy
        elif abs(player.top - ball.bottom) < 10 and dy > 0:
            dy = -dy

    if ball.colliderect(bot) and dx > 0:
        pong.play()
        if abs(ball.right - bot.left) < 10:
            dx = -dx
        elif abs(ball.top - bot.bottom) < 10 and dy < 0:
            dy = -dy
        elif abs(bot.top - ball.bottom) < 10 and dy > 0:
            dy = -dy

    now = pygame.time.get_ticks()
    if now - score_time > pause_len and not is_over and now - START_game > pause_len:
        ball.x += dx
        ball.y += dy

    return dx, dy


def restart_ball():
    ball.center = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

    dx = random.choice((random.randint(-ball_max_speed, -ball_min_speed),
                        random.randint(ball_min_speed, ball_max_speed)))
    dy = random.choice((random.randint(-ball_max_speed, -ball_min_speed),
                        random.randint(ball_min_speed, ball_max_speed)))

    return dx, dy


def move_bot():
    if ball.centerx > SCREEN_WIDTH // 2 and ball_dx > 0:
        if ball.top >= bot.bottom:
            bot.y += bot_speed
        if ball.bottom <= bot.top:
            bot.y -= bot_speed


def move_bot2():
    if ball.centerx < SCREEN_WIDTH // 2 and ball_dx < 0:
        if ball.top >= player.bottom:
            player.y += bot_speed
        if ball.bottom <= player.top:
            player.y -= bot_speed


def win_or_lose():
    if player_score == win_score:
        win.play()
    elif bot_score == win_score:
        lose.play()
    else:
        score.play()


def on_state_lvl3():
    global state_menu, state_menu2, state_1, state_2, ball_max_speed, ball_min_speed, bot_speed
    ball_max_speed = 9
    ball_min_speed = 7
    bot_speed = 8
    state_menu = False
    state_menu2 = False
    state_1 = True
    state_2 = False


def on_state_2():
    global state_menu, state_1, state_2, ball_max_speed, ball_min_speed
    ball_max_speed = 9
    ball_min_speed = 7
    state_menu = False
    state_1 = False
    state_2 = True


def esc():
    global state_menu, state_1, state_2, ball_max_speed, ball_min_speed, ball_dx, ball_dy
    state_menu = True
    state_1 = False
    state_2 = False


drawing = svg2rlg('photo_2023-01-08_21-42-12.svg')
renderPM.drawToFile(drawing, 'vector_image.png', fmt='PNG')
vector_image = pygame.image.load('image/vector_image.png')
new_size = (int(vector_image.get_width() * 0.2), int(vector_image.get_height() * 0.2))
vector_image = pygame.transform.scale(vector_image, new_size)

drawing2 = svg2rlg('photo.svg')
renderPM.drawToFile(drawing2, 'vector_image2.png', fmt='PNG')
vector_image2 = pygame.image.load('image/vector_image2.png')
new_size2 = (int(vector_image.get_width() * 0.2), int(vector_image.get_height() * 0.2))
vector_image2 = pygame.transform.scale(vector_image2, new_size)

player = pygame.Rect(10, SCREEN_HEIGHT // 2, 10, 100)
bot = pygame.Rect(SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2, 10, 100)
ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 20, 20)

customButton1 = Button(315, 150, 256, 100, vector_image, on_state_lvl3)
customButton2 = Button(315, SCREEN_HEIGHT // 2 + 50, 256, 100, vector_image, on_state_2)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f and is_over:
                is_over = False
                player_score, bot_score = 0, 0
                score_time = pygame.time.get_ticks()
            if event.key == pygame.K_w:
                player_speed -= 7
            if event.key == pygame.K_s:
                player_speed += 7
            if event.key == pygame.K_UP:
                player2_speed -= 7
            if event.key == pygame.K_DOWN:
                player2_speed += 7
            if event.key == pygame.K_ESCAPE:
                esc()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player_speed += 7
            if event.key == pygame.K_s:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player2_speed += 7
            if event.key == pygame.K_DOWN:
                player2_speed -= 7

    if state_1:
        move_player()
        move_bot()
        ball_dx, ball_dy = move_ball(ball_dx, ball_dy)
    elif state_2:
        move_player()
        move_player2()
        ball_dx, ball_dy = move_ball(ball_dx, ball_dy)

    if ball.right <= 0:
        score_time = pygame.time.get_ticks()
        bot_score += 1
        win_or_lose()
        ball_dy *= -1
        if bot_score == win_score:
            is_over = True
    if ball.left >= SCREEN_WIDTH:
        score_time = pygame.time.get_ticks()
        player_score += 1
        win_or_lose()
        ball_dy *= 1
        if player_score == win_score:
            is_over = True

    if ball.right <= 0 or ball.left >= SCREEN_WIDTH:
        ball_dx, ball_dy = restart_ball()

    screen.fill(BG_COLOR)

    if state_menu:
        for object in objects:
            object.process()
            if state_1:
                score_time = pygame.time.get_ticks()
                restart_ball()
            if state_2:
                score_time = pygame.time.get_ticks()
                restart_ball()
        screen.blit(vector_image, (315, 150))
        screen.blit(vector_image2, (315, SCREEN_HEIGHT // 2 + 50))
        main_font.render_to(screen, (SCREEN_WIDTH // 2.3, 75), "Pong")
    elif state_1:
        main_font.render_to(screen, (330, 25), str(player_score))
        main_font.render_to(screen, (550, 25), str(bot_score))
        pygame.draw.rect(screen, PADDLE_COLOR, player)
        pygame.draw.rect(screen, PADDLE_COLOR, bot)
        pygame.draw.ellipse(screen, PADDLE_COLOR, ball)
        pygame.draw.line(screen, PADDLE_COLOR, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), width=3)
    elif state_2:
        main_font.render_to(screen, (330, 25), str(player_score))
        main_font.render_to(screen, (550, 25), str(bot_score))
        pygame.draw.rect(screen, PADDLE_COLOR, player)
        pygame.draw.rect(screen, PADDLE_COLOR, bot)
        pygame.draw.ellipse(screen, PADDLE_COLOR, ball)
        pygame.draw.line(screen, PADDLE_COLOR, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), width=3)

    if is_over:
        screen.fill(BG_COLOR)
        main_font.render_to(screen, (160, 200), "Game over, Press F for restart")

    clock.tick(FPS)
    pygame.display.update()
