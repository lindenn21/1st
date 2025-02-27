import pygame
import sys
import random

# LINDEN POWELL L. RIVERA BSCPE 1-2: Shoot the correct answer

pygame.init()

WIDTH = 500
HEIGHT = 750
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load("images/BGGAME.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
WHITE = (255, 255, 255)
RED = (255, 0, 0)
player1 = pygame.image.load("images/PLAYER1.png")
player_bullet = pygame.image.load("images/BALL.png")

player1 = pygame.transform.scale(player1, (player1.get_width() * 3, player1.get_height() * 3))
PLAYER_WIDTH, PLAYER_HEIGHT = player1.get_size()
BULLET_WIDTH, BULLET_HEIGHT = player_bullet.get_size()

font = pygame.font.Font(None, 36)

lives = 3
score = 0
player_x = WIDTH // 30
player_y = HEIGHT - 100
player_speed = 20
player_bullet_speed = 30
player_bullets = []

equation = ""
correct_answer = 0
answers = []
answer_speed = 1
answer_positions = []
time_limit = 20
clock = pygame.time.Clock()
timer_start = pygame.time.get_ticks()


def generate_equation():
    global equation, correct_answer, answers, answer_positions
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(['+', '-', '*'])

    if operator == '+':
        correct_answer = num1 + num2
    elif operator == '-':
        correct_answer = num1 - num2
    else:
        correct_answer = num1 * num2

    equation = f"{num1} {operator} {num2} = ?"

    answers = [correct_answer]
    while len(answers) < 6:
        wrong_answer = random.randint(1, 100)
        if wrong_answer != correct_answer and wrong_answer not in answers:
            answers.append(wrong_answer)
    random.shuffle(answers)

    answer_positions.clear()
    y_positions = [100, 200, 300]
    for i in range(6):
        x = random.randint(50, WIDTH - 100)
        y = y_positions[i // 2]
        answer_positions.append([x, y, random.choice([-1, 1]) * answer_speed])


generate_equation()

running = True
while running:
    WINDOW.fill((0, 0, 0))
    WINDOW.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_bullets.append([player_x + PLAYER_WIDTH // 2 - BULLET_WIDTH // 2, player_y])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - PLAYER_WIDTH:
        player_x += player_speed



    WINDOW.blit(player1, (player_x, player_y))

    for bullet in player_bullets:
        bullet[1] -= player_bullet_speed
        WINDOW.blit(player_bullet, (bullet[0], bullet[1]))

    equation_text = font.render(equation, True, WHITE)
    WINDOW.blit(equation_text, (WIDTH // 2 - equation_text.get_width() // 2, 20))

    for i in range(6):
        answer_text = font.render(str(answers[i]), True, WHITE)
        answer_positions[i][0] += answer_positions[i][2]
        if answer_positions[i][0] <= 0 or answer_positions[i][0] >= WIDTH - 50:
            answer_positions[i][2] *= -1
        WINDOW.blit(answer_text, (answer_positions[i][0], answer_positions[i][1]))


    elapsed_time = (pygame.time.get_ticks() - timer_start) // 1000
    timer_text = font.render(f"Time: {time_limit - elapsed_time}", True, RED)
    WINDOW.blit(timer_text, (20, 50))

    if elapsed_time >= time_limit:
        lives -= 1
        generate_equation()
        timer_start = pygame.time.get_ticks()


    for bullet in player_bullets[:]:
        for i in range(6):
            if (answer_positions[i][0] <= bullet[0] <= answer_positions[i][0] + 50 and
                    answer_positions[i][1] <= bullet[1] <= answer_positions[i][1] + 30):
                if answers[i] == correct_answer:
                    score += 1
                    lives += 1
                else:
                    lives -= 1
                player_bullets.remove(bullet)
                generate_equation()
                timer_start = pygame.time.get_ticks()
                break

    controls_text = font.render("Controls:", True, WHITE)
    move_left = font.render("LEFT ARROW", True, WHITE)
    move_right = font.render("RIGHT ARROW", True, WHITE)
    shoot_tip = font.render("SPACE = Shoot", True, WHITE)

    WINDOW.blit(controls_text, (WIDTH - 250, 470))
    WINDOW.blit(move_left, (WIDTH - 250, 500))
    WINDOW.blit(move_right, (WIDTH - 250, 540))
    WINDOW.blit(shoot_tip, (WIDTH - 250, 580))

    score_text = font.render(f"Score: {score}", True, WHITE)
    WINDOW.blit(score_text, (20, 20))
    lives_text = font.render(f"Lives: {lives}", True, RED)
    WINDOW.blit(lives_text, (20, 80))

    if lives <= 0:
        game_over_text = font.render("Game Over", True, RED)
        retry_text = font.render("Retry?", True, WHITE)
        retry_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50)

        retrying = True
        while retrying:
            WINDOW.fill((0, 0, 0))
            WINDOW.blit(background, (0, 0))

            WINDOW.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))


            pygame.draw.rect(WINDOW, (0, 255, 0), retry_rect)
            pygame.draw.rect(WINDOW, (255, 255, 255), retry_rect, 3)
            WINDOW.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 65))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_rect.collidepoint(event.pos):

                        lives = 3
                        score = 0
                        player_x = WIDTH // 2
                        player_bullets.clear()
                        generate_equation()
                        timer_start = pygame.time.get_ticks()
                        retrying = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()