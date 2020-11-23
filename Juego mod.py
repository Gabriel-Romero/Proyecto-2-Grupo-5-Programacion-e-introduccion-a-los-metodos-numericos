"""Inicio del código que creará una simulación del comportamiento de una
epidemia con respecto a diferentes parámetros que podrán ser controlados
por el usuario por medio de deslizadores como el mostrado a continuación"""

import pygame, sys, random, math
from pygame_widgets import *
from pygame.locals import *

"""inicializar simulación, definir parámetros"""

pygame.init()
FPS = pygame.time.Clock()
num_fps = 60
X = 1000
Y = 650
radio_circulo = 5
densidad = 1
ProbabilidadDeContagio = 0.01
TamañoDeLaPoblacion = 250
porcentajeinicialinf= 0.04
porcentajeasimptomatico=0.8
mortalidad = 1/20
TiempoDeEnfermedad = 10
radiocontagio=10
pantalla = pygame.display.set_mode((X,Y))
sanos = []
contagiadosvisibles=[]
contagiadosnovisibles=[]
retirados=[]
font=pygame.font.Font("Louis George Cafe.ttf",16)

class Circulo:
    def __init__(self):      # definir círculos
        self.r = radio_circulo
        self.x = random.randint(X-590,X-25)
        self.y = random.randint(Y-590,Y-25)
        self.velx = ((random.randint(1,10)/10)*(-1)**random.randint(0,1))
        self.vely = ((random.randint(1,10)/10)*(-1)**random.randint(0,1))
        self.color = (255,255,255)
        self.MomentoDeContagio = None

for i in range(TamañoDeLaPoblacion-int(TamañoDeLaPoblacion*porcentajeinicialinf)):
    sanos.append(Circulo())

for i in range(int(TamañoDeLaPoblacion*porcentajeinicialinf)):
 if i <= int(TamañoDeLaPoblacion*porcentajeinicialinf*porcentajeasimptomatico):
   contagiadosnovisibles.append(Circulo())
   contagiadosnovisibles[i].color=(255,255,40)
 else: 
   contagiadosvisibles.append(Circulo())
   contagiadosvisibles[i-int(TamañoDeLaPoblacion*porcentajeinicialinf*porcentajeasimptomatico)-1].color=(255,0,0)
   
 

def infeccion():
    for inf in contagiadosvisibles+contagiadosnovisibles:
        for san in reversed(sanos):
           if ((inf.x-san.x)**2+(inf.y-san.y)**2)**0.5<radiocontagio :
               if random.randint(1,100)<=100*ProbabilidadDeContagio:
                  if random.randint(1,100)<=100*porcentajeasimptomatico: 
                    san.color=(255,255,40)
                    contagiadosnovisibles.append(san)
                  else:  
                    san.color=(255,0,0)
                    contagiadosvisibles.append(san)
                  sanos.remove(san)
                    


def detectar_colision():     # detectar colisiones con los bordes
    for c in sanos+contagiadosvisibles+contagiadosnovisibles+retirados:
        if c.x <= X-595 or c.x >= X-15:
            c.velx = -c.velx
        elif c.y <= Y-595 or c.y >= Y-15:
            c.vely = -c.vely

def mover():                 # actualizar la posición de los círculos
    for c in sanos+contagiadosvisibles+contagiadosnovisibles+retirados:
        c.x += c.velx
        c.y += c.vely

def dibujar():  # mostrar círculos
    pantalla.fill((0,0,0))
    pygame.draw.rect(pantalla,(0,0,255),[X-600,Y-600,590,590],1)   
    Sanos = font.render('Hay %s personas sanas' % len(sanos), True, (255,255,255),(0,0,0))
    Sanos_pos=Sanos.get_rect()
    Sanos_pos.bottomleft=(20,100)         
    pantalla.blit(Sanos,Sanos_pos)
    I = font.render('Hay %s personas enfermas' % len(contagiadosvisibles+contagiadosnovisibles), True,(0,255,0), (0,0,0))
    I_pos=I.get_rect()
    I_pos.bottomleft=(20,120)       
    pantalla.blit(I,I_pos)
    IV = font.render('%s visiblemente' % len(contagiadosvisibles), True,(255,0,0), (0,0,0))
    IV_pos=IV.get_rect()
    IV_pos.bottomleft=(30,140)       
    pantalla.blit(IV,IV_pos)
    INV = font.render('%s asimptomaticamente' % len(contagiadosnovisibles), True,(255,255,40), (0,0,0))
    INV_pos=INV.get_rect()
    INV_pos.bottomleft=(30,160)       
    pantalla.blit(INV,INV_pos)
    for i in contagiadosvisibles+contagiadosnovisibles:
        pygame.draw.circle(pantalla,(5, 153, 29),(int(i.x),int(i.y)),radiocontagio)
    for c in sanos+contagiadosvisibles+contagiadosnovisibles+retirados:
        pygame.draw.circle(pantalla,c.color,(int(c.x),int(c.y)),c.r)
    pygame.display.flip()
    FPS.tick(num_fps)

def finalizar():             # revisar si se debe finalizar la simulación
    acciones = pygame.event.get()
    for accion in acciones:
        if accion.type == QUIT:
            pygame.quit()
            sys.exit()
        elif accion.type == pygame.KEYDOWN:
            if accion.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

def correr_simulacion():
    
    while True:
        finalizar()
        mover()
        detectar_colision()
        infeccion()
        dibujar()

correr_simulacion()