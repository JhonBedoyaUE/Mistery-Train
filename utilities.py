import pygame, types

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
            spriteWidth = sprite.get_rect().width / lenght
            spriteHeight = sprite.get_rect().height
            for i in range(lenght):
                self.sprite.append(sprite.subsurface((spriteWidth * i, 0, spriteWidth, spriteHeight)))
        else:
            self.lenght = len(sprite)
            self.sprite = sprite

class Transformation:
    def IDENTITY(sprite:Texture, variationIndex:int, name:str, scalar:float=1) -> dict:
        scalledSprite = [pygame.transform.scale_by(frame, scalar) for frame in sprite.sprite]
        return {'sprite': Texture(scalledSprite), 'name': name}

    def XFLIP(sprite:Texture, variationIndex:int, name:str, scalar:float=1) -> dict:
        if variationIndex == 0:
            scalledSprite = [pygame.transform.scale_by(frame, scalar) for frame in sprite.sprite]
            return {'sprite': Texture(scalledSprite), 'name': name}
        else:
            flippedSprite = [pygame.transform.scale_by(pygame.transform.flip(frame, flip_x=True, flip_y=False), scalar) for frame in sprite.sprite]
            return {'sprite': Texture(flippedSprite), 'name': 'xflip_'+name}

        
def create_textures(fileNameList:list, spriteLeghtList:list, path:str='textures/', variations:int=1, transformFunction:types.FunctionType=Transformation.IDENTITY, scalar:float=1) -> dict:
    textures = {'default': Texture(pygame.Surface((500, 500)), 1)}
    for index in range(len(fileNameList)):
        sprite = pygame.image.load(path + fileNameList[index]).convert()
        for variationIndex in range(variations):
            texture = Texture(sprite, spriteLeghtList[index])
            textureVariation = transformFunction(texture, variationIndex, fileNameList[index].split('.')[0], scalar)
            textures[textureVariation['name']] = textureVariation['sprite']
    return textures

def create_hitbox(dimentions:pygame.Rect, margin) -> pygame.Rect:
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
            right = margin[3]
            bottom = margin[4]
        
        return pygame.Rect(dimentions.left - left, dimentions.top - top, dimentions.size[0] + left + right, dimentions.size[1] + top + bottom)

class Animation:
    def __init__(self, textures:dict=create_textures([], []), actualTexture:str='default', frame:int=0, startFrame:int = 0, frameLimit:int=0, FPS:int=10, animationTime:int=0, animationIterationBehavior:int=AnimationIterationBehavior.INFINITE, animationIterationLimit:int=1, animationIterationCount:int=0) -> None:
        self.textures = textures
        self.actualTexture = actualTexture
        self.frame = frame
        self.FPS = FPS
        self.animationTime = animationTime
        self.frameLimit = frameLimit
        self.animationIterationBehavior = animationIterationBehavior
        self.animationIterationCount = animationIterationCount
        self.animationIterationLimit = animationIterationLimit
        self.startFrame = startFrame

class Physics:
    def __init__(self, position:list, velocity:list=[0, 0], aceleration:list=[0, 0], direction:int=Direction.LEFT, limitRestrictions:bool=False, dimentions:pygame.Rect=pygame.Rect(0,0,0,0), margin:list=[0]) -> None:
        self.position = position 
        self.velocity = velocity
        self.aceleration = aceleration
        self.direction = direction
        self.limitRestrictions = limitRestrictions
        self.margin = margin
        self.hitbox  = create_hitbox(dimentions, margin)
    
    def update_hitbox(self, dimentions:pygame.Rect, margin:list=None):
        if isinstance(margin, list):
            self.margin = margin
        self.hitbox = create_hitbox(dimentions, self.margin)

class EventListener:
    LISTEN_KEY = 0
    LISTEN_COLLISION = 1