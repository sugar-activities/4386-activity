#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Bichos_Cantores_Main.py por:
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
IMAGENES = os.getcwd() + "/Bichos_Cantores/Imagenes/"
CANTOS = os.getcwd() + "/Bichos_Cantores/Sonidos/"
# Sonidos de Insectos: http://mushinone.cool.ne.jp/English/ENGitiran.htm

import CeibalJAM_Lib
from CeibalJAM_Lib.JAMFrame import JAMFrame
from CeibalJAM_Lib.JAMButton import JAMButton, JAMLabel
from CeibalJAM_Lib.JAMDialog import JAMDialog

class Bichos_Cantores_Main():
# Subprograma independiente Crustaceos
	def __init__(self, menu_principal):
		self.menu_principal = menu_principal 		# para volver al menú cuando el usuario salga
		self.ventana = None
		self.reloj = None
		self.fondo = None
		self.Bichos = None
		self.nivel = None
		self.mensajes = None
		self.dialog_cerrar = None
		self.dialog_limite = None

	def precarga(self, JAMatrix):
	# en lugar de llamar a run, se hace precarga con presentacion JAMatrix
		JAMatrix.setup()
		self.setup()
		thread1 = threading.Thread( target=self.Bichos.setup )
		thread1.start()
		while not self.Bichos.carga:
		# mientras esté corriendo el hilo se dibuja JAMatrix
			JAMatrix.Run()
		JAMatrix.descarga_todo()
		pygame.time.wait(3)
		gc.collect()		
		self.Run() # Se ejecuta el juego

	def descarga_todo(self):
		self.reloj = None
		self.fondo = None
		self.Bichos = None
		self.nivel = None
		self.mensajes = None
		self.dialog_cerrar = None
		self.dialog_limite = None
		self.ventana = None

	def Run(self):
	# este juego
		pygame.display.set_caption("Bichos Cantores (Versión 1) - CeibalJAM! - Uruguay - 2010")
		pygame.mouse.set_visible(True)
		self.ventana.blit(self.fondo, (0,0))
		self.Bichos.draw(self.ventana)
		pygame.display.update()

		self.nivel = "Bichos"
		while self.nivel == "Bichos":
		# Corre menú inicial
			self.reloj.tick(35)

			if list(self.mensajes):
			# Si hay un mensaje, se pausa el juego
				self.pause_game_mensajes()

			cambios=[]
			self.Bichos.clear(self.ventana, self.fondo)
			self.Bichos.update()
			cambios.extend ( self.Bichos.draw(self.ventana) )
			self.handle_event()
			pygame.display.update(cambios)
			pygame.time.wait(2)

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

	def selecciona_mensaje_limite(self):
		pygame.event.clear()
		self.deselecciona_mensajes()
		self.mensajes = self.dialog_limite

	def setup(self):
		if not self.ventana: self.ventana = self.menu_principal.ventana
		pygame.event.set_blocked([JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP, JOYBUTTONDOWN,
					KEYUP, VIDEORESIZE, VIDEOEXPOSE, USEREVENT, QUIT, ACTIVEEVENT]) # bloqueados
		pygame.event.set_allowed([MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN, KEYDOWN]) # permitidos
		pygame.mouse.set_visible(True)

		if not self.Bichos: self.Bichos = Bichos_Cantores(self)
		#if not self.ventana: self.ventana = pygame.display.get_surface() # la ventana del juego
		if not self.reloj: self.reloj = pygame.time.Clock()
		if not self.fondo: self.fondo = self.get_fondo()
		if not self.mensajes: self.mensajes = pygame.sprite.OrderedUpdates()

		if not self.dialog_cerrar:
			self.dialog_cerrar = JAMDialog(mensaje="¿Deseas Salir?", resolucion_monitor=RESOLUCION_MONITOR)
			self.dialog_cerrar.boton_aceptar.connect(callback=self.salir, sonido_select=None)
			self.dialog_cerrar.boton_cancelar.connect(callback=self.deselecciona_mensajes, sonido_select=None)

		if not self.dialog_limite:
			self.dialog_limite = JAMDialog(mensaje="No se puede reproducir más de 8 canciones simultáneas.", resolucion_monitor=RESOLUCION_MONITOR)
			self.dialog_limite.boton_aceptar.connect(callback=self.deselecciona_mensajes, sonido_select=None)
			self.dialog_limite.boton_cancelar.kill()

		# Sonido
		if not pygame.mixer.get_init():
			pygame.mixer.init(44100, -16, 2, 2048)
		pygame.mixer.music.set_volume(1.0)
		
	def get_fondo(self, color=(100,100,100,1), tamanio=RESOLUCION_MONITOR):
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
		self.Bichos.detiene_cantos()
		if pygame.mixer.music.get_busy():
			pygame.mixer.music.stop()
		self.deselecciona_mensajes()
		self.descarga_todo()
		return self.menu_principal.Run()	

class Bichos_Cantores(pygame.sprite.OrderedUpdates):
		def __init__(self, juego):
			pygame.sprite.OrderedUpdates.__init__(self)
			self.juego = juego
			self.botones = {}
			self.carga = False

		def setup(self):
			if not self.carga:
				self.get_bichos_cantores()
				self.carga = True

		def get_bichos_cantores(self):
		# carga las imágenes
			for imagen in os.listdir(IMAGENES):
				boton = JAMButton(imagen=IMAGENES + imagen, texto=None, tamanio_panel=(190, 180), grosor_borde=0)
				self.add(boton)
				jam_label = JAMLabel(imagen=None, texto="Cantando . . .", tamanio_de_letra=25, color=(255,0,0,1))
				direccion = str(imagen.split(".")[0])+".ogg"
				self.botones[boton] = [direccion, jam_label, False, direccion]
				boton.connect(callback=self.play_canto, sonido_select=None)
			x = 0
			y = 0
			contador = 0
			for boton in self:
				boton.set_posicion(punto=(x,y))
				x += 200
				contador += 1

				if contador == 6:
					x = 0
					y += boton.rect.h
					contador = 0

		def play_canto(self):
		# carga y reproduce los sonidos
			posicion = pygame.mouse.get_pos()
			for boton in self.botones.keys():
				if boton.rect.collidepoint(posicion):
					pygame.event.clear()
					if self.botones[boton][2] == False:
					# si no se está reproduciendo, se reproduce
						if self.verifica_cantos() >= 8:
						# más de 8 simultáneos no aguanta la xo.
							self.juego.selecciona_mensaje_limite()
							break

						if type(self.botones[boton][0]) == str:
						# si no se ha cargado
							self.botones[boton][0] = pygame.mixer.Sound(CANTOS + self.botones[boton][0])

						self.botones[boton][0].play(-1)
						posicion = (boton.rect.x+5, boton.rect.y+5)
						# etiqueta
						self.botones[boton][1].set_posicion(posicion)
						self.add(self.botones[boton][1])
						self.botones[boton][2] = True
						return
					else:
					# si se está reproduciendo, se detiene
						self.botones[boton][0].stop()
						self.botones[boton][0] = self.botones[boton][3] # descarga el sonido xque la xo no aguanta
						self.botones[boton][1].kill()
						self.botones[boton][2] = False
						return
					return

		def detiene_cantos(self):
			for boton in self.botones.keys():
				if self.botones[boton][2] == True:
					self.botones[boton][0].stop()
					self.botones[boton][0] = self.botones[boton][3] # descarga el sonido xque la xo no aguanta
					self.botones[boton][1].kill()
					self.botones[boton][2] = False

		def verifica_cantos(self):
		# cuenta cuantos sonidos se están reproduciendo porque la xo no soporta mas de 15 simultaneos.
			cantos = 0
			for boton in self.botones.keys():
				if self.botones[boton][2]: cantos += 1
			return cantos
