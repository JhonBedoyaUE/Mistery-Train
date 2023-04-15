import pygame, math
from utilities import *
        
class Entity:
    def __init__(self, position:list, animation:Animation, velocity:list=[0, 0], aceleration:list=[0, 0], location:int=Location.LEFTTOP) -> None:
        self.position = position
        self.animation = animation
        self.velocity = velocity
        self.aceleration = aceleration
        self.location = location

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
                self.animation.frame = 0
                self.animation.animationTime = 0
        elif self.animation.animationIterationBehavior == AnimationIterationBehavior.ONCE:
            if self.animation.frame >= self.get_frame_limit():
                self.animation.frame = self.get_frame_limit() - 1
                self.animation.animationTime = self.animation.frame / self.animation.FPS
        else:
            if self.animation.animationIterationCount < self.animation.animationIterationLimit:
                if self.animation.frame >= self.get_frame_limit():
                    self.animation.frame = 0
                    self.animation.animationTime = 0
                    self.animation.animationIterationCount += 1
            else:
                if self.animation.frame >= self.get_frame_limit():
                    self.animation.frame = self.get_frame_limit() - 1
                    self.animation.animationTime = self.animation.frame / self.animation.FPS

    def change_actual_texture(self, textureName:str) -> None:
        self.animation.actualTexture = textureName
        if self.animation.frame >= self.get_frame_limit():
            self.animation.frame = 0
            self.animation.animationTime = 0


    def get_texture(self) -> pygame.Surface:
        return self.animation.textures[self.animation.actualTexture].sprite[self.animation.frame]

    def compute_position(self, time:float) -> None:
        finalVelocity = [self.velocity[0] + self.aceleration[0] * time, self.velocity[1] + self.aceleration[1] * time]
        self.position = [self.position[0] + (self.velocity[0] + finalVelocity[0]) / 2 * time,
                         self.position[1] + (self.velocity[1] + finalVelocity[1]) / 2 * time]
        self.velocity = finalVelocity    

    def update(self, FPS:int) -> None:
        """Update the textures frames and physics attributes with the give FPS.
        Args:
            FPS (int): Frames per second
        """
        time = 1 / FPS
        self.animation.animationTime += time
        self.animation.frame = math.floor(self.animation.animationTime * self.animation.FPS)

        self.limit_frame()
        

        self.compute_position(time)
    
    def get_texture_position(self) -> list:
        if self.location == Location.LEFTTOP:
            return self.position
        elif self.location == Location.CENTERTOP:
            return [self.position[0] - self.get_texture().get_rect().width / 2, self.position[1]]
        elif self.location == Location.RIGHTTOP:
            return [self.position[0] - self.get_texture().get_rect().width, self.position[1]]
        elif self.location == Location.CENTERRIGHT:
            return [self.position[0] - self.get_texture().get_rect().width, self.position[1] - self.get_texture().get_rect().height / 2]
        elif self.location == Location.RIGHTBOTTOM:
            return [self.position[0] - self.get_texture().get_rect().width, self.position[1] - self.get_texture().get_rect().height]
        elif self.location == Location.CENTERBOTTOM:
            return [self.position[0] - self.get_texture().get_rect().width / 2, self.position[1] - self.get_texture().get_rect().height]
        elif self.location == Location.LEFTBOTTOM:
            return [self.position[0], self.position[1] - self.get_texture().get_rect().height]
        elif self.location == Location.CENTERLEFT:
            return [self.position[0], self.position[1] - self.get_texture().get_rect().height / 2]
        elif self.location == Location.CENTER:
            return [self.position[0] - self.get_texture().get_rect().width / 2, self.position[1] - self.get_texture().get_rect().height / 2]
        else:
            return self.position
        
class Background(Entity):
    def __init__(self, position, animation:Animation, displaySize, scalar=1.5, velocity=[0, 0], aceleration=[0, 0], location=Location.LEFTTOP):
        super().__init__(position, animation, velocity, aceleration, location)

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

class MainCharacter(Entity):
    def __init__(self, position:list, animation:Animation, velocity=[0, 0], aceleration=[0, 0], location=Location.CENTERBOTTOM):
        super().__init__(position, animation, velocity, aceleration, location)

class LevelWorksSpace(Entity):
    def __init__(self, background:Background, mainCharacter:MainCharacter,  position=[0, 0], animation=Animation(), velocity=[0, 0], aceleration=[0, 0], location=Location.LEFTTOP):
        super().__init__(position, animation, velocity, aceleration, location)
        self.background = background
        self.mainCharacter = mainCharacter
    
    def compute_position(self):
        """Compute the works space position to try centrate de main character."""

        # computing axis x position offset
        if self.mainCharacter.position[0] <= self.background.displaySize[0] / 2:
            self.position[0] = 0

        elif self.mainCharacter.position[0] >= self.background.get_texture().get_rect().width - self.background.displaySize[0] / 2:
            self.position[0] = -1 * (self.background.get_texture().get_rect().width - self.background.displaySize[0])

        else:
            self.position[0] = -1 * (self.mainCharacter.position[0] - self.background.displaySize[0] / 2)

        # computing axis y position offset 
        if self.mainCharacter.position[1] <= self.background.displaySize[1] / 2:
            self.position[1] = 0

        elif self.mainCharacter.position[1] >= self.background.get_texture().get_rect().height - self.background.displaySize[1] / 2:
            self.position[1] = -1 * (self.background.get_texture().get_rect().height - self.background.displaySize[1])

        else:
            self.position[1] = -1 * (self.mainCharacter.position[1] - self.background.displaySize[1] / 2)
    
    def update(self, FPS:int) -> None:        

        self.mainCharacter.update(FPS)
        self.background.update(FPS)

        time = 1 / FPS

        self.compute_position()
    
    def fitThePosition(self, position:list) -> list:
        return self.position[0] + position[0], self.position[1] + position[1]
 