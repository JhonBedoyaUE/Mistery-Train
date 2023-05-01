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
        self.defaultMenu = None#create_game_inventary_interface() # Default menu to show when all menus closed
        self.worksSpacesStack = [template.create_level(windowSize)] # List of loaded levels
        self.actualLevel = 0 # Actual position of the actual level in the workspacesStack
        self.isInTrasition = False # Determines if theres a transition happenning
        self.finalLevelTransition = None # The position of the destiny level 

        for menu in self.contextualMenusStack:
            menu.parent = self
        
        if self.defaultMenu is not None:
            self.defaultMenu.parent = self

        for level in self.worksSpacesStack:
            level.parent = self
    
    def show_menu(self, newMenu:ContextualMenu):
        newMenu.parent = self
        if newMenu.closeAllMenusBeforeShow:
            for menu in self.contextualMenusStack:
                menu.close()
            self.contextualMenusStack = []
        
        self.contextualMenusStack.append(newMenu)



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
            keys = pygame.key.get_pressed()
            
            if len(self.contextualMenusStack) > 0:
                entitiesStack = self.contextualMenusStack[::-1]
            elif self.defaultMenu is not None:
                entitiesStack = [self.defaultMenu]
            else:
                entitiesStack = []
            
            entitiesStack += self.worksSpacesStack[::-1]

            listenning = True
            for entity in entitiesStack:
                entity.update_all(self.FPS)
                if listenning:
                    entity.listen_keys_all(keys)
                    entity.listen_mouse(mousePosition, mousePressed)
                    listenning = not entity.preventOthersListening

                
                if entity.preventOthersUpdates:
                    break
            
            for entity in entitiesStack[::-1]:
                entity.show(self.windowSurface)
            
            pygame.display.update()

            if keys[pygame.K_p]:
                self.show_menu(create_paused_menu())
            self.CLOCK.tick(self.FPS)