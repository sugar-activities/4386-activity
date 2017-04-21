#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Cria_Bichos_Main.py por:
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

import sys, random, os, threading
from math import sin, cos, radians

import CeibalJAM_Lib
from CeibalJAM_Lib.JAMFrame import JAMFrame
from CeibalJAM_Lib.JAMButton import JAMButton, JAMLabel, JAMBaseButton
from CeibalJAM_Lib.JAMDialog import JAMDialog

import Variables_Globales as VG

from Bicho import Bicho
from Interfaz import Interfaz
from Ficha_Bicho import Ficha_Bicho
from Libreta_de_Lectura import Libreta_de_Lectura

class Cria_Bichos_Main():
# Subprograma independiente Crustaceos

	def __init__(self, cucarasims):
	# inicialización de objeto Crustaceos_Main

		self.velocidad_juego = VG.VELOCIDADJUEGO
		self.maximo_cucas = VG.MAXIMOCUCAS

		self.cucarasims = cucarasims
		
		self.ventana = self.cucarasims.ventana
		self.reloj = None
		self.fondo = None

		self.sonido_bicho = None
		self.imagenes_bicho = None
		self.Bichos = None # cucarachas
		self.interfaz = None # botones

		self.nivel = None
		self.area_visible = None # Donde pueden caminar las cucas

		self.puntero = None # grupo para contener la imagen del puntero actual
		self.pan_select = None # puntero del mouse para pan seleccionado
		self.agua_select = None

		self.alimento = None # grupo de alimento en escenario
		self.unidad_alimento = None # imagen para alimento en escenario

		self.agua = None # grupo de agua en escenario
		self.unidad_agua = None # imagen para agua en escenario

		self.tiempo_de_juego = 0
		self.horas = 0
		self.dias = 0
		self.anios = 0

		self.ficha_bicho = None # para mostrar los datos del bicho seleccionado
		self.ficha = None

		self.secuencia_muda = 0 # las veces que se ha reproducido automáticamente esta lección
		self.lecciones = None # contenedor para leccion en pantalla
		self.leccion_muda = None # leccion muda

		self.reproduccion = 0
		self.leccion_reproduccion = None
		self.ootecas = None

		self.nacimientos = 0
		self.leccion_ciclo_vital = None

		self.muertes = 0
		self.leccion_muerte = None
		self.cadaveres = None

		self.leccion_generica = None # para cualquier lección sin imagenes extras
		self.plaga = 0

		self.machos, self.hembras = 0,0
		self.mensajes = None
		self.mensajes_emergentes = None
		self.puntos = 0

		self.dialog_cerrar = None
		self.dialog_guardar = None

		self.sonido_select = None
		self.nivel_carga = 0

	def Run(self):
		self.setup_event()
		self.nivel = "Bichos"
		self.ventana.blit(self.fondo, (0,0))	
		self.Bichos.draw(self.ventana)
		self.interfaz.draw(self.ventana)
		pygame.display.update()
		self.selecciona_leccion_ciclo()
		
		while self.nivel == "Bichos":
		# Corre menú inicial
			self.reloj.tick(35)

			if list(self.lecciones):
			# Si hay una lección abierta, se pausa el juego
				self.pause_game_lecciones()

			cambios=[]
			self.agua.clear(self.ventana, self.fondo)  
			self.alimento.clear(self.ventana, self.fondo)
			self.cadaveres.clear(self.ventana, self.fondo)
			self.ootecas.clear(self.ventana, self.fondo)
			self.Bichos.clear(self.ventana, self.fondo)
			self.interfaz.clear(self.ventana, self.fondo)
			self.ficha.clear(self.ventana, self.fondo)
			self.mensajes.clear(self.ventana, self.fondo)
			self.puntero.clear(self.ventana, self.fondo) 
		
			self.agua.update() 
			self.alimento.update()
			self.cadaveres.update()
			self.ootecas.update()
			self.Bichos.update()
			self.interfaz.update()
			self.ficha.update()
			self.mensajes.update()
			self.puntero.update()

			cambios.extend ( self.agua.draw(self.ventana) )
			cambios.extend ( self.alimento.draw(self.ventana) )
			cambios.extend ( self.cadaveres.draw(self.ventana) )
			cambios.extend ( self.ootecas.draw(self.ventana) )
			cambios.extend ( self.Bichos.draw(self.ventana) )
			cambios.extend ( self.interfaz.draw(self.ventana) )
			cambios.extend ( self.ficha.draw(self.ventana) )
			cambios.extend ( self.mensajes.draw(self.ventana) )
			cambios.extend ( self.puntero.draw(self.ventana) )

			self.handle_event()
			pygame.display.update(cambios)

			self.set_tiempo_de_juego()
			pygame.time.wait(2)

	def get_end(self):
		pygame.event.clear()
		self.event_end_game() # cuando pierde nada más

	def set_musica(self):
		pygame.event.clear()
		self.set_mensaje(texto="Musica Activada.")
		self.interfaz.boton_musica.set_imagen(imagen=self.interfaz.imagenes_audio[0])
		self.interfaz.boton_musica.set_posicion(punto=self.interfaz.posicion_boton_audio)
		pygame.mixer.music.load(VG.MUSICA1)
		pygame.mixer.music.play(-1, 0.0)

	def set_pause_musica(self):
		pygame.event.clear()
		self.set_mensaje(texto="Musica Desactivada.")
		self.interfaz.boton_musica.set_imagen(imagen=self.interfaz.imagenes_audio[1])
		self.interfaz.boton_musica.set_posicion(punto=self.interfaz.posicion_boton_audio)
		if pygame.mixer.music.get_busy():
			pygame.mixer.music.stop()
		else:
			self.set_musica()

	def no_mensajes(self):
		self.mensajes.clear(self.ventana, self.fondo)
		pygame.display.update()
		self.mensajes = pygame.sprite.OrderedUpdates()

		if not self.ootecas.sprites():
		# no habrán más naciemientos
			if not self.machos or not self.hembras:
			# faltan especímenes de uno de los sexos
				self.get_end()
		if self.machos + self.hembras >= self.maximo_cucas:
			self.migrar()

	def migrar(self):
	# la mitad de los machos y de las hembras se van
		migracion_machos = self.machos/2
		migracion_hembras = self.hembras/2

		for bicho in self.Bichos.sprites():
			if bicho.sexo == "M" and migracion_machos > 0 and self.machos >= 2:
				bicho.kill()
				self.puntos += 1
				migracion_machos -= 1

			if bicho.sexo == "F" and migracion_hembras > 0 and self.hembras >= 2:
				bicho.kill()
				self.puntos += 1
				migracion_hembras -= 1

		self.set_mensaje(texto="Algunas Cucarachas han migrado hacia otros habitats.")

	def set_mensaje(self, texto=""):
		self.sonido_bicho.play()
		if self.mensajes_emergentes.texto != texto:
			self.mensajes_emergentes.set_mensaje(texto)
		if self.mensajes != self.mensajes_emergentes:
			self.mensajes = self.mensajes_emergentes

	def get_nuevo_Juego(self):
	# poner todo a cero y empezar de nuevo
		self.Bichos.empty()
		self.cadaveres.empty()
		self.alimento.empty()
		self.ootecas.empty()
		self.agua.empty()
		self.ficha = pygame.sprite.OrderedUpdates()
		self.puntos = 0
		self.tiempo_de_juego = 0
		self.horas = 0
		self.dias = 0
		self.anios = 0
		self.machos, self.hembras = 0,0

		self.secuencia_muda = 0
		self.reproduccion = 0
		self.nacimientos = 0
		self.muertes = 0
		self.plaga = 0

		while not self.machos or not self.hembras:
		# asegurar un macho y una hembra
			self.event_nacer()
			self.machos, self.hembras = self.verificar_sexos_en_habitat()

	def verificar_sexos_en_habitat(self):
	# verifica si hay machos para reproducirse
		machos = 0
		hembras = 0
		for cuca in self.Bichos.sprites():
			if cuca.sexo == "M":
				machos += 1
			if cuca.sexo == "F":
				hembras += 1
		return machos, hembras

	def event_morir(self, posicion=(0,0), dias=0, leccion=False):
	# muere una cuca
		if self.muertes == 0:
			self.muertes = 1
			self.sonido_bicho.play()
			self.deselecciona_leccion()
			self.lecciones = self.leccion_muerte
			if not self.interfaz.boton_muerte in self.interfaz:
				self.interfaz.add(self.interfaz.boton_muerte)
		if leccion == False:
		# Cuando es True se está llamando desde el botón para ver la lección
			self.cadaveres.add(Cadaver(self, posicion=posicion, dias=dias))
			self.set_mensaje(texto="Se han producido muertes en el habitat.")

	def event_nacer(self, leccion=False):
	# nace una cuca
		if self.nacimientos == 0:
			self.nacimientos = 1
			self.sonido_bicho.play()
			self.deselecciona_leccion()
			self.lecciones = self.leccion_ciclo_vital
			if not self.interfaz.boton_ciclo in self.interfaz:
				self.interfaz.add(self.interfaz.boton_ciclo)
		if leccion == False:
		# Cuando es True se está llamando desde el botón para ver la lección
			self.Bichos.add(Bicho(self))
			self.set_mensaje(texto="Se han producido nacimientos en el habitat.")

	def pause_game_lecciones(self):
	# pausa el juego y reproduce las lecciones
		while list(self.lecciones):
			self.reloj.tick(35)
			cambios=[]
			self.lecciones.clear(self.ventana, self.fondo)
			self.lecciones.update()
			cambios.extend ( self.lecciones.draw(self.ventana) )
			self.handle_event()
			pygame.display.update(cambios)

	def event_muda(self, posicion=(0, 0), tamanio=(63,50)):
	# dejar exoesqueleto
		self.set_mensaje(texto="Algunas Cucarachas han realizado la muda de su exoesqueleto.")
		if self.secuencia_muda == 0:
			self.secuencia_muda = 1
			self.sonido_bicho.play()
			self.deselecciona_leccion()
			self.lecciones = self.leccion_muda
			if not self.interfaz.boton_muda in self.interfaz:
				self.interfaz.add(self.interfaz.boton_muda)

	def event_reproduccion(self, posicion=(0, 0)):
	# dejar ooteca
		if posicion != None:
			self.ootecas.add(Ooteca(self, posicion=posicion))
			self.set_mensaje(texto="Hay nuevas ootecas en el habitat.")

		if self.reproduccion == 0:
		# self.reproduccion es para verificar si se ha visto la leccion.
		# la leccion se activa automaticamente la 1ª vez nada más y despues no se muestra automaticamente
		# para no molestar al usuario
			self.reproduccion = 1
			self.sonido_bicho.play()
			self.deselecciona_leccion()
			self.lecciones = self.leccion_reproduccion
			if not self.interfaz.boton_reproduccion in self.interfaz:
				self.interfaz.add(self.interfaz.boton_reproduccion)

	def event_end_game(self):
	# lectura perder
		self.sonido_bicho.play()
		self.deselecciona_leccion()
		self.leccion_generica.set_lectura(VG.LECTURAENDGAME)
		x = VG.RESOLUCION_MONITOR[0]/2 - self.leccion_generica.hoja_impresa.rect.w/5
		y = VG.RESOLUCION_MONITOR[1]/2 - self.leccion_generica.hoja_impresa.rect.h/2
		self.leccion_generica.set_posicion(punto=(x,y))
		self.lecciones = self.leccion_generica

	def event_plaga(self):
	# dejar exoesqueleto
		if self.plaga == 0:
			self.plaga = 1
			self.sonido_bicho.play()
			self.deselecciona_leccion()
			self.leccion_generica.set_lectura(VG.LECTURAPLAGA)
			x = VG.RESOLUCION_MONITOR[0]/2 - self.leccion_generica.hoja_impresa.rect.w/5
			y = VG.RESOLUCION_MONITOR[1]/2 - self.leccion_generica.hoja_impresa.rect.h/2
			self.leccion_generica.set_posicion(punto=(x,y))
			self.lecciones = self.leccion_generica
			if not self.interfaz.boton_plaga in self.interfaz:
				self.interfaz.add(self.interfaz.boton_plaga)

	def get_leccion_muerte(self):
	# La lección sobre la muerte 
		libreta = Libreta_de_Lectura(VG.LECTURAMUERTE)
		x = VG.RESOLUCION_MONITOR[0]/2 - libreta.hoja_impresa.rect.w/5
		y = VG.RESOLUCION_MONITOR[1]/2 - libreta.hoja_impresa.rect.h/2
		libreta.set_posicion(punto=(x,y))

		muertea = pygame.sprite.Sprite()
		muertea.image = pygame.transform.scale(pygame.image.load(VG.MUERTE), (400,252)).convert_alpha()
		muertea.rect = muertea.image.get_rect()
		
		y = (VG.RESOLUCION_MONITOR[1]/2) - (muertea.rect.h/2)
		x = libreta.hoja_impresa.rect.x - muertea.rect.w - 20
		muertea.rect.x, muertea.rect.y = x, y
		y = muertea.rect.y + muertea.rect.h + 10
		
		# frame contenedor
		frame = pygame.sprite.Sprite()
		ancho = 10 + muertea.rect.w + 10
		altura = 10 + muertea.rect.h + 10
		x, y = muertea.rect.x - 10, muertea.rect.y - 10
		jambutton = JAMBaseButton()
		frame.image = jambutton.get_surface(color_relleno=(255,255,255,1), color_borde=(0,0,0,1), tamanio_panel=(ancho,altura), grosor_borde=3)
		frame.rect = frame.image.get_rect()
		frame.rect.x, frame.rect.y = x, y

		libreta.add(frame)
		libreta.add(muertea)

		libreta.boton_cerrar.connect(callback=self.deselecciona_leccion, sonido_select=self.sonido_select)
		libreta.boton_leeme.connect(callback=self.lee, sonido_select=self.sonido_select)
		return libreta

	def get_leccion_cilo_vital(self):
	# La lección sobre el ciclo vital
		libreta = Libreta_de_Lectura(VG.LECTURACICLOVITAL)
		x = VG.RESOLUCION_MONITOR[0]/2 - libreta.hoja_impresa.rect.w/5
		y = VG.RESOLUCION_MONITOR[1]/2 - libreta.hoja_impresa.rect.h/2
		libreta.set_posicion(punto=(x,y))
		
		cicloa = pygame.sprite.Sprite()
		cicloa.image = pygame.transform.scale(pygame.image.load(VG.CICLO1), (400,398)).convert_alpha()
		cicloa.rect = cicloa.image.get_rect()
		
		ciclob = pygame.sprite.Sprite()
		ciclob.image = pygame.transform.scale(pygame.image.load(VG.CICLO2), (400,270)).convert_alpha()
		ciclob.rect = ciclob.image.get_rect()
		
		y = VG.RESOLUCION_MONITOR[1]/2 - (cicloa.rect.h + 10 + ciclob.rect.h)/2
		x = libreta.hoja_impresa.rect.x - cicloa.rect.w - 20
		cicloa.rect.x, cicloa.rect.y = x, y
		y = cicloa.rect.y + cicloa.rect.h + 10
		ciclob.rect.x, ciclob.rect.y = x, y
		
		# frame contenedor
		frame = pygame.sprite.Sprite()
		ancho = 10 + cicloa.rect.w + 10
		altura = 10 + cicloa.rect.h + 10 + ciclob.rect.h + 10
		x, y = cicloa.rect.x - 10, cicloa.rect.y - 10
		jambutton = JAMBaseButton()
		frame.image = jambutton.get_surface(color_relleno=(255,255,255,1), color_borde=(0,0,0,1), tamanio_panel=(ancho,altura), grosor_borde=3)
		frame.rect = frame.image.get_rect()
		frame.rect.x, frame.rect.y = x, y

		libreta.add(frame)
		libreta.add(cicloa)
		libreta.add(ciclob)

		libreta.boton_cerrar.connect(callback=self.deselecciona_leccion, sonido_select=self.sonido_select)
		libreta.boton_leeme.connect(callback=self.lee, sonido_select=self.sonido_select)
		return libreta

	def get_leccion_reproduccion(self):
	# La lección sobre reproducción
		libreta = Libreta_de_Lectura(VG.LECTURAREPRODUCCION)
		x = VG.RESOLUCION_MONITOR[0]/2 - libreta.hoja_impresa.rect.w/5
		y = VG.RESOLUCION_MONITOR[1]/2 - libreta.hoja_impresa.rect.h/2
		libreta.set_posicion(punto=(x,y))

		reproa = pygame.sprite.Sprite()
		reproa.image = pygame.transform.scale(pygame.image.load(VG.REPRODUCCION1), (400,250)).convert_alpha()
		reproa.rect = reproa.image.get_rect()

		reprob = pygame.sprite.Sprite()
		reprob.image = pygame.transform.scale(pygame.image.load(VG.REPRODUCCION2), (400,248)).convert_alpha()
		reprob.rect = reprob.image.get_rect()

		y = VG.RESOLUCION_MONITOR[1]/2 - (reproa.rect.h + 10 + reprob.rect.h)/2
		x = libreta.hoja_impresa.rect.x - reproa.rect.w - 20
		reproa.rect.x, reproa.rect.y = x, y
		y = reproa.rect.y + reproa.rect.h + 10
		reprob.rect.x, reprob.rect.y = x, y

		# frame contenedor
		frame = pygame.sprite.Sprite()
		ancho = 10 + reproa.rect.w + 10
		altura = 10 + reproa.rect.h + 10 + reprob.rect.h + 10
		x, y = reproa.rect.x - 10, reproa.rect.y - 10
		jambutton = JAMBaseButton()
		frame.image = jambutton.get_surface(color_relleno=(255,255,255,1), color_borde=(0,0,0,1), tamanio_panel=(ancho,altura), grosor_borde=3)
		frame.rect = frame.image.get_rect()
		frame.rect.x, frame.rect.y = x, y

		libreta.add(frame)
		libreta.add(reproa)
		libreta.add(reprob)

		libreta.boton_cerrar.connect(callback=self.deselecciona_leccion, sonido_select=self.sonido_select)
		libreta.boton_leeme.connect(callback=self.lee, sonido_select=self.sonido_select)
		return libreta

	def get_leccion_muda(self):
	# Leccion Muda de Exoesqueleto
		libreta = Libreta_de_Lectura(VG.LECTURAMUDA)
		x = VG.RESOLUCION_MONITOR[0]/2 - libreta.hoja_impresa.rect.w/5
		y = VG.RESOLUCION_MONITOR[1]/2 - libreta.hoja_impresa.rect.h/2
		libreta.set_posicion(punto=(x,y))

		secuencia = Secuencia_muda()
		mudaa = pygame.sprite.Sprite()
		mudaa.image = pygame.transform.scale(pygame.image.load(VG.MUDA1), (400,192)).convert_alpha()
		mudaa.rect = mudaa.image.get_rect()
		mudab = pygame.sprite.Sprite()
		mudab.image = pygame.transform.scale(pygame.image.load(VG.MUDA2), (400,140)).convert_alpha()
		mudab.rect = mudab.image.get_rect()

		y = VG.RESOLUCION_MONITOR[1]/2 - (secuencia.rect.h + 10 + mudaa.rect.h + 10 + mudab.rect.h)/2
		x = libreta.hoja_impresa.rect.x - secuencia.rect.w - 20
		secuencia.rect.x, secuencia.rect.y = x, y
		y = secuencia.rect.y + secuencia.rect.h + 10
		mudaa.rect.x, mudaa.rect.y = x, y
		y = mudaa.rect.y + mudaa.rect.h + 10
		mudab.rect.x, mudab.rect.y = x, y

		# frame contenedor
		frame = pygame.sprite.Sprite()
		ancho = 10 + secuencia.rect.w + 10
		altura = 10 + secuencia.rect.h + 10 + mudaa.rect.h + 10 + mudab.rect.h + 10
		x, y = secuencia.rect.x - 10, secuencia.rect.y - 10
		jambutton = JAMBaseButton()
		frame.image = jambutton.get_surface(color_relleno=(255,255,255,1), color_borde=(0,0,0,1), tamanio_panel=(ancho,altura), grosor_borde=3)
		frame.rect = frame.image.get_rect()
		frame.rect.x, frame.rect.y = x, y

		libreta.add(frame)
		libreta.add(secuencia)
		libreta.add(mudaa)
		libreta.add(mudab)
		libreta.boton_cerrar.connect(callback=self.deselecciona_leccion, sonido_select=self.sonido_select)
		libreta.boton_leeme.connect(callback=self.lee, sonido_select=self.sonido_select)
		return libreta

	def get_leccion_generica(self):
	# La lección sobre reproducción
		libreta = Libreta_de_Lectura(" ")
		x = VG.RESOLUCION_MONITOR[0]/2 - libreta.hoja_impresa.rect.w/5
		y = VG.RESOLUCION_MONITOR[1]/2 - libreta.hoja_impresa.rect.h/2
		libreta.set_posicion(punto=(x,y))
		libreta.boton_cerrar.connect(callback=self.deselecciona_leccion, sonido_select=self.sonido_select)
		libreta.boton_leeme.connect(callback=self.lee, sonido_select=self.sonido_select)
		return libreta

	def deselecciona_leccion(self):
	# deselecciona cualquier leccion que se este ejecutando para detenerla
		pygame.event.clear()
		self.lecciones.clear(self.ventana, self.fondo)
		self.lecciones = pygame.sprite.OrderedUpdates()
		pygame.display.update()

	def selecciona_mensaje_salir(self):
		pygame.event.clear()
		self.deselecciona_leccion()
		self.lecciones = self.dialog_cerrar
	def selecciona_mensaje_guardar(self):
		pygame.event.clear()
		self.deselecciona_leccion()
		self.lecciones = self.dialog_guardar

	def guardar_juego(self):
		pygame.event.clear()
		base = self.cucarasims.base_de_datos
		datos = self.get_datos_para_guardar()
		self.cucarasims.Archivos_y_Directorios.guardar(base=base, datos=datos)
		self.salir()

	def get_datos_para_guardar(self):
		datos_de_juego = [self.anios, self.dias, self.horas, self.puntos]
		bichos = []
		for bicho in self.Bichos.sprites():
			sexo = bicho.sexo
			anios = bicho.anios
			dias = bicho.dias
			horas = bicho.horas
			hambre = bicho.hambre
			sed = bicho.sed
			dato_bicho = [sexo, anios, dias, horas, hambre, sed]

			bichos.append(dato_bicho)

		ootecas = []
		for ooteca in self.ootecas.sprites():
			dias = ooteca.dias
			horas = ooteca.horas
			huevos = ooteca.huevos
			dato_ooteca = [dias, horas, huevos]
			ootecas.append(dato_ooteca)

		datos = (datos_de_juego, bichos, ootecas)
		return datos

	def selecciona_leccion_extra(self):
	# para conectar al boton de la leccion correspondiente
		pygame.event.clear()
		self.sonido_bicho.play()
		self.deselecciona_leccion()
		self.leccion_generica.set_lectura(VG.LECTURASEXTRAS)
		x = VG.RESOLUCION_MONITOR[0]/2 - self.leccion_generica.hoja_impresa.rect.w/5
		y = VG.RESOLUCION_MONITOR[1]/2 - self.leccion_generica.hoja_impresa.rect.h/2
		self.leccion_generica.set_posicion(punto=(x,y))
		self.lecciones = self.leccion_generica

	def selecciona_leccion_plaga(self):
	# para conectar al boton de la leccion correspondiente
		pygame.event.clear()
		plaga = self.plaga
		self.deselecciona_leccion()
		self.plaga = 0
		self.event_plaga()
		self.plaga = plaga # para devolverlo al estado inicial

	def selecciona_leccion_muerte(self):
	# para conectar al boton de la leccion correspondiente
		pygame.event.clear()
		muertes = self.muertes
		self.deselecciona_leccion()
		self.muertes = 0
		self.event_morir(leccion=True)
		self.muertes = muertes # para devolverlo al estado inicial

	def selecciona_leccion_ciclo(self):
	# para conectar al boton de la leccion correspondiente
		pygame.event.clear()
		nacimientos = self.nacimientos
		self.deselecciona_leccion()
		self.nacimientos = 0
		self.event_nacer(leccion=True)
		self.nacimientos = nacimientos # para devolverlo al estado inicial

	def selecciona_leccion_muda(self):
	# para conectar al boton de la leccion correspondiente
		pygame.event.clear()
		mudas = self.secuencia_muda
		self.deselecciona_leccion()
		self.secuencia_muda = 0
		self.event_muda()
		self.secuencia_muda = mudas # para devolverlo al estado inicial

	def selecciona_leccion_reproduccion(self):
	# para conectar al boton de la leccion correspondiente
		pygame.event.clear()
		reproduccion = self.reproduccion
		self.deselecciona_leccion()
		self.reproduccion = 0
		self.event_reproduccion(posicion=None)
		self.reproduccion = reproduccion # para devolverlo al estado inicial

	def set_tiempo_de_juego(self):
	# calculos vitales de tiempo
		self.tiempo_de_juego += 1
		cambios = False
		if self.tiempo_de_juego == self.velocidad_juego:
			self.horas += 1
			self.tiempo_de_juego = 0
			for bicho in self.Bichos.sprites():
				bicho.set_tiempo_de_vida()
			for ooteca in self.ootecas.sprites():
				ooteca.set_tiempo_de_vida()
			for cadaver in self.cadaveres.sprites():
				cadaver.set_tiempo_de_vida()
			cambios = True

		if self.horas == 1:
			# ************************************* #
			self.machos, self.hembras = self.verificar_sexos_en_habitat()
			total = self.machos + self.hembras
			ootecas = len(self.ootecas.sprites())
			bichos = "Cucarachas: %s, Machos: %s, Hembras: %s, Ootecas: %s Migración: %s" % (total, self.machos, self.hembras, ootecas, self.puntos)
			self.interfaz.set_informacion_de_habitat(bichos)

			if not self.machos and not ootecas:
				self.set_mensaje(texto="No quedan Machos ni ootecas en el habitat, la Reproducción ya no será posible.")
			elif not self.hembras and not ootecas:
				self.set_mensaje(texto="No quedan Hembras ni ootecas en el habitat, la Reproducción ya no será posible.")
			elif not self.machos and not self.hembras and not ootecas:
				self.set_mensaje(texto="Todas las Cucarachas han muerto y no hay ootecas en el habitat.")
			elif self.machos + self.hembras >= self.maximo_cucas:
				self.event_plaga()
				self.set_mensaje(texto="Hay Demasiadas Cucarachas en el habitat. Algunas migrarán. !!!")
			# ************************************* #
		if self.horas == 24:
			self.dias += 1
			self.horas = 0
			self.aumenta_hambre()
			self.aumenta_sed()

		if self.dias == 365:
			self.anios += 1
			self.dias = 0

		if cambios:
			tiempo = "Tiempo de Juego = Años: %s Dias: %s Horas: %s" % (self.anios, self.dias, self.horas)
			self.interfaz.set_tiempo_de_juego(tiempo)

	def aumenta_hambre(self):
	# cada 24 horas aumenta el hambre de los bichos
		for bicho in self.Bichos.sprites():
			bicho.hambre -= VG.AUMENTAHAMBRE
	def aumenta_sed(self):
	# cada 24 horas aumenta la sed de los bichos
		for bicho in self.Bichos.sprites():
			bicho.sed -= VG.AUMENTASED

	# ------------------------------- CONFIGURACIONES ------------------------------------------------ #
	def setup_event(self):
		pygame.display.set_caption("CucaraSims (Versión 1)")

		# Captura de Eventos
		pygame.event.set_blocked([JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP, JOYBUTTONDOWN,
					KEYUP, VIDEORESIZE, VIDEOEXPOSE, USEREVENT, QUIT, ACTIVEEVENT]) # bloqueados
		pygame.event.set_allowed([MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN, KEYDOWN]) # permitidos
		pygame.mouse.set_visible(True)

	def setup1(self):
	# configuraciones y precarga de imágenes
		if not self.sonido_select: self.sonido_select = pygame.mixer.Sound("CeibalJAM_Lib/select.ogg")
		if not self.area_visible: self.area_visible = pygame.Rect(35,35,VG.RESOLUCION_MONITOR[0]-70,VG.RESOLUCION_MONITOR[1]-70)
		if not self.reloj: self.reloj = pygame.time.Clock()
		if not self.fondo: self.fondo = self.get_fondo()
		if not self.imagenes_bicho:
			self.imagenes_bicho = [pygame.transform.rotate(pygame.image.load(VG.CUCARACHA1), -90),
			pygame.transform.rotate(pygame.image.load(VG.CUCARACHA2), -90),
			pygame.transform.rotate(pygame.image.load(VG.CUCARACHA3), -90),
			pygame.transform.rotate(pygame.image.load(VG.CUCARACHA4), -90)]
		self.nivel_carga += 1
		#def setup2(self):
		if not self.sonido_bicho: self.sonido_bicho = pygame.mixer.Sound(VG.SONIDOCUCARACHA)
		if not self.puntero: self.puntero = pygame.sprite.OrderedUpdates()
		if not self.pan_select: self.pan_select = Puntero(1)
		if not self.agua_select: self.agua_select = Puntero(2)
		if not self.interfaz:
			self.interfaz = Interfaz()
			self.interfaz.boton_pan.connect(callback=self.get_pan, sonido_select=self.sonido_select)
			self.interfaz.boton_jarra.connect(callback=self.get_agua, sonido_select=self.sonido_select)
			self.interfaz.boton_muda.connect(callback=self.selecciona_leccion_muda, sonido_select=self.sonido_select)
			self.interfaz.boton_reproduccion.connect(callback=self.selecciona_leccion_reproduccion, sonido_select=self.sonido_select)
			self.interfaz.boton_ciclo.connect(callback=self.selecciona_leccion_ciclo, sonido_select=self.sonido_select)
			self.interfaz.boton_muerte.connect(callback=self.selecciona_leccion_muerte, sonido_select=self.sonido_select)
			self.interfaz.boton_plaga.connect(callback=self.selecciona_leccion_plaga, sonido_select=self.sonido_select)
			self.interfaz.boton_musica.connect(callback=self.set_pause_musica, sonido_select=self.sonido_select)
			self.interfaz.boton_extras.connect(callback=self.selecciona_leccion_extra, sonido_select=self.sonido_select)
			self.interfaz.boton_salir.connect(callback=self.selecciona_mensaje_salir, sonido_select=self.sonido_select)
		self.nivel_carga += 1
		#def setup3(self):
		# Carga de Lecciones
		if not self.lecciones: self.lecciones = pygame.sprite.OrderedUpdates()
		if not self.leccion_muda: self.leccion_muda = self.get_leccion_muda()
		if not self.leccion_generica: self.leccion_generica = self.get_leccion_generica()
		if not self.leccion_reproduccion: self.leccion_reproduccion = self.get_leccion_reproduccion()
		if not self.leccion_ciclo_vital: self.leccion_ciclo_vital = self.get_leccion_cilo_vital()
		if not self.leccion_muerte: self.leccion_muerte = self.get_leccion_muerte()
		self.nivel_carga += 1
		#def setup4(self):
		if not self.alimento: self.alimento = pygame.sprite.OrderedUpdates()		
		if not self.mensajes: self.mensajes = pygame.sprite.OrderedUpdates()
		if not self.mensajes_emergentes: self.mensajes_emergentes = Mensaje(self)
		if not self.cadaveres: self.cadaveres = pygame.sprite.OrderedUpdates()
		if not self.ootecas: self.ootecas = pygame.sprite.OrderedUpdates()
		if not self.unidad_alimento: self.unidad_alimento = Alimento(self.interfaz)
		if not self.agua: self.agua = pygame.sprite.OrderedUpdates()
		if not self.unidad_agua: self.unidad_agua = Agua(self.interfaz)
		if not self.Bichos: self.Bichos = pygame.sprite.OrderedUpdates()
		if not self.ficha_bicho: self.ficha_bicho = Ficha_Bicho()
		if not self.ficha: self.ficha = pygame.sprite.OrderedUpdates()

		if not self.dialog_cerrar:
			self.dialog_cerrar = JAMDialog(mensaje="¿Deseas Salir del Juego?", resolucion_monitor=VG.RESOLUCION_MONITOR)
			self.dialog_cerrar.boton_aceptar.connect(callback=self.selecciona_mensaje_guardar, sonido_select=self.sonido_select)
			self.dialog_cerrar.boton_cancelar.connect(callback=self.deselecciona_leccion, sonido_select=self.sonido_select)
		if not self.dialog_guardar:
			self.dialog_guardar = JAMDialog(mensaje="¿Guardar Antes de Salir?", resolucion_monitor=VG.RESOLUCION_MONITOR)
			self.dialog_guardar.boton_aceptar.connect(callback=self.guardar_juego, sonido_select=self.sonido_select)
			self.dialog_guardar.boton_cancelar.connect(callback=self.Borrar_salir, sonido_select=self.sonido_select)
		self.nivel_carga += 1

	def lee(self):
	# Sobreescritura de un método de la libreta de lecciones
		if pygame.mixer.music.get_busy():
			self.set_pause_musica()
		pygame.mixer.quit()
		textbuffer = ""
		for elem in self.lecciones.lectura[self.lecciones.indice_pagina_actual]:
			textbuffer += (" " + elem)
		self.lecciones.motor_de_voz.lee(textbuffer)
		pygame.mixer.init()
		self.set_pause_musica()

	def get_agua(self):
	# imagen pan para el puntero del mouse al seleccionar alimento
		imagen = bool(self.puntero.sprites())
		if imagen:
			self.puntero.empty()
			pygame.mouse.set_visible(True)
		elif not imagen:
			self.puntero.add(self.agua_select)
			pygame.mouse.set_visible(False)
	
	def get_pan(self):
	# imagen pan para el puntero del mouse al seleccionar alimento
		imagen = bool(self.puntero.sprites())
		if imagen:
			self.puntero.empty()
			pygame.mouse.set_visible(True)
		elif not imagen:
			self.puntero.add(self.pan_select)
			pygame.mouse.set_visible(False)

	def get_fondo(self, color=(200,200,200,1), tamanio=VG.RESOLUCION_MONITOR):
	# devuelve una superficie de color para el fondo de la ventana
		superficie = pygame.transform.scale(pygame.image.load(VG.FONDO), (VG.RESOLUCION_MONITOR))
		return superficie

	def handle_event(self):
	# Eventos del Teclado
		if pygame.event.get(pygame.MOUSEBUTTONDOWN):
			if self.pan_select in list(self.puntero):
			# si tenemos seleccionado el alimento dejar el pan en el escenario
				if not bool(self.alimento.sprites()):
					self.unidad_alimento.cantidad = VG.UNIDADALIMENTO
					self.unidad_alimento.rect.center = pygame.mouse.get_pos()
					self.alimento.add(self.unidad_alimento)
					self.puntero.empty()
					pygame.mouse.set_visible(True)
					self.set_mensaje(texto="Las Cucarachas detectan con sus antenas, el alimento en el habitat.")
			elif self.agua_select in list(self.puntero):
			# si tenemos seleccionado el agua, dejar el agua en el escenario
				if not bool(self.agua.sprites()):
					self.unidad_agua.cantidad = VG.UNIDADAGUA
					self.unidad_agua.rect.center = pygame.mouse.get_pos()
					self.agua.add(self.unidad_agua)
					self.puntero.empty()
					pygame.mouse.set_visible(True)
					self.set_mensaje(texto="Las Cucarachas detectan con sus antenas, el agua en el habitat.")

			elif not self.pan_select in list(self.puntero) and not self.agua_select in list(self.puntero):
			# si no tenemos seleccionado el alimento, vemos si se ha seleccionado alguna cuca
				posicion = pygame.mouse.get_pos()
				bicho_select = None
				for bicho in self.Bichos.sprites():
					if bicho.rect.collidepoint(posicion):
					# cuando seleccionamos una cucaracha
						bicho.play_sonido_bicho()
						bicho_select = bicho
				if bicho_select:
					self.ficha_bicho.set_bicho(bicho_select)
					self.ficha = self.ficha_bicho
				else:
					self.ficha_bicho.bicho = None
					self.ficha.clear(self.ventana, self.fondo)
					self.ficha = pygame.sprite.OrderedUpdates()

		for event in pygame.event.get():
			teclas = pygame.key.get_pressed()
			if teclas[pygame.K_ESCAPE]:
				self.selecciona_mensaje_salir()
				pygame.event.clear()
				return

		pygame.event.clear()

	def salir(self):
		pygame.event.clear()
		self.cucarasims.nivel = "Menu"
		self.nivel = None
		self.deselecciona_leccion()
		#return self.cucarasims.RunMenu() # no es necesario, sale solo por valor de nivel

	def Borrar_salir(self):
		# Si no hay datos borra la base
		pygame.event.clear()
		self.cucarasims.Archivos_y_Directorios.verifica(base_abrir=self.cucarasims.base_de_datos)
		self.salir()

class Agua(pygame.sprite.Sprite):
# Agua en el escenario, recibe interfaz para informar de los cambios segun consumo
	def __init__(self, interfaz):
		pygame.sprite.Sprite.__init__(self)

		self.interfaz = interfaz
		self.cantidad = 0
		self.ultima_cantidad = 0
		imagen_original = pygame.transform.scale(pygame.image.load(VG.AGUA), (40,30)).convert_alpha()

		self.imagen1 =  imagen_original.copy()
		self.imagen2 =  pygame.transform.scale(imagen_original.copy(), (30,20)).convert_alpha()
		self.imagen3 =  pygame.transform.scale(imagen_original.copy(), (20,10)).convert_alpha()

		self.image = self.imagen1
		self.rect = self.image.get_rect()

	def update(self):
		parte = VG.UNIDADAGUA/3
		if self.cantidad >= parte * 2:
			if self.image != self.imagen1: 
				self.image = self.imagen1
		if self.cantidad >= parte and self.cantidad < parte * 2:
			if self.image != self.imagen2:
				self.image = self.imagen2
		if self.cantidad > 0 and self.cantidad < parte:
			if self.image != self.imagen3:
				self.image = self.imagen3

		# informa sobre la cantidad de agua que hay en el escenario
		if self.ultima_cantidad != self.cantidad:
			self.interfaz.set_agua_en_escenario(self.cantidad)

		self.ultima_cantidad = self.cantidad

class Alimento(pygame.sprite.Sprite):
# Alimento en el escenario, recibe interfaz para informar de los cambios segun consumo
	def __init__(self, interfaz):
		pygame.sprite.Sprite.__init__(self)

		self.interfaz = interfaz
		self.cantidad = 0
		self.ultima_cantidad = 0
		imagen_original = pygame.transform.scale(pygame.image.load(VG.PAN), (40,30)).convert_alpha()

		self.imagen1 =  imagen_original.copy()
		self.imagen2 =  imagen_original.copy().subsurface(0,0,27,30)
		self.imagen3 =  imagen_original.copy().subsurface(0,0,13,30)

		self.image = self.imagen1
		self.rect = self.image.get_rect()

	def update(self):
		parte = VG.UNIDADALIMENTO/3
		if self.cantidad >= parte*2:
			if self.image != self.imagen1: 
				self.image = self.imagen1
		if self.cantidad >= parte and self.cantidad < parte*2:
			if self.image != self.imagen2:
				self.image = self.imagen2
		if self.cantidad > 0 and self.cantidad < parte:
			if self.image != self.imagen3:
				self.image = self.imagen3

		# informa sobre la cantidad de alimento que hay en el escenario
		if self.ultima_cantidad != self.cantidad:
			self.interfaz.set_pan_en_escenario(self.cantidad)

		self.ultima_cantidad = self.cantidad

class Puntero(pygame.sprite.Sprite):
# El puntero del mouse, pan o agua
	def __init__(self, tipo):
		pygame.sprite.Sprite.__init__(self)

		self.tipo = tipo

		if self.tipo == 1:
		# pan seleccionado
			self.image =  pygame.transform.scale(pygame.image.load(VG.PAN), (40,30)).convert_alpha()
		elif self.tipo == 2:
		# agua seleccionada
			self.image =  pygame.transform.scale(pygame.image.load(VG.AGUA), (40,30)).convert_alpha()
		self.rect = self.image.get_rect()

	def update(self):
		self.rect.center = pygame.mouse.get_pos()

class Secuencia_muda(pygame.sprite.Sprite):
# Secuencia de imagenes sobre muda
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.lista_de_imagenes = self.get_imagenes()
		self.indice = 0
		self.image = self.lista_de_imagenes[self.indice]
		self.rect = self.image.get_rect()

	def get_imagenes(self):
		lista = []
		for archivo in os.listdir(VG.MUDAS):
			imagen = pygame.transform.scale(pygame.image.load(VG.MUDAS + archivo), (400,360)).convert_alpha()
			lista.append(imagen)
		return lista

	def update(self):
		self.image = self.lista_de_imagenes[self.indice]
		if len(self.lista_de_imagenes)-1 > self.indice:
			self.indice += 1
		else:
			self.indice = 0

class Ooteca(pygame.sprite.Sprite):
# Ootecas
	def __init__(self, juego, posicion=(0,0)):
		pygame.sprite.Sprite.__init__(self)
	
		self.juego = juego
		self.dias = 0
		self.horas = 0
		huevos = [1, 2, 3]
		random.seed()
		self.huevos = random.choice(huevos)
		self.image = pygame.image.load(VG.OOTECA).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = posicion

	def set_tiempo_de_vida(self):
		self.horas += 1
		if self.horas == 24:
			self.dias += 1
			self.horas = 0
		if self.dias == VG.NACER:
			# nacimiento 30 dias de incubacion
			for huevo in range(self.huevos):
				self.juego.event_nacer()
			self.kill() # la ooteca desaparece

class Cadaver(pygame.sprite.Sprite):
# Cadaver
	def __init__(self, juego, posicion=(0,0), dias=0):
		pygame.sprite.Sprite.__init__(self)
	
		self.juego = juego
		self.dias = 0
		self.horas = 0

		if dias <= VG.DIASMUDAS[0]:
			escala = (53,63)
		elif dias >= VG.DIASMUDAS[0] and dias < VG.DIASMUDAS[1]:
			escala = VG.ESCALASMUDAS[0]
		elif dias >= VG.DIASMUDAS[1] and dias < VG.DIASMUDAS[2]:
			escala = VG.ESCALASMUDAS[1]
		elif dias >= VG.DIASMUDAS[2] and dias < VG.DIASMUDAS[3]:
			escala = VG.ESCALASMUDAS[2]
		elif dias >= VG.DIASMUDAS[3]:
			escala = VG.ESCALASMUDAS[3]

		self.image = pygame.transform.scale(pygame.image.load(VG.CADAVER), escala).convert_alpha()

		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = posicion

	def set_tiempo_de_vida(self):
		self.horas += 1
		if self.horas == 24:
			self.dias += 1
			self.horas = 0
		if self.dias == VG.DIASCADAVER:
			self.kill()

class Mensaje(pygame.sprite.OrderedUpdates):
# mensajes emergentes
	def __init__(self, juego):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.juego = juego
		self.texto = ""
		self.contador = 0
		self.etiqueta = JAMLabel ( imagen=None, texto="mensaje", tamanio_de_letra=40, color=(255,255,0,1) )
		self.add(self.etiqueta)

	def set_mensaje(self, texto):
		self.texto = texto
		self.etiqueta.set_text(texto=texto)
		self.set_posicion()

	def set_posicion(self):
		x = VG.RESOLUCION_MONITOR[0]/2 - self.etiqueta.rect.w/2
		y = VG.RESOLUCION_MONITOR[1] - 40 - self.etiqueta.rect.h
		self.etiqueta.set_posicion((x,y))

	def update(self):
	# Aparece y desaparece automáticamente al cabo de cierto tiempo
		if self.juego.mensajes == self:
			self.contador += 1
			if self.contador == 100:
				self.contador = 0
				self.juego.no_mensajes()
				return
