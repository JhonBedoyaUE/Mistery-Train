import pygame, types, math

class Direction:
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

class Location:
    LEFT_TOP = 0
    CENTER_TOP = 1
    RIGHT_TOP = 2
    CENTER_RIGHT = 3
    RIGHT_BOTTOM = 4
    CENTER_BOTTOM = 5
    LEFT_BOTTOM = 6
    CENTER_LEFT = 7
    CENTER = 8
    CUSTOM = 9

class AnimationDirection:
    NORMAL = 0
    REVERSE = 1
    ALTERNATE = 2
    ALTERNATE_REVERSE = 3

class AnimationIterationBehavior:
    INFINITE = -1
    CUSTOM = 0
    ONCE = 1

class Texture:
    def __init__(self, sprite:pygame.Surface, lenght:int=-1) -> None:
        if lenght >= 0:
            self.lenght = lenght
            self.sprite = []
            spriteWidth = math.floor(sprite.get_rect().width / lenght)
            spriteHeight = sprite.get_rect().height
            for i in range(lenght):
                self.sprite.append(sprite.subsurface((spriteWidth * i, 0, spriteWidth, spriteHeight)))
        else:
            self.lenght = len(sprite)
            self.sprite = sprite

def find_content(surface:pygame.Surface) -> pygame.Rect:
    minX = surface.get_width()
    maxX = 0
    minY = surface.get_height()
    maxY = 0
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            color = surface.get_at((x,y))
            if color[3] != 0:
                if x < minX:
                    minX = x
                if x > maxX:
                    maxX = x
                if y < minY:
                    minY = y
                if y > maxY:
                    maxY = y
    return pygame.Rect(minX, minY, maxX - minX, maxY - minY)

def extract_content(surface:pygame.Surface, extract) -> pygame.Rect:
    if extract:
        return surface.subsurface(find_content(surface))
    else:
        return surface

class Transformation:
    def IDENTITY(sprite:Texture, variationIndex:int, name:str, scalar:float=1, extractContent:bool=False) -> dict:
        scalledSprite = [extract_content(pygame.transform.scale_by(frame, scalar), extractContent) for frame in sprite.sprite]
        return {'sprite': Texture(scalledSprite), 'name': name}

    def XFLIP(sprite:Texture, variationIndex:int, name:str, scalar:float=1, extractContent:bool=False) -> dict:
        flippedSprite = [extract_content(pygame.transform.scale_by(pygame.transform.flip(frame, flip_x=(variationIndex != 0), flip_y=False), scalar), extractContent) for frame in sprite.sprite]
        return {'sprite': Texture(flippedSprite), 'name': ('xflip_'*(variationIndex != 0))+name}


        
def create_textures(fileNameList:list, spriteLeghtList:list, path:str='textures/', variations:int=1, transformFunction:types.FunctionType=Transformation.IDENTITY, scalar:float=1, extractContent:bool=False) -> dict:
    textures = {'default': Texture(pygame.Surface((500, 500)), 1)}
    for index in range(len(fileNameList)):
        sprite = pygame.image.load(path + fileNameList[index]).convert_alpha()
        for variationIndex in range(variations):
            texture = Texture(sprite, spriteLeghtList[index])
            textureVariation = transformFunction(texture, variationIndex, fileNameList[index].split('.')[0], scalar, extractContent)
            textures[textureVariation['name']] = textureVariation['sprite']
    return textures

def create_hitbox(dimentions:pygame.Rect, margin:list) -> pygame.Rect:
        if len(margin) == 1:
            left = margin[0]
            top = margin[0]
            right = margin[0]
            bottom = margin[0]
        elif len(margin) == 2:
            left = margin[0]
            top = margin[1]
            right = margin[0]
            bottom = margin[1]
        else:
            left = margin[0]
            top = margin[1]
            right = margin[2]
            bottom = margin[3]
        
        return pygame.Rect(dimentions.left - left, dimentions.top - top, dimentions.size[0] + left + right, dimentions.size[1] + top + bottom)

class Animation:
    def __init__(self, textures:dict=create_textures([], []), actualTexture:str='default', zIndex:int=0, frame:int=0, startFrame:int = 0, frameLimit:int=0, FPS:int=10, animationTime:int=0, animationIterationBehavior:int=AnimationIterationBehavior.INFINITE, animationIterationLimit:int=1, animationIterationCount:int=0) -> None:
        self.textures = textures
        self.actualTexture = actualTexture
        self.zIndex = zIndex
        self.frame = frame
        self.FPS = FPS
        self.animationTime = animationTime
        self.frameLimit = frameLimit
        self.animationIterationBehavior = animationIterationBehavior
        self.animationIterationCount = animationIterationCount
        self.animationIterationLimit = animationIterationLimit
        self.startFrame = startFrame
    
    def update_frame(self, FPS:int):
        time = 1 / FPS
        self.animationTime += time
        self.frame = math.floor(self.animationTime * self.FPS) + self.startFrame
        self.limit_frame()  
    
    def get_frame_limit(self) -> int:
        if self.frameLimit == 0:
            return self.textures[self.actualTexture].lenght
        elif self.frameLimit >= 1:
            return self.frameLimit
        else:
            return self.textures[self.actualTexture].lenght + self.frameLimit
    
    def limit_frame(self) -> None:
        if self.animationIterationBehavior == AnimationIterationBehavior.INFINITE:
            if self.frame >= self.get_frame_limit():
                self.frame = self.startFrame
                self.animationTime = 0
        elif self.animationIterationBehavior == AnimationIterationBehavior.ONCE:
            if self.frame >= self.get_frame_limit():
                self.frame = self.get_frame_limit() - 1
                self.animationTime = self.frame / self.FPS
        else:
            if self.animationIterationCount < self.animationIterationLimit:
                if self.frame >= self.get_frame_limit():
                    self.frame = self.startFrame
                    self.animationTime = 0
                    self.animationIterationCount += 1
            else:
                if self.frame >= self.get_frame_limit():
                    self.frame = self.get_frame_limit() - 1
                    self.animationTime = self.frame / self.FPS

    def change_actual_texture(self, textureName:str) -> None:
        self.actualTexture = textureName

        if self.startFrame >= self.get_frame_limit():
            self.startFrame = self.get_frame_limit() - 1
            
        if self.frame >= self.get_frame_limit():
            self.frame = self.startFrame
            self.animationTime = 0


    def get_texture(self) -> pygame.Surface:
        return self.textures[self.actualTexture].sprite[self.frame]

class Physics:
    def __init__(self, position:list, velocity:list=[0, 0], aceleration:list=[0, 0], direction:int=Direction.LEFT, limitRestrictions:bool=False, hitRestrictions:bool=False, dimentions:pygame.Rect=pygame.Rect(0,0,0,0), margin:list=[0]) -> None:
        self.position = position 
        self.velocity = velocity
        self.aceleration = aceleration
        self.direction = direction
        self.limitRestrictions = limitRestrictions
        self.hitRestrictions = hitRestrictions
        self.margin = margin
        self.hitbox  = create_hitbox(dimentions, margin)
    
    def update_hitbox(self, dimentions:pygame.Rect, margin:list=None):
        if isinstance(margin, list):
            self.margin = margin
        self.hitbox = create_hitbox(dimentions, self.margin)

    def update_position(self, FPS:int) -> None:
        time = 1 / FPS
        finalVelocity = [self.velocity[0] + self.aceleration[0] * time, self.velocity[1] + self.aceleration[1] * time]
        self.position = [self.position[0] + (self.velocity[0] + finalVelocity[0]) / 2 * time,
                         self.position[1] + (self.velocity[1] + finalVelocity[1]) / 2 * time]
        self.velocity = finalVelocity 

class EventListener:
    pass