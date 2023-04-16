import pygame
from entities import *
from utilities import *

pygame.init()

FPS = 60
CLOCK = pygame.time.Clock()
SIZE = (800,600)

screen = pygame.display.set_mode(SIZE)

bgTextures = create_textures(['bg1.png'], [1])
mcTextures = create_textures(['Idle.png', 'Walk.png', 'Jump.png'], [6, 9, 9], path='textures/Samurai/', variations=2, transformFunction=Transformation.XFLIP, scalar=2)

bg = Background(Physics([0,0]), Animation(textures=bgTextures, actualTexture='bg1'), SIZE, scalar=1)

mainCharacter = MainCharacter(Physics([0,250]), Animation(textures=mcTextures, actualTexture='xflip_Idle'), location=Location.CENTER)

levelWorksSpace = LevelWorksSpace(bg, mainCharacter)




running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
    if not running:
        break

    screen.fill((0,0,0))
    levelWorksSpace.update(FPS)

    keys = pygame.key.get_pressed()

    levelWorksSpace.listen_events(pygame.key.get_pressed())


    screen.blit(bg.get_texture(), levelWorksSpace.fitThePosition(bg.get_texture_position()))
    screen.blit(mainCharacter.get_texture(), levelWorksSpace.fitThePosition(mainCharacter.get_texture_position()))
    pygame.display.update()
    CLOCK.tick(FPS)