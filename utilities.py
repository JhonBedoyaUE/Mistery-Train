import pygame

class Location:
    LEFTTOP = 0
    CENTERTOP = 1
    RIGHTTOP = 2
    CENTERRIGHT = 3
    RIGHTBOTTOM = 4
    CENTERBOTTOM = 5
    LEFTBOTTOM = 6
    CENTERLEFT = 7
    CENTER = 8
    CUSTOM = 9

class AnimationDirection:
    NORMAL = 0
    REVERSE = 1
    ALTERNATE = 2
    ALTERNATEREVERSE = 3

class AnimationIterationBehavior:
    INFINITE = -1
    CUSTOM = 0
    ONCE = 1

class Texture:
    def __init__(self, sprite, lenght=-1):
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
    def IDENTITY(sprite:Texture, variationIndex:int, name:str, scalar:float=1):
        scalledSprite = [pygame.transform.scale_by(frame, scalar) for frame in sprite.sprite]
        return {'sprite': Texture(scalledSprite), 'name': name}

    def XFLIP(sprite:Texture, variationIndex:int, name:str, scalar:float=1):
        if variationIndex == 0:
            scalledSprite = [pygame.transform.scale_by(frame, scalar) for frame in sprite.sprite]
            return {'sprite': Texture(scalledSprite), 'name': name}
        else:
            flippedSprite = [pygame.transform.scale_by(pygame.transform.flip(frame, flip_x=True, flip_y=False), scalar) for frame in sprite.sprite]
            return {'sprite': Texture(flippedSprite), 'name': 'xflip_'+name}

        
def create_textures(fileNameList, spriteLeghtList, path='textures/', variations=1, transformFunction=Transformation.IDENTITY, scalar=1):
    textures = {'default': Texture(pygame.Surface((500, 500)), 1)}
    for index in range(len(fileNameList)):
        sprite = pygame.image.load(path + fileNameList[index]).convert()
        for variationIndex in range(variations):
            texture = Texture(sprite, spriteLeghtList[index])
            textureVariation = transformFunction(texture, variationIndex, fileNameList[index].split('.')[0], scalar)
            textures[textureVariation['name']] = textureVariation['sprite']
    return textures

class Animation:
    def __init__(self, textures=create_textures([], []), actualTexture='default', frame=0, frameLimit=0, FPS=10, animationTime=0, animationIterationBehavior=AnimationIterationBehavior.INFINITE, animationIterationLimit=1, animationIterationCount=0) -> None:
        self.textures = textures
        self.actualTexture = actualTexture
        self.frame = frame
        self.FPS = FPS
        self.animationTime = animationTime
        self.frameLimit = frameLimit
        self.animationIterationBehavior = animationIterationBehavior
        self.animationIterationCount = animationIterationCount
        self.animationIterationLimit = animationIterationLimit