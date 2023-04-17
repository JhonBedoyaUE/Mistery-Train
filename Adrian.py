import pygame as pg
pg.init()

def juego1(PANTALLA):
    pg.draw.rect(PANTALLA, (250,250,250), (180,200,400,160))
    titulo = impactFont.render("El mentiroso",True,(0, 0, 0, 1))
    texto1 = calibriFont.render("Intenta adivinar cuando la maquina miente.",True,(0, 0, 0, 1))
    texto2 = calibriFont.render("para esto es necesario responder",True,(0, 0, 0, 1))
    texto3 = calibriFont.render("5 preguntas bien con respuestas si y no",True,(0, 0, 0, 1))
    texto4 = impactFont1.render("Al final obtendras el codigo de la puerta",True,(0, 0, 0, 1))
    return PANTALLA.blit(titulo,(300,196)),PANTALLA.blit(texto1,(210,240)),PANTALLA.blit(texto2,(210,270)), PANTALLA.blit(texto3,(210,300)), PANTALLA.blit(texto4,(210,330))

def menu(PANTALLA):
    pg.draw.rect(PANTALLA, (250,250,250), (180,200,400,160))
    titulo = impactFont.render("MENU",True,(0, 0, 0, 1))
    texto1 = calibriFont.render("Teclas Moviniento: A,W,S,D",True,(0, 0, 0, 1))
    texto2 = calibriFont.render("Botones adicionales: Click derecho e izquierdo ",True,(0, 0, 0, 1))
    texto3 = calibriFont.render(" f - cerrar ventanas, Ctrl - salir, VisionN - v",True,(0, 0, 0, 1))
    texto4 = impactFont1.render("Mision: Escapar del tren",True,(0, 0, 0, 1))
    return PANTALLA.blit(titulo,(300,196)),PANTALLA.blit(texto1,(210,240)),PANTALLA.blit(texto2,(210,270)), PANTALLA.blit(texto3,(210,300)), PANTALLA.blit(texto4,(210,330))

def visionNocturna(Pantalla, tiempo):
    return Pantalla.fill((0,0,0))
class Silla():

    def __init__(self, img):
        self.silla1 = img
        print('why')


    def mostrar(self,ubx,uby,pantalla):
        pass
        #pantalla.blit(self.silla1,(ubx,uby))

PANTALLA = pg.display.set_mode((800,600))
pg.display.set_caption("Juego Maestro")
fondo = pg.image.load("textures/bg1.png")
PANTALLA.blit(fondo,(0,0))

#moviniento personaje
x = 50
y = 280
timeReal = 0
tiempoV = 0
juego = True
actCodigo = False
menuAct = False
vision = False
impactFont = pg.font.SysFont("Impact",30)
impactFont1 = pg.font.SysFont("Impact",20)
calibriFont = pg.font.SysFont("Calibri",20)

imgsilla = pg.image.load("textures/chair1.png").convert()
s1 = Silla(imgsilla)


while juego:
    time = pg.time.get_ticks()/1000
    if timeReal == int(time):
        timeReal += 1
        if vision:
            tiempoV += 1 
            if tiempoV == 1:
                vision = False
        if not vision:
            tiempoV = 0
    PANTALLA.blit(fondo,(0,0))
    Keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                menuAct = True
            if event.key == pg.K_LCTRL:
                juego = False
            if event.key == pg.K_f:
                actCodigo = False
                menuAct =False
            if event.key == pg.K_v:
                vision = True
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button==3:
                print("hola")
            if event.button==1:
                if pg.mouse.get_pos()[0]>590 and pg.mouse.get_pos()[0]<600 and pg.mouse.get_pos()[1]>120 and pg.mouse.get_pos()[1]<130:
                    actCodigo = True
                
    if Keys[pg.K_a]:
        x -= 0.5
    if Keys[pg.K_d]:
        x += 0.5
    if Keys[pg.K_w]:
        y-= 0.5
    if Keys[pg.K_s]:
        y += 0.5
    if x< 40:
        x = 40
    if x> 687:
        x = 687
    if y< 100:
        y = 100
    if y> 443:
        y = 443
    #sillas
    pg.draw.rect(PANTALLA, (0,0,0), (70,350,90,140))
    pg.draw.rect(PANTALLA, (0,0,0), (200,350,90,140))
    pg.draw.rect(PANTALLA, (0,0,0), (330,350,90,140))
    pg.draw.rect(PANTALLA, (0,0,0), (460,350,90,140))
    pg.draw.rect(PANTALLA, (0,0,0), (590,350,90,140))
    
    pg.draw.rect(PANTALLA, (0,0,0), (70,120,90,140))
    pg.draw.rect(PANTALLA, (0,0,0), (200,120,90,140))
    pg.draw.rect(PANTALLA, (0,0,0), (330,120,90,140))
    pg.draw.rect(PANTALLA, (0,0,0), (460,120,90,140))
    pg.draw.rect(PANTALLA, (0,0,0), (590,120,90,140))
    #puertas
    pg.draw.rect(PANTALLA, (250,250,250), (746,250,65,100))
    #personaje
    pg.draw.rect(PANTALLA, (0,0,0), (x,y,60,60))
    if vision:
        visionNocturna(PANTALLA, timeReal)
        #pistas
        pg.draw.rect(PANTALLA, (89,205,178), (590,120,20,10)) 
    if menuAct: 
        menu(PANTALLA)
    if actCodigo:
        juego1(PANTALLA)
    s1.mostrar(70,120,PANTALLA)
    pg.display.update() 
pg.quit()