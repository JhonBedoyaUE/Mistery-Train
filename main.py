import pygame
from entities import *
from utilities import *

pygame.init()

def chair_negative(self:Entity, entity:Entity):
    if entity.type == "MainCharacter":
        self.animation.actualTexture = "negative_chair1"

FPS = 60
CLOCK = pygame.time.Clock()
SIZE = (800,600)

screen = pygame.display.set_mode(SIZE)

bg1Textures = create_textures(['bg1.png'], [1])
bg2Textures = create_textures(['bg2.png'], [1])
mcTextures = create_textures(['Idle.png', 'Walk.png'], [4, 6], path='textures/main_character/', variations=2, transformFunction=Transformation.XFLIP, scalar=4, extractContent=True)
mcSize = list(mcTextures.values())[1].sprite[0].get_rect().size

ch1Textures = create_textures(['chair1.png'], [1], scalarBase=mcSize, scalar=1.2, transformFunction=Transformation.NEGATIVE_COLOR, variations=2)

bg1 = Background(Physics([0,0]), Animation(textures=bg1Textures, actualTexture='bg1', zIndex=2), SIZE, scalar=1)
bg2 = Background(Physics([0,0], velocity=[-200,0]), Animation(textures=bg2Textures, actualTexture='bg2', zIndex=1), SIZE, scalar=1)

mainCharacter = MainCharacter(Physics([50,250], isCollidable=True, hitboxSize=[40,60]), Animation(textures=mcTextures, actualTexture='xflip_Idle'), location=Location.CENTER)
levelSize = bg1.animation.get_texture().get_rect().size
leftLimit = Entity(Physics([0,0], isCollidable=True), Animation(create_empty_texture(20, levelSize[1]), isAnimated=False))
rightLimit = Entity(Physics([bg1.animation.get_texture().get_rect().size[0] - 20,0], isCollidable=True), Animation(create_empty_texture(20, levelSize[1]), isAnimated=False))
topLimit = Entity(Physics([0,0], isCollidable=True), Animation(create_empty_texture(levelSize[0], 120), isAnimated=False))
bottomLimit = Entity(Physics([0,bg1.animation.get_texture().get_rect().size[1]], isCollidable=True), Animation(create_empty_texture(bg1.animation.get_texture().get_rect().size[0], 10), isAnimated=False))

chairList = [leftLimit, topLimit, rightLimit, bottomLimit]
for i in range(10):

    for j in [100, 175, 250]:
        chairList.append(Entity(Physics([100 + 100*i, j], margin=[0, -120, 0, 0], isCollidable=True), Animation(textures=ch1Textures, actualTexture='chair1'), collideListeners={"MainCharacter": chair_negative}))

levelWorksSpace = LevelWorksSpace(levelSize,[bg1, bg2], mainCharacter, SIZE, entitiesList=chairList)




running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
    if not running:
        break

    screen.fill((0,0,0))
    levelWorksSpace.update_all(FPS)

    keys = pygame.key.get_pressed()

    levelWorksSpace.listen_keys(pygame.key.get_pressed())


    levelWorksSpace.show(screen, showHitbox=True)
    #pygame.draw.rect(screen, (255,0,0), pygame.Rect(levelWorksSpace.fitThePosition([mainCharacter.physics.hitbox.x, mainCharacter.physics.hitbox.y]), mainCharacter.physics.hitbox.size), 10)
    pygame.display.update()
    CLOCK.tick(FPS)
