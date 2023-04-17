import pygame
from entities import *
from utilities import *

pygame.init()

FPS = 60
CLOCK = pygame.time.Clock()
SIZE = (800,600)

screen = pygame.display.set_mode(SIZE)

bg1Textures = create_textures(['bg1.png'], [1])
bg2Textures = create_textures(['bg2.png'], [1])
mcTextures = create_textures(['Idle.png', 'Walk.png'], [4, 6], path='textures/main_character/', variations=2, transformFunction=Transformation.XFLIP, scalar=2, extractContent=True)

bg1 = Background(Physics([0,0]), Animation(textures=bg1Textures, actualTexture='bg1', zIndex=2), SIZE, scalar=1)
bg2 = Background(Physics([0,0], velocity=[-200,0]), Animation(textures=bg2Textures, actualTexture='bg2', zIndex=1), SIZE, scalar=1)

mainCharacter = MainCharacter(Physics([0,250], margin=[5], hitRestrictions=True), Animation(textures=mcTextures, actualTexture='xflip_Idle'), location=Location.CENTER)

levelWorksSpace = LevelWorksSpace((1500,600),[bg1, bg2], mainCharacter, SIZE)




running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
    if not running:
        break

    screen.fill((0,0,0))
    levelWorksSpace.update_all(FPS)

    keys = pygame.key.get_pressed()

    levelWorksSpace.listen_keys(pygame.key.get_pressed())


    levelWorksSpace.show(screen)
    #pygame.draw.rect(screen, (255,0,0), pygame.Rect(levelWorksSpace.fitThePosition([mainCharacter.physics.hitbox.x, mainCharacter.physics.hitbox.y]), mainCharacter.physics.hitbox.size), 10)
    pygame.display.update()
    CLOCK.tick(FPS)