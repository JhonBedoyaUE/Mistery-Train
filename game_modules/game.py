import pygame
from game_modules.entities import *
from game_modules.utilities import *
from menus.basic_game_menus import *
import levels.levelExample as template

class GameManager:
    def __init__(self, windowSize:tuple[int]=(800,600), FPS:int=30):
        pygame.init()
        self.windowSize = windowSize
        self.FPS = FPS
        self.windowSurface = pygame.display.set_mode(self.windowSize)
        self.running = False
        self.CLOCK = pygame.time.Clock()
        self.contextualMenusStack = [] # List of the loaded contextual menus
        #self.contextualMenusStack[0].physics.position = [400,500]
        self.defaultMenu = create_game_inventary_interface() # Default menu to show when all menus closed
        self.worksSpacesStack = [template.create_level(windowSize)] # List of loaded levels
        self.actualLevel = 0 # Actual position of the actual level in the workspacesStack
        self.isInTrasition = False # Determines if theres a transition happenning
        self.finalLevelTransition = None # The position of the destiny level 



    def start_game(self):
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
            if not self.running:
                break

            self.windowSurface.fill((0,0,0))

            mousePosition = pygame.mouse.get_pos()
            mousePressed = pygame.mouse.get_pressed(3)

            self.worksSpacesStack[self.actualLevel].listen_mouse(mousePosition, mousePressed)
            self.defaultMenu.listen_mouse(mousePosition, mousePressed)

            keys = pygame.key.get_pressed()
            self.worksSpacesStack[self.actualLevel].listen_keys_all(keys)
            self.defaultMenu.listen_keys_all(keys)

            self.worksSpacesStack[self.actualLevel].show(self.windowSurface)
            self.defaultMenu.show(self.windowSurface)

            self.worksSpacesStack[self.actualLevel].update_all(self.FPS)
            self.defaultMenu.update_all(self.FPS)
            
            
            pygame.display.update()
            self.CLOCK.tick(self.FPS)