#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Interfaz.py por:
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

class Interfaz(pygame.sprite.OrderedUpdates):
# botones en barra lateral
	def __init__(self):
		pygame.sprite.OrderedUpdates.__init__(self)

		separador = 10

		# para dar de comer
		self.boton_pan = JAMButton(imagen=VG.PAN, texto=None)
		ancho_botones = self.boton_pan.rect.w
		self.boton_jarra = JAMButton(imagen=VG.JARRA, texto=None)

		x = VG.RESOLUCION_MONITOR[0] - separador - ancho_botones
		y = separador

		self.boton_pan.set_posicion(punto=(x,y))
		y += self.boton_pan.rect.h + separador
		self.boton_jarra.set_posicion(punto=(x,y))

		y += self.boton_jarra.rect.h + separador*2
		self.boton_ciclo = JAMButton(texto="Ciclo Vital", tamanio_de_letra=20, tamanio_panel=(ancho_botones,50))
		self.boton_ciclo.set_posicion(punto=(x,y))

		y += self.boton_ciclo.rect.h + separador
		self.boton_muda = JAMButton(texto="Muda", tamanio_de_letra=20, tamanio_panel=(ancho_botones,50))
		self.boton_muda.set_posicion(punto=(x,y))

		y += self.boton_muda.rect.h + separador
		self.boton_reproduccion = JAMButton(texto="Reproducción", tamanio_de_letra=20, tamanio_panel=(ancho_botones,50))
		self.boton_reproduccion.set_posicion(punto=(x,y))

		y += self.boton_reproduccion.rect.h + separador
		self.boton_muerte = JAMButton(texto="Muerte", tamanio_de_letra=20, tamanio_panel=(ancho_botones,50))
		self.boton_muerte.set_posicion(punto=(x,y))

		y += self.boton_reproduccion.rect.h + separador
		self.boton_plaga = JAMButton(texto="Plaga", tamanio_de_letra=20, tamanio_panel=(ancho_botones,50))
		self.boton_plaga.set_posicion(punto=(x,y))

		self.boton_salir = JAMButton(texto="Salir", tamanio_de_letra=20, tamanio_panel=(ancho_botones,50))
		y = VG.RESOLUCION_MONITOR[1] - separador - self.boton_salir.rect.h
		self.boton_salir.set_posicion(punto=(x,y))

		self.imagenes_audio = VG.ICONOSAUDIO
		self.boton_musica = JAMButton(texto=None, imagen=self.imagenes_audio[0], tamanio_panel=(ancho_botones,70))
		y = self.boton_salir.rect.y - separador - self.boton_musica.rect.h	
		self.boton_musica.set_posicion(punto=(x,y))
		self.posicion_boton_audio = (x,y)

		self.boton_extras = JAMButton(texto="Lectura", tamanio_de_letra=20, tamanio_panel=(ancho_botones,50))
		y = self.boton_musica.rect.y - separador - self.boton_extras.rect.h
		self.boton_extras.set_posicion(punto=(x,y))

		self.add(self.boton_pan)
		self.add(self.boton_jarra)
		self.add(self.boton_extras)
		self.add(self.boton_musica)
		self.add(self.boton_salir)

		# Etiquetas
		self.label_pan = JAMLabel(imagen=VG.PAN, tamanio_imagen=(40,30), texto="000", tamanio_de_letra=25)
		posicion = (0,0)
		self.label_pan.set_posicion((posicion))
		self.add(self.label_pan)

		self.label_agua = JAMLabel(imagen=VG.AGUA, tamanio_imagen=(40,30), texto="000", tamanio_de_letra=25)
		posicion = (100,0)
		self.label_agua.set_posicion((posicion))
		self.add(self.label_agua)

		self.label_tiempo = JAMLabel(imagen=None, texto="Tiempo de Juego = Años: 0 Dias: 0 Horas: 0", tamanio_de_letra=25)
		posicion = (200,0)
		self.label_tiempo.set_posicion((posicion))
		self.add(self.label_tiempo)

		self.informacion_cucas = "Cucarachas: 0, Machos: 0, Hembras: 0, Ootecas: 0, Migración: 0"
		self.label_cucas_info = JAMLabel(imagen=None, texto=self.informacion_cucas, tamanio_de_letra=25)
		x = 10
		y = VG.RESOLUCION_MONITOR[1] - 10 - self.label_cucas_info.rect.h
		posicion = (x, y)
		self.label_cucas_info.set_posicion(posicion)
		self.add(self.label_cucas_info)

	def set_pan_en_escenario(self, cantidad):
		self.label_pan.set_text(texto=cantidad)
		posicion = (0,0)
		self.label_pan.set_posicion(posicion)

	def set_agua_en_escenario(self, cantidad):
		self.label_agua.set_text(texto=cantidad)
		posicion = (100,0)
		self.label_agua.set_posicion(posicion)

	def set_tiempo_de_juego(self, tiempo):
		self.label_tiempo.set_text(texto=tiempo)
		posicion = (200,0)
		self.label_tiempo.set_posicion(posicion)

	def set_informacion_de_habitat(self, bichos):
		if self.informacion_cucas != bichos:
			self.informacion_cucas = bichos
			self.label_cucas_info.set_text(texto=self.informacion_cucas)
			x = 10
			y = VG.RESOLUCION_MONITOR[1] - 10 - self.label_cucas_info.rect.h
			posicion = (x, y)
			self.label_cucas_info.set_posicion(posicion)


