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

import Variables_Globales as VG

INDICE_ROTACION = 25

class Bicho(pygame.sprite.Sprite):
# Las Cucarachas. Recibe alimento en escenario para poder encontrarlo.
	def __init__(self, juego_main):

		pygame.sprite.Sprite.__init__(self)
		
		self.juego = juego_main
		self.alimento_en_escenario = self.juego.alimento
		self.agua_en_escenario = self.juego.agua

		self.velocidad = 8

		self.anios = 0
		self.dias = 0
		self.horas = 0

		self.hambre = 0
		self.sed = 0

		self.sonido_bicho = self.juego.sonido_bicho
		self.area_visible =  self.juego.area_visible

		random.seed()
		self.tipo = random.choice(self.juego.imagenes_bicho)
		self.imagen_original = self.get_imagen_original()
		if self.juego.imagenes_bicho.index(self.tipo) == 2 or self.juego.imagenes_bicho.index(self.tipo) == 3:
			self.sexo = "F"
		else:
			self.sexo = "M"

		self.image = self.imagen_original.copy()
		self.rect = self.image.get_rect()

		acciones = ["camina", "gira", "quieto"]
		self.accion = random.choice(acciones)

		self.sent = 0
		self.angulo = 0

		self.contador = 0

		self.escalas_mudas = VG.ESCALASMUDAS
		self.dias_mudas = VG.DIASMUDAS
		self.control_mudas = self.dias_mudas[0] 

		self.x, self.y = (0,0)
		self.dx = 0
		self.dy = 0
		self.posicionar_al_azar()
		
		self.dias_repro = VG.DIASREPRO
		self.control_repro = self.dias_repro[0]

	# Tamaños
	def get_imagen_original(self):
		return pygame.transform.scale(self.tipo, (60,50))

	def set_muda(self, escala=(63,50)):
	# cuando crece, muda el exoesqueleto
		self.imagen_original = pygame.transform.scale(self.tipo, escala)
		self.image = pygame.transform.rotate(self.imagen_original, -self.angulo)
		x,y = self.rect.x, self.rect.y
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = x, y
		self.juego.event_muda(posicion=(self.rect.x, self.rect.y), tamanio=escala)

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

	def play_sonido_bicho(self):
		self.sonido_bicho.play()

	def set_tiempo_de_vida(self):
		self.horas += 1
		if self.horas == 24:
			self.dias += 1
			self.horas = 0

		if self.dias == 365:
			self.anios += 1
			self.dias = 0
	
	def update(self):
	# Actualiza el sprite
		# determinar condiciones de vida
		if self.hambre <= VG.LIMITEHAMBRE or self.sed <= VG.LIMITESED or self.dias >= VG.LIMITEVIDA:
			comportamiento = "muere"
		else:
			comportamiento = "vive"

		# Si está viva		
		if comportamiento == "vive":
			# Mudas de exoesqueleto
			if self.dias == self.control_mudas and self.horas == 0:

				indice = self.dias_mudas.index(self.dias)
				self.set_muda(escala=self.escalas_mudas[indice])
				self.velocidad += int(self.velocidad/3)
				
				if indice+1 < len(self.dias_mudas):
					self.control_mudas = self.dias_mudas[indice+1]
				else:
					self.control_mudas = self.dias_mudas[0]

			# Reproducción
			if self.dias == self.control_repro and self.horas == 0 and self.sexo == "F":
				indice = self.dias_repro.index(self.dias)
	
				if indice+1 < len(self.dias_repro):
					self.control_repro = self.dias_repro[indice+1]
				else:
					self.control_repro = self.dias_repro[0]

				if self.juego.machos:
					self.juego.event_reproduccion(posicion=(self.rect.centerx, self.rect.centery))

			comportamiento = "normal"

		elif comportamiento == "muere":
		# se muere
			self.juego.event_morir(posicion=(self.rect.centerx, self.rect.centery), dias=self.dias)
			self.kill()
			return

		if not bool(self.agua_en_escenario.sprites()) or self.sed >= 100:
		# Si no hay alimento en el escenario o el bicho no tiene sed
			comportamiento = "normal"
		elif bool(self.agua_en_escenario.sprites()) and self.sed < 100:
		# si hay alimento y tiene hambre
			comportamiento = "buscar agua"

		if comportamiento == "normal":
			if not bool(self.alimento_en_escenario.sprites()) or self.hambre >= 100:
			# Si no hay alimento en el escenario o el bicho no tiene hambre
				comportamiento = "normal"
			elif bool(self.alimento_en_escenario.sprites()) and self.hambre < 100:
			# si hay alimento y tiene hambre
				comportamiento = "buscar comida"

		self.comportamiento(comportamiento)

	def comportamiento(self, comportamiento):
	# decide el tipo de comportamiento según necesidades
		if comportamiento == "normal":
			if self.contador == 30:
			# cada 30 pasadas, cambia acción
				acciones = ["camina", "gira", "quieto"]
				random.seed()
				self.accion = random.choice(acciones)
				self.contador = 0
			self.contador += 1
			self.decide()
		elif comportamiento == "buscar comida":
			self.alimentarse()
		elif comportamiento == "buscar agua":
			self.beber()
		else:
			print "comportamiento sin tratar: ", comportamiento

	def beber(self):
	# Busca el alimento, cuando lo encuentra se alimenta
		agua = self.agua_en_escenario.sprites()[0]

		if self.rect.colliderect(agua.rect):
		# si ya llegamos al agua no nos movemos
			self.accion = "quieto"

			if self.contador >= 30:
			# cada treinta pasadas bebe
				self.sed += VG.RINDEAGUA
				agua.cantidad -= VG.CONSUMOAGUA
				self.contador = 0
				if self.sed >= 100: self.sed = 150
				if agua.cantidad <= 0:
					agua.kill()
					self.agua_en_escenario.empty()
			self.contador += 1
			return

		else:
		# Si no hemos llegado al agua
			posicion_agua = agua.rect.center

			# calcular la distancia al alimento
			distancia_x = posicion_agua[0] - self.rect.x
			distancia_y = posicion_agua[1] - self.rect.y

			self.dx, self.dy = self.get_vector(self.angulo)

			# calcular distancia si me muevo en el sentido actual
			futura_posicion_x = self.rect.x + self.dx
			futura_posicion_y = self.rect.y + self.dy

			# Verificar si al moverme me acerco o me alejo del alimento
			if ((futura_posicion_x - self.rect.x) <= distancia_x and (futura_posicion_y - self.rect.y) <= distancia_y):
			# Si me acerco, camino
				self.accion = "camina"
				self.decide()
			else:
			# si no me acerco, giro
				self.accion = "gira"
				self.decide()

	def alimentarse(self):
	# Busca el alimento, cuando lo encuentra se alimenta
		alimento = self.alimento_en_escenario.sprites()[0]

		if self.rect.colliderect(alimento.rect):
		# si ya llegamos al alimento no nos movemos
			self.accion = "quieto"

			if self.contador >= 30:
			# cada treinta pasadas come
				self.hambre += VG.RINDEALIMENTO
				alimento.cantidad -= VG.CONSUMOALIMENTO
				self.contador = 0
				if self.hambre >= 100: self.hambre = 150
				if alimento.cantidad <= 0:
				# el que come de último limpia :P
					alimento.kill()
					self.alimento_en_escenario.empty()
			self.contador += 1
			return

		else:
		# Si no hemos llegado al alimento
			posicion_alimento = alimento.rect.center

			# calcular la distancia al alimento
			distancia_x = posicion_alimento[0] - self.rect.x
			distancia_y = posicion_alimento[1] - self.rect.y

			self.dx, self.dy = self.get_vector(self.angulo)

			# calcular distancia si me muevo en el sentido actual
			futura_posicion_x = self.rect.x + self.dx
			futura_posicion_y = self.rect.y + self.dy

			# Verificar si al moverme me acerco o me alejo del alimento
			if ((futura_posicion_x - self.rect.x) <= distancia_x and (futura_posicion_y - self.rect.y) <= distancia_y):
			# Si me acerco, camino
				self.accion = "camina"
				self.decide()
			else:
			# si no me acerco, giro
				self.accion = "gira"
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
				self.accion = "quieto"
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
