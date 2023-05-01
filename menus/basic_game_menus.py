from game_modules.entities import *
from game_modules.utilities import *

def text_behaviour(entity:Entity):
    if len(entity.animation.text) >= 100:
        entity.animation.text = ""
        entity.time = 0
    if entity.time >= 1:
        entity.animation.text += '\n'
        entity.time = 0
        #entity.physics.velocity[0] *= -1
    if int(entity.time * 100) % 1 == 0:
        entity.animation.text += 'A'
        #entity.physics.velocity[0] *= -1
        #if entity.physics.velocity[0] == 0:
        #    entity.physics.velocity[0] = 100

# In Game Inventary Interface
def create_game_inventary_interface(windowSize:tuple[int]=[800, 600]):
    heartTexture = create_textures(['heart32.png'], [1])
    font = pygame.font.SysFont('Arial', 30)
    inGameInventaryInterfaceEntities = [Entity(Physics([100, 100]), TextIconAnimation("", font, (255, 255, 255, 255), backgroundColor=(0,0,0,120)), entity_id='text', behaviour=text_behaviour)]
    for i in range(3):
        heart = Entity(Physics([20 + 40 * i, 20]), IconAnimation(textures=heartTexture, actualTexture='heart32', background=Animation(create_textures(['chair0.png'], [12]), actualTexture='chair0')), entity_id=f'heart{i}')
        inGameInventaryInterfaceEntities.append(heart)
    return ContextualMenu(windowSize, True, False, False, False, Background(Physics([0,0]), Animation(create_empty_texture(windowSize[0], windowSize[1])), windowSize, scalar=1), windowSize, inGameInventaryInterfaceEntities, 'game_inventary_interface')

def continue_click(selfEntity:Entity, mousePosition:tuple[int], buttons:tuple[bool]):
    if buttons[0]:
        selfEntity.parent.parent.show_menu(create_continue_menu())

def si_click(selfEntity:Entity, mousePosition:tuple[int], buttons:tuple[bool]):
    if buttons[0]:
        selfEntity.parent.parent.contextualMenusStack = []

def no_click(selfEntity:Entity, mousePosition:tuple[int], buttons:tuple[bool]):
    if buttons[0]:
        selfEntity.parent.parent.contextualMenusStack.remove(selfEntity.parent)

def continue_behaviour(selfEntity:Entity):
    if selfEntity.isHover:
        selfEntity.animation.backgroundColor = (0, 0, 255, 255)
    else:
        selfEntity.animation.backgroundColor = (120, 120, 120, 200)


def create_paused_menu(windowSize:tuple[int]=[800, 600]):
    font = pygame.font.SysFont('Arial', 30, bold=True)
    pausedMenuEntities = [Entity(Physics([350, 300]), TextIconAnimation("Continuar", font, (255, 255, 255, 255), backgroundColor=(120,120,120,200)), entity_id='continue_button', mouseListener=continue_click, behaviour=continue_behaviour)]

    return ContextualMenu(windowSize, True, False, False, True, Background(Physics([0,0]), Animation(create_empty_texture(windowSize[0], windowSize[1])), windowSize, scalar=1), windowSize, pausedMenuEntities, 'create_paused_menu', backgroundColor=(0,0,0,80))

def create_continue_menu(windowSize:tuple[int]=[800, 600]):
    font = pygame.font.SysFont('Arial', 30, bold=True)
    mensaje= Entity(Physics([200, 200]), TextIconAnimation("Seguro quiere continuar", font, (255, 255, 255, 255), backgroundColor=(0,0,0,0)), entity_id='msg')
    si = Entity(Physics([300, 350]), TextIconAnimation("Si", font, (255, 255, 255, 255), backgroundColor=(120,120,120,200)), entity_id='si', mouseListener=si_click, behaviour=continue_behaviour)
    no = Entity(Physics([400, 350]), TextIconAnimation("No", font, (255, 255, 255, 255), backgroundColor=(120,120,120,200)), entity_id='no', mouseListener=no_click, behaviour=continue_behaviour)
    continueMenuEntities = [mensaje, si, no]

    return ContextualMenu(windowSize, False, False, False, True, Background(Physics([0,0]), Animation(create_empty_texture(windowSize[0], windowSize[1])), windowSize, scalar=1), windowSize, continueMenuEntities, 'create_continue_menu', backgroundColor=(0,0,0,80))

