import pygame
import sys
import random

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-Понг")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 255)

# Настройки ракеток
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
paddle_speed = 7
ai_base_speed = 5

# Левая ракетка (игрок)
left_paddle = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Правая ракетка (компьютер)
right_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Мяч
ball = pygame.Rect(WIDTH//2 - 10, HEIGHT//2 - 10, 20, 20)
ball_speed_x = 5
ball_speed_y = 5
max_ball_speed = 12  # Максимальная скорость мяча

# Загрузка звука
try:
    bounce_sound = pygame.mixer.Sound("bounce.ogg")
except pygame.error:
    print("⚠️ Файл 'bounce.wav' не найден. Звук отключён.")
    bounce_sound = None

# Часы для контроля FPS
clock = pygame.time.Clock()

# Вероятность промаха ИИ
ai_mistake_chance = 20

# Основной игровой цикл
running = True
while running:
    screen.fill(BLACK)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление левой ракеткой (игрок)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= paddle_speed
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += paddle_speed

    # Управление правой ракеткой (ИИ)
    if random.randint(1, 100) > ai_mistake_chance:
        ai_speed = ai_base_speed + random.choice([-1, 0, 1])
        if right_paddle.centery < ball.centery:
            right_paddle.y += min(ai_speed, abs(right_paddle.centery - ball.centery))
        elif right_paddle.centery > ball.centery:
            right_paddle.y -= min(ai_speed, abs(right_paddle.centery - ball.centery))
    else:
        pass

    # Ограничение движения правой ракетки
    if right_paddle.top < 0:
        right_paddle.top = 0
    if right_paddle.bottom > HEIGHT:
        right_paddle.bottom = HEIGHT

    # Движение мяча
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Отскок от верхней и нижней границ
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Отскок от ракеток
    collision = False
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x *= -1
        # Увеличиваем скорость мяча при отскоке
        if abs(ball_speed_x) < max_ball_speed:
            ball_speed_x *= 1.1
        if abs(ball_speed_y) < max_ball_speed:
            ball_speed_y *= 1.1
        collision = True

    # Воспроизведение звука
    if collision and bounce_sound:
        bounce_sound.play()

    # Перезапуск мяча, если он вышел за экран
    if ball.left <= 0 or ball.right >= WIDTH:
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed_x = 5 * (-1 if ball.right >= WIDTH else 1)
        ball_speed_y = 5 * (-1 if random.random() > 0.5 else 1)

    # Отрисовка объектов
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)

# Завершение работы
pygame.quit()
sys.exit()