import pygame, types, math



class FitThePositionBehaviour:
    FOLLOW_MAIN_CHARACTER = 0
    TO_LOCATION = 1

class ClickableSpace:
    SPRITE = 0
    HITBOX = 1

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
    def __init__(self, sprite:list[pygame.Surface], lenght:int=-1, size:tuple[int, int] = [0, 0]) -> None:
        if lenght >= 0:
            self.lenght = lenght
            self.sprite = []
            self.size = [math.floor(sprite.get_rect().width / lenght), sprite.get_rect().height]
            for i in range(lenght):
                self.sprite.append(sprite.subsurface((self.size[0] * i, 0, self.size[0], self.size[1])))
        else:
            self.lenght = len(sprite)
            self.sprite = sprite
            if len(self.sprite) >= 1:
                self.size = self.sprite[0].get_rect().size
            else:
                self.size = size

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

def invert_colors(surface:pygame.Surface, invert:bool) -> pygame.Rect:
    if invert:
        invertedSurface = surface.copy()
        for x in range(surface.get_width()):
            for y in range(surface.get_height()):
                color = surface.get_at((x,y))
                invertedColor = 255 - color[0], 255 - color[1], 255 - color[2], color[3]
                invertedSurface.set_at((x,y), invertedColor)
        return invertedSurface
    else:
        return surface


class Transformation:
    def BASIC(sprite:Texture, variationIndex:int, name:str, scalar:float=1, extractContent:bool=False, scalarBase:tuple=(0,0)) -> dict:
        scalledSprite = [] 
        for frame in sprite.sprite:
            textureScalar = scalar
            if scalarBase != (0, 0):
                textureAspectRatio = frame.get_rect().height / frame.get_rect().width
                displayAspectRatio = scalarBase[1] / scalarBase[0]
                if textureAspectRatio <= displayAspectRatio:
                    textureScalar = scalarBase[1] * scalar / frame.get_rect().height
                else:
                    textureScalar = scalarBase[0] * scalar / frame.get_rect().width
            
            scalledSprite.append(extract_content(pygame.transform.scale_by(frame, textureScalar), extractContent))
        return {'sprite': Texture(scalledSprite), 'name': name}

    def XFLIP(sprite:Texture, variationIndex:int, name:str, scalar:float=1, extractContent:bool=False, scalarBase:tuple=(0,0)) -> dict:
        flippedSprite = []
        for frame in sprite.sprite:
            textureScalar = scalar
            if scalarBase != (0, 0):
                textureAspectRatio = frame.get_rect().height / frame.get_rect().width
                displayAspectRatio = scalarBase[1] / scalarBase[0]
                if textureAspectRatio <= displayAspectRatio:
                    textureScalar = scalarBase[1] * scalar / frame.get_rect().height
                else:
                    textureScalar = scalarBase[0] * scalar / frame.get_rect().width
            flippedSprite.append(extract_content(pygame.transform.scale_by(pygame.transform.flip(frame, flip_x=(variationIndex != 0), flip_y=False), textureScalar), extractContent))
        return {'sprite': Texture(flippedSprite), 'name': ('xflip_'*(variationIndex != 0))+name}
    
    
    def NEGATIVE_COLOR(sprite:Texture, variationIndex:int, name:str, scalar:float=1, extractContent:bool=False, scalarBase:tuple=(0,0)) -> dict:
        negativeSprite = []
        for frame in sprite.sprite:
            textureScalar = scalar
            if scalarBase != (0, 0):
                textureAspectRatio = frame.get_rect().height / frame.get_rect().width
                displayAspectRatio = scalarBase[1] / scalarBase[0]
                if textureAspectRatio <= displayAspectRatio:
                    textureScalar = scalarBase[1] * scalar / frame.get_rect().height
                else:
                    textureScalar = scalarBase[0] * scalar / frame.get_rect().width
            negativeSprite.append(invert_colors(extract_content(pygame.transform.scale_by(frame, textureScalar), extractContent), (variationIndex != 0)))
        return {'sprite': Texture(negativeSprite), 'name': ('negative_'*(variationIndex != 0))+name}
    
    def RECT_ROTATION(sprite:Texture, variationIndex:int, name:str, scalar:float=1, extractContent:bool=False, scalarBase:tuple=(0,0)) -> dict:
        flippedSprite = []
        for frame in sprite.sprite:
            textureScalar = scalar
            if scalarBase != (0, 0):
                textureAspectRatio = frame.get_rect().height / frame.get_rect().width
                displayAspectRatio = scalarBase[1] / scalarBase[0]
                if textureAspectRatio <= displayAspectRatio:
                    textureScalar = scalarBase[1] * scalar / frame.get_rect().height
                else:
                    textureScalar = scalarBase[0] * scalar / frame.get_rect().width
            flippedSprite.append(extract_content(pygame.transform.scale_by(pygame.transform.rotate(frame, 90*variationIndex), textureScalar), extractContent))
        return {'sprite': Texture(flippedSprite), 'name': (f'{90*variationIndex}rotated_'*(variationIndex != 0))+name}


        
def create_textures(fileNameList:list, spriteLeghtList:list, path:str='textures/', variations:int|tuple[int]=1, transformFunctions:types.FunctionType|tuple[types.FunctionType]=Transformation.BASIC, scalar:float=1, extractContent:bool=False, scalarBase:tuple=(0,0)) -> dict:
    textures = {'default': Texture(pygame.Surface((500, 500), pygame.SRCALPHA), 1)}
    for index in range(len(fileNameList)):
        sprite = pygame.image.load(path + fileNameList[index]).convert_alpha()
        textures[fileNameList[index].split('.')[0]] = Transformation.BASIC(Texture(sprite, spriteLeghtList[index]), 0, '', scalar, extractContent, scalarBase=scalarBase)['sprite']

    if (not isinstance(variations, list)) and (not isinstance(variations, tuple)):
        variations = [variations]
    
    if (not isinstance(transformFunctions, list)) and (not isinstance(transformFunctions, tuple)):
        transformFunctions = [transformFunctions]
    
    

    for transformFunctionIndex in range(len(transformFunctions)):
        procesingTextures = textures.copy()
        for TextureName, loadedTexture in procesingTextures.items():
            for variationIndex in range(variations[transformFunctionIndex]):
                textureVariation = transformFunctions[transformFunctionIndex](loadedTexture, variationIndex, TextureName)
                textures[textureVariation['name']] = textureVariation['sprite']

    return textures

def create_empty_texture(width:int, height:int, name:str='default', scalar:float=1, scalarBase:tuple=(0,0)):
    emptySprite = pygame.Surface((width, height), pygame.SRCALPHA)
    emptySprite.set_alpha(0)
    textureVariation = Transformation.BASIC(Texture(emptySprite, 1), None, name, scalar=scalar, scalarBase=scalarBase)
    return {name: textureVariation['sprite']}

def create_text_texture(text:str, textColor:tuple[int, int, int, int], font:pygame.font.Font, name:str='default', scalar:float=1, scalarBase:tuple=(0,0)):
    textLines = text.split('\n')
    renderedTextLines = [font.render(line, True, textColor) for line in textLines]

    joinedLines = renderedTextLines[0].copy()

    for line in renderedTextLines[1:]:
        width = joinedLines.get_width()

        if line.get_width() > width:
            width = line.get_width()

        height = joinedLines.get_height() + line.get_height()
        joinedToActualLine = pygame.Surface((width, height), pygame.SRCALPHA)
        joinedToActualLine.blit(joinedLines, (0,0))
        joinedToActualLine.blit(line, (0, height - line.get_height()))
        joinedLines = joinedToActualLine
    
    textureVariation = Transformation.BASIC(Texture(joinedLines, 1), None, name, scalar=scalar, scalarBase=scalarBase)
    return {name: textureVariation['sprite']}
    




def create_hitbox(dimentions:pygame.Rect, margin:list, hitboxSize:list[int], hitboxLocation:int, previousPosition:list[int]=None, actualPosition:list[int]=None, actualHitbox:pygame.Rect=None) -> pygame.Rect:
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

        if hitboxSize == [0, 0]:
            newLeft, newTop, newWidth, newHeigth = dimentions.left - left, dimentions.top - top, dimentions.size[0] + left + right, dimentions.size[1] + top + bottom
        else:
            if hitboxLocation == Location.LEFT_TOP:
                newLeft, newTop, newWidth, newHeigth = left+dimentions.left, right+dimentions.top, hitboxSize[0], hitboxSize[1]
            elif hitboxLocation == Location.CENTER_TOP:
                newLeft, newTop, newWidth, newHeigth = left+dimentions.left + dimentions.width / 2 - hitboxSize[0] / 2, right+dimentions.top, hitboxSize[0], hitboxSize[1]
            elif hitboxLocation == Location.RIGHT_TOP:
                newLeft, newTop, newWidth, newHeigth = left+dimentions.left + dimentions.width - hitboxSize[0], right+dimentions.top, hitboxSize[0], hitboxSize[1]
            elif hitboxLocation == Location.CENTER_RIGHT:
                newLeft, newTop, newWidth, newHeigth = left+dimentions.left + dimentions.width - hitboxSize[0], right+dimentions.top + dimentions.height / 2 - hitboxSize[1] / 2, hitboxSize[0], hitboxSize[1]
            elif hitboxLocation == Location.RIGHT_BOTTOM:
                newLeft, newTop, newWidth, newHeigth = left+dimentions.left + dimentions.width - hitboxSize[0], right+dimentions.top + dimentions.height - hitboxSize[1], hitboxSize[0], hitboxSize[1]
            elif hitboxLocation == Location.CENTER_BOTTOM:

                newLeft, newTop, newWidth, newHeigth = left+dimentions.left + dimentions.width / 2 - hitboxSize[0] / 2, right+dimentions.top + dimentions.height - hitboxSize[1], hitboxSize[0], hitboxSize[1]
                
            elif hitboxLocation == Location.LEFT_BOTTOM:
                newLeft, newTop, newWidth, newHeigth = left+dimentions.left, right+dimentions.top + dimentions.height - hitboxSize[1], hitboxSize[0], hitboxSize[1]
            elif hitboxLocation == Location.CENTER_LEFT:
                newLeft, newTop, newWidth, newHeigth = left+dimentions.left, right+dimentions.top + dimentions.height / 2 - hitboxSize[1] / 2, hitboxSize[0], hitboxSize[1]
            else:
                newLeft, newTop, newWidth, newHeigth = left+dimentions.left + dimentions.width / 2 - hitboxSize[0] / 2, right+dimentions.top + dimentions.height / 2 - hitboxSize[1] / 2, hitboxSize[0], hitboxSize[1]
        
        #print(dimentions.left, dimentions.top,newLeft, newTop, newWidth, newHeigth)
        if actualHitbox is not None:
            if previousPosition[0] == actualPosition[0] and actualHitbox.width == newWidth:
                newLeft = actualHitbox.left
            if previousPosition[1] == actualPosition[1] and actualHitbox.height == newHeigth:
                newTop = actualHitbox.top

        return pygame.Rect(newLeft, newTop, newWidth, newHeigth)

class Animation:
    def __init__(self, textures:dict[any, Texture]=create_textures([], []), actualTexture:str='default', zIndex:int=0, frame:int=0, startFrame:int = 0, frameLimit:int=0, FPS:int=10, animationTime:int=0, animationIterationBehavior:int=AnimationIterationBehavior.INFINITE, animationIterationLimit:int=1, animationIterationCount:int=0, isAnimated:bool=True) -> None:
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
        self.isAnimated = isAnimated
    
    def update_frame(self, FPS:int):
        if self.isAnimated:
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
        
class IconAnimation(Animation):
    def __init__(self, textures: dict[any, Texture] = create_textures([], []), actualTexture: str = 'default', zIndex: int = 0, frame: int = 0, startFrame: int = 0, frameLimit: int = 0, FPS: int = 10, animationTime: int = 0, animationIterationBehavior: int = AnimationIterationBehavior.INFINITE, animationIterationLimit: int = 1, animationIterationCount: int = 0, isAnimated: bool = True, background:Animation=None, backgroundColor:tuple[int, int, int, int]=(255,0,255, 120)) -> None:

        super().__init__(textures, actualTexture, zIndex, frame, startFrame, frameLimit, FPS, animationTime, animationIterationBehavior, animationIterationLimit, animationIterationCount, isAnimated)
        
        self.background = background
        self.backgroundColor = backgroundColor
    
    def update_frame(self, FPS:int):
        if self.isAnimated:
            time = 1 / FPS
            self.animationTime += time
            self.frame = math.floor(self.animationTime * self.FPS) + self.startFrame
            self.limit_frame() 
            if self.background is not None:
                self.background.update_frame(FPS)
    
    def get_texture(self) -> pygame.Surface:
        texture = pygame.Surface(self.textures[self.actualTexture].sprite[self.frame].get_rect().size, pygame.SRCALPHA)
        texture.fill(self.backgroundColor)
        
        if self.background is not None:
            texture.blit(self.background.get_texture(), (0,0))

        texture.blit(self.textures[self.actualTexture].sprite[self.frame], (0,0))
            
        return texture

class TextIconAnimation(IconAnimation):
    def __init__(self, text:str, font:pygame.font.Font, textColor:tuple[int, int, int, int] =  (0, 0, 0, 255), actualTexture: str = 'default', zIndex: int = 0, frame: int = 0, startFrame: int = 0, frameLimit: int = 0, FPS: int = 10, animationTime: int = 0, animationIterationBehavior: int = AnimationIterationBehavior.INFINITE, animationIterationLimit: int = 1, animationIterationCount: int = 0, isAnimated: bool = True, background: Animation = None, backgroundColor: tuple[int, int, int, int] = (255, 0, 255, 120)) -> None:
        super().__init__(create_text_texture(text, textColor, font), actualTexture, zIndex, frame, startFrame, frameLimit, FPS, animationTime, animationIterationBehavior, animationIterationLimit, animationIterationCount, isAnimated, background, backgroundColor)
    
        self.text = text
        self.previousText = text
        self.font = font
        self.previousFont = font
        self.textColor = textColor
        self.previousTextColor = textColor

    def update_frame(self, FPS:int):
        if self.isAnimated:
            time = 1 / FPS
            self.animationTime += time
            self.frame = math.floor(self.animationTime * self.FPS) + self.startFrame 
            self.limit_frame()

            if self.text != self.previousText or self.font != self.previousFont or self.textColor != self.previousTextColor:
                self.textures = create_text_texture(self.text, self.textColor, self.font)
                self.previousText = self.text
                self.previousFont = self.font
                self.previousTextColor = self.textColor

            if self.background is not None:
                self.background.update_frame(FPS)



class Physics:
    def __init__(self, position:list, velocity:list=[0, 0], aceleration:list=[0, 0], direction:int=Direction.LEFT, limitRestrictions:bool=False, isCollidable:bool=False, margin:list=[0], hitboxSize:list[int]=[0,0], hitboxLocation:int=Location.CENTER_BOTTOM, isUpdatable:bool=True) -> None:
        self.position = position 
        self.previousPosition = [None, None]
        self.velocity = velocity
        self.aceleration = aceleration
        self.direction = direction
        self.limitRestrictions = limitRestrictions
        self.isCollidable = isCollidable
        self.margin = margin
        self.hitbox = create_hitbox(pygame.Rect([0,0], [1000, 1000]), margin, hitboxSize, hitboxLocation)
        self.previousHitbox = self.hitbox.copy()
        self.hitboxColor = 0, 0, 255
        self.positionColor = 0, 255, 0
        self.isPositionChanged = False
        self.isUpdatable = isUpdatable
        self.hitboxSize = hitboxSize
        self. hitboxLocation =  hitboxLocation

    
    def update_hitbox(self, dimentions:pygame.Rect, margin:list[int]=None, hitboxSize:list[int]=None,  hitboxLocation:int=None):
        self.previousHitbox = self.hitbox.copy()
        if isinstance(margin, list):
            self.margin = margin
        if isinstance(hitboxSize, list):
            self.hitboxSize = hitboxSize
        if isinstance(hitboxLocation, int):
            self.hitboxLocation = hitboxLocation
        
        
        self.hitbox = create_hitbox(dimentions, self.margin, self.hitboxSize, self.hitboxLocation, previousPosition=self.previousPosition, actualPosition=self.position, actualHitbox=self.hitbox)
        
    def update_position(self, FPS:int) -> None:
        if self.isUpdatable:
            self.previousPosition = self.position.copy()
            time = 1 / FPS
            finalVelocity = [self.velocity[0] + self.aceleration[0] * time, self.velocity[1] + self.aceleration[1] * time]
            self.position = [self.position[0] + (self.velocity[0] + finalVelocity[0]) / 2 * time,
                            self.position[1] + (self.velocity[1] + finalVelocity[1]) / 2 * time]
            self.velocity = finalVelocity 

            if self.previousPosition == self.position:
                self.isPositionChanged = False
            else:
                self.isPositionChanged = True
    
    def move_position(self, entity, offsetPosition:list[int]):
        if self.previousPosition != [None, None]:
            self.previousPosition[0] += offsetPosition[0]
            self.previousPosition[1] += offsetPosition[1]
        self.hitbox = create_hitbox(pygame.Rect(entity.get_texture_position(), entity.animation.get_texture().get_size()), self.margin, self.hitboxSize, self.hitboxLocation, previousPosition=self.previousPosition, actualPosition=self.position, actualHitbox=self.hitbox)
        pygame.Rect(self.hitbox.left + 0.1, self.hitbox.top + 0.1, self.hitbox.width, self.hitbox.height)
        self.previousHitbox = self.hitbox.copy()
        self.position[0] += offsetPosition[0]
        self.position[1] += offsetPosition[1]
