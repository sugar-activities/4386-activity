#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Libreta_de_Lectura.py por:
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

import subprocess

import CeibalJAM_Lib
from CeibalJAM_Lib.JAMFrame import JAMFrame
from CeibalJAM_Lib.JAMButton import JAMButton, JAMLabel, JAMBaseButton
import Variables_Globales as VG

class Libreta_de_Lectura(pygame.sprite.OrderedUpdates):
# Libreta para lectura con los botones de navegación

	def __init__(self, lectura):
		pygame.sprite.OrderedUpdates.__init__(self)

		pygame.mixer.init(44100, -16, 2, 512)
		pygame.mixer.music.set_volume(1.0)
		self.sonido_ambiente = None
		self.sonido_select = pygame.mixer.Sound("CeibalJAM_Lib/select.ogg")
		self.motor_de_voz = Motor_de_voz()
		self.posicion_hoja = None
		self.hoja = self.get_hoja()
		self.texto = None
		self.pagina_actual = ""
		self.hoja_impresa = pygame.sprite.Sprite()

		self.lectura = lectura
		self.paginas = []
		self.indice_pagina_actual = 0
		self.set_lectura(self.lectura)

		self.frame = self.get_frame()
		self.boton_anterior, self.boton_leeme, self.boton_siguiente, self.boton_cerrar = self.get_botones_lectura()

		self.add(self.hoja_impresa)
		self.add(self.frame)
		self.add(self.boton_anterior)
		self.add(self.boton_leeme)
		self.add(self.boton_siguiente)
		self.add(self.boton_cerrar)

	def next_pagina(self):
	# navega por las imagenes
		if len(self.paginas)-1 > self.indice_pagina_actual:
			self.indice_pagina_actual += 1
		else:
			self.indice_pagina_actual = 0
		self.hoja_impresa.image = self.paginas[self.indice_pagina_actual]
		self.hoja_impresa.rect = self.hoja_impresa.image.get_rect()
		self.set_posicion(punto=self.posicion_hoja)

	def previous_pagina(self):
	# navega por las imagenes
		if self.indice_pagina_actual > 0:
			self.indice_pagina_actual -= 1
		else:
			self.indice_pagina_actual = len(self.paginas)-1
		self.hoja_impresa.image = self.paginas[self.indice_pagina_actual]
		self.hoja_impresa.rect = self.hoja_impresa.image.get_rect()
		self.set_posicion(punto=self.posicion_hoja)

	def audio_stop(self):
	# detiene los sonidos
		self.sonido_ambiente.stop()

	def play(self, sonido_ambiente, valor):
	# reproduce un sonido
		self.sonido_ambiente = pygame.mixer.Sound(sonido_ambiente)
		self.sonido_ambiente.play(valor)

	def lee(self):
	# lee la pagina actual cuando el usuario hace click en el boton leeme
		if self.sonido_ambiente:
			self.sonido_ambiente.stop()

		pygame.mixer.quit() # necesario en la xo

		textbuffer = ""
		for elem in self.lectura[self.indice_pagina_actual]:
			textbuffer += (" " + elem)
		self.motor_de_voz.lee(textbuffer)

		pygame.mixer.init(44100, -16, 2, 512)
		pygame.mixer.music.set_volume(1.0)

		if self.sonido_ambiente:	
			self.sonido_ambiente.play(-1)

	def set_posicion(self, punto=(0,0)):
	# cambia la posicion de todos los objetos

		# posicion de la hoja impresa
		x, y = punto
		self.hoja_impresa.rect.x, self.hoja_impresa.rect.y = x, y
		self.frame.set_posicion(punto=(x,y))
		self.posicion_hoja = punto

		# Posicion de los botones
		y = self.hoja_impresa.rect.h + y - self.boton_anterior.rect.h - 20
		x = self.hoja_impresa.rect.centerx + 20
		x -= self.boton_leeme.rect.w/2
		self.boton_leeme.set_posicion(punto=(x, y))
		a = x - 20 - self.boton_anterior.rect.w
		self.boton_anterior.set_posicion(punto=(a, y))
		b = x + 20 + self.boton_siguiente.rect.w
		self.boton_siguiente.set_posicion(punto=(b, y))

		x = self.hoja_impresa.rect.x + self.hoja_impresa.rect.w - 10 - self.boton_cerrar.rect.w
		y = self.hoja_impresa.rect.y + 10
		self.boton_cerrar.set_posicion(punto=(x, y))

	def set_lectura(self, lectura):
	# pasas un texto y lo imprime en la hoja
		self.indice_pagina_actual = 0
		self.lectura = lectura
		self.paginas = []
		for pagina in self.lectura:
			hoja_impresa = self.get_hoja_impresa(pagina, self.hoja.copy())
			self.paginas.append(hoja_impresa)

		self.hoja_impresa.image = self.paginas[self.indice_pagina_actual]
		self.hoja_impresa.rect = self.hoja_impresa.image.get_rect()

	def get_hoja(self):
	# superficie de hoja vacía
		fondo = pygame.image.load(VG.FONDO_LIBRO)
		basebutton = JAMBaseButton()
		superficie = basebutton.get_surface(color_relleno=None, color_borde=(0,0,0,1), tamanio_panel=(500,648), grosor_borde=1)
		y = 0
		for x in range(1,19):
			superficie.blit(fondo, (0,y))
			y+=36
		return superficie

	def get_hoja_impresa(self,texto, superficie):
	# devuelve superficie de hoja impresa
		y = 20
		for linea in texto:
			fuente = pygame.font.Font(pygame.font.match_font("Arial", False, False), 26)

			string_to_render = unicode( str(linea).decode("utf-8") )
			imagen_fuente = fuente.render(string_to_render, 1, (0,0,0,1))

			rectangulo_fuente = imagen_fuente.get_rect()
			superficie.blit(imagen_fuente, (80,y))
			y += rectangulo_fuente.h
		return superficie

	def get_frame(self):
	# la etiqueta donde se muestra la imagen
		tamanio =  (self.hoja_impresa.rect.w, self.hoja_impresa.rect.h)
		frame = JAMFrame(color_borde=(0,0,0,1), grosor_borde=3, color_relleno=None, tamanio=tamanio)
		return frame

	def get_botones_lectura(self):
	# construye los botones de navegación
		x, y = 0,0
		boton1 = JAMButton(texto=None, imagen=VG.ANTERIOR)
		boton1.connect(callback=self.previous_pagina, sonido_select=self.sonido_select)
		boton1.set_posicion(punto=(x,y))

		x += 25 + boton1.rect.w
		boton2 = JAMButton(texto=None, imagen=VG.PLAY)
		boton2.connect(callback=self.lee, sonido_select=self.sonido_select)
		boton2.set_posicion(punto=(x,y))

		x += 25 + boton2.rect.w
		boton3 = JAMButton(texto=None, imagen=VG.SIGUIENTE)
		boton3.connect(callback=self.next_pagina, sonido_select=self.sonido_select)
		boton3.set_posicion(punto=(x,y))

		x += 25 + boton2.rect.w
		boton4 = JAMButton(texto=None, imagen=VG.CERRAR)
		boton4.connect(callback=self.cerrar, sonido_select=self.sonido_select)
		x = self.hoja_impresa.rect.x + self.hoja_impresa.rect.w - 10 - boton4.rect.w
		y = self.hoja_impresa.rect.y + 10
		boton4.set_posicion(punto=(x,y))

		return boton1, boton2, boton3, boton4

	def cerrar(self):
	# vacía el grupo
		self.empty()

class Motor_de_voz():
# Lee el texto que le pasen
	def __init__(self):
		pass

	def lee(self, textbuffer):
		subprocess.call(['espeak', "-ves", "-a 200", "-g 5", "-p 10", "--punct=<>", textbuffer])

