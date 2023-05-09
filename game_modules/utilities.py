import pygame, types
from math import floor
from enum import Enum

# En la definicion de las funciones se utilizo type hint que permite informar cual es el tipo de los parametros y del retorno de la funcion
# Por lo que recomiendo usar una version de Python superior a 3.5
# Para más onformación sobre type hint visita https://docs.python.org/3/library/typing.html 
# Las siguientes clases son Enumeraciones (Enum) que permiten darle orden y entendimiento a las diversas comparaciones y asignaciones que se hacen en el codigo
# Para más información sobre los Enums visita https://docs.python.org/es/3/library/enum.html

class FitThePositionBehaviour(Enum):
    """Usado en la clase LevelWorksSpace para definir el comportamiento de la vista del nivel."""
    FOLLOW_MAIN_CHARACTER = 0
    TO_LOCATION = 1

class ClickableSpace(Enum):
    """Usado en la clase Entity para definir el area en que se le puede dar click a una entidad."""
    SPRITE = 0
    HITBOX = 1

class Direction(Enum):
    """Usado para tener en cuenta la direccion que toma el personaje al caminar."""
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

class Location(Enum):
    """Usado para darle una posicion relativa a distintos objetos en relacion a otros objetos."""
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

class AnimationDirection(Enum):
    """Usado en la clase Animation para definir el comportamiento de repeticion de una animacion (como en CSS y HTML)."""
    NORMAL = 0
    REVERSE = 1
    ALTERNATE = 2
    ALTERNATE_REVERSE = 3

class AnimationIterationBehavior(Enum):
    """Usado para la clase Animation para definir la veces en que se repite una animacion."""
    INFINITE = -1
    CUSTOM = 0
    ONCE = 1

# La siguiente parte corresponde a la carga, procesado y almacenamiento de las imagenes utilizadas en las entidades del juego, permitiendo trabajar con los fotogramas de las animaciones

class Texture:
    """Sus instancias procesan y almacenan las imagenes en forma de fotogramas agrupadas de los sprites como textura de las entidades."""
    def __init__(self, sprite:list[pygame.Surface]|pygame.Surface, lenght:int=-1, size:tuple[int, int] = [0, 0]) -> None:
        """Si no se especifica el lenght (cantidad o longitud), se debe dar una lista de imagenes en sprite guardarlas como fotogramas.Si se especifica el lenght se debe dar una imagen (pygame.Surface) para transformala y dividirla en partes iguales horizontalmente.


        Args:
            sprite (list[pygame.Surface]): lista de imagenes o imagen a dividir, que se almacenara.

            lenght (int, optional): (Si se especifica) Es la cantidad de fotogramas que contiene horizontalmente. Defaults to -1.

            size (tuple[int, int], optional): No especificar, su uso es de depuracion. Defaults to [0, 0].

        """
        if lenght >= 0:
            self.lenght = lenght
            self.sprite = []
            self.size = [floor(sprite.get_rect().width / lenght), sprite.get_rect().height]
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
    """Retorna un rectangulo que abarca la region que no es transparente en la imagen.


    Args:
        surface (pygame.Surface): La imagen donde se buscara el la region que no es transparente.


    Returns:
        pygame.Rect: El rectangulo que abarca la region que no es transparente.

    """
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

def extract_content(surface:pygame.Surface, extract:bool) -> pygame.Rect:
    """Si extract es True recorta y retorna la region de la imagen que no es transparente.


    Args:
        surface (pygame.Surface): La imagen a extraer el contenido.

        extract (bool): si es True extrae el contenido, si es False retorna la imagen sin modificarla.


    Returns:
        pygame.Rect: La imagen con el contenido extraido o la misma que se paso como surface.

    """
    if extract:
        return surface.subsurface(find_content(surface))
    else:
        return surface

def invert_colors(surface:pygame.Surface, invert:bool) -> pygame.Rect:
    """Si invert es True invierte los colores de la imagen.


    Args:
        surface (pygame.Surface): La imagen a invertir los colores.

        invert (bool): si es True invierte los colores, si es False retorna la imagen sin modificarla.


    Returns:
        pygame.Rect: La imagen con los colores invertidos o la misma que se paso como surface.

    """
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
    """Contiene las funciones necesarias para transformar las imagenes, donde cada una puede reescalar y ectraer el contenido de imagen y define el nombre de la resultante."""
    
    @staticmethod
    def BASIC(sprite:Texture, variationIndex:int, name:str, scalar:float=1, extractContent:bool=False, scalarBase:tuple=(0,0)) -> dict[str, Texture|str]:
        """Retorna las imagenes en la textura con las transformaciones basicas como reescalar o extraer el contenido. 

        Args:
            sprite (Texture): La textura con las imagenes a transformar.

            variationIndex (int): Es ignorado, esta por compatibilidad en la creacion de texturas.

            name (str): El nombre de la textura, no es modificado, 
            scalar (float, optional): El factor a reescalar las imagenes. Defaults to 1.

            extractContent (bool, optional): Define si extraer el contenido no transparente de las imagenes. Defaults to False.

            scalarBase (tuple, optional): Si se define reescala las imagenes teniendo en cuenta este tamaño como base. Defaults to (0,0).


        Returns:
            dict: El diccionario con el sprite con trasformaciones basicas y el nombre de la textura sin modificar.

        """

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

    @staticmethod
    def XFLIP(sprite:Texture, variationIndex:int, name:str, scalar:float=1, extractContent:bool=False, scalarBase:tuple=(0,0)) -> dict[str, Texture|str]:
        """Ademas de las transformaciones basicas, puede retornar las imagenes de la textura invertidas horizontalmente y modificar su nombre con el prefijo 'xflip_'. 

        Args:
            sprite (Texture): La textura con las imagenes a transformar.

            variationIndex (int): Si es distinto a cero invierte las imagenes horizontalmente.

            name (str): El nombre de la textura, si se invierte se retorna con el prefijo  'xflip_', 
            scalar (float, optional): El factor a reescalar las imagenes. Defaults to 1.

            extractContent (bool, optional): Define si extraer el contenido no transparente de las imagenes. Defaults to False.

            scalarBase (tuple, optional): Si se define reescala las imagenes teniendo en cuenta este tamaño como base. Defaults to (0,0).


        Returns:
            dict: El diccionario con el sprite transformado y el nombre de la textura, que si es invertida tendra el subfijo 'xflip_'.

        """

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
    
    @staticmethod
    def NEGATIVE_COLOR(sprite:Texture, variationIndex:int, name:str, scalar:float=1, extractContent:bool=False, scalarBase:tuple=(0,0)) -> dict[str, Texture|str]:
        """Ademas de las transformaciones basicas, puede retornar las imagenes de la textura con los colores invertidos y modificar su nombre con el prefijo 'negative_'. 

        Args:
            sprite (Texture): La textura con las imagenes a transformar.

            variationIndex (int): Si es distinto a cero invierte los colores de las imagenes.

            name (str): El nombre de la textura, si se invierte se retorna con el prefijo  'negative_', 
            scalar (float, optional): El factor a reescalar las imagenes. Defaults to 1.

            extractContent (bool, optional): Define si extraer el contenido no transparente de las imagenes. Defaults to False.

            scalarBase (tuple, optional): Si se define reescala las imagenes teniendo en cuenta este tamaño como base. Defaults to (0,0).


        Returns:
            dict: El diccionario con el sprite transformado y el nombre de la textura, que si es invertida tendra el subfijo 'negative_'.

        """

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
    
    @staticmethod
    def RECT_ROTATION(sprite:Texture, variationIndex:int, name:str, scalar:float=1, extractContent:bool=False, scalarBase:tuple=(0,0)) -> dict[str, Texture|str]:
        """Ademas de las transformaciones basicas, puede retornar las imagenes de la textura rotadas con angulos rectos y modificar su nombre con el prefijo f'{90*variationIndex}rotated_'. 

        Args:
            sprite (Texture): La textura con las imagenes a transformar.

            variationIndex (int): Si es distinto a cero rota las imagenes, el agulo de rotacion es la multiplicacion de variationIndex por 90.

            name (str): El nombre de la textura, si se invierte se retorna con el prefijo  f'{90*variationIndex}rotated_', 
            scalar (float, optional): El factor a reescalar las imagenes. Defaults to 1.

            extractContent (bool, optional): Define si extraer el contenido no transparente de las imagenes. Defaults to False.

            scalarBase (tuple, optional): Si se define reescala las imagenes teniendo en cuenta este tamaño como base. Defaults to (0,0).


        Returns:
            dict: El diccionario con el sprite transformado y el nombre de la textura, que si es rotada tendra el subfijo f'{90*variationIndex}rotated_'.

        """

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


        
def create_textures(fileNameList:list[str], spriteLeghtList:list[int], path:str='textures/', variations:int|tuple[int]=1, transformFunctions:types.FunctionType|tuple[types.FunctionType]=Transformation.BASIC, scalar:float=1, extractContent:bool=False, scalarBase:tuple=(0,0)) -> dict[str, Texture]:
    """Carga las imagenes y crea las texturas correspondientes a cada imagen transformadas segun las funciones de transformacion, y retorna las texturas en un diccionario donde cada llave es el nombre que le corresponde, el cual es la primera parte del nombre del archivo antes del punto junto con el prefijo correspondiente si son trasformadas.


    Args:
        fileNameList (list[str]): Lista de los nombres de las imagenes a cargar.

        spriteLeghtList (list[int]): Lista de la cantidad de de Fotogramas que contiene cada imagen.

        path (str, optional): Es la ruta de la carpeta donde se encuentran las imagenes. Defaults to 'textures/'.

        variations (int, optional): Lista de la cantidad de variaciones de cada imagen para cada funcion de tranformacion. Defaults to 1.

        transformFunctions (types.FunctionType, optional): Lista de las funciones de tranformacion a aplicar a cada una de las imagenes. Defaults to Transformation.BASIC.

        scalar (float, optional): El factor a reescalar las imagenes. Defaults to 1.

        extractContent (bool, optional): Define si extraer el contenido no transparente de las imagenes. Defaults to False.

        scalarBase (tuple, optional): Si se define reescala las imagenes teniendo en cuenta este tamaño como base. Defaults to (0,0).


    Returns:
        dict[str, Texture]: El diccionario con todas las texturas creadas y transformadas a base de las imagenes cargadas, donde su llave es el nombre correspondiente (subfijo+nombre_antes_del_punto).

    """

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

def create_empty_texture(width:int, height:int, name:str='default', scalar:float=1, scalarBase:tuple[int, int]=(0,0)) -> dict[str, Texture]:
    """Retorna un diccionario con una textura con una sola imagen transparente con el tamaño indicado.


    Args:
        width (int): Ancho de la imagen de la textura.

        height (int): Alto de la imagen de la textura.

        name (str, optional): Nombre de la textura. Defaults to 'default'.

        scalar (float, optional): El factor a reescalar la imagen. Defaults to 1.

        scalarBase (tuple[int, int], optional): Si se define reescala la imagen teniendo en cuenta este tamaño como base. Defaults to (0,0).


    Returns:
        dict[str, Texture]: El diccionario la textura de imagen transparente creada y transformada, donde su llave es el valor de name.

    """

    emptySprite = pygame.Surface((width, height), pygame.SRCALPHA)
    emptySprite.set_alpha(0)
    textureVariation = Transformation.BASIC(Texture(emptySprite, 1), None, name, scalar=scalar, scalarBase=scalarBase)
    return {name: textureVariation['sprite']}

def create_text_texture(text:str, textColor:tuple[int, int, int, int], font:pygame.font.Font, name:str='default', padding:list[int] = [0], scalar:float=1, scalarBase:tuple=(0,0)) -> dict[str, Texture]:
    """Retorna un diccionario con una textura con la imagen del texto renderizado y con saltos de linea. La imagen reescalada y con un espacio entre los bordes especificado por padding. 

    Args:
        text (str): El texto a renderizar.

        textColor (tuple[int, int, int, int]): El color del texto.

        font (pygame.font.Font): La fuente con la cual se renderiza el texto
        name (str, optional): El nombre de la textura en el diccionario. Defaults to 'default'.

        padding (list[int], optional): El espacio entre el texto y los bordes. Un solo valor se aplica a los cuatro bordes. Con dos valores, el primero se aplica a la derecha e izquierda y el segundo arriba y abajo.Con cuatro valores se aplican en oreden a la izquierda, arriba, derecha y abajo. Defaults to [0].

        scalar (float, optional): El factor a reescalar la imagen. Defaults to 1.

        scalarBase (tuple, optional): Si se define reescala la imagen teniendo en cuenta este tamaño como base. Defaults to (0,0).


    Returns:
        dict[str, Texture]:  El diccionario la textura del texto renderizado y transformado, donde su llave es el valor de name.

    """

    if len(padding) == 1:
        left = padding[0]
        top = padding[0]
        right = padding[0]
        bottom = padding[0]
    elif len(padding) == 2:
        left = padding[0]
        top = padding[1]
        right = padding[0]
        bottom = padding[1]
    else:
        left = padding[0]
        top = padding[1]
        right = padding[2]
        bottom = padding[3]

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
    
    finalWidth = left + joinedLines.get_width() + right
    finalHeight = top + joinedLines.get_height() + bottom

    if finalWidth < 1:
        finalWidth = 1
    
    if finalHeight < 1:
        finalHeight = 1
    
    finalImage = pygame.Surface((finalWidth, finalHeight), pygame.SRCALPHA)
    finalImage.blit(joinedLines, (left, top))
    
    textureVariation = Transformation.BASIC(Texture(finalImage, 1), None, name, scalar=scalar, scalarBase=scalarBase)
    return {name: textureVariation['sprite']}
    


# La siguiente parte corresponde a las clases de las animaciones, fisicas y la funcion para crear hitboxes

def create_hitbox(dimentions:pygame.Rect, margin:list[int], hitboxSize:list[int], hitboxLocation:int) -> pygame.Rect:
        """Retorna un rectangulo correspondiente a la hitbox que se ajusta al rectangulo de dimentions, con una posicion modificada por margin y hitboxLocation. Donde solo se toman los valores del margen correspondientes al borde donde esta la posicion, si esta en el centro solo toma el la izquierda y arriba.   

        Args:
            dimentions (pygame.Rect): El rectango desde donde se posicionara la hitbox.

            margin (list[int]): Los valores que modifican la posicionn de la hitbox. Un solo valor se aplica a los cuatro lados. Con dos valores, el primero se aplica a la derecha e izquierda y el segundo arriba y abajo.Con cuatro valores se aplican en oreden a la izquierda, arriba, derecha y abajo.

            hitboxSize (list[int]): El tamaño (ancho, alto) de la hitbox.

            hitboxLocation (int): La posicion relativa de la hitbox entre dimentions, desde donde se empezara a posicionar. Defaults to None.


        Returns:
            pygame.Rect: Rectangulo correspondiente a la hitbox especificada. 
        """

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

        return pygame.Rect(newLeft, newTop, newWidth, newHeigth)

class Animation:
    """Sus instancias almacenan las texturas y administran las animaciones."""

    def __init__(self, textures:dict[any, Texture]=create_textures([], []), actualTexture:str='default', zIndex:int=0, frame:int=0, startFrame:int = 0, frameLimit:int=0, FPS:int=10, animationTime:int=0, animationIterationBehavior:int=AnimationIterationBehavior.INFINITE, animationIterationLimit:int=1, animationIterationCount:int=0, isAnimated:bool=True) -> None:
        """Guarda las texturas. Establece la animacion en la textura con el nombre del valor de actualTexture, iniciando desde el frame especificado en frame, donde al repetirse incicia en start frame, termina en frameLimit segun el comportamiento de repeticion especificado.


        Args:
            textures (dict[any, Texture], optional): Las texturas con los frames de cada animacion. Defaults to create_textures([], []).

            actualTexture (str, optional): El nombre de la textura empleada en la animacion a ejecutar. Defaults to 'default'.

            zIndex (int, optional): Usado para ordenar los fondos, de atras hacia adelante ascendentemente en LevelWorksSpace. Defaults to 0.

            frame (int, optional): El frame actual de la animacion en la textura actual. Defaults to 0.

            startFrame (int, optional): El frame inicial al repetirse. Defaults to 0.

            frameLimit (int, optional): El ultimo frame antes de repetirse. De ser negativo corresponde a los frames de atras hacia adelante. De ser 0 el limite sera el ultimo frame. Defaults to 0.

            FPS (int, optional): La velocidad con la que se ejecuta la animacion. Es independiente a los FPS globales con que se ejecuta el juego. Defaults to 10.

            animationTime (int, optional): El tiempo transcurrido por cada actualizacion del juego para determinar el fotograma actual o frame. Defaults to 0.

            animationIterationBehavior (int, optional): El comportamiento en que se debe repetir la animacion. Defaults to AnimationIterationBehavior.INFINITE.

            animationIterationLimit (int, optional): Las maximas veces en que se puede repetir una animacion si el animationIterationBehavior es AnimationIterationBehavior.CUSTOM. Defaults to 1.

            animationIterationCount (int, optional): Las veces en que se ha repetido la animacion. Defaults to 0.

            isAnimated (bool, optional): De ser False evita que se realicen las actualizaciones de animacion. Defaults to True.

        """

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
        """Si el atributo isAnimated es True, actualiza el fotograma de la animacion teniendo en cuenta el tiempo de actualizacion que se calcula por los FPS de actualizacion del juego.

        Args:
            FPS (int): FPS de actualizacion del juego.
        """

        if self.isAnimated:
            time = 1 / FPS
            self.animationTime += time
            self.frame = floor(self.animationTime * self.FPS) + self.startFrame
            self.limit_frame() 
    
    def get_frame_limit(self) -> int:
        """Retorna el limite del frame antes de repetirse. si el atributo frameLimit es negativo se retorna el fotograma contando de atras hacia adelante.

        Returns:
            int: El numero del limite del frame antes de repetirse.
        """
        if self.frameLimit == 0:
            return self.textures[self.actualTexture].lenght
        elif self.frameLimit >= 1:
            return self.frameLimit
        else:
            return self.textures[self.actualTexture].lenght + self.frameLimit
    
    def limit_frame(self) -> None:
        """Repite la animacion en caso de alcanzar el limite del frame. Si el atributo animationIterationBehavior es .INFINITE entonces la animacion se repite indefinidamente, si es .ONCE se repite una sola vez, y si es .CUSTOM se repite la cantidad de veces que indique el atributo animationIterationLimit.
        """
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
        """Cambia la textura actual en la que se esta ejecutando la animacion.

        Args:
            textureName (str): El nombre de la textura a cambiar. Debe estar como llave en el diccionario del atributo textures.
        """

        self.actualTexture = textureName

        if self.startFrame >= self.get_frame_limit():
            self.startFrame = self.get_frame_limit() - 1
            
        if self.frame >= self.get_frame_limit():
            self.frame = self.startFrame
            self.animationTime = 0


    def get_texture(self) -> pygame.Surface:
        """Retorna la imagen del fotograma actual de la animacion.

        Returns:
            pygame.Surface: Imagen del fotograma actual.
        """

        return self.textures[self.actualTexture].sprite[self.frame]
        
class IconAnimation(Animation):
    """Clase heredera de Animation, donde sus instancias tienen un color y otra animacion de fondo."""

    def __init__(self, textures: dict[any, Texture] = create_textures([], []), actualTexture: str = 'default', zIndex: int = 0, frame: int = 0, startFrame: int = 0, frameLimit: int = 0, FPS: int = 10, animationTime: int = 0, animationIterationBehavior: int = AnimationIterationBehavior.INFINITE, animationIterationLimit: int = 1, animationIterationCount: int = 0, isAnimated: bool = True, background:Animation=None, backgroundColor:tuple[int, int, int, int]=(255,0,255, 120)) -> None:
        """Crea una animacion con el color y animacion de fondo especificada. Para mas informacion sobre animaciones revisa el docstring del constructor (__init__) de Animation.

        Args:
            textures (dict[any, Texture], optional): Texturas de cada animacion. Defaults to create_textures([], []).

            actualTexture (str, optional): Textura actual de la animacion. Defaults to 'default'.

            zIndex (int, optional): indice usado para ordenar fondos. Defaults to 0.

            frame (int, optional): frame actual. Defaults to 0.

            startFrame (int, optional): frame inicial. Defaults to 0.

            frameLimit (int, optional): frame final. Defaults to 0.

            FPS (int, optional): FPS de la animacion. Defaults to 10.

            animationTime (int, optional): Tiempo para calcular el frame. Defaults to 0.

            animationIterationBehavior (int, optional): Como se debe repetir la animacion. Defaults to AnimationIterationBehavior.INFINITE.

            animationIterationLimit (int, optional): Veces maximas de repetir la animacion. Defaults to 1.

            animationIterationCount (int, optional): Veces de repetir la animacion. Defaults to 0.

            isAnimated (bool, optional): De ser False evita que se realicen las actualizaciones de animacion. Defaults to True.

            background (Animation, optional): Animacion que se muestra en el fondo. Defaults to None.

            backgroundColor (tuple[int, int, int, int], optional): color del fondo. Defaults to (255,0,255, 120).
        """

        super().__init__(textures, actualTexture, zIndex, frame, startFrame, frameLimit, FPS, animationTime, animationIterationBehavior, animationIterationLimit, animationIterationCount, isAnimated)
        
        self.background = background
        self.backgroundColor = backgroundColor
    
    def update_frame(self, FPS:int):
        """Si el atributo isAnimated es True, actualiza el fotograma de la animacion y de su fondo teniendo en cuenta el tiempo de actualizacion que se calcula por los FPS de actualizacion del juego.

        Args:
            FPS (int): FPS de actualizacion del juego.
        """

        if self.isAnimated:
            time = 1 / FPS
            self.animationTime += time
            self.frame = floor(self.animationTime * self.FPS) + self.startFrame
            self.limit_frame() 
            if self.background is not None:
                self.background.update_frame(FPS)
    
    def get_texture(self) -> pygame.Surface:
        """Retorna la imagen del fotograma actual de la animacion junto con su fondo y color de fondo.

        Returns:
            pygame.Surface: Imagen del fotograma actual.
        """

        texture = pygame.Surface(self.textures[self.actualTexture].sprite[self.frame].get_rect().size, pygame.SRCALPHA)
        texture.fill(self.backgroundColor)
        
        if self.background is not None:
            texture.blit(self.background.get_texture(), (0,0))

        texture.blit(self.textures[self.actualTexture].sprite[self.frame], (0,0))
            
        return texture

class TextIconAnimation(IconAnimation):
    """Clase heredera de IconAnimation, donde sus intancias por defecto solo tienen una textura que es del texto renderizado."""

    def __init__(self, text:str, font:pygame.font.Font, textColor:tuple[int, int, int, int] =  (0, 0, 0, 255), padding:list = [10], actualTexture: str = 'default', zIndex: int = 0, frame: int = 0, startFrame: int = 0, frameLimit: int = 0, FPS: int = 10, animationTime: int = 0, animationIterationBehavior: int = AnimationIterationBehavior.INFINITE, animationIterationLimit: int = 1, animationIterationCount: int = 0, isAnimated: bool = True, background: Animation = None, backgroundColor: tuple[int, int, int, int] = (255, 0, 255, 120)) -> None:
        """AI is creating summary for __init__

        Args:
            text (str): Texto a renderizar.

            font (pygame.font.Font): Fuente con la que renderiza el texto.

            textColor (tuple[int, int, int, int], optional): Color del texto. Defaults to (0, 0, 0, 255).

            padding (list, optional): Espacio entre el texto y los bordes. Defaults to [10].

            actualTexture (str, optional): Nombre de la textura actual, es decir del texto renderizado. Defaults to 'default'.

            zIndex (int, optional): indice usado para ordenar fondos. Defaults to 0.

            frame (int, optional): frame actual. Defaults to 0.

            startFrame (int, optional): frame inicial. Defaults to 0.

            frameLimit (int, optional): frame final. Defaults to 0.

            FPS (int, optional): FPS de la animacion. Defaults to 10.

            animationTime (int, optional): Tiempo para calcular el frame. Defaults to 0.

            animationIterationBehavior (int, optional): Como se debe repetir la animacion. Defaults to AnimationIterationBehavior.INFINITE.

            animationIterationLimit (int, optional): Veces maximas de repetir la animacion. Defaults to 1.

            animationIterationCount (int, optional): Veces de repetir la animacion. Defaults to 0.

            isAnimated (bool, optional): De ser False evita que se realicen las actualizaciones de animacion. Defaults to True.

            background (Animation, optional): Animacion que se muestra en el fondo. Defaults to None.

            backgroundColor (tuple[int, int, int, int], optional): color del fondo. Defaults to (255, 0, 255, 120).
        """
        super().__init__(create_text_texture(text, textColor, font, padding = padding, name=actualTexture), actualTexture, zIndex, frame, startFrame, frameLimit, FPS, animationTime, animationIterationBehavior, animationIterationLimit, animationIterationCount, isAnimated, background, backgroundColor)
    
        self.text = text
        self.previousText = text
        self.font = font
        self.previousFont = font
        self.textColor = textColor
        self.previousTextColor = textColor
        self.padding = padding
        self.previousPadding = padding

    def update_frame(self, FPS:int):
        """Si el atributo isAnimated es True, actualiza el renderizado del texto si algun atributo relacionado cambia, por compatibilidad actualiza el fotograma de la animacion  y de su fondo teniendo en cuenta el tiempo de actualizacion que se calcula por los FPS de actualizacion del juego.

        Args:
            FPS (int): FPS de actualizacion del juego.
        """
        
        if self.isAnimated:
            time = 1 / FPS
            self.animationTime += time
            self.frame = floor(self.animationTime * self.FPS) + self.startFrame 
            self.limit_frame()

            if self.text != self.previousText or self.font != self.previousFont or self.textColor != self.previousTextColor or self.padding != self.previousPadding:
                self.textures = create_text_texture(self.text, self.textColor, self.font, padding=self.padding)
                self.previousText = self.text
                self.previousFont = self.font
                self.previousTextColor = self.textColor
                self.previousPadding = self.padding

            if self.background is not None:
                self.background.update_frame(FPS)



class Physics:
    """Sus instancias almacenan y administran las variables de movimiento de la entidad, como posicion, velocidad y aceleracion, asi como la hitbos de la entidad correpondiente."""

    def __init__(self, position:list[int, int], velocity:list[int, int]=[0, 0], aceleration:list[int, int]=[0, 0], direction:int=Direction.LEFT, isCollidable:bool=False, margin:list=[0], hitboxSize:list[int]=[0,0], hitboxLocation:int=Location.CENTER_BOTTOM, isUpdatable:bool=True) -> None:
        """AI is creating summary for __init__

        Args:
            position (list[int, int]): Posicion (x, y) de la entidad.

            velocity (list[int, int], optional): Velocidad (x, y) de la entidad. Defaults to [0, 0].

            aceleration (list[int, int], optional): Aceleracion (x, y) de entidad. Defaults to [0, 0].

            direction (int, optional): Direccion de la entidad, usado como auxiliar en el cambio de animaciones cuando en los comportamientos de la entidad. Defaults to Direction.LEFT.

            isCollidable (bool, optional): Determina si el movimiento debe estar restringido por las colisiones de la hitbox. Defaults to False.

            margin (list, optional): Margen que modifica la posicion de la hitbox en su creacion. Defaults to [0].

            hitboxSize (list[int], optional): el tamaño (ancho, alto) de la hitbox. Defaults to [0,0].

            hitboxLocation (int, optional): La posicion relativa de la hitbox respecto al fotograma actual de la entidad, desde donde se empezara a posicionar. Defaults to Location.CENTER_BOTTOM.

            isUpdatable (bool, optional): De ser False evita que se realicen las actualizaciones de las fisicas. Defaults to True.
        """

        self.position = position 
        self.previousPosition = [None, None]
        self.velocity = velocity
        self.aceleration = aceleration
        self.direction = direction
        self.isCollidable = isCollidable
        self.margin = margin
        self.hitbox = create_hitbox(pygame.Rect([0,0], [1000, 1000]), margin, hitboxSize, hitboxLocation)
        self.hitboxColor = 0, 0, 255
        self.positionColor = 0, 255, 0
        self.isPositionChanged = False
        self.isUpdatable = isUpdatable
        self.hitboxSize = hitboxSize
        self. hitboxLocation =  hitboxLocation

    
    def update_hitbox(self, dimentions:pygame.Rect, margin:list[int]=None, hitboxSize:list[int]=None,  hitboxLocation:int=None):
        """Crea una nueva hitbox que se ajusta al rectangulo dado en dimentions, y de especificarse, con un nuevo margen, tamaño y posicion relativa.

        Args:
            dimentions (pygame.Rect): El rectango desde donde se posicionara la hitbox.

            margin (list[int], optional): Si se especifica, son los valores que modifican la posicionn de la hitbox. Un solo valor se aplica a los cuatro lados. Con dos valores, el primero se aplica a la derecha e izquierda y el segundo arriba y abajo.Con cuatro valores se aplican en oreden a la izquierda, arriba, derecha y abajo. Defaults to None.

            hitboxSize (list[int], optional): Si se especifica, es el tamaño (ancho, alto) de la hitbox. Defaults to None.

            hitboxLocation (int, optional): Si se especifica, es la nueva posicion relativa de la hitbox entre dimentions, desde donde se empezara a posicionar. Defaults to None. Defaults to None.
        """
        if isinstance(margin, list):
            self.margin = margin
        if isinstance(hitboxSize, list):
            self.hitboxSize = hitboxSize
        if isinstance(hitboxLocation, int):
            self.hitboxLocation = hitboxLocation
        
        
        self.hitbox = create_hitbox(dimentions, self.margin, self.hitboxSize, self.hitboxLocation)
        
    def update_position(self, FPS:int) -> None:
        """Si el atributo isUpdatable es True, actualiza la posicion (x, y) y la velocidad (x, y) respecto a la aceleracion segun las formulas del movimiento uniformemente acelerado.

        Args:
            FPS (int): [description]
        """
        
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
        """Mueve la posicion de la entidad y de la hitbox, segun el desface (x, y) en offsetPosition. Era necesaria para las transciciones no implementadas.

        Args:
            entity ([type]): Entidad que posee como atributo physics esta instancia de Physics.
            offsetPosition (list[int]): desface (x, y).
        """
        if self.previousPosition != [None, None]:
            self.previousPosition[0] += offsetPosition[0]
            self.previousPosition[1] += offsetPosition[1]
        self.hitbox = create_hitbox(pygame.Rect(entity.get_texture_position(), entity.animation.get_texture().get_size()), self.margin, self.hitboxSize, self.hitboxLocation)
        pygame.Rect(self.hitbox.left + 0.1, self.hitbox.top + 0.1, self.hitbox.width, self.hitbox.height)
        self.position[0] += offsetPosition[0]
        self.position[1] += offsetPosition[1]
