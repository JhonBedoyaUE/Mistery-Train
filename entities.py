import pygame, math
from utilities import *
        
class Entity:

    def __init__(self, physics:list|Physics, animation:Animation, location:int=Location.LEFT_TOP, eventListeners:dict={}, collideListeners:dict={}) -> None:
        """Initialize the object .

        Args:
            physics (list): [description]
            animation (Animation): [description]
            location (int, optional): [description]. Defaults to Location.LEFT_TOP.
            eventListeners (dict, optional): [description]. Defaults to {}.
        """
        
        if isinstance(physics, Physics):
            self.physics = physics
        else:
            self.physics = Physics(physics)
        self.animation = animation
        self.location = location
        self.eventListeners = eventListeners
        self.collideListeners = collideListeners
        self.physics.update_hitbox(pygame.Rect(self.physics.position, self.animation.get_texture().get_size()))
        self.entity_id = None
        self.parent = None
        self.type = None
    
    def listen_collide(self, collidedEntity):
        if collidedEntity.type in self.collideListeners.keys():
            self.collideListeners[collidedEntity.type](self, collidedEntity)

    def listen_keys(self, pressedEventList:list):
        for key, listener in self.eventListeners.items():
            listener(entity=self, state=pressedEventList[key])  

    def update(self, FPS:int) -> None:
        """Update the animation .

        Args:
            FPS (int): [description]
        """


        
        self.animation.update_frame(FPS)      
        self.physics.update_position(FPS)
        self.physics.update_hitbox(pygame.Rect(self.get_texture_position(), self.animation.get_texture().get_size()))
    
    def get_texture_position(self) -> list:
        """AI is creating summary for get_texture_position

        Returns:
            list: [description]
        """
        if self.location == Location.LEFT_TOP:
            return self.physics.position
        elif self.location == Location.CENTER_TOP:
            return [self.physics.position[0] - self.animation.get_texture().get_rect().width / 2, self.physics.position[1]]
        elif self.location == Location.RIGHT_TOP:
            return [self.physics.position[0] - self.animation.get_texture().get_rect().width, self.physics.position[1]]
        elif self.location == Location.CENTER_RIGHT:
            return [self.physics.position[0] - self.animation.get_texture().get_rect().width, self.physics.position[1] - self.animation.get_texture().get_rect().height / 2]
        elif self.location == Location.RIGHT_BOTTOM:
            return [self.physics.position[0] - self.animation.get_texture().get_rect().width, self.physics.position[1] - self.animation.get_texture().get_rect().height]
        elif self.location == Location.CENTER_BOTTOM:
            return [self.physics.position[0] - self.animation.get_texture().get_rect().width / 2, self.physics.position[1] - self.animation.get_texture().get_rect().height]
        elif self.location == Location.LEFT_BOTTOM:
            return [self.physics.position[0], self.physics.position[1] - self.animation.get_texture().get_rect().height]
        elif self.location == Location.CENTER_LEFT:
            return [self.physics.position[0], self.physics.position[1] - self.animation.get_texture().get_rect().height / 2]
        elif self.location == Location.CENTER:
            return [self.physics.position[0] - self.animation.get_texture().get_rect().width / 2, self.physics.position[1] - self.animation.get_texture().get_rect().height / 2]
        else:
            return self.physics.position

    def get_max_y_texture_position(self) -> list:
        """Returns the maximum y - coordinate position of the texture in the mesh .

        Returns:
            list: [description]
        """
        if self.location == Location.LEFT_TOP or self.location == Location.CENTER_TOP or self.location == Location.RIGHT_TOP:
            return self.physics.position[1] + self.animation.get_texture().get_rect().height
        elif self.location == Location.CENTER_RIGHT or self.location == Location.CENTER_LEFT or self.location == Location.CENTER:
            return self.physics.position[1] + self.animation.get_texture().get_rect().height / 2
        else:
            return self.physics.position[1]

def walk_to_left(entity:Entity, state:bool) -> None:
    """Walk the entity to the left and right .

    Args:
        entity (Entity): [description]
        state (bool): [description]
    """
    if state:
        entity.physics.direction = Direction.LEFT
        entity.physics.velocity[0] = -200
        entity.animation.change_actual_texture('xflip_Walk')
    else:
        if entity.physics.velocity[0] == -200:
            entity.physics.velocity[0] = 0
            entity.animation.change_actual_texture('xflip_Idle')
    
def walk_to_right(entity:Entity, state:bool) -> None:
    """Turn the entity to the right .

    Args:
        entity (Entity): [description]
        state (bool): [description]
    """
    if state:
        entity.physics.direction = Direction.RIGHT
        entity.physics.velocity[0] = 200
        entity.animation.change_actual_texture('Walk')
    else:
        if entity.physics.velocity[0] == 200:
            entity.physics.velocity[0] = 0
            entity.animation.change_actual_texture('Idle')

def walk_to_up(entity:Entity, state:bool) -> None:
    """Walk the scene to the animation .

    Args:
        entity (Entity): [description]
        state (bool): [description]
    """
    if state:
        #entity.direction = Direction.UP
        entity.physics.velocity[1] = -200
        if entity.physics.direction == Direction.LEFT:
            entity.animation.change_actual_texture('xflip_Walk')
        else:
            entity.animation.change_actual_texture('Walk')
    else:
        if entity.physics.velocity[1] == -200:
            entity.physics.velocity[1] = 0
            if entity.physics.direction == Direction.LEFT:
                entity.animation.change_actual_texture('xflip_Idle')
            else:
                entity.animation.change_actual_texture('Idle')
    
def walk_to_down(entity:Entity, state:bool) -> None:
    if state:
        #entity.direction = Direction.DOWN
        entity.physics.velocity[1] = 200
        if entity.physics.direction == Direction.LEFT:
            entity.animation.change_actual_texture('xflip_Walk')
        else:
            entity.animation.change_actual_texture('Walk')
    else:
        if entity.physics.velocity[1] == 200:
            entity.physics.velocity[1] = 0
            if entity.physics.direction == Direction.LEFT:
                entity.animation.change_actual_texture('xflip_Idle')
            else:
                entity.animation.change_actual_texture('Idle')
        
class Background(Entity):

    def __init__(self, physics:list|Physics, animation:Animation, displaySize:tuple, scalar=1.5, location=Location.LEFT_TOP, eventListeners:dict={}):
        """Initialize the animation .

        Args:
            physics (list): [description]
            animation (Animation): [description]
            displaySize (tuple): [description]
            scalar (float, optional): [description]. Defaults to 1.5.
            location ([type], optional): [description]. Defaults to Location.LEFT_TOP.
            eventListeners (dict, optional): [description]. Defaults to {}.
        """
        super().__init__(physics, animation, location, eventListeners=eventListeners)
        self.type = 'Background'

        self.displaySize = displaySize
 
        for key in self.animation.textures.keys():

            for index in range(self.animation.textures[key].lenght):
                textureAspectRatio = self.animation.textures[key].sprite[index].get_rect().height / self.animation.textures[key].sprite[index].get_rect().width
                displayAspectRatio = displaySize[1] / displaySize[0]
                if textureAspectRatio <= displayAspectRatio:
                    textureScalar = displaySize[1] * scalar / self.animation.textures[key].sprite[index].get_rect().height
                else:
                    textureScalar = displaySize[0] * scalar / self.animation.textures[key].sprite[index].get_rect().width
                self.animation.textures[key].sprite[index] = pygame.transform.scale_by(self.animation.textures[key].sprite[index], textureScalar)
    
    def get_texture(self) -> pygame.Surface:
        finalTexture = pygame.Surface(self.animation.textures[self.animation.actualTexture].sprite[self.animation.frame].get_size())
        finalTexture.set_colorkey((0,0,0,0))
        imageFrame = self.animation.textures[self.animation.actualTexture].sprite[self.animation.frame]
        width = imageFrame.get_width()
        height = imageFrame.get_height()
        x, y = self.physics.position
        if self.physics.position[0] > 0:
            self.physics.position[0] -= width
        elif self.physics.position[0] < -width:
            self.physics.position[0] += width

        if self.physics.position[1] > 0:
            self.physics.position[1] -= height
        elif self.physics.position[1] < -height:
            self.physics.position[1] += height
        
        finalTexture.blit(imageFrame, (x, y))
        finalTexture.blit(imageFrame,  (x + width, y))
        finalTexture.blit(imageFrame,  (x, y + height))
        finalTexture.blit(imageFrame,  (x + width, y + height))

        return finalTexture
    
    def get_texture_position(self) -> list:
        if self.location == Location.LEFT_TOP:
            return 0, 0
        elif self.location == Location.CENTER_TOP:
            return [-self.animation.get_texture().get_rect().width / 2, 0]
        elif self.location == Location.RIGHT_TOP:
            return [-self.animation.get_texture().get_rect().width, 0]
        elif self.location == Location.CENTER_RIGHT:
            return [-self.animation.get_texture().get_rect().width, -self.animation.get_texture().get_rect().height / 2]
        elif self.location == Location.RIGHT_BOTTOM:
            return [-self.animation.get_texture().get_rect().width, -self.animation.get_texture().get_rect().height]
        elif self.location == Location.CENTER_BOTTOM:
            return [-self.animation.get_texture().get_rect().width / 2, -self.animation.get_texture().get_rect().height]
        elif self.location == Location.LEFT_BOTTOM:
            return [0, -self.animation.get_texture().get_rect().height]
        elif self.location == Location.CENTER_LEFT:
            return [0, -self.animation.get_texture().get_rect().height / 2]
        elif self.location == Location.CENTER:
            return [-self.animation.get_texture().get_rect().width / 2, -self.animation.get_texture().get_rect().height / 2]
        else:
            return 0,0
        




basicCharacterBehaviour = {pygame.K_LEFT: walk_to_left, pygame.K_RIGHT: walk_to_right, pygame.K_UP: walk_to_up, pygame.K_DOWN: walk_to_down}

class MainCharacter(Entity):
    def __init__(self, physics:list|Physics, animation:Animation, location=Location.CENTER_BOTTOM, eventListeners:dict=basicCharacterBehaviour, collideListeners:dict={}):
        super().__init__(physics, animation, location, eventListeners=eventListeners, collideListeners=collideListeners)
        self.type = "MainCharacter"


def quick_backgrounds_sort(backgroundsList:list):
    if 0 < len(backgroundsList) - 1:
        pivot = backgroundsList[:1]
        left = []
        right = []
        
        for element in backgroundsList[1:]:
            if pivot[0].animation.zIndex > element.animation.zIndex:
                left.append(element)
            else:
                right.append(element)
                
        left = quick_backgrounds_sort(left)
        right = quick_backgrounds_sort(right)
        
        return left + pivot + right
        
    else:
        return backgroundsList    

def quick_entities_sort(entitiesList:list[Entity]):
    if 0 < len(entitiesList) - 1:
        pivot = entitiesList[:1]
        left = []
        right = []
        
        for element in entitiesList[1:]:
            if pivot[0].get_max_y_texture_position() > element.get_max_y_texture_position():
                left.append(element)
            else:
                right.append(element)
                
        left = quick_entities_sort(left)
        right = quick_entities_sort(right)
        
        return left + pivot + right
        
    else:
        return entitiesList  

def collide_and_limit(listeningEntity:Entity, entitiesList:list[Entity], changeColor:bool=True):
    collided = False
    if len(entitiesList) >= 1:
        for entity in entitiesList:
            horizontal = 0
            vertical = 0
            if listeningEntity.physics.hitbox.colliderect(entity.physics.hitbox):
                collided = True
                
                if listeningEntity.physics.isCollidable and entity.physics.isCollidable:
                    horizontal = listeningEntity.physics.position[0] - listeningEntity.physics.previousPosition[0]
                    vertical = listeningEntity.physics.position[1] - listeningEntity.physics.previousPosition[1]

                    if listeningEntity.physics.isPositionChanged:
                        if horizontal > 0:
                            pending = vertical / horizontal
                            newYPositionByX = (entity.physics.hitbox.left - listeningEntity.physics.hitbox.width) * pending + (listeningEntity.physics.hitbox.top - listeningEntity.physics.hitbox.left * pending)

                            if newYPositionByX + listeningEntity.physics.hitbox.height < entity.physics.hitbox.top or newYPositionByX > entity.physics.hitbox.top + entity.physics.hitbox.height:
                                #The movement must be returned on y axis
                                if vertical > 0: 
                                    #The movement must be returned to up  
                                    #print('up', f'prev: {listeningEntity.physics.previousHitbox.left}, {listeningEntity.physics.previousHitbox.top}; actu: {listeningEntity.physics.hitbox.left}, {listeningEntity.physics.hitbox.top}', end='; ')             
                                    listeningEntity.physics.position = [listeningEntity.physics.position[0],  listeningEntity.physics.position[1] + (entity.physics.hitbox.top - listeningEntity.physics.hitbox.height) - listeningEntity.physics.hitbox.top]
                                else:
                                    #Te movement must be returned to down
                                    #print('down', f'prev: {listeningEntity.physics.previousHitbox.left}, {listeningEntity.physics.previousHitbox.top}; actu: {listeningEntity.physics.hitbox.left}, {listeningEntity.physics.hitbox.top}', end='; ')
                                    listeningEntity.physics.position = [listeningEntity.physics.position[0],  listeningEntity.physics.position[1] + (entity.physics.hitbox.top + entity.physics.hitbox.height) - listeningEntity.physics.hitbox.top]
                            else:
                                #The movement must be returned to left
                                #print('left', f'prev: {listeningEntity.physics.previousHitbox.left}, {listeningEntity.physics.previousHitbox.top}; actu: {listeningEntity.physics.hitbox.left}, {listeningEntity.physics.hitbox.top}', end='; ') 
                                listeningEntity.physics.position = [listeningEntity.physics.position[0] + (entity.physics.hitbox.left - listeningEntity.physics.hitbox.width) - listeningEntity.physics.hitbox.left, listeningEntity.physics.position[1]]
                        elif horizontal < 0:
                            pending = vertical / horizontal
                            newYPositionByX = (entity.physics.hitbox.left + entity.physics.hitbox.width) * pending + (listeningEntity.physics.hitbox.top - listeningEntity.physics.hitbox.left * pending)


                            if newYPositionByX + listeningEntity.physics.hitbox.height < entity.physics.hitbox.top or newYPositionByX > entity.physics.hitbox.top + entity.physics.hitbox.height:
                                #The movement must be returned on y axis
                                if vertical > 0:  
                                    #The movement must be returned to up
                                    #print('up', f'prev: {listeningEntity.physics.previousHitbox.left}, {listeningEntity.physics.previousHitbox.top}; actu: {listeningEntity.physics.hitbox.left}, {listeningEntity.physics.hitbox.top}', end='; ')             
                                    listeningEntity.physics.position = [listeningEntity.physics.position[0],  listeningEntity.physics.position[1] + (entity.physics.hitbox.top - listeningEntity.physics.hitbox.height) - listeningEntity.physics.hitbox.top]
                                else:
                                    #Te movement must be returned to down
                                    #print('down', f'prev: {listeningEntity.physics.previousHitbox.left}, {listeningEntity.physics.previousHitbox.top}; actu: {listeningEntity.physics.hitbox.left}, {listeningEntity.physics.hitbox.top}', end='; ')
                                    listeningEntity.physics.position = [listeningEntity.physics.position[0],  listeningEntity.physics.position[1] + (entity.physics.hitbox.top + entity.physics.hitbox.height) - listeningEntity.physics.hitbox.top]
                            else:
                                #The movement must be returned to right
                                #print('right', f'prev: {listeningEntity.physics.previousHitbox.left}, {listeningEntity.physics.previousHitbox.top}; actu: {listeningEntity.physics.hitbox.left}, {listeningEntity.physics.hitbox.top}', end='; ') 
                                listeningEntity.physics.position = [listeningEntity.physics.position[0] + (entity.physics.hitbox.left + entity.physics.hitbox.width) - listeningEntity.physics.hitbox.left, listeningEntity.physics.position[1]]
                        else:
                            #The movement must be returned on y axis
                            if vertical > 0:
                                #The movement must be returned to up
                                #print('up', f'prev: {listeningEntity.physics.previousHitbox.left}, {listeningEntity.physics.previousHitbox.top}; actu: {listeningEntity.physics.hitbox.left}, {listeningEntity.physics.hitbox.top}', end='; ') 
                                listeningEntity.physics.position = [listeningEntity.physics.position[0],  listeningEntity.physics.position[1] + (entity.physics.hitbox.top - listeningEntity.physics.hitbox.height) - listeningEntity.physics.hitbox.top]
                            elif vertical < 0:
                                #Te movement must be returned to down
                                #print('down', f'prev: {listeningEntity.physics.previousHitbox.left}, {listeningEntity.physics.previousHitbox.top}; actu: {listeningEntity.physics.hitbox.left}, {listeningEntity.physics.hitbox.top}', end='; ')
                                listeningEntity.physics.position = [listeningEntity.physics.position[0],  listeningEntity.physics.position[1] + (entity.physics.hitbox.top + entity.physics.hitbox.height) - listeningEntity.physics.hitbox.top]
                        listeningEntity.physics.update_hitbox(pygame.Rect(listeningEntity.get_texture_position(), listeningEntity.animation.get_texture().get_size()))
                        #print(f'nuev: {listeningEntity.physics.hitbox.left}, {listeningEntity.physics.hitbox.top}')

                if changeColor:
                    entity.physics.hitboxColor = (255,100,0)

                listeningEntity.listen_collide(entity)
                entity.listen_collide(listeningEntity)
            else:
                if changeColor:
                    entity.physics.hitboxColor = (0,200,255)
    
            
    if collided:
        if changeColor:
            listeningEntity.physics.hitboxColor = (255,100,0)
        #listeningEntity.physics.previousPosition
    else:
        if changeColor:
            listeningEntity.physics.hitboxColor = (0,200,255)

class LevelWorksSpace(Entity):
    def __init__(self, levelSize:tuple, background:Background|list, mainCharacter:MainCharacter, displaySize:tuple, entitiesList:Entity|list=[], physics:list|Physics=Physics([0, 0]), animation=Animation(), location=Location.LEFT_TOP, eventListeners:dict={}, backgroundColor:tuple=(0,0,255)) -> None:
        super().__init__(physics, animation, location, eventListeners=eventListeners)

        self.areBackgroundsSorted = False
        self.areEntitiesSorted = False
        self.globals = {}
        self.mainCharacter = mainCharacter
        self.mainCharacter.parent = self

        self.entities = {}
        if self.mainCharacter.entity_id is not None:
            self.entities[self.mainCharacter.entity_id] = self.mainCharacter.entity_id


        self.displaySize = displaySize
        self.levelSize =levelSize
        self.backgroundColor = backgroundColor
        self.background = pygame.Surface(displaySize)
        self.type = "LevelWorksSpace"
        
        if isinstance(background, Background):
            self.backgroundList = [background]
        else:
            self.backgroundList = background

        for bacground in self.backgroundList:
            bacground.parent = self
            if bacground.entity_id is not None:
                self.entities[bacground.entity_id] = bacground.entity_id

        if isinstance(entitiesList, Entity):
            self.entitiesList = [entitiesList]
        else:
            self.entitiesList = entitiesList
        
        for entity in self.entitiesList:
            entity.parent = self
            if entity.entity_id is not None:
                self.entities[entity.entity_id] = entity.entity_id
        
        self.update_backgrounds()

    def update_entities(self, FPS:int=0) -> None:
        if not self.areEntitiesSorted:
            self.entitiesList = quick_entities_sort(self.entitiesList)
            self.areEntitiesSorted = True
            print([entity.get_max_y_texture_position() for entity in self.entitiesList])
        if FPS > 0:
            for entityIndex in range(len(self.entitiesList)):
                self.entitiesList[entityIndex].update(FPS)

    
    def update_backgrounds(self, FPS:int=0) -> None:
        if not self.areBackgroundsSorted:
            self.backgroundList = quick_backgrounds_sort(self.backgroundList)
            self.areBackgroundsSorted = True
        if FPS > 0:
            self.background.fill(self.backgroundColor)
            for backgroundIndex in range(len(self.backgroundList)):
                self.backgroundList[backgroundIndex].update(FPS)
                self.background.blit(self.backgroundList[backgroundIndex].get_texture(), self.fitThePosition(self.backgroundList[backgroundIndex].get_texture_position()))
    
    def update_works_space_position(self) -> None:
        """Compute the works space position to try centrate de main character."""

        # computing axis x position offset
        if self.mainCharacter.physics.position[0] <= self.displaySize[0] / 2:
            self.physics.position[0] = 0

        elif self.mainCharacter.physics.position[0] >= self.levelSize[0] - self.displaySize[0] / 2:
            self.physics.position[0] = -1 * (self.levelSize[0] - self.displaySize[0])

        else:
            self.physics.position[0] = -1 * (self.mainCharacter.physics.position[0] - self.displaySize[0] / 2)

        # computing axis y position offset 
        if self.mainCharacter.physics.position[1] <= self.displaySize[1] / 2:
            self.physics.position[1] = 0

        elif self.mainCharacter.physics.position[1] >= self.levelSize[1] - self.displaySize[1] / 2:
            self.physics.position[1] = -1 * (self.levelSize[1] - self.displaySize[1])

        else:
            self.physics.position[1] = -1 * (self.mainCharacter.physics.position[1] - self.displaySize[1] / 2)
            print('e3')
    
    def update_all(self, FPS:int) -> None:        

        self.mainCharacter.update(FPS)
        self.update_backgrounds(FPS=FPS)
        self.update_entities(FPS=FPS)
        self.update_works_space_position()
        collide_and_limit(self.mainCharacter, self.entitiesList)
        
    
    def fitThePosition(self, position:list) -> list:
        return self.physics.position[0] + position[0], self.physics.position[1] + position[1]
    
    def listen_keys(self, keyPressedList) -> None:
        self.mainCharacter.listen_keys(keyPressedList)
        for background in self.backgroundList:
            background.listen_keys(keyPressedList)

    def show(self, display:pygame.Surface, showHitbox=False) -> None:
        display.blit(self.background, (0,0))
        isMainCharacterShowed = False
        if showHitbox:
            hitboxesImage = pygame.Surface(self.levelSize)
            hitboxesImage.set_colorkey((0,0,0))
            pygame.draw.rect(hitboxesImage, self.mainCharacter.physics.hitboxColor, self.mainCharacter.physics.hitbox, 10)

        for entity in self.entitiesList:
            if not isMainCharacterShowed and entity.get_max_y_texture_position() > self.mainCharacter.get_max_y_texture_position():
                display.blit(self.mainCharacter.animation.get_texture(), self.fitThePosition(self.mainCharacter.get_texture_position()))
                isMainCharacterShowed = True
                    
            display.blit(entity.animation.get_texture(), self.fitThePosition(entity.get_texture_position()))
            if showHitbox:
                pygame.draw.rect(hitboxesImage, entity.physics.hitboxColor, entity.physics.hitbox, 10)
        if not isMainCharacterShowed:
            display.blit(self.mainCharacter.animation.get_texture(), self.fitThePosition(self.mainCharacter.get_texture_position()))
        
        if showHitbox:
            display.blit(hitboxesImage, self.fitThePosition((0,0)))
        
    
 