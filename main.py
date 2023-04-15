import pygame
from entities import *
from utilities import *

pygame.init()

#entonces instalalo y tambien instala python desde la pagina oficial 
#Python:https://www.python.org/downloads/
#VSCode: https://code.visualstudio.com/download
#instalo la ultima version de py? si y cuando este en visual en la 
# pagina de inicio te debe aparacer la opcion de configurarlo para varios lenguajes 
#puedes crear un archivo .py para que te recomiende el lenguaje a configurar
#En visual no habia una extension?
FPS = 60
CLOCK = pygame.time.Clock()
SIZE = (800,600)

screen = pygame.display.set_mode(SIZE)

bgTextures = create_textures(['bg1.png'], [1])
mcTextures = create_textures(['Idle.png', 'Walk.png', 'Jump.png'], [6, 9, 9], path='textures/Samurai/', variations=2, transformFunction=Transformation.XFLIP, scalar=2)

bg = Background((0,0), Animation(textures=bgTextures, actualTexture='bg1'), SIZE, scalar=1)

mainCharacter = MainCharacter([100, 250], Animation(textures=mcTextures, actualTexture='xflip_Idle'), location=Location.CENTER)

levelWorksSpace = LevelWorksSpace(bg, mainCharacter)



running = True
suffix = ''
jumping = False
initialYPosition = 0

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

    if jumping:
        if mainCharacter.velocity[1] >= 0:
            mainCharacter.animation.frameLimit = -2
        if mainCharacter.position[1] > initialYPosition:
            jumping = False
            mainCharacter.position[1] = initialYPosition
            mainCharacter.velocity[1] = 0
            mainCharacter.aceleration = [0, 0]
            
    else:
        if keys[pygame.K_SPACE]:
            jumping = True
            initialYPosition = mainCharacter.position[1]
            mainCharacter.velocity[1] = -750
            mainCharacter.aceleration[1] = 2500
            mainCharacter.change_actual_texture(suffix+'Jump')
            mainCharacter.animation.animationIterationBehavior = AnimationIterationBehavior.ONCE
            mainCharacter.animation.frameLimit = 2
        else:
            mainCharacter.animation.animationIterationBehavior = AnimationIterationBehavior.INFINITE
            mainCharacter.animation.frameLimit = 0
            if keys[pygame.K_RIGHT]:
                suffix = ''
                mainCharacter.velocity[0] = 100
                mainCharacter.change_actual_texture(suffix+'Walk')
            elif keys[pygame.K_LEFT]:
                suffix = 'xflip_'
                mainCharacter.velocity[0] = -100
                mainCharacter.change_actual_texture(suffix+'Walk')
            else:
                mainCharacter.velocity[0] = 0

            if keys[pygame.K_UP]:
                mainCharacter.velocity[1] = -100
                mainCharacter.change_actual_texture(suffix+'Walk')
            elif keys[pygame.K_DOWN]:
                mainCharacter.velocity[1] = 100
                mainCharacter.change_actual_texture(suffix+'Walk')
            else:
                mainCharacter.velocity[1] = 0

            if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                mainCharacter.velocity = [0, 0]
                mainCharacter.change_actual_texture(suffix+'Idle')

    screen.blit(bg.get_texture(), levelWorksSpace.fitThePosition(bg.get_texture_position()))
    screen.blit(mainCharacter.get_texture(), levelWorksSpace.fitThePosition(mainCharacter.get_texture_position()))
    pygame.display.update()
    CLOCK.tick(FPS)