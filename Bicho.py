#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Bicho.py por:
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

import random
from math import sin, cos, radians

INDICE_ROTACION = 25

class Bicho(pygame.sprite.Sprite):
	def __init__(self, juego_main):
		pygame.sprite.Sprite.__init__(self)
		
		self.juego = juego_main
		self.velocidad = 8
		self.area_visible =  self.juego.area_visible
		random.seed()
		self.tipo = random.choice(self.juego.imagenes_bicho)
		self.imagen_original = self.tipo.copy()#self.get_imagen_original()
		self.image = self.imagen_original.copy()
		self.rect = self.image.get_rect()
		acciones = ["camina", "gira"]# "quieto"]
		self.accion = random.choice(acciones)

		self.sent = 0
		self.angulo = 0

		self.contador = 0

		self.x, self.y = (0,0)
		self.dx = 0
		self.dy = 0
		self.posicionar_al_azar()

	def get_imagen_original(self):
		return pygame.transform.scale(self.tipo, (60,50))

	def posicionar_al_azar(self):
	# elige una posicion inicial al azar para el bicho
		lista_de_rectangulos = []
		for bicho in list(self.juego.Bichos):
		# los rectangulos de los otros bichos
			rectangulo = (bicho.rect.x, bicho.rect.y, bicho.rect.w, bicho.rect.h)
			lista_de_rectangulos.append(rectangulo)

		random.seed()
		x = random.randrange(self.area_visible[0]+10, self.area_visible[0]+self.area_visible[2]-10, 1)
		y = random.randrange(self.area_visible[1]+10, self.area_visible[1]+self.area_visible[3]-10, 1)
		self.x, self.y = (x,y)
		self.dx = 0
		self.dy = 0
		self.actualizar_posicion()

		while self.rect.collidelist(lista_de_rectangulos) != -1:
			x = random.randrange(self.area_visible[0]+10, self.area_visible[0]+self.area_visible[2]-10, 1)
			y = random.randrange(self.area_visible[1]+10, self.area_visible[1]+self.area_visible[3]-10, 1)
			self.x, self.y = (x,y)
			self.dx = 0
			self.dy = 0
			self.actualizar_posicion()
	
	def update(self):
	# Actualiza el sprite
		if self.rect.colliderect(self.area_visible):
			self.comportamiento()
		else:
			self.kill()
			return

	def comportamiento(self):
	# decide el tipo de comportamiento según necesidades
		if self.contador == 30:
		# cada 30 pasadas, cambia acción
			acciones = ["camina", "gira"]#, "quieto"]
			random.seed()
			self.accion = random.choice(acciones)
			self.contador = 0
		self.contador += 1
		self.decide()

	def decide(self):
	# gira, camina o se queda quieto
		if self.accion == "gira":
			self.gira()
			self.accion = "camina"

		if self.accion == "camina":
			self.dx, self.dy = self.get_vector(self.angulo)
			self.actualizar_posicion()

		if self.accion == "quieto":
			pass

	def gira(self, sent=0):
	# la cuca gira
		random.seed()
		if sent == 0: self.sent = random.randrange(1, 3, 1)

		if self.sent == 1:
		# hacia la izquierda
			self.angulo -= int(0.7 * INDICE_ROTACION)
		elif self.sent == 2:
		# hacia la derecha
			self.angulo += int(0.7 * INDICE_ROTACION)

	    	self.image = pygame.transform.rotate(self.imagen_original, -self.angulo)
		
	def actualizar_posicion(self):
	# La cuca se mueve
		x = self.x + self.dx
		y = self.y + self.dy
		posicion = (x,y)
		if self.area_visible.collidepoint(posicion):
		# Si no me salgo del area permitida
			if not self.verificar_colision_en_grupo(posicion):
			# Si no caminaré sobre otra cucaracha
				self.x += self.dx
				self.y += self.dy
				self.rect.centerx = int(self.x)
				self.rect.centery = int(self.y)
			else:
				self.gira(sent=self.sent)
				#self.accion = "quieto"
		else:
			self.gira(sent=self.sent)

	def verificar_colision_en_grupo(self, posicion):
	# evita que caminen unas sobre otras
		grupo = self.groups()
		for group in grupo:
			for cuca in group.sprites():
				if cuca != self:
					if cuca.rect.collidepoint(posicion):
						return True
		return False

	def get_vector(self, angulo):
	# Recibe un ángulo que da orientación. Devuelve el incremento de puntos x,y
		x = int(cos(radians(angulo)) * self.velocidad)
		y = int(sin(radians(angulo)) * self.velocidad)
		return x,y
