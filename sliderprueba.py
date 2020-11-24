# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 13:07:22 2020

@author: pedro
"""

import pygame, math, sys
pygame.init()

X = 900  # screen width
Y = 600  # screen height

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


class Slider():
    def __init__(self, name, val, maxi, mini, pos):
        self.val = val  # valor iniciaol del slider
        self.maxi = maxi  # el valor maximo del slider a la derecha
        self.mini = mini  # el valor minimo del slider a la izquierda
        self.xpos = pos  # La posicion del eje horizontal en la pantalla
        self.ypos = 550
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
        pos = (10+int((self.val-self.mini)/(self.maxi-self.mini)*80), 33)
        self.button_rect = self.button_surf.get_rect(center=pos)
        surf.blit(self.button_surf, self.button_rect)
        self.button_rect.move_ip(self.xpos, self.ypos)  # esto mueve el boton a la posicion que le corresponde en la pantalla

        # esta seccion dibuja todo en la pantalla
        screen.blit(surf, (self.xpos, self.ypos))

    def move(self):
        """
    Esta funcion se encarga de reaccionar al movimiento del mouse con respecto al boton
    """
        self.val = (pygame.mouse.get_pos()[0] - self.xpos - 10) / 80 * (self.maxi - self.mini) + self.mini
        if self.val < self.mini:
            self.val = self.mini
        if self.val > self.maxi:
            self.val = self.maxi


font = pygame.font.SysFont("Verdana", 12) 
screen = pygame.display.set_mode((X, Y))
clock = pygame.time.Clock()



velocidad = Slider("velocidad", 10, 15, 1, 25)
r = Slider("radio de infeccion", 5, 5, 10, 150)
ProbabilidadDeContagio = Slider("Probabilidad de contagio", 0.5, 0, 1, 400)
TamañoDeLaPoblacion = Slider("Tamaño de la poblacion", 50, 50, 500, 525)
Asintomatico = Slider("Asintomatismo", 0, 0, 1, 775)
slides = [velocidad, r, ProbabilidadDeContagio, TamañoDeLaPoblacion, Asintomatico]



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for s in slides:
                if s.button_rect.collidepoint(pos):
                    s.hit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            for s in slides:
                s.hit = False

    # Mueve el boton del slider
    for s in slides:
        if s.hit:
            s.move()

    # Actualiza la pantalla para que el movimiento sea fluido
   

    for s in slides:
        s.draw()
    
    I = font.render('velocidad= %s ' % velocidad.val, True,(0,0,0), (255,255,250))
    I_pos=I.get_rect()
    I_pos.bottomleft=(20,120) 
    screen.blit(I,I_pos)

    pygame.display.flip()
    clock.tick(velocidad.val)
    
    
    """ Codigo adaptado de https://www.dreamincode.net/forums/topic/401541-buttons-and-sliders-in-pygame/ """
