#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMatrix.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM! - Uruguay - Plan Ceibal

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import pygame
from pygame.locals import *

import gc
gc.enable()

import sys, os, random

RESOLUCION_MONITOR = (1200,900)
LOGO_JAM = os.getcwd() + "/CucaraSims/Iconos/icono_jam.png"

import CeibalJAM_Lib
from CeibalJAM_Lib.JAMButton import JAMLabel

class JAMatrix():
	def __init__(self, ventana):
		self.ventana = ventana		# la ventana
		self.widgets = None		# grupo de terrones
		self.interval = 0		# intervalo para agregar terrones
		self.reloj = None		# pygame.time
		self.imagen = None		# el fondo
		self.etiqueta = None		# el mensaje sobre lo que se está cargando
		self.posicion_label = None	# la posicion de la etiqueta para cambiar el mensaje

	def Run(self):
		pygame.display.set_caption("JAMatrix (Versión 1) - CeibalJAM! - Uruguay - 2010")
		pygame.mouse.set_visible(False)
		self.reloj.tick(35)
		if self.interval == 10:
			self.genera_terrones()
			self.interval = 0
		cambios=[]
		self.widgets.clear(self.ventana, self.imagen)
		self.widgets.update()
		cambios.extend ( self.widgets.draw(self.ventana) )
		pygame.display.update(cambios)
		pygame.time.wait(1)
		self.interval += 1

	def descarga_todo(self):
		self.widgets = None
		self.interval = 0
		self.reloj = None
		self.imagen = None
		self.etiqueta = None
		self.posicion_label = None

	def setup(self):
		pygame.display.set_mode(RESOLUCION_MONITOR , 0, 0) # para que quede negra la pantalla
		if not self.widgets: self.widgets = pygame.sprite.OrderedUpdates()
		if not self.reloj: self.reloj = pygame.time.Clock()
		if not self.imagen: self.imagen = self.get_imagen(color=(0,0,0,1), tamanio=RESOLUCION_MONITOR) # superficie
		if not self.etiqueta: self.etiqueta = JAMLabel ( imagen=None , texto="Cargando . . .", tamanio_de_letra=50, color=(255,255,255,1))
		if not self.posicion_label: self.posicion_label = RESOLUCION_MONITOR[0]/2 - self.etiqueta.rect.w/2, RESOLUCION_MONITOR[1]/2 - self.etiqueta.rect.h/2
		self.etiqueta.set_posicion(self.posicion_label)
		if not self.etiqueta in self.widgets.sprites(): self.widgets.add(self.etiqueta)

	def get_imagen(self, color=(100,100,100,1), tamanio=(800,600)):
		superficie = pygame.Surface( tamanio, flags=HWSURFACE )
		superficie.fill(color)
		return superficie

	def genera_terrones(self):
		x = random.randrange(0, 1190, 10)
		terron = Terron()
		terron.rect.x, terron.rect.y = (x,-50)
		self.widgets.add(terron)

class Terron(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.imagen1 = pygame.image.load(LOGO_JAM)
		self.image = self.imagen1
		self.rect = self.image.get_rect()
		self.cuenta = 0
	def update(self):
		self.rect.y += 4
		if self.rect.y > 900:
			self.kill()

