import pygame
from game_modules.entities import *
from game_modules.utilities import *
import levels.levelExample as template

class GameManager:
    pass

def start_game(windowSize:tuple[int]=(800,600), FPS:int=60):
    pygame.init()
    CLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode(windowSize)
    levelWorksSpace = template.create_level(windowSize)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
        if not running:
            break

        screen.fill((0,0,0))

        levelWorksSpace.listen_mouse(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3))
        keys = pygame.key.get_pressed()
        levelWorksSpace.listen_keys_all(keys)

        levelWorksSpace.show(screen)

        levelWorksSpace.update_all(FPS)
        
        pygame.display.update()
        CLOCK.tick(FPS)