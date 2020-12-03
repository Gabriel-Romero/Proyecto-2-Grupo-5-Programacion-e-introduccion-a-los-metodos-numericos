"""Inicio del código que creará una simulación del comportamiento de una
epidemia con respecto a diferentes parámetros que podrán ser controlados
por el usuario por medio de deslizadores como el mostrado a continuación"""

import pygame, sys, random, math
import matplotlib as plt
import matplotlib.backends.backend_agg as agg
import pylab
from pygame_widgets import *
from pygame.locals import *

"""inicializar simulación, definir parámetros"""

pygame.init()
FPS = pygame.time.Clock()
num_fps = 30
X = 1080
Y = 720
pygame.display.set_caption("Simulacion de una epidemia")
radio_circulo = 5
densidad = 1
ProbabilidadDeContagio = 0.03
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
Num_sanos=[]
Num_enfermos=[]
Num_retirados=[]
fig = pylab.figure(figsize=[3, 3], dpi=100,)
font=pygame.font.SysFont("Louis George Cafe.ttf",16)

class Circulo:
    def __init__(self):      # definir círculos
        self.r = radio_circulo
        self.x = random.randint(X-590,X-25)
        self.y = random.randint(Y-590,Y-25)
        self.velx = ((random.randint(1,10)/10)*(-1)**random.randint(0,1))
        self.vely = ((random.randint(1,10)/10)*(-1)**random.randint(0,1))
        self.color = (255,255,255)
        self.TiempoDeContagio = 0
        self.retiro= random.randint(35000,40000)

for i in range(TamañoDeLaPoblacion-int(TamañoDeLaPoblacion*porcentajeinicialinf)):
    sanos.append(Circulo())

for i in range(int(TamañoDeLaPoblacion*porcentajeinicialinf)):
 if i <= int(TamañoDeLaPoblacion*porcentajeinicialinf*porcentajeasimptomatico):
   contagiadosnovisibles.append(Circulo())
   contagiadosnovisibles[i].color=(255,255,40)
    contagiadosnovisibles[i].TiempoDeContagio=pygame.time.get_ticks()
 else: 
   contagiadosvisibles.append(Circulo())
   contagiadosvisibles[i-int(TamañoDeLaPoblacion*porcentajeinicialinf*porcentajeasimptomatico)-1].color=(255,0,0)
   contagiadosvisibles[i-int(TamañoDeLaPoblacion*porcentajeinicialinf*porcentajeasimptomatico)-1].TiempoDeContagio=pygame.time.get_ticks()
 

def infeccion():
    for inf in contagiadosvisibles:
        if pygame.time.get_ticks()-inf.TiempoDeContagio>inf.retiro:
            inf.color=(110,110,110)
            retirados.append(inf)
            contagiadosvisibles.remove(inf)
            
    for inf in contagiadosnovisibles:
        if pygame.time.get_ticks()-inf.TiempoDeContagio>inf.retiro:
            inf.color=(110,110,110)
            retirados.append(inf)
            contagiadosnovisibles.remove(inf)
            
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
    I = font.render('Hay %s personas contagiadas:' % len(contagiadosvisibles+contagiadosnovisibles), True,(0,255,0), (0,0,0))
    I_pos=I.get_rect()
    I_pos.bottomleft=(20,120)       
    pantalla.blit(I,I_pos)
    IV = font.render('%s presentan sintomas' % len(contagiadosvisibles), True,(255,0,0), (0,0,0))
    IV_pos=IV.get_rect()
    IV_pos.bottomleft=(30,140)       
    pantalla.blit(IV,IV_pos)
    INV = font.render('%s son asintomaticos' % len(contagiadosnovisibles), True,(255,255,40), (0,0,0))
    INV_pos=INV.get_rect()
    INV_pos.bottomleft=(30,160)       
    pantalla.blit(INV,INV_pos)
    R = font.render('%s personas han sido retiradas' % len(retirados), True,(110,110,110), (0,0,0))
    R_pos=R.get_rect()
    R_pos.bottomleft=(20,180)       
    pantalla.blit(R,R_pos)
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
