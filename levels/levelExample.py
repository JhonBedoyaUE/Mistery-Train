from game_modules.entities import *
from game_modules.utilities import *

def chair_negative(self:Entity, entity:Entity) -> None:
    """Es un ejemplo de escuchador del evento de colision o collide listener, el cual cambia los colores de la textura de la silla a negativo. 

    Args:
        self (Entity): Es la entidad que esta esta ecuchando la colision tras colisionar.
        entity (Entity): Es la entidad con la que colisiono.
    """
    if entity.type == "MainCharacter":
        self.animation.actualTexture = "negative_chair1"

def example_of_click_event(selfEntity:Entity, mousePosition:tuple[int], buttons:tuple[bool]) -> None:
    """Es un ejemplo de escuchador de los eventos de mouse o mouse listener, el cual alterna los colores de la textura de la silla a negativo. 

    Args:
        selfEntity (Entity): Entidad que fue clickeada
        mousePosition (tuple[int]): Las coordenadas de la posicion del mouse
        buttons (tuple[bool]): Los estados de los botones del mouse (izquierdo, scroll, derecho)
    """
    if not 'isClickUp' in selfEntity.globals.keys():
        selfEntity.globals['isClickUp'] = False
    if selfEntity.globals['isClickUp'] and buttons[0]:
        selfEntity.globals['isClickUp'] = False
        if selfEntity.animation.actualTexture == "negative_chair1":
            selfEntity.animation.actualTexture = "chair1"
        else:
            selfEntity.animation.actualTexture = "negative_chair1"
    elif selfEntity.time >= 0.5:
        selfEntity.time = 0
        selfEntity.globals['isClickUp'] = True

def change_to_negative(selfEntity:Entity, mousePosition:tuple[int], buttons:tuple[bool]) -> None:
    """Es un ejemplo de escuchador de los eventos de mouse o mouse listener, el cual alterna los colores de la textura de la silla a negativo con click izquierdo, o la gira 180 grados con click derecho.

    Args:
        selfEntity (Entity): Entidad que fue clickeada
        mousePosition (tuple[int]): Las coordenadas de la posicion del mouse
        buttons (tuple[bool]): Los estados de los botones del mouse (izquierdo, scroll, derecho)
    """
    if not 'isClickUp' in selfEntity.globals.keys():
        selfEntity.globals['isClickUp'] = False
    if selfEntity.globals['isClickUp'] and buttons[0]:
        selfEntity.globals['isClickUp'] = False
        
        if "negative" in selfEntity.animation.actualTexture:
            selfEntity.animation.actualTexture = selfEntity.animation.actualTexture.replace('negative_', '')
            selfEntity.globals['prefix'] = selfEntity.globals['prefix'].replace('negative_', '')
        else:
            if '180rotated_' in selfEntity.animation.actualTexture:
                selfEntity.animation.actualTexture = '180rotated_' + "negative_" + selfEntity.animation.actualTexture.replace('180rotated_', '')
            else:
                selfEntity.animation.actualTexture = "negative_" + selfEntity.animation.actualTexture
            selfEntity.globals['prefix'] = 'negative_'
    elif selfEntity.globals['isClickUp'] and buttons[2]:
        selfEntity.globals['isClickUp'] = False
        
        if "180rotated_" in selfEntity.animation.actualTexture:
            selfEntity.animation.actualTexture = selfEntity.animation.actualTexture.replace('180rotated_', '')
            selfEntity.globals['prefix'] = selfEntity.globals['prefix'].replace('180rotated_', '')
        else:
            selfEntity.animation.actualTexture = "180rotated_" + selfEntity.animation.actualTexture
            selfEntity.globals['prefix'] = '180rotated_' + selfEntity.globals['prefix']
    elif selfEntity.time >= 0.5:
        selfEntity.time = 0
        selfEntity.globals['isClickUp'] = True




def create_level(SIZE:tuple[int]) -> LevelWorksSpace:
    """Crea un nivel de ejemplo.

    Args:
        SIZE (tuple[int]): Tamaño de la ventana

    Returns:
        LevelWorksSpace
    """

    print('\nPresiona H para mostrar las hitboxes,\n         j para mostrar los puntos de las posiciones\n       y k para mostrar los espacios clickeables')

    # Cargando y creando las texturas
    bg1Textures = create_textures(['bg1.png'], [1])
    bg2Textures = create_textures(['bg2.png'], [1])
    mcTextures = create_textures(['Idle.png', 'Walk.png'], [4, 6], path='textures/main_character/', variations=[2, 2, 3], transformFunctions=[Transformation.XFLIP, Transformation.NEGATIVE_COLOR, Transformation.RECT_ROTATION], scalar=4, extractContent=True)

    # Guardando el tamaño del personaje principal para agrandar algunas texturas al tamaño del personaje principal 
    mcSize = list(mcTextures.values())[1].sprite[0].get_rect().size
    
    ch1Textures = create_textures(['chair1.png'], [1], scalarBase=mcSize, scalar=1.2, transformFunctions=Transformation.NEGATIVE_COLOR, variations=2)


    # Creando Las diferentes entidades a usar como los fondos, el personaje principal, los limites o como mas abajo entidades 'silla'  
    bg1 = Background(Physics([0,0]), Animation(textures=bg1Textures, actualTexture='bg1', zIndex=2), SIZE, scalar=1)
    bg2 = Background(Physics([0,0], velocity=[-200,0]), Animation(textures=bg2Textures, actualTexture='bg2', zIndex=1), SIZE, scalar=1)
    mainCharacter = MainCharacter(Physics([50,200], isCollidable=True, hitboxSize=[50,50], hitboxLocation=Location.CENTER), Animation(textures=mcTextures, actualTexture='Idle', frameLimit=0), location=Location.CENTER, clickableSpace=ClickableSpace.HITBOX, mouseListener=change_to_negative)


    # Guardando el tamaño del fondo del tren para escalar el nivel y sus limites
    levelSize = bg1.animation.get_texture().get_rect().size

    # Creando los limites del nivel para que el personaje no se salga del espacio visible
    leftLimit = Entity(Physics([0,0], isCollidable=True), Animation(create_empty_texture(20, levelSize[1]), isAnimated=False))
    rightLimit = Entity(Physics([bg1.animation.get_texture().get_rect().size[0] - 20,0], isCollidable=True), Animation(create_empty_texture(20, levelSize[1]), isAnimated=False))
    topLimit = Entity(Physics([0,0], isCollidable=True), Animation(create_empty_texture(levelSize[0], 120), isAnimated=False))
    bottomLimit = Entity(Physics([0,bg1.animation.get_texture().get_rect().size[1]], isCollidable=True), Animation(create_empty_texture(bg1.animation.get_texture().get_rect().size[0], 10), isAnimated=False))

    # Guardando los limites en la lista de entidades a cargar en el juego
    entitiesList = [leftLimit, topLimit, rightLimit, bottomLimit]

    # Creando las entidades silla de forma dinamica
    for i in range(10):
        for j in [100, 175, 350, 425]:
            entitiesList.append(Entity(Physics([100 + 100*i, j], margin=[0, -50, 0, 0], isCollidable=True), Animation(textures=ch1Textures, actualTexture='chair1'), collideListeners={"MainCharacter": chair_negative}, entity_id=i+j, mouseListener=example_of_click_event, clickableSpace=ClickableSpace.SPRITE))

    # Creando el LevelworksSpace que representa nuestro nivel, con su tamaño, sus fondos, personaje principal, tamaño de la ventana y las entidades a interactuar
    levelWorksSpace = LevelWorksSpace(levelSize,[bg1, bg2], mainCharacter, SIZE, entitiesList=entitiesList)


    return levelWorksSpace