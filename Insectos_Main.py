#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Insectos_Main.py por:
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

import CeibalJAM_Lib
from CeibalJAM_Lib.JAMButton import JAMLabel
from CeibalJAM_Lib.JAMElipseButton import JAMElipseButton
from CeibalJAM_Lib.JAMDialog import JAMDialog

from JAMatrix import JAMatrix
from Bicho import Bicho
imagenes_bichos = os.getcwd() + "/Imagenes_Bichos/"

from CucaraSims.CucaraSims import CucaraSims_Main
from Bichos_Cantores.Bichos_Cantores_Main import Bichos_Cantores_Main
from Ojos_Compuestos.Ojos_Compuestos_Main import Ojos_Compuestos_Main

cucarasims_logo = os.getcwd() + "/CucaraSims/CUCARACHA/Imagenes/logo.png"
bichos_cantores_logo = os.getcwd() + "/Bichos_Cantores/Iconos/logo.png"
creditos_logo = os.getcwd() + "/Iconos/creditos.png"
ojos_compuestos_logo = os.getcwd() + "/Ojos_Compuestos/Iconos/logo.png"

RESOLUCION_MONITOR = (1200,900)

class Insectos_Main():
	'''Ventana de Pruebas para tu botón '''
	def __init__(self):
		pygame.init()
		pygame.display.set_mode(RESOLUCION_MONITOR , 0, 0)
		self.ventana = None
		self.widgets = None
		self.reloj = None
		self.fondo = None
		self.bichos_cantores = None
		self.cucarasims = None
		self.ojos_compuesto = None
		self.mensaje = None
		self.dialog_cerrar = None
		self.sonido_select = None

		self.sonido_mosca = None
		self.sonido_bicho1 = None
		self.sonido_bicho2 = None

		# Bichos en pantalla
		self.imagenes_bicho = None
		self.Bichos = None
		self.area_visible = None
		self.contador = 0
		self.estado = None
		self.carga = False

		#self.setup()
		# cambié self.setup() por lo que sigue
		if not self.ventana: self.ventana = pygame.display.get_surface()
		jamatrix = JAMatrix(self.ventana)
		jamatrix.setup()
		thread = threading.Thread( target=self.setup )
		thread.start()
		while not self.carga:
		# mientras esté corriendo el hilo se dibuja JAMatrix
			jamatrix.Run()
		jamatrix.descarga_todo()
		pygame.time.wait(3)
		gc.collect()
		self.carga = False
		self.Run()

	def precarga(self):
		if not self.fondo: self.fondo = pygame.transform.scale(pygame.image.load(os.getcwd() + "/Iconos/fondo.png"), (1200,900))
		pygame.display.set_caption("Insectos.activity (Versión 1) - CeibalJAM! - Uruguay - 2010")
		if not self.sonido_select: self.sonido_select = pygame.mixer.Sound(os.getcwd() + "/CeibalJAM_Lib/select.ogg")
		if not self.sonido_mosca: self.sonido_mosca = pygame.mixer.Sound(os.getcwd() + "/Sonidos/moscas.ogg")

		if not self.sonido_bicho1 or not self.sonido_bicho2:
			lista_sonidos = os.listdir(os.getcwd() + "/Bichos_Cantores/Sonidos/")
			random.seed()
			self.sonido_bicho1 = pygame.mixer.Sound(os.getcwd() + "/Bichos_Cantores/Sonidos/" + random.choice(lista_sonidos))
			self.sonido_bicho2 = pygame.mixer.Sound(os.getcwd() + "/Bichos_Cantores/Sonidos/" + random.choice(lista_sonidos))

		self.sonido_mosca.play(-1)
		self.sonido_bicho1.play(-1)
		self.sonido_bicho2.play(-1)

		while len(self.Bichos.sprites()) < 12:
			self.Bichos.add(Bicho(self))
		self.carga = True

	def Run(self):
	# Precarga con presentacion JAMatrix
		self.carga = False
		jamatrix = JAMatrix(self.ventana)
		jamatrix.setup()
		thread = threading.Thread( target=self.precarga )
		thread.start()
		while not self.carga:
		# mientras esté corriendo el hilo se dibuja JAMatrix
			jamatrix.Run()

		jamatrix.descarga_todo()
		pygame.time.wait(3)
		gc.collect()
		self.estado = "Insectos"
		self.ventana.blit(self.fondo, (0,0))
		pygame.mouse.set_visible(True)

		self.Bichos.draw(self.ventana)
		self.widgets.draw(self.ventana)
		pygame.display.update()
		pygame.time.wait(2)

		while self.estado == "Insectos":
			self.reloj.tick(35)

			if list(self.mensaje):
				self.pause_menu()

			cambios=[]
			self.Bichos.clear(self.ventana, self.fondo)
			self.widgets.clear(self.ventana, self.fondo)
			self.Bichos.update()
			self.widgets.update()
			cambios.extend ( self.Bichos.draw(self.ventana) )
			cambios.extend ( self.widgets.draw(self.ventana) )
			
			self.handle_event()
			pygame.display.update(cambios)
			pygame.time.wait(2)


	def pause_menu(self):
	# pausa el juego y reproduce mensajes emergentes
		while list(self.mensaje):
			self.reloj.tick(35)
			cambios=[]
			self.mensaje.clear(self.ventana, self.fondo)
			self.mensaje.update()
			cambios.extend ( self.mensaje.draw(self.ventana) )
			self.handle_event()
			pygame.display.update(cambios)

	def get_creditos(self):
		pygame.event.clear()
		self.RunCreditos()

	def RunCreditos(self):
		pygame.mouse.set_visible(False)

		barra = BarraCreditos()
		x = 0
		y = RESOLUCION_MONITOR[1] - barra.rect.h
		fondo = self.fondo.copy()
		fondo.blit(barra.image, (x,y))
		self.ventana.blit(fondo, (0,0))
		self.widgets.clear(self.ventana, fondo)
		pygame.display.update()

		creditos = Creditos()
		
		ver_creditos = True
		while ver_creditos:
			self.reloj.tick(35)
			cambios=[]
			self.Bichos.clear(self.ventana, fondo)
			creditos.clear(self.ventana, fondo)
			self.Bichos.update()
			creditos.update()
			cambios.extend ( self.Bichos.draw(self.ventana) )
			cambios.extend ( creditos.draw(self.ventana) )
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					teclas = pygame.key.get_pressed()
					if teclas[pygame.K_ESCAPE]:
						self.ventana.blit(self.fondo, (0,0))
						pygame.display.update()
						pygame.mouse.set_visible(True)
						ver_creditos = False
						pygame.event.clear()
						creditos.empty()
						creditos = None

			pygame.display.update(cambios)
			pygame.time.wait(1)

	def setup(self):
		pygame.event.set_blocked([JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP, JOYBUTTONDOWN,
					KEYUP, VIDEORESIZE, VIDEOEXPOSE, USEREVENT, QUIT, ACTIVEEVENT]) # bloqueados
		pygame.event.set_allowed([MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN, KEYDOWN]) # permitidos
		pygame.mixer.init(44100, -16, 2, 2048)
		pygame.mixer.music.set_volume(1.0)

		# todavia se puede hacer una descarga de esto cuando se llame a un juego interno y luego recargarlo con hilos
		if not self.ventana: self.ventana = pygame.display.get_surface()
		if not self.widgets: self.widgets = pygame.sprite.OrderedUpdates()	
		if not self.area_visible: self.area_visible = pygame.Rect(35,35,RESOLUCION_MONITOR[0]-70,RESOLUCION_MONITOR[1]-70) 
		if not self.imagenes_bicho:
			self.imagenes_bicho = [pygame.transform.rotate(pygame.image.load(imagenes_bichos+"escarabajo1.png"), -90),
			pygame.transform.rotate(pygame.image.load(imagenes_bichos+"escarabajo3.png"), -90),
			pygame.transform.rotate(pygame.image.load(imagenes_bichos+"escarabajo4.png"), -90),
			pygame.transform.rotate(pygame.image.load(imagenes_bichos+"cucaracha1.png"), -90),
			pygame.transform.rotate(pygame.image.load(imagenes_bichos+"cucaracha2.png"), -90),
			pygame.transform.rotate(pygame.image.load(imagenes_bichos+"avispa1.png"), -90),
			pygame.transform.rotate(pygame.image.load(imagenes_bichos+"mariposa1.png"), -90),
			pygame.transform.rotate(pygame.image.load(imagenes_bichos+"bicho.png"), -90),
			pygame.transform.rotate(pygame.image.load(imagenes_bichos+"hormiga.png"), -90)]

		if not self.Bichos: self.Bichos = pygame.sprite.OrderedUpdates() 

		w = RESOLUCION_MONITOR[0]/9
		h = RESOLUCION_MONITOR[1]/9

		# Boton Creditos
		boton = JAMElipseButton(texto="", tamanio_panel=(200, 130), imagen=creditos_logo, tamanio_imagen=(127,77))
		boton.connect(callback=self.get_creditos, sonido_select=self.sonido_select)
		x = w*4
		y = h*3
		boton.set_posicion(punto=(x,y))
		self.widgets.add(boton)

		# Boton CucaraSims
		boton = JAMElipseButton(imagen=cucarasims_logo, tamanio_imagen=(190,97), texto="", tamanio_panel=(250, 180))
		boton.connect(callback=self.get_cucarasims, sonido_select=self.sonido_select)
		x = w*6
		y = h*1
		boton.set_posicion(punto=(x,y))
		self.widgets.add(boton)

		# Boton Bichos Cantores
		boton = JAMElipseButton(imagen=bichos_cantores_logo, tamanio_imagen=(128,77), texto="", tamanio_panel=(250, 180))
		boton.connect(callback=self.get_bichos_cantores, sonido_select=self.sonido_select)
		x = w*7
		y = h*3
		boton.set_posicion(punto=(x,y))
		self.widgets.add(boton)

		# Boton Salir
		boton = JAMElipseButton(texto="Salir", tamanio_panel=(200, 130), tamanio_de_letra=50)
		boton.connect(callback=self.selecciona_mensaje_cerrar, sonido_select=self.sonido_select)
		x = w*6
		y = h*5
		boton.set_posicion(punto=(x,y))
		self.widgets.add(boton)

		# Boton Ojos Compuestos
		boton = JAMElipseButton(texto="", tamanio_panel=(250, 180), imagen=ojos_compuestos_logo, tamanio_imagen=(165,77))
		boton.connect(callback=self.get_ojos_compuestos, sonido_select=self.sonido_select)
		x = w*3 + w/2
		y = h*1 - h/2
		boton.set_posicion(punto=(x,y))
		self.widgets.add(boton)

		if not self.reloj: self.reloj = pygame.time.Clock()
		if not self.mensaje: self.mensaje = pygame.sprite.OrderedUpdates()
		if not self.dialog_cerrar:
			self.dialog_cerrar = JAMDialog(mensaje="¿Deseas Salir?", resolucion_monitor=RESOLUCION_MONITOR)
			self.dialog_cerrar.boton_aceptar.connect(callback=self.salir, sonido_select=self.sonido_select)
			self.dialog_cerrar.boton_cancelar.connect(callback=self.deselecciona_mensaje, sonido_select=self.sonido_select)

		self.carga = True

	def deselecciona_mensaje(self):
	# cierra mensaje emergente
		self.mensaje.clear(self.ventana, self.fondo)
		pygame.display.update()
		self.mensaje = pygame.sprite.OrderedUpdates()

	def selecciona_mensaje_cerrar(self):
	# Mensaje cerrar el juego
		pygame.event.clear()
		self.deselecciona_mensaje()
		self.mensaje = self.dialog_cerrar

	# --------------------- Ejecución de Juegos --------------------------------
	def detiene_todo(self):
		pygame.event.clear()
		# detener todos los sonidos
		self.sonido_mosca.stop()
		self.sonido_bicho1.stop()
		self.sonido_bicho2.stop()
		if pygame.mixer.music.get_busy():
			pygame.mixer.music.stop()

		# liberar memoria (todavía se puede liberar más)
		self.sonido_select = None
		self.sonido_mosca = None
		self.sonido_bicho1 = None
		self.sonido_bicho2 = None
		self.fondo = None
		self.Bichos.empty()

	def get_cucarasims(self):
		self.detiene_todo()

		self.bichos_cantores = None
		self.ojos_compuesto = None

		self.cucarasims = CucaraSims_Main(self)
		self.cucarasims.precarga(JAMatrix(self.ventana))
		self.estado = "CucaraSims"

	def get_bichos_cantores(self):
		self.detiene_todo()

		self.cucarasims = None
		self.ojos_compuesto = None

		self.bichos_cantores = Bichos_Cantores_Main(self)
		self.bichos_cantores.precarga(JAMatrix(self.ventana))
		self.estado = "Bichos_Cantores"

	def get_ojos_compuestos(self):
		self.detiene_todo()

		self.cucarasims = None
		self.bichos_cantores = None

		self.ojos_compuesto = Ojos_Compuestos_Main(self)
		self.ojos_compuesto.precarga(JAMatrix(self.ventana))
		self.estado = "Ojos_Compuestos"

	# --------------------- Ejecución de Juegos --------------------------------

	def get_fondo(self, color=(100,100,100,1), tamanio=(800,600)):
		superficie = pygame.Surface( tamanio, flags=HWSURFACE )
		superficie.fill(color)
		return superficie

	def handle_event(self):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				teclas = pygame.key.get_pressed()
				if teclas[pygame.K_ESCAPE]:
					self.selecciona_mensaje_cerrar()
					pygame.event.clear()
					return
		pygame.event.clear()

	def salir(self):
		pygame.quit()
		sys.exit()

class BarraCreditos(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		#barra = pygame.sprite.Sprite()
		self.image = pygame.image.load(os.getcwd() + "/Iconos/barra.png")
		self.rect = self.image.get_rect()


class Creditos(pygame.sprite.OrderedUpdates):
	def __init__(self):
		pygame.sprite.OrderedUpdates.__init__(self)

		self.grupo1 = {}
		self.grupo2 = {}
		self.grupo3 = {}
		self.grupo4 = {}

		self.get_sprites()
		self.seleccion = 1
		self.velocidad = 4
	
	def update(self):
		if self.seleccion == 1:
			for num in self.grupo1.keys():
				etiqueta, (x,y) = self.grupo1[num]
				x = etiqueta.rect.x
				y = etiqueta.rect.y
				y -= self.velocidad
				etiqueta.set_posicion((x,y))
			if y < -50:
				self.seleccion = 2
				for num in self.grupo1.keys():
					etiqueta, (x,y) = self.grupo1[num]
					etiqueta.set_posicion((x,y))

		if self.seleccion == 2:
			for num in self.grupo2.keys():
				etiqueta, (x,y) = self.grupo2[num]
				x = etiqueta.rect.x
				y = etiqueta.rect.y
				y -= self.velocidad
				etiqueta.set_posicion((x,y))
			if y < -50:
				self.seleccion = 3
				for num in self.grupo2.keys():
					etiqueta, (x,y) = self.grupo2[num]
					etiqueta.set_posicion((x,y))
		
		if self.seleccion == 3:
			for num in self.grupo3.keys():
				etiqueta, (x,y) = self.grupo3[num]
				x = etiqueta.rect.x
				y = etiqueta.rect.y
				y -= self.velocidad
				etiqueta.set_posicion((x,y))
			if y < -50:
				self.seleccion = 4
				for num in self.grupo3.keys():
					etiqueta, (x,y) = self.grupo3[num]
					etiqueta.set_posicion((x,y))

		if self.seleccion == 4:
			for num in self.grupo4.keys():
				etiqueta, (x,y) = self.grupo4[num]
				x = etiqueta.rect.x
				y = etiqueta.rect.y
				y -= self.velocidad
				etiqueta.set_posicion((x,y))
			if y < -50:
				self.seleccion = 1
				for num in self.grupo4.keys():
					etiqueta, (x,y) = self.grupo4[num]
					etiqueta.set_posicion((x,y))
 
	def get_sprites(self):	
		Textos1 = ["Insectos.activity",
		"Para Aprender Jugando y Jugar Aprendiendo.",
		"Insectos.activity forma parte de Artrópodos.activity.",
		"Todo se encuentra en desarrollo y apenas iniciado.",
		"Si deseas participar en el proyecto contáctate conmigo",
		"a fdanesse@hotmail.com, serás bienvenido."]

		Textos2 = ["También se encuentra en desarrollo la librería",
		"de widgets utilizada: CeibalJAM_Lib.",
		"Si eres programador python y deseas colaborar,",
		"puedes descargar la librería desde:",
		"https://sites.google.com/site/sugaractivities/ceibaljam_lib"]

		Textos3 = ["Idea Original, Edición de Audio y Video,",
		"Diseño Gráfico, Desarrollo y Contenidos:",
		"Flavio Danesse - fdanesse@hotmail.com",
		"Imágenes e Información: Wikipedia - Wikiespecies",
		"Música: MATI - ARUAL - http://www.jamendo.com"]

		Textos4 = ["Si eres un jóven que desea aprender a programar",
		"en python y necesitas ayuda, realiza la solicitud",
		"para unirte a python jóven en:",
		"https://sites.google.com/site/flaviodanesse/python-joven"]

		color = (255,255,255,1)
		y = RESOLUCION_MONITOR[1]

		contador = 1
		for texto in Textos1:
			etiqueta = JAMLabel (imagen=None, texto=texto, tamanio_de_letra=40, color=color)
			x = RESOLUCION_MONITOR[0]/2 - etiqueta.rect.w/2 # centrado en la pantalla
			etiqueta.set_posicion((x,y))
			self.add(etiqueta)
			self.grupo1[contador] = etiqueta, (x,y)
			y += 100
			contador += 1
		
		contador = 1
		y = RESOLUCION_MONITOR[1]
		for texto in Textos2:
			etiqueta = JAMLabel (imagen=None, texto=texto, tamanio_de_letra=40, color=color)
			x = RESOLUCION_MONITOR[0]/2 - etiqueta.rect.w/2 # centrado en la pantalla
			etiqueta.set_posicion((x,y))
			self.add(etiqueta)
			self.grupo2[contador] = etiqueta, (x,y)
			y += 100
			contador += 1

		contador = 1
		y = RESOLUCION_MONITOR[1]
		for texto in Textos3:
			etiqueta = JAMLabel (imagen=None, texto=texto, tamanio_de_letra=40, color=color)
			x = RESOLUCION_MONITOR[0]/2 - etiqueta.rect.w/2 # centrado en la pantalla
			etiqueta.set_posicion((x,y))
			self.add(etiqueta)
			self.grupo3[contador] = etiqueta, (x,y)
			y += 100
			contador += 1

		contador = 1
		y = RESOLUCION_MONITOR[1]
		for texto in Textos4:
			etiqueta = JAMLabel (imagen=None, texto=texto, tamanio_de_letra=40, color=color)
			x = RESOLUCION_MONITOR[0]/2 - etiqueta.rect.w/2 # centrado en la pantalla
			etiqueta.set_posicion((x,y))
			self.add(etiqueta)
			self.grupo4[contador] = etiqueta, (x,y)
			y += 100
			contador += 1

if __name__ == "__main__":
	insectos = Insectos_Main()
	insectos.Run()
