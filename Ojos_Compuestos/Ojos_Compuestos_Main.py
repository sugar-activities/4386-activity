#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Ojos_Compuestos_Main.py por:
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

import sys, os, threading, random

RESOLUCION_MONITOR = (1200,900)
IMAGENES = os.getcwd() + "/Ojos_Compuestos/Imagenes/"
#CANTOS = os.getcwd() + "/Bichos_Cantores/Sonidos/"

SIGUIENTE = os.getcwd() + "/Ojos_Compuestos/Iconos/siguiente.png"
ANTERIOR = os.getcwd() + "/Ojos_Compuestos/Iconos/anterior.png"
PLAY = os.getcwd() + "/Ojos_Compuestos/Iconos/play.png"
CERRAR = os.getcwd() + "/Ojos_Compuestos/Iconos/cerrar.png"
MAGENTA  = (255, 0, 255)

import CeibalJAM_Lib
from CeibalJAM_Lib.JAMFrame import JAMFrame
from CeibalJAM_Lib.JAMButton import JAMButton, JAMLabel
from CeibalJAM_Lib.JAMDialog import JAMDialog

class Ojos_Compuestos_Main():
# Subprograma independiente Crustaceos
	def __init__(self, menu_principal):
		self.menu_principal = menu_principal 		# para volver al menú cuando el usuario salga
		self.ventana = None
		self.reloj = None
		self.fondo = None

		self.imagen = None
		self.barra_de_reproduccion = None
		self.widget_imagen = None

		self.nivel = None
		self.carga = None

		self.mensajes = None
		self.dialog_cerrar = None

	def precarga(self, JAMatrix):
	# en lugar de llamar a run, se hace precarga con presentacion JAMatrix
		JAMatrix.setup()
		thread = threading.Thread( target=self.setup )
		thread.start()
		while not self.carga:
		# mientras esté corriendo el hilo se dibuja JAMatrix
			JAMatrix.Run()
		JAMatrix.descarga_todo()
		pygame.time.wait(3)
		gc.collect()		
		self.Run() # Se ejecuta el juego

	def descarga_todo(self):
		self.ventana = None
		self.reloj = None
		self.fondo = None

		self.imagen = None
		self.barra_de_reproduccion = None
		self.widget_imagen = None

		self.nivel = None
		self.carga = None

		self.mensajes = None
		self.dialog_cerrar = None

	def Run(self):
	# este juego
		pygame.display.set_caption("Ojos Compuestos (Versión 1) - CeibalJAM! - Uruguay - 2010")
		pygame.mouse.set_visible(True)
		self.ventana.blit(self.fondo, (0,0))
		self.widget_imagen.draw(self.ventana)
		self.barra_de_reproduccion.draw(self.ventana)
		pygame.display.update()

		self.nivel = "Imagenes"
		while self.nivel == "Imagenes":
		# Corre menú inicial
			self.reloj.tick(35)

			if list(self.mensajes):
			# Si hay un mensaje, se pausa el juego
				self.pause_game_mensajes()

			evento = None
			if not self.imagen.presentacion:
			# si está en modo presentacion debe actualizarse, de lo contrario, espera un evento
				evento = pygame.event.wait() 	# detiene y espera un evento
				pygame.event.post(evento)	# wait en evento borra de la cola el evento retornado, por eso hay que republicarlo

			if evento or self.imagen.presentacion:	# si hay un evento o está en modo presentacion	
				cambios=[]
				self.widget_imagen.clear(self.ventana, self.fondo)
				self.barra_de_reproduccion.clear(self.ventana, self.fondo)
				self.widget_imagen.update()
				self.barra_de_reproduccion.update()
				cambios.extend ( self.widget_imagen.draw(self.ventana) )
				cambios.extend ( self.barra_de_reproduccion.draw(self.ventana) )
				self.handle_event()
				pygame.display.update(cambios)
				#pygame.time.wait(2)

	def pause_game_mensajes(self):
		while list(self.mensajes):
			self.reloj.tick(35)
			cambios=[]
			self.mensajes.clear(self.ventana, self.fondo)
			self.mensajes.update()
			cambios.extend ( self.mensajes.draw(self.ventana) )
			self.handle_event()
			pygame.display.update(cambios)

	def deselecciona_mensajes(self):
		self.mensajes.clear(self.ventana, self.fondo)
		pygame.display.update()
		self.mensajes = pygame.sprite.OrderedUpdates()

	def selecciona_mensaje_salir(self):
		pygame.event.clear()
		self.deselecciona_mensajes()
		self.mensajes = self.dialog_cerrar

	def setup(self):
		if not self.ventana: self.ventana = self.menu_principal.ventana
		pygame.event.set_blocked([JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP, JOYBUTTONDOWN,
					KEYUP, VIDEORESIZE, VIDEOEXPOSE, USEREVENT, QUIT, ACTIVEEVENT]) # bloqueados
		pygame.event.set_allowed([MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN, KEYDOWN]) # permitidos
		pygame.mouse.set_visible(True)

		if not self.imagen:
			self.imagen = Imagen(self)
			self.widget_imagen = pygame.sprite.OrderedUpdates()
			self.widget_imagen.add (self.imagen)

		# if not self.barra_de_reproduccion: self.barra_de_reproduccion = None
		if not self.reloj: self.reloj = pygame.time.Clock()
		if not self.fondo: self.fondo = self.get_fondo()
		if not self.mensajes: self.mensajes = pygame.sprite.OrderedUpdates()
		if not self.barra_de_reproduccion:
			self.barra_de_reproduccion = Barra_de_Reproduccion()
			self.barra_de_reproduccion.boton_anterior.connect(callback=self.imagen.previous, sonido_select=None)
			self.barra_de_reproduccion.boton_play.connect(callback=self.imagen.set_presentacion, sonido_select=None)
			self.barra_de_reproduccion.boton_siguiente.connect(callback=self.imagen.next, sonido_select=None)
			self.barra_de_reproduccion.boton_cerrar.connect(callback=self.selecciona_mensaje_salir, sonido_select=None)
		if not self.dialog_cerrar:
			self.dialog_cerrar = JAMDialog(mensaje="¿Deseas Salir?", resolucion_monitor=RESOLUCION_MONITOR)
			self.dialog_cerrar.boton_aceptar.connect(callback=self.salir, sonido_select=None)
			self.dialog_cerrar.boton_cancelar.connect(callback=self.deselecciona_mensajes, sonido_select=None)

		''' # Sonido
		if not pygame.mixer.get_init():
			pygame.mixer.init(44100, -16, 2, 2048)
		pygame.mixer.music.set_volume(1.0)'''
		self.carga = True

	def get_fondo(self, color=(0,0,0,1), tamanio=RESOLUCION_MONITOR):
	# superficie gris simulando ventana gtk
		superficie = pygame.Surface( tamanio, flags=HWSURFACE )
		superficie.fill(color)
		return superficie

	def handle_event(self):
	# Eventos del Teclado
		for event in pygame.event.get():
			teclas = pygame.key.get_pressed()
			if teclas[pygame.K_ESCAPE]:
				self.selecciona_mensaje_salir()
				pygame.event.clear()
				return
		pygame.event.clear()

	def salir(self):
		pygame.event.clear()
		self.deselecciona_mensajes()
		self.descarga_todo()
		return self.menu_principal.Run()	


class Imagen(pygame.sprite.Sprite):
		def __init__(self, juego):
			pygame.sprite.Sprite.__init__(self)
			self.juego = juego
			self.indice = 0
			#self.imagen = None
			#self.rect = None
			self.intervalo = 0
			self.presentacion = False
			self.imagenes = []
			self.get_imagenes()

		def get_imagenes(self):
		# carga las imágenes
			self.imagenes = []
			for imagen in os.listdir(IMAGENES):
				#self.imagenes.append(pygame.transform.scale(pygame.image.load(IMAGENES+imagen), (1200,900)).convert_alpha()
				self.imagenes.append(IMAGENES+imagen)
			#self.image = self.imagenes[self.indice]
			self.image = pygame.transform.scale(pygame.image.load(self.imagenes[self.indice]), (1200,900)).convert_alpha()
			self.rect = self.image.get_rect()

		def next(self):
			if len(self.imagenes)-1 > self.indice:
				self.indice += 1
			else:
				self.indice = 0
			#self.image = self.imagenes[self.indice]
			self.image = pygame.transform.scale(pygame.image.load(self.imagenes[self.indice]), (1200,900)).convert_alpha()

		def previous(self):
			if self.indice >= 1:
				self.indice -= 1
			else:
				self.indice = len(self.imagenes)-1
			#self.image = self.imagenes[self.indice]
			self.image = pygame.transform.scale(pygame.image.load(self.imagenes[self.indice]), (1200,900)).convert_alpha()

		def set_presentacion(self):
			if self.presentacion:
				self.presentacion = False
			else:
				self.presentacion = True
				self.next()

		def update(self):
			if self.presentacion:
				if self.intervalo == 20:
					self.next()
					self.intervalo = 0
				else:
					self.intervalo += 1

class Barra_de_Reproduccion(pygame.sprite.OrderedUpdates):
	def __init__(self):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.separador = 10

		# construye los botones de navegación
		self.boton_anterior = JAMButton(texto=None, imagen=ANTERIOR)
		self.boton_play = JAMButton(texto=None, imagen=PLAY)
		self.boton_siguiente = JAMButton(texto=None, imagen=SIGUIENTE)
		self.boton_cerrar = JAMButton(texto=None, imagen=CERRAR)

		self.ancho = self.separador
		self.ancho += self.boton_anterior.rect.w + self.separador + self.boton_play.rect.w + self.separador
		self.ancho += self.boton_siguiente.rect.w + self.separador + self.boton_cerrar.rect.w + self.separador
		self.alto = self.separador + self.boton_anterior.rect.h + self.separador

		self.contenedor = pygame.sprite.Sprite()
		superficie = pygame.Surface( (self.ancho, self.alto), flags=HWSURFACE )
		superficie.fill(MAGENTA)
		superficie.set_colorkey(MAGENTA, pygame.RLEACCEL)		
		self.contenedor.image = superficie
		self.contenedor.rect = self.contenedor.image.get_rect()

		x, y = RESOLUCION_MONITOR[0]/2 - self.contenedor.rect.w/2, RESOLUCION_MONITOR[1] - self.separador/2 - self.contenedor.rect.h
		self.contenedor.rect.x = x
		self.contenedor.rect.y = y

		x += self.separador
		y += self.separador
		self.boton_anterior.set_posicion(punto=(x,y))

		x += self.boton_anterior.rect.w + self.separador
		self.boton_play.set_posicion(punto=(x,y))

		x += self.boton_play.rect.w + self.separador
		self.boton_siguiente.set_posicion(punto=(x,y))

		x += self.boton_siguiente.rect.w + self.separador
		self.boton_cerrar.set_posicion(punto=(x,y))

		self.add(self.contenedor)
		self.add(self.boton_anterior)
		self.add(self.boton_play)
		self.add(self.boton_siguiente)
		self.add(self.boton_cerrar)
