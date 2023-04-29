from game_modules.entities import *
from game_modules.utilities import *

def chair_negative(self:Entity, entity:Entity):
    if entity.type == "MainCharacter":
        self.animation.actualTexture = "negative_chair1"

def example_of_click_event(selfEntity:Entity, mousePosition:tuple[int], buttons:tuple[bool]):
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

def create_level(SIZE:tuple[int]):
    bg1Textures = create_textures(['bg1.png'], [1])
    bg2Textures = create_textures(['bg2.png'], [1])
    mcTextures = create_textures(['Idle.png', 'Walk.png'], [4, 6], path='textures/main_character/', variations=2, transformFunction=Transformation.XFLIP, scalar=4, extractContent=True)
    mcSize = list(mcTextures.values())[1].sprite[0].get_rect().size

    ch1Textures = create_textures(['chair1.png'], [1], scalarBase=mcSize, scalar=1.2, transformFunction=Transformation.NEGATIVE_COLOR, variations=2)

    bg1 = Background(Physics([0,0]), Animation(textures=bg1Textures, actualTexture='bg1', zIndex=2), SIZE, scalar=1)
    bg2 = Background(Physics([0,0], velocity=[-200,0]), Animation(textures=bg2Textures, actualTexture='bg2', zIndex=1), SIZE, scalar=1)

    mainCharacter = MainCharacter(Physics([50,200], isCollidable=True, hitboxSize=[50,50], hitboxLocation=Location.CENTER), Animation(textures=mcTextures, actualTexture='Idle', frameLimit=0), location=Location.CENTER, clickableSpace=ClickableSpace.HITBOX)
    levelSize = bg1.animation.get_texture().get_rect().size
    leftLimit = Entity(Physics([0,0], isCollidable=True), Animation(create_empty_texture(20, levelSize[1]), isAnimated=False))
    rightLimit = Entity(Physics([bg1.animation.get_texture().get_rect().size[0] - 20,0], isCollidable=True), Animation(create_empty_texture(20, levelSize[1]), isAnimated=False))
    topLimit = Entity(Physics([0,0], isCollidable=True), Animation(create_empty_texture(levelSize[0], 120), isAnimated=False))
    bottomLimit = Entity(Physics([0,bg1.animation.get_texture().get_rect().size[1]], isCollidable=True), Animation(create_empty_texture(bg1.animation.get_texture().get_rect().size[0], 10), isAnimated=False))

    chairList = [leftLimit, topLimit, rightLimit, bottomLimit]
    for i in range(10):

        for j in [100, 175, 350, 425]:
            chairList.append(Entity(Physics([100 + 100*i, j], margin=[0, -50, 0, 0], isCollidable=True), Animation(textures=ch1Textures, actualTexture='chair1'), collideListeners={"MainCharacter": chair_negative}, entity_id=i+j, mouseListener=example_of_click_event, clickableSpace=ClickableSpace.HITBOX))

    levelWorksSpace = LevelWorksSpace(levelSize,[bg1, bg2], mainCharacter, SIZE, entitiesList=chairList)

    levelWorksSpace.showHitboxes = True

    return levelWorksSpace