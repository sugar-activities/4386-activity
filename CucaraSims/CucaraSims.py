#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   CucaraSims_Main.py por:
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

import sys, threading, random

import CeibalJAM_Lib
from CeibalJAM_Lib.JAMButton import JAMLabel, JAMButton
from CeibalJAM_Lib.JAMFrame import JAMFrame
from CeibalJAM_Lib.JAMDialog import JAMDialog 

import Variables_Globales as VG
from Cria_Bichos_Main import Cria_Bichos_Main, Ooteca
from Archivos_y_Directorios import Archivos_y_Directorios
from Bicho import Bicho

class CucaraSims_Main():
	def __init__(self,  menu_principal):
		self.menu_principal = menu_principal
		self.ventana = None
		self.reloj = pygame.time.Clock()
		self.fondo = None
		self.sonido_select = None
		self.sprites = None
		self.Archivos_y_Directorios = None
		self.base_de_datos = None
		self.creditos = None
		self.dialog_cerrar = None
		self.menu = None
		self.mensaje = None
		self.interval = 0
		self.nivel = None
		self.Juegos_guardados = None
		self.Cria_Bichos = None

	def precarga(self, JAMatrix):
	# en lugar de llamar a run, se hace precarga con presentacion JAMatrix
		JAMatrix.setup()
		self.setup()
		self.Cria_Bichos = Cria_Bichos_Main(self)
		thread1 = threading.Thread( target=self.Cria_Bichos.setup1 )
		thread1.start()
		while self.Cria_Bichos.nivel_carga != 4:
		# mientras esté corriendo el hilo se dibuja JAMatrix
			JAMatrix.Run()
		JAMatrix.descarga_todo()
		self.nivel = "Menu"
		self.sprites = self.menu
		pygame.time.wait(3)
		gc.collect()
		self.RunMenu()

	def descarga_todo(self):
		self.reloj = None
		self.fondo = None
		self.sonido_select = None
		self.sprites = None
		self.Archivos_y_Directorios = None
		self.base_de_datos = None
		self.creditos = None
		self.dialog_cerrar = None
		self.menu = None
		self.mensaje = None
		self.etiqueta = None
		self.interval = 0
		self.nivel = None
		self.Juegos_guardados = None
		self.Cria_Bichos = None
		self.ventana = None

	def RunMenu(self):
	# Se Ejecuta el menú
		pygame.display.set_caption("CucaraSims (Versión 1) - CeibalJAM! - Uruguay - 2010")
		pygame.mouse.set_visible(True)
		self.Cria_Bichos.set_musica()
		self.fondo = self.get_fondo2()
		self.ventana.blit(self.fondo, (0,0))
		pygame.display.update()
		
		while self.nivel == "Menu":
		# Corre menú inicial
			self.reloj.tick(35)

			if list(self.mensaje):
				self.sprites.clear(self.ventana, self.fondo)
				pygame.display.update()
				self.pause_menu()

			cambios=[]
			self.sprites.clear(self.ventana, self.fondo)
			self.sprites.update()
			cambios.extend ( self.sprites.draw(self.ventana) )
			self.handle_event()
			pygame.display.update(cambios)
			pygame.time.wait(2)

		if self.nivel == "CucaraSims":
			self.Cria_Bichos.Run()
		if self.nivel == "Creditos":
			self.RunCreditos()
		
		self.verifica()

	def verifica(self):
		if self.nivel == "Menu":
			self.RunMenu()
		else:
			print "Verifica no vuelve al menu", self.nivel

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
	def selecciona_menu_cargar(self):
	# cargar un juego guardado
		pygame.event.clear()
		self.deselecciona_mensaje()
		self.Juegos_guardados = Juegos_Guardados(self.Archivos_y_Directorios, self)
		self.mensaje = self.Juegos_guardados
	def cargar_juego(self, datos):
	# Carga el juegon Juego guardado seleccionado
		# poner todo a cero
		self.Cria_Bichos.Bichos.empty()
		self.Cria_Bichos.cadaveres.empty()
		self.Cria_Bichos.alimento.empty()
		self.Cria_Bichos.ootecas.empty()
		self.Cria_Bichos.agua.empty()
		self.Cria_Bichos.ficha = pygame.sprite.OrderedUpdates()
		self.Cria_Bichos.puntos = 0
		self.Cria_Bichos.tiempo_de_juego = 0
		self.Cria_Bichos.horas = 0
		self.Cria_Bichos.dias = 0
		self.Cria_Bichos.anios = 0
		self.Cria_Bichos.machos, self.Cria_Bichos.hembras = 0,0

		self.Cria_Bichos.secuencia_muda = 0
		self.Cria_Bichos.reproduccion = 0
		self.Cria_Bichos.nacimientos = 0
		self.Cria_Bichos.muertes = 0
		self.Cria_Bichos.plaga = 0

		# recuperar datos
		(base, datos_juego, cucas, ootecas) = datos # return (base, datos_juego, cucas, Ootecas)

		self.base_de_datos = base

		# datos generales del juego
		# datos 0 Tabla Juego [anios, dias, horas, puntos]
		self.Cria_Bichos.anios = int(datos_juego[1])
		self.Cria_Bichos.dias = int(datos_juego[2])
		self.Cria_Bichos.horas = int(datos_juego[3])
		self.Cria_Bichos.puntos = int(datos_juego[4])

		for cuca in cucas:
		# datos de cucarachas
		# datos 1 Tabla Cucas [sexo, anios, dias, horas, hambre, sed]
			contador, sexo, anios, dias, horas, hambre, sed = cuca
			tipo = None
			while tipo != sexo:
				bicho = Bicho(self.Cria_Bichos)
				tipo = bicho.sexo
			self.Cria_Bichos.Bichos.add(bicho)

			if bicho.sexo == "M":
				self.Cria_Bichos.machos += 1
			elif bicho.sexo == "F":
				self.Cria_Bichos.hembras += 1

			bicho.anios = int(anios)
			bicho.dias = int(dias)
			bicho.horas = int(horas)
			bicho.hambre = int(hambre)
			bicho.sed = int(sed)

			# escalar
			for dia in range (0, bicho.dias):
			# desde dia cero hasta los dias que tiene el bicho
				if dia == bicho.control_mudas: # bicho.control_mudas es una lista de dias de mudas

					indice = bicho.dias_mudas.index(dia)
					bicho.set_muda(escala=bicho.escalas_mudas[indice]) # se obtiene el tamaño
					bicho.velocidad += int(bicho.velocidad/3)
	
					if indice+1 < len(bicho.dias_mudas):
						bicho.control_mudas = bicho.dias_mudas[indice+1]
					else:
						bicho.control_mudas = bicho.dias_mudas[0]

		#if self.Cria_Bichos.hembras + self.Cria_Bichos.machos != len(cucas): print "HAY INCOHERENCIAS DE CANTIDAD DE BICHOS ALMACENADOS/CARGADOS"

		for ooteca in ootecas:
		# datos de cucarachas
		# datos 2 Tabla ootecas [dias, horas, huevos]
			contador, dias, horas, huevos = ooteca
			ooteca = Ooteca(self.Cria_Bichos, posicion=(0,0))
			self.Cria_Bichos.ootecas.add(ooteca)
			ooteca.dias = int(dias)
			ooteca.horas = int(horas)
			ooteca.huevos = int(huevos)

		self.deselecciona_mensaje()
		self.nivel = "CucaraSims"


	def get_new_game(self):
	# comienza un juego nuevo
		self.base_de_datos = self.Archivos_y_Directorios.CrearBasededatos()
		self.Cria_Bichos.get_nuevo_Juego()
		if self.base_de_datos:
			self.nivel = "CucaraSims"
		else:
			print "Error al crear la base de datos"

	def RunCreditos(self):
		pygame.mouse.set_visible(False)
		pygame.mixer.music.load(VG.MUSICA2)
		pygame.mixer.music.play(-1, 0.0)
		self.sprites.clear(self.ventana, self.fondo)
		pygame.display.update()
		
		while self.nivel == "Creditos":
			self.reloj.tick(35)
			cambios=[]
			self.creditos.clear(self.ventana, self.fondo)
			self.creditos.update()
			cambios.extend ( self.creditos.draw(self.ventana) )
			self.handle_event()
			pygame.display.update(cambios)
			pygame.time.wait(1)
		if self.nivel == "Menu":
			self.RunMenu()

	def get_fondo2(self, tamanio=VG.RESOLUCION_MONITOR):
		superficie = pygame.transform.scale(pygame.image.load(VG.FONDO4), (VG.RESOLUCION_MONITOR))
		return superficie

	def get_creditos(self):
		pygame.event.clear()
		self.nivel = "Creditos"

	def setup(self):
	# configuraciones y precarga
		#pygame.display.set_mode(VG.RESOLUCION_MONITOR , 0, 0)
		if not self.ventana: self.ventana = self.menu_principal.ventana
		pygame.event.set_blocked([JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP, JOYBUTTONDOWN,
					KEYUP, VIDEORESIZE, VIDEOEXPOSE, USEREVENT, QUIT, ACTIVEEVENT, MOUSEMOTION, MOUSEBUTTONUP]) # bloqueados
		pygame.event.set_allowed([KEYDOWN, MOUSEBUTTONDOWN]) # permitidos

		if not self.sprites: self.sprites = pygame.sprite.OrderedUpdates()
		if not self.Archivos_y_Directorios: self.Archivos_y_Directorios = Archivos_y_Directorios(VG.DIRECTORIO_DATOS)
 		if not self.sonido_select: self.sonido_select = pygame.mixer.Sound("CeibalJAM_Lib/select.ogg")
		#if not self.ventana: self.ventana = pygame.display.get_surface() # la ventana del juego
		if not self.reloj: self.reloj = pygame.time.Clock()
		if not self.fondo: self.fondo = self.get_fondo()
		if not self.menu:
			self.menu = Menu()
			self.menu.boton_nuevo.connect(callback=self.get_new_game, sonido_select=self.sonido_select)
			self.menu.boton_cargar.connect(callback=self.selecciona_menu_cargar, sonido_select=self.sonido_select)
			self.menu.boton_creditos.connect(callback=self.get_creditos, sonido_select=self.sonido_select)
			self.menu.boton_salir.connect(callback=self.selecciona_mensaje_cerrar, sonido_select=self.sonido_select)

		if not self.creditos: self.creditos = Creditos()

		if not self.dialog_cerrar:
			self.dialog_cerrar = JAMDialog(mensaje="¿Deseas Salir?", resolucion_monitor=VG.RESOLUCION_MONITOR)
			self.dialog_cerrar.boton_aceptar.connect(callback=self.salir, sonido_select=self.sonido_select)
			self.dialog_cerrar.boton_cancelar.connect(callback=self.deselecciona_mensaje, sonido_select=self.sonido_select)

		if not self.mensaje: self.mensaje = pygame.sprite.OrderedUpdates()

	def get_fondo(self, color=(0,0,0,1), tamanio=VG.RESOLUCION_MONITOR):
	# devuelve una superficie de color para el fondo de la ventana
		superficie = pygame.Surface( tamanio, flags=HWSURFACE )
		superficie.fill(color)
		return superficie

	def handle_event(self):
		for event in pygame.event.get():
			teclas = pygame.key.get_pressed()
			if teclas[pygame.K_ESCAPE]:
				if self.nivel == "JAM":
					self.salir()
				elif self.nivel == "Menu" and not list(self.mensaje):
					self.selecciona_mensaje_cerrar()					
				elif self.nivel == "Creditos":
					self.nivel = "Menu"
				elif list(self.mensaje):
					self.deselecciona_mensaje()
				pygame.event.clear()
				return

	def salir(self):
		pygame.event.clear()
		self.deselecciona_mensaje()
		if pygame.mixer.music.get_busy():
			pygame.mixer.music.stop()
		self.descarga_todo()
		return self.menu_principal.Run()

class Menu(pygame.sprite.OrderedUpdates):
	def __init__(self):
		pygame.sprite.OrderedUpdates.__init__(self)

		separador = 40
		ancho = 500
		alto = 100

		self.boton_nuevo = JAMButton(texto="Juego Nuevo", tamanio_de_letra=50, tamanio_panel=(ancho,alto))
		self.boton_cargar = JAMButton(texto="Cargar Juego", tamanio_de_letra=50, tamanio_panel=(ancho,alto))
		self.boton_creditos = JAMButton(texto="Creditos", tamanio_de_letra=50, tamanio_panel=(ancho,alto))
		self.boton_salir = JAMButton(texto="Salir", tamanio_de_letra=50, tamanio_panel=(ancho,alto))

		y = 150
		x = VG.RESOLUCION_MONITOR[0]/2 - self.boton_nuevo.rect.w/2
		self.boton_nuevo.set_posicion(punto=(x,y))

		y += self.boton_nuevo.rect.h + separador
		x = VG.RESOLUCION_MONITOR[0]/2 - self.boton_cargar.rect.w/2
		self.boton_cargar.set_posicion(punto=(x,y))

		y += self.boton_cargar.rect.h + separador
		x = VG.RESOLUCION_MONITOR[0]/2 - self.boton_creditos.rect.w/2
		self.boton_creditos.set_posicion(punto=(x,y))

		y += self.boton_creditos.rect.h + separador
		x = VG.RESOLUCION_MONITOR[0]/2 - self.boton_salir.rect.w/2
		self.boton_salir.set_posicion(punto=(x,y))

		self.add(self.boton_nuevo)
		self.add(self.boton_cargar)
		self.add(self.boton_creditos)
		self.add(self.boton_salir)

class Creditos(pygame.sprite.OrderedUpdates):
	def __init__(self):
		pygame.sprite.OrderedUpdates.__init__(self)

		self.grupo1 = {}
		self.grupo2 = {}
		self.grupo3 = {}
		self.grupo4 = {}
		self.grupo5 = {}

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
				self.seleccion = 5
				for num in self.grupo4.keys():
					etiqueta, (x,y) = self.grupo4[num]
					etiqueta.set_posicion((x,y))

		if self.seleccion == 5:
			for num in self.grupo5.keys():
				etiqueta, (x,y) = self.grupo5[num]
				x = etiqueta.rect.x
				y = etiqueta.rect.y
				y -= self.velocidad
				etiqueta.set_posicion((x,y))
			if y < -50:
				self.seleccion = 1
				for num in self.grupo5.keys():
					etiqueta, (x,y) = self.grupo5[num]
					etiqueta.set_posicion((x,y))

 
	def get_sprites(self):	
		Textos1 = ["CucaraSims.",
		"El Sims de las Cucarachas.",
		"Para Aprender Jugando y Jugar Aprendiendo.",
		"Dedicado con Cariño a mis Compañeros Voluntarios de",
		"CeibalJAM!, RAP Ceibal y a Todos los Niños y Jóvenes",
		"del Uruguay y demás comunidades Sugar."]

		Textos2 = ["CucaraSims forma parte de un paquete de actividades",
		"sobre inséctos, para aprender jugando y jugar aprendiendo.",
		"Dicho paquete a su vez, forma parte de Artrópodos.activity.",
		"Todo se encuentra en desarrollo y apenas iniciado.",
		"Si deseas participar en el proyecto contáctate conmigo",
		"a fdanesse@hotmail.com, serás bienvenido."]

		Textos3 = ["También se encuentra en desarrollo la librería",
		"de widgets utilizada: CeibalJAM_Lib.",
		"Si eres programador python y deseas colaborar,",
		"puedes descargar la librería desde:",
		"https://sites.google.com/site/sugaractivities/ceibaljam_lib"]

		Textos4 = ["Idea Original, Edición de Audio y Video,",
		"Diseño Gráfico, Desarrollo y Contenidos:",
		"Flavio Danesse - fdanesse@hotmail.com",
		"Imágenes e Información: Wikipedia - Wikiespecies",
		"Música: MATI - ARUAL - http://www.jamendo.com"]

		Textos5 = ["Si eres un jóven que desea aprender a programar",
		"en python y necesitas ayuda, realiza la solicitud",
		"para unirte a python jóven en:",
		"https://sites.google.com/site/flaviodanesse/python-joven"]

		# logo
		color = (255,255,255,1)
		contador = 1
		logo = JAMLabel (imagen=VG.LOGO, texto=None, tamanio_imagen=(255,117))
		y = VG.RESOLUCION_MONITOR[1]
		x = VG.RESOLUCION_MONITOR[0]/2 - logo.rect.w/2
		logo.set_posicion((x,y))
		self.add(logo)
		self.grupo1[contador] = logo, (x,y)
		y += 95
		contador += 1
		# textos1
		for texto in Textos1:
			etiqueta = JAMLabel (imagen=None, texto=texto, tamanio_de_letra=40, color=color)
			x = VG.RESOLUCION_MONITOR[0]/2 - etiqueta.rect.w/2 # centrado en la pantalla
			etiqueta.set_posicion((x,y))
			self.add(etiqueta)
			self.grupo1[contador] = etiqueta, (x,y)
			y += 100
			contador += 1
		
		contador = 1
		y = VG.RESOLUCION_MONITOR[1]
		for texto in Textos2:
			etiqueta = JAMLabel (imagen=None, texto=texto, tamanio_de_letra=40, color=color)
			x = VG.RESOLUCION_MONITOR[0]/2 - etiqueta.rect.w/2 # centrado en la pantalla
			etiqueta.set_posicion((x,y))
			self.add(etiqueta)
			self.grupo2[contador] = etiqueta, (x,y)
			y += 100
			contador += 1

		contador = 1
		y = VG.RESOLUCION_MONITOR[1]
		for texto in Textos3:
			etiqueta = JAMLabel (imagen=None, texto=texto, tamanio_de_letra=40, color=color)
			x = VG.RESOLUCION_MONITOR[0]/2 - etiqueta.rect.w/2 # centrado en la pantalla
			etiqueta.set_posicion((x,y))
			self.add(etiqueta)
			self.grupo3[contador] = etiqueta, (x,y)
			y += 100
			contador += 1

		contador = 1
		y = VG.RESOLUCION_MONITOR[1]
		for texto in Textos4:
			etiqueta = JAMLabel (imagen=None, texto=texto, tamanio_de_letra=40, color=color)
			x = VG.RESOLUCION_MONITOR[0]/2 - etiqueta.rect.w/2 # centrado en la pantalla
			etiqueta.set_posicion((x,y))
			self.add(etiqueta)
			self.grupo4[contador] = etiqueta, (x,y)
			y += 100
			contador += 1

		contador = 1
		y = VG.RESOLUCION_MONITOR[1]
		for texto in Textos5:
			etiqueta = JAMLabel (imagen=None, texto=texto, tamanio_de_letra=40, color=color)
			x = VG.RESOLUCION_MONITOR[0]/2 - etiqueta.rect.w/2 # centrado en la pantalla
			etiqueta.set_posicion((x,y))
			self.add(etiqueta)
			self.grupo5[contador] = etiqueta, (x,y)
			y += 100
			contador += 1

class Juegos_Guardados(pygame.sprite.OrderedUpdates):
	def __init__(self, archivosydirectorios, juego_base):
		pygame.sprite.OrderedUpdates.__init__(self)

		self.juego_base = juego_base

		self.Archivos_y_Directorios = archivosydirectorios
		lista_juegos_guardados = self.Archivos_y_Directorios.get_juegos()
		self.directorio = lista_juegos_guardados[0]	# string
		self.juegos = lista_juegos_guardados[1]	# lista
	
		y = 50
		self.items = []
		for juego in self.juegos:
			item = Item_Juego(self.Archivos_y_Directorios, juego, self)
			item.agregate(self)
			x = VG.RESOLUCION_MONITOR[0]/2 - item.etiqueta_juego.rect.w/2
			item.set_posicion(punto=(x, y))
			y += item.etiqueta_juego.rect.h + 30
			self.items.append(item)

	def reordenar_juegos(self, item):
		self.items.remove(item)
		y = 50
		for item in self.items:
			x = VG.RESOLUCION_MONITOR[0]/2 - item.etiqueta_juego.rect.w/2
			item.set_posicion(punto=(x, y))
			y += item.etiqueta_juego.rect.h + 30

			
class Item_Juego():
	def __init__(self, archivosydirectorios, juego, grupo):

		self.grupo = grupo
		self.Archivos_y_Directorios = archivosydirectorios
		self.juego = juego
		self.texto = self.juego #juego.split(".")[0]

		self.separador = 10

		self.etiqueta_juego = JAMLabel(imagen=None, texto=self.texto, tamanio_de_letra=40)
		self.boton_borrar = JAMButton(texto="Borrar", tamanio_de_letra=30, tamanio_panel=(50,self.etiqueta_juego.rect.h),
			color_relleno=(255,255,255,1), grosor_borde=0, color_panel=None)
		self.boton_load = JAMButton(texto="Cargar", tamanio_de_letra=30, tamanio_panel=(50,self.etiqueta_juego.rect.h),
			color_relleno=(255,255,255,1), grosor_borde=0, color_panel=None)

		ancho = self.boton_borrar.rect.w + self.separador + self.etiqueta_juego.rect.w + self.separador + self.boton_load.rect.w

		self.frame = self.get_frame(color=(255,200,0,1), tamanio=(ancho+self.separador*2,self.etiqueta_juego.rect.h+self.separador*2))
		self.boton_borrar.connect(callback=self.delete_game, sonido_select=None)
		self.boton_load.connect(callback=self.carga_game, sonido_select=None)

	def agregate(self, grupo):
		grupo.add(self.frame)
		grupo.add(self.etiqueta_juego)
		grupo.add(self.boton_borrar)
		grupo.add(self.boton_load)

	def get_frame(self, color=(0,0,0,1), tamanio=VG.RESOLUCION_MONITOR):
	# devuelve una superficie de color para el fondo de la ventana
		frame = pygame.sprite.Sprite()
		superficie = pygame.Surface( tamanio, flags=HWSURFACE )
		superficie.fill(color)
		frame.image = superficie
		frame.rect = frame.image.get_rect()
		return frame

	def set_posicion(self, punto=(0,0)):
		(x,y) = punto
		self.etiqueta_juego.set_posicion((x,y))
		a = x - self.separador - self.boton_borrar.rect.w
		self.boton_borrar.set_posicion((a,y))
		b = x + self.separador + self.etiqueta_juego.rect.w
		self.boton_load.set_posicion((b,y))

		self.frame.rect.x = self.boton_borrar.rect.x-self.separador
		self.frame.rect.y = self.boton_borrar.rect.y-self.separador

	def delete_game(self):
		self.Archivos_y_Directorios.borrar_tabla(self.juego)
		self.frame.kill()
		self.etiqueta_juego.kill()
		self.boton_borrar.kill()
		self.boton_load.kill()
		self.grupo.reordenar_juegos(self)
		return

	def carga_game(self):
		self.grupo.juego_base.cargar_juego(self.Archivos_y_Directorios.Leer_Base_de_Datos(self.juego))


if __name__ == "__main__":
	CucaraSims = CucaraSims_Main()
	CucaraSims.Run()
