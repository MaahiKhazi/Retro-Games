import random

import pygame

pygame.init()

# Game Screen
# Variables Declaration

WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")
FPS = 60

ball = pygame.Rect((WIDTH / 2) - 15, (HEIGHT / 2) - 15, 30, 30)
player = pygame.Rect(WIDTH - 20, (HEIGHT / 2) - 70, 10, 140)
opponent = pygame.Rect(10, (HEIGHT / 2) - 70, 10, 140)
p_color = (255, 255, 255)
b_color = (255, 0, 0)
l_color = (255, 255, 255)
light_grey = (200, 200, 200)
bg_color = pygame.Color('grey12')
ball_speed_x = 9 * random.choice((1, -1))
ball_speed_y = 9 * random.choice((1, -1))
player_speed = 0
opponent_speed = 10
player_score = 0
opponent_score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)


def draw_window():
    WIN.fill((0, 0, 0))
    # pygame.display.update()


# Drawing
def draw_rect():
    pygame.draw.rect(WIN, p_color, player)
    pygame.draw.rect(WIN, p_color, opponent)
    pygame.draw.ellipse(WIN, b_color, ball)
    pygame.draw.aaline(WIN, l_color, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))
    # pygame.display.update()


def ball_movement():
    global ball_speed_x, ball_speed_y, player_score, opponent_score
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
    if ball.left <= 0:
        ball_restart()
        player_score += 1
    if ball.right >= WIDTH:
        ball_restart()
        opponent_score += 1
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1


def ball_restart():
    global ball_speed_x, ball_speed_y
    pygame.time.delay(1000)
    ball.center = (WIDTH / 2, HEIGHT / 2)
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))


def player_movement():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= HEIGHT:
        player.bottom = HEIGHT


def opponent_movement():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= HEIGHT:
        opponent.bottom = HEIGHT


# Loop


def main():
    global player_speed
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player_speed += 7
                if event.key == pygame.K_UP:
                    player_speed -= 7
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player_speed -= 7
                if event.key == pygame.K_UP:
                    player_speed += 7
        ball_movement()
        player_movement()
        opponent_movement()
        draw_window()
        draw_rect()

        player_text = basic_font.render(f'{player_score}', False, light_grey)
        WIN.blit(player_text, (520, 360))
        opponent_text = basic_font.render(f'{opponent_score}', False, light_grey)
        WIN.blit(opponent_text, (460, 360))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
