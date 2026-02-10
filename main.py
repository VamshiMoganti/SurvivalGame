import pygame
import sys
from settings import *
from player import Player
from enemy import Enemy

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Survival Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

def reset_game():
    return Player(), [], 0, 0, False

player, enemies, spawn_timer, score, game_over = reset_game()

running = True

while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                player, enemies, spawn_timer, score, game_over = reset_game()

    if not game_over:
        keys = pygame.key.get_pressed()
        player.move(keys)

        spawn_timer += 1
        if spawn_timer > 30:
            enemies.append(Enemy())
            spawn_timer = 0

        for enemy in enemies[:]:
            enemy.update()

            if enemy.off_screen():
                enemies.remove(enemy)
                score += 1

            if pygame.Rect(player.x, player.y, player.size, player.size).colliderect(enemy.get_rect()):
                game_over = True

        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

    else:
        over_text = font.render("GAME OVER", True, (0, 0, 0))
        restart_text = font.render("Press R to Restart", True, (0, 0, 0))

        screen.blit(over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
        screen.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2 + 20))

    pygame.display.flip()

pygame.quit()
sys.exit()
