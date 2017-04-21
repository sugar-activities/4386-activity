#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Ficha_Bicho.py por:
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

import CeibalJAM_Lib
from CeibalJAM_Lib.JAMFrame import JAMFrame
from CeibalJAM_Lib.JAMButton import JAMButton, JAMLabel

import Variables_Globales as VG
MAGENTA  = (255, 0, 255)

class Ficha_Bicho(pygame.sprite.OrderedUpdates):
	def __init__(self):
		pygame.sprite.OrderedUpdates.__init__(self)

		self.bicho = None

		x = 10
		y = 50
		self.separador = 5

		self.label_tiempo = JAMLabel(imagen=None, texto="Años: 0 Dias: 0 Horas: 0", tamanio_de_letra=30)
		posicion = (x,y)
		self.label_tiempo.set_posicion((posicion))
		self.add(self.label_tiempo)

		y += self.label_tiempo.rect.h + self.separador
		self.label_hambre = JAMLabel(imagen=None, texto="Nivel de Apetito: ", tamanio_de_letra=25)
		posicion = (x,y)
		self.label_hambre.set_posicion((posicion))
		self.add(self.label_hambre)

		y += self.label_hambre.rect.h + self.separador
		self.label_sed = JAMLabel(imagen=None, texto="Nivel de Sed: ", tamanio_de_letra=25)
		posicion = (x,y)
		self.label_sed.set_posicion((posicion))
		self.add(self.label_sed)

		self.barra_nutricion = Barra()
		self.barra_nutricion.rect.x = self.label_tiempo.rect.x + 170
		self.barra_nutricion.rect.centery = self.label_hambre.rect.centery
		self.add(self.barra_nutricion)

		self.barra_hidratacion = Barra()
		self.barra_hidratacion.rect.x = self.label_tiempo.rect.x + 170
		self.barra_hidratacion.rect.centery = self.label_sed.rect.centery
		self.add(self.barra_hidratacion)

		self.circulo = Circulo((60,60))
		self.add(self.circulo)

	def set_bicho(self, bicho):
		tamanio = (bicho.rect.w, bicho.rect.h)
		self.circulo.image = pygame.transform.scale(self.circulo.imagen_original, (tamanio))
		self.bicho = bicho

	def update(self):
		if self.bicho:
			self.actualizar_datos()

	def actualizar_datos(self):
		x = 10
		y = 50

		edad = "Dias: %s Horas: %s" % (self.bicho.dias, self.bicho.horas)
		if edad != self.label_tiempo.valor_texto:
			self.label_tiempo.set_text(texto=edad)
			posicion = (x,y)
			self.label_tiempo.set_posicion((posicion))

		y += self.label_tiempo.rect.h + self.separador
		nutricion = "Nutrición: %s" % (self.bicho.hambre)
		if nutricion != self.label_hambre.valor_texto:
			self.label_hambre.set_text(texto=nutricion)
			posicion = (x,y)
			self.label_hambre.set_posicion((posicion))
			self.barra_nutricion.set_valor(self.bicho.hambre)

		y += self.label_hambre.rect.h + self.separador
		hidratacion = "Hidratación: %s" % (self.bicho.sed)
		if hidratacion != self.label_sed.valor_texto:
			self.label_sed.set_text(texto=hidratacion)
			posicion = (x,y)
			self.label_sed.set_posicion((posicion))	
			self.barra_hidratacion.set_valor(self.bicho.sed)	

		self.circulo.rect.center = self.bicho.rect.center

class Barra(pygame.sprite.Sprite):
# Barra de Progreso
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.imagen_original = self.get_barra()
		self.image = self.imagen_original.copy()
		self.rect = self.image.get_rect()
		self.ultimo_valor = 0

	def set_valor(self, valor):
	# actualiza el progreso en la barra
		if valor == self.ultimo_valor: return
		if valor >= 0 and valor <= 100:
			verde = (0,255,0,1)
			amarillo = (255,255,0,1)
			rojo = (255,0,0,1)
			if valor <= 33:
				color = rojo
			if valor > 33 and valor <= 66:
				color = amarillo
			if valor > 66:
				color = verde

			rectangulo = (1,1,valor,8)
			self.image = self.imagen_original.copy()
			pygame.draw.rect(self.image, color, rectangulo, 0)
		elif valor > 100:
			verde = (0,255,0,1)
			rectangulo = (1,1,100,8)
			self.image = self.imagen_original.copy()
			pygame.draw.rect(self.image, verde, rectangulo, 0)
		else:
			self.image = self.imagen_original.copy()
		self.ultimo_valor =  valor

	def get_barra(self):
	# genera una superficie
		superficie = pygame.Surface( (100, 10), flags=HWSURFACE )
		superficie.fill(MAGENTA)
		# El fondo
		superficie.set_colorkey(MAGENTA, pygame.RLEACCEL)
		rectangulo = superficie.get_rect()
		# El borde
		pygame.draw.rect(superficie, (255,255,0,1), rectangulo, 1)
		return superficie

class Circulo(pygame.sprite.Sprite):
# Circulo para seleccion de bichos
	def __init__(self, tamanio):
		pygame.sprite.Sprite.__init__(self)

		self.imagen_original = self.get_surface(tamanio)
		self.image = self.imagen_original.copy()
		self.rect = self.image.get_rect()

	def get_surface(self, tamanio_panel):
	# genera una superficie
		superficie = pygame.Surface( tamanio_panel, flags=HWSURFACE )
		superficie.fill(MAGENTA)
		superficie.set_colorkey(MAGENTA, pygame.RLEACCEL)
		rectangulo = superficie.get_rect()
		pygame.draw.circle(superficie, (255,255,0,1), (30,30), 28, 5)
		return superficie

