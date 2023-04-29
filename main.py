import pygame
import levels.levelExample as template

#Importante: Para no saturar el archivo principal los niveles deben crearse como archivos .py en la carpeta /levels
# En el archivo del nivel debe existir una funcion llamada create_level() que retornara el LevelWorsSpace del nivel 
# Ademas los modulos deben estar en la carpeta /game_modules para mantener en orden los archivos del juego
# Aún falta integracion con el mouse, textos o menus contextuales

pygame.init()

FPS = 60
CLOCK = pygame.time.Clock()
SIZE = (800,600)

screen = pygame.display.set_mode(SIZE)

levelWorksSpace = template.create_level(SIZE)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
    if not running:
        break

    screen.fill((0,0,0))

    keys = pygame.key.get_pressed()

    levelWorksSpace.listen_mouse(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3))

    levelWorksSpace.listen_keys_all(pygame.key.get_pressed())


    levelWorksSpace.show(screen)

    levelWorksSpace.update_all(FPS)
    pygame.display.update()
    CLOCK.tick(FPS)
