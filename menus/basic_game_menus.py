from game_modules.entities import *
from game_modules.utilities import *

def text_behaviour(entity:Entity):
    if len(entity.animation.text) >= 100:
        entity.animation.text = ""
        entity.time = 0
    if entity.time >= 1:
        entity.animation.text += '\n'
        entity.time = 0
        entity.physics.velocity[0] *= -1
    if int(entity.time * 100) % 1 == 0:
        entity.animation.text += 'A'
        entity.physics.velocity[0] *= -1
        if entity.physics.velocity[0] == 0:
            entity.physics.velocity[0] = 100

# In Game Inventary Interface
def create_game_inventary_interface(windowSize:tuple[int]=[800, 600]):
    heartTexture = create_textures(['heart32.png'], [1])
    font = pygame.font.SysFont('Arial', 30)
    inGameInventaryInterfaceEntities = [Entity(Physics([100, 100]), TextIconAnimation("", font, (255, 255, 255, 255), backgroundColor=(0,0,0,120)), entity_id='text', behaviour=text_behaviour)]
    for i in range(3):
        heart = Entity(Physics([20 + 40 * i, 20]), IconAnimation(textures=heartTexture, actualTexture='heart32', background=Animation(create_textures(['chair0.png'], [12]), actualTexture='chair0')), entity_id=f'heart{i}')
        inGameInventaryInterfaceEntities.append(heart)
    return ContextualMenu(windowSize, True, False, False, False, Background(Physics([0,0]), Animation(create_empty_texture(windowSize[0], windowSize[1])), windowSize, scalar=1), windowSize, inGameInventaryInterfaceEntities, 'game_inventary_interface')
