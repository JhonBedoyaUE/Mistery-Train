import pygame, math
from utilities import *
        
class Entity:

    def __init__(self, physics:list|Physics, animation:Animation, location:int=Location.LEFT_TOP, eventListeners:dict={}) -> None:
        if isinstance(physics, Physics):
            self.physics = physics
        else:
            self.physics = Physics(physics)
        self.animation = animation
        self.location = location
        self.eventListeners = eventListeners

    def listen_events(self, pressedEventList:list, collisionEventList:list=[]):
        if EventListener.LISTEN_KEY in self.eventListeners.keys():
            keyListeners = self.eventListeners[EventListener.LISTEN_KEY]
            for key, listener in keyListeners.items():
                listener(entity=self, state=pressedEventList[key])
        elif EventListener.LISTEN_COLLISION in self.eventListeners.keys():
            collisionListeners = self.eventListeners[EventListener.LISTEN_COLLISION]
            for objectType, listener in collisionListeners.items():
                listener(entity=self, state=collisionEventList[objectType])

    def get_frame_limit(self) -> int:
        if self.animation.frameLimit == 0:
            return self.animation.textures[self.animation.actualTexture].lenght
        elif self.animation.frameLimit >= 1:
            return self.animation.frameLimit
        else:
            return self.animation.textures[self.animation.actualTexture].lenght + self.animation.frameLimit
    
    def limit_frame(self) -> None:
        if self.animation.animationIterationBehavior == AnimationIterationBehavior.INFINITE:
            if self.animation.frame >= self.get_frame_limit():
                self.animation.frame = self.animation.startFrame
                self.animation.animationTime = 0
        elif self.animation.animationIterationBehavior == AnimationIterationBehavior.ONCE:
            if self.animation.frame >= self.get_frame_limit():
                self.animation.frame = self.get_frame_limit() - 1
                self.animation.animationTime = self.animation.frame / self.animation.FPS
        else:
            if self.animation.animationIterationCount < self.animation.animationIterationLimit:
                if self.animation.frame >= self.get_frame_limit():
                    self.animation.frame = self.animation.startFrame
                    self.animation.animationTime = 0
                    self.animation.animationIterationCount += 1
            else:
                if self.animation.frame >= self.get_frame_limit():
                    self.animation.frame = self.get_frame_limit() - 1
                    self.animation.animationTime = self.animation.frame / self.animation.FPS

    def change_actual_texture(self, textureName:str) -> None:
        self.animation.actualTexture = textureName

        if self.animation.startFrame >= self.get_frame_limit():
            self.animation.startFrame = self.get_frame_limit() - 1
            
        if self.animation.frame >= self.get_frame_limit():
            self.animation.frame = self.animation.startFrame
            self.animation.animationTime = 0


    def get_texture(self) -> pygame.Surface:
        return self.animation.textures[self.animation.actualTexture].sprite[self.animation.frame]

    def compute_position(self, time:float) -> None:
        finalVelocity = [self.physics.velocity[0] + self.physics.aceleration[0] * time, self.physics.velocity[1] + self.physics.aceleration[1] * time]
        self.physics.position = [self.physics.position[0] + (self.physics.velocity[0] + finalVelocity[0]) / 2 * time,
                         self.physics.position[1] + (self.physics.velocity[1] + finalVelocity[1]) / 2 * time]
        self.physics.velocity = finalVelocity    

    def update(self, FPS:int) -> None:
        """Update the textures frames and physics attributes with the give FPS.
        Args:
            FPS (int): Frames per second
        """
        time = 1 / FPS
        self.animation.animationTime += time
        self.animation.frame = math.floor(self.animation.animationTime * self.animation.FPS) + self.animation.startFrame
        self.limit_frame()        
        self.compute_position(time)
    
    def get_texture_position(self) -> list:
        if self.location == Location.LEFT_TOP:
            return self.physics.position
        elif self.location == Location.CENTER_TOP:
            return [self.physics.position[0] - self.get_texture().get_rect().width / 2, self.physics.position[1]]
        elif self.location == Location.RIGHT_TOP:
            return [self.physics.position[0] - self.get_texture().get_rect().width, self.physics.position[1]]
        elif self.location == Location.CENTER_RIGHT:
            return [self.physics.position[0] - self.get_texture().get_rect().width, self.physics.position[1] - self.get_texture().get_rect().height / 2]
        elif self.location == Location.RIGHT_BOTTOM:
            return [self.physics.position[0] - self.get_texture().get_rect().width, self.physics.position[1] - self.get_texture().get_rect().height]
        elif self.location == Location.CENTER_BOTTOM:
            return [self.physics.position[0] - self.get_texture().get_rect().width / 2, self.physics.position[1] - self.get_texture().get_rect().height]
        elif self.location == Location.LEFT_BOTTOM:
            return [self.physics.position[0], self.physics.position[1] - self.get_texture().get_rect().height]
        elif self.location == Location.CENTER_LEFT:
            return [self.physics.position[0], self.physics.position[1] - self.get_texture().get_rect().height / 2]
        elif self.location == Location.CENTER:
            return [self.physics.position[0] - self.get_texture().get_rect().width / 2, self.physics.position[1] - self.get_texture().get_rect().height / 2]
        else:
            return self.physics.position

def walk_to_left(entity:Entity, state:bool):
    if state:
        entity.physics.direction = Direction.LEFT
        entity.physics.velocity[0] = -100
        entity.change_actual_texture('xflip_Walk')
    else:
        if entity.physics.velocity[0] == -100:
            entity.physics.velocity[0] = 0
            entity.change_actual_texture('xflip_Idle')
    
def walk_to_right(entity:Entity, state:bool):
    if state:
        entity.physics.direction = Direction.RIGHT
        entity.physics.velocity[0] = 100
        entity.change_actual_texture('Walk')
    else:
        if entity.physics.velocity[0] == 100:
            entity.physics.velocity[0] = 0
            entity.change_actual_texture('Idle')

def walk_to_up(entity:Entity, state:bool):
    if state:
        #entity.direction = Direction.UP
        entity.physics.velocity[1] = -100
        if entity.physics.direction == Direction.LEFT:
            entity.change_actual_texture('xflip_Walk')
        else:
            entity.change_actual_texture('Walk')
    else:
        if entity.physics.velocity[1] == -100:
            entity.physics.velocity[1] = 0
            if entity.physics.direction == Direction.LEFT:
                entity.change_actual_texture('xflip_Idle')
            else:
                entity.change_actual_texture('Idle')
    
def walk_to_down(entity:Entity, state:bool):
    if state:
        #entity.direction = Direction.DOWN
        entity.physics.velocity[1] = 100
        if entity.physics.direction == Direction.LEFT:
            entity.change_actual_texture('xflip_Walk')
        else:
            entity.change_actual_texture('Walk')
    else:
        if entity.physics.velocity[1] == 100:
            entity.physics.velocity[1] = 0
            if entity.physics.direction == Direction.LEFT:
                entity.change_actual_texture('xflip_Idle')
            else:
                entity.change_actual_texture('Idle')
        
class Background(Entity):
    def __init__(self, physics:list|Physics, animation:Animation, displaySize, scalar=1.5, location=Location.LEFT_TOP, eventListeners:dict={}):
        super().__init__(physics, animation, location, eventListeners=eventListeners)

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
            return [-self.get_texture().get_rect().width / 2, 0]
        elif self.location == Location.RIGHT_TOP:
            return [-self.get_texture().get_rect().width, 0]
        elif self.location == Location.CENTER_RIGHT:
            return [-self.get_texture().get_rect().width, -self.get_texture().get_rect().height / 2]
        elif self.location == Location.RIGHT_BOTTOM:
            return [-self.get_texture().get_rect().width, -self.get_texture().get_rect().height]
        elif self.location == Location.CENTER_BOTTOM:
            return [-self.get_texture().get_rect().width / 2, -self.get_texture().get_rect().height]
        elif self.location == Location.LEFT_BOTTOM:
            return [0, -self.get_texture().get_rect().height]
        elif self.location == Location.CENTER_LEFT:
            return [0, -self.get_texture().get_rect().height / 2]
        elif self.location == Location.CENTER:
            return [-self.get_texture().get_rect().width / 2, -self.get_texture().get_rect().height / 2]
        else:
            return 0,0



basicCharacterBehaviour = {EventListener.LISTEN_KEY: {pygame.K_LEFT: walk_to_left, pygame.K_RIGHT: walk_to_right, pygame.K_UP: walk_to_up, pygame.K_DOWN: walk_to_down}}

class MainCharacter(Entity):
    def __init__(self, physics:list|Physics, animation:Animation, location=Location.CENTER_BOTTOM, eventListeners:dict=basicCharacterBehaviour):
        super().__init__(physics, animation, location, eventListeners=eventListeners)

        

class LevelWorksSpace(Entity):
    def __init__(self, background:Background, mainCharacter:MainCharacter,  physics:list|Physics=Physics([0, 0]), animation=Animation(), location=Location.LEFT_TOP, eventListeners:dict={}):
        super().__init__(physics, animation, location, eventListeners=eventListeners)
        self.background = background
        self.mainCharacter = mainCharacter
    
    def compute_position(self):
        """Compute the works space position to try centrate de main character."""

        # computing axis x position offset
        if self.mainCharacter.physics.position[0] <= self.background.displaySize[0] / 2:
            self.physics.position[0] = 0

        elif self.mainCharacter.physics.position[0] >= self.background.get_texture().get_rect().width - self.background.displaySize[0] / 2:
            self.physics.position[0] = -1 * (self.background.get_texture().get_rect().width - self.background.displaySize[0])

        else:
            self.physics.position[0] = -1 * (self.mainCharacter.physics.position[0] - self.background.displaySize[0] / 2)

        # computing axis y position offset 
        if self.mainCharacter.physics.position[1] <= self.background.displaySize[1] / 2:
            self.physics.position[1] = 0

        elif self.mainCharacter.physics.position[1] >= self.background.get_texture().get_rect().height - self.background.displaySize[1] / 2:
            self.physics.position[1] = -1 * (self.background.get_texture().get_rect().height - self.background.displaySize[1])

        else:
            self.physics.position[1] = -1 * (self.mainCharacter.physics.position[1] - self.background.displaySize[1] / 2)
            print('e3')
    
    def update(self, FPS:int) -> None:        

        self.mainCharacter.update(FPS)
        self.background.update(FPS)

        time = 1 / FPS

        self.compute_position()
    
    def fitThePosition(self, position:list) -> list:
        return self.physics.position[0] + position[0], self.physics.position[1] + position[1]
    
    def listen_events(self, keyPressedList):
        self.mainCharacter.listen_events(keyPressedList)
        self.background.listen_events(keyPressedList)
    
 