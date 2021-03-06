# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 20:22:32 2020

@author: INGENIERO
"""

import pygame, sys, random, math
import matplotlib as plt
import matplotlib.backends.backend_agg as agg
import pylab
from pygame_widgets import *
from pygame.locals import *
import numpy as np

"""inicializar simulación, definir parámetros"""

pygame.init()
FPS = pygame.time.Clock()
num_fps = 120
X = 1080
Y = 610
pygame.display.set_caption("Simulacion de una epidemia")
radio_circulo = 5
ProbabilidadDeContagio = 0.01
TamañoDeLaPoblacion = 263
porcentajeinicialinf= 0.05
porcentajeasimptomatico=0.8
TiempoDeEnfermedadpromedio = 50000
radiocontagio=10
pantalla = pygame.display.set_mode((X,Y))
sanos = []
contagiadosvisibles=[]
contagiadosnovisibles=[]
retirados=[]
Num_sanos=[]
Num_enfermos=[]
Top=[TamañoDeLaPoblacion]
L0=[0]
fig = pylab.figure(figsize=[3, 3], dpi=100,)
ax = fig.gca()
font=pygame.font.SysFont("Louis George Cafe.ttf",16)
pausa= False


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 50)
BLUE = (50, 50, 255)
GREY = (200, 200, 200)
ORANGE = (200, 100, 50)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
TRANS = (1, 1, 1)


class Circulo:
    def __init__(self):      # definir círculos
        self.r = radio_circulo
        self.x = random.randint(X-590,X-25)
        self.y = random.randint(Y-590,Y-25)
        self.velx = ((random.randint(1,10)/10)*(-1)**random.randint(0,1))
        self.vely = ((random.randint(1,10)/10)*(-1)**random.randint(0,1))
        self.color = (255,255,255)
        self.TiempoDeContagio = 0
        self.retiro= random.randint(int(TiempoDeEnfermedadpromedio*0.75),int(TiempoDeEnfermedadpromedio*1.25))

def inicio():
 for i in range(TamañoDeLaPoblacion-int(TamañoDeLaPoblacion*porcentajeinicialinf)):
  sanos.append(Circulo())
 Num_sanos.append(len(sanos))

 for i in range(int(TamañoDeLaPoblacion*porcentajeinicialinf)):
  if i <= int(TamañoDeLaPoblacion*porcentajeinicialinf*porcentajeasimptomatico):
   contagiadosnovisibles.append(Circulo())
   contagiadosnovisibles[i].color=(255,255,40)
   contagiadosnovisibles[i].TiempoDeContagio=pygame.time.get_ticks()
  else: 
   contagiadosvisibles.append(Circulo())
   contagiadosvisibles[i-int(TamañoDeLaPoblacion*porcentajeinicialinf*porcentajeasimptomatico)-1].color=(255,0,0)
   contagiadosvisibles[i-int(TamañoDeLaPoblacion*porcentajeinicialinf*porcentajeasimptomatico)-1].TiempoDeContagio=pygame.time.get_ticks()
 Num_enfermos.append(len(contagiadosvisibles)+len(contagiadosnovisibles))


class Slider():
    def __init__(self, name, val, maxi, mini, pos):
        self.val = val  # valor inicial del slider
        self.maxi = maxi  # el valor maximo del slider a la derecha
        self.mini = mini  # el valor minimo del slider a la izquierda
        self.xpos = 350
        self.ypos = pos
        self.surf = pygame.surface.Surface((100, 50))
        self.hit = False  # Esta variable indica el movmiento del boton por accion del mouse

        self.txt_surf = font.render(name, 1, BLACK)
        self.txt_rect = self.txt_surf.get_rect(center=(50, 15))

        # Se define las graficas estaticas del slider, como el fondo #
        self.surf.fill((100, 100, 100))
        pygame.draw.rect(self.surf, GREY, [0, 0, 100, 50], 3)
        pygame.draw.rect(self.surf, ORANGE, [10, 10, 80, 10], 0)
        pygame.draw.rect(self.surf, WHITE, [10, 30, 80, 5], 0)

        self.surf.blit(self.txt_surf, self.txt_rect)  # Por esto mismo esta superficie nunca cambia

        # Aqui se define las partes moviles del slider, como la superficie del boton que se mueve #
        self.button_surf = pygame.surface.Surface((20, 20))
        self.button_surf.fill(TRANS)
        self.button_surf.set_colorkey(TRANS)
        pygame.draw.circle(self.button_surf, BLACK, (10, 10), 6, 0)
        pygame.draw.circle(self.button_surf, ORANGE, (10, 10), 4, 0)

    def draw(self):
        """ Esta seccion se encarga de dibujar las partes tanto estaticas como
        dinamicas de los sliders
    """
        # Esto corresponde a lo estatico, y se empieza por crear una copia de
        # la superficie anterior
        surf = self.surf.copy()

        # Esta seccion corresponde a la creacion de las partes moviles del slider
        pos = (10+int((self.val-self.mini)/(self.maxi-self.mini)*70), 33)
        self.button_rect = self.button_surf.get_rect(center=pos)
        surf.blit(self.button_surf, self.button_rect)
        self.button_rect.move_ip(self.xpos, self.ypos)  # esto mueve el boton a la posicion que le corresponde en la pantalla

        # esta seccion dibuja todo en la pantalla
        pantalla.blit(surf, (self.xpos, self.ypos))

    def move(self):
        """
    Esta funcion se encarga de reaccionar al movimiento del mouse con respecto al boton
    """
        self.val = (pygame.mouse.get_pos()[0] - self.xpos - 5) / 80 * (self.maxi - self.mini) + self.mini
        if self.val < self.mini:
            self.val = self.mini
        if self.val > self.maxi:
            self.val = self.maxi



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
           if ((inf.x-san.x)**2+(inf.y-san.y)**2)**0.5<rcontagio.val :
               if random.randint(1,10000)<=10000*Contagio.val:
                  san.TiempoDeContagio=pygame.time.get_ticks()
                  if random.randint(1,100)<=100*Asintomatismo.val: 
                    san.color=(255,255,40)
                    contagiadosnovisibles.append(san)
                  else:  
                    san.color=(255,0,0)
                    contagiadosvisibles.append(san)
                  sanos.remove(san)
    Num_sanos.append(len(sanos)+len(contagiadosvisibles)+len(contagiadosnovisibles))
    Num_enfermos.append(len(contagiadosnovisibles)+len(contagiadosvisibles))
    Top.append(Top[0])
    L0.append(L0[-1]+1)
    

def detectar_colision():     # detectar colisiones con los bordes
    for c in sanos+contagiadosvisibles+contagiadosnovisibles:
        if c.x <= X-595 or c.x >= X-15:
            c.velx = -c.velx
        elif c.y <= Y-595 or c.y >= Y-15:
            c.vely = -c.vely

def mover():                 # actualizar la posición de los círculos
    for c in sanos+contagiadosvisibles+contagiadosnovisibles:
        c.x += c.velx
        c.y += c.vely

def graficas():
    ax.fill_between(L0, Num_enfermos,Num_sanos, color='green', alpha =.25)
    ax.fill_between(L0,Num_enfermos,color='red',alpha=.25)
    ax.fill_between(L0,Num_sanos,Top,color="gray",alpha=.25)
    ax.axis('off')
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    global surf
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    

def dibujar():  # mostrar círculos
    pantalla.fill((0,0,0))
    pygame.draw.rect(pantalla,(0,0,255),[X-600,Y-600,590,590],1)   
    Sanos = font.render(' %s' % int(rcontagio.val), True, (0,255,0),(0,0,0))
    Sanos_pos=Sanos.get_rect()
    Sanos_pos.bottomleft=(390,170)         
    pantalla.blit(Sanos,Sanos_pos)
    I = font.render('%s' % round(Contagio.val,4), True,(255,0,0), (0,0,0))
    I_pos=I.get_rect()
    I_pos.bottomleft=(390,270)       
    pantalla.blit(I,I_pos)
    IV = font.render('%s' % int(round(Poblacion.val,-1)), True,(255,255,255), (0,0,0))
    IV_pos=IV.get_rect()
    IV_pos.bottomleft=(390,365)       
    pantalla.blit(IV,IV_pos)
    INV = font.render('%s' % round(Asintomatismo.val,2), True,(255,255,0), (0,0,0))
    INV_pos=INV.get_rect()
    INV_pos.bottomleft=(390,465)       
    pantalla.blit(INV,INV_pos)
    for i in contagiadosvisibles+contagiadosnovisibles:
        pygame.draw.circle(pantalla,(5, 153, 29),(int(i.x),int(i.y)),rcontagio.val)
    for c in sanos+contagiadosvisibles+contagiadosnovisibles+retirados:
        pygame.draw.circle(pantalla,c.color,(int(c.x),int(c.y)),c.r)
    pantalla.blit(surf, (30,150))
    for s in slides:
        s.draw()
       
  
graficas_delay =pygame.USEREVENT+0
pygame.time.set_timer(graficas_delay,3000)  

def finalizar():             # revisar si se debe finalizar la simulación
    global pausa
    acciones = pygame.event.get()
    for accion in acciones:
        if accion.type == QUIT:
            pygame.quit()
            sys.exit()
        elif accion.type == pygame.KEYDOWN:
            if accion.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if accion.type == pygame.KEYDOWN:
            if accion.key== pygame.K_p:
                pausa= not pausa
        if accion.type==graficas_delay:
            graficas()
        elif accion.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for s in slides:
                if s.button_rect.collidepoint(pos):
                    s.hit = True
        elif accion.type == pygame.MOUSEBUTTONUP:
            for s in slides:
                s.hit = False

    # Mueve el boton del slider
    for s in slides:
        if s.hit:
            s.move()

    # Actualiza la pantalla para que el movimiento sea fluido
   



rcontagio = Slider("radio infeccion", radiocontagio, 20, 5, 100)
Contagio = Slider("Contagio", ProbabilidadDeContagio, 0.1, 0, 200)
Poblacion = Slider("Poblacion", TamañoDeLaPoblacion, 500, 50, 300)
Asintomatismo = Slider("Asintomatismo", porcentajeasimptomatico, 1, 0, 400)
slides =  [rcontagio, Contagio, Poblacion, Asintomatismo]

def correr_simulacion():
    inicio()
    graficas() 
    global TamañoDeLaPoblacion
    global ProbabilidadDeContagio
    global porcentajeasimptomatico
    global radiocontagio
    global sanos
    global contagiadosvisibles
    global contagiadosnovisibles
    global retirados        
    global Num_sanos
    global Num_enfermos
    global Top
    global L0
    global fig
    global ax
    while True:
      finalizar()       
      if pausa==False:
        mover()
        detectar_colision()
        infeccion()
        dibujar()
        pygame.display.flip()
        FPS.tick(num_fps)
      if not int(round(Poblacion.val,-1))==TamañoDeLaPoblacion:
          TamañoDeLaPoblacion = int(round(Poblacion.val,-1))
          ProbabilidadDeContagio = round(Contagio.val,4)
          porcentajeasimptomatico=round(Asintomatismo.val,2)
          radiocontagio=int(rcontagio.val)
          sanos = []
          contagiadosvisibles=[]
          contagiadosnovisibles=[]
          retirados=[]          
          Num_sanos=[]
          Num_enfermos=[]
          Top=[TamañoDeLaPoblacion]
          L0=[0]
          plt.pyplot.close()
          fig = pylab.figure(figsize=[3, 3], dpi=100,)
          ax = fig.gca()
          inicio()
          graficas() 
      
correr_simulacion()