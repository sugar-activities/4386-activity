#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMDialog.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM! - Uruguay - Plan Ceibal
#
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

from JAMButton import JAMButton, JAMLabel
from JAMFrame import JAMFrame

class JAMDialog(pygame.sprite.OrderedUpdates):
	def __init__(self, mensaje="JAMDialog", resolucion_monitor=(1024,768)):
		pygame.sprite.OrderedUpdates.__init__(self)

		self.resolucion_monitor = resolucion_monitor
		separador = 20

		# Etiqueta con mensaje
		self.label = JAMLabel(texto=mensaje, tamanio_de_letra=50)
		(x,y) = (self.resolucion_monitor[0]/2 - self.label.rect.w/2, self.resolucion_monitor[1]/2 - self.label.rect.h/2)
		self.posicion_label = (x,y)
		self.label.set_posicion(self.posicion_label)

		# Boton Aceptar
		(x,y) = (x + separador, y + self.label.rect.h + separador)
		self.tamanio_botones = (self.label.rect.w/3, self.label.rect.h)

		self.boton_aceptar = JAMButton(texto="Aceptar", tamanio_de_letra=30, tamanio_panel=self.tamanio_botones)
		self.posicion_boton_aceptar = (x,y)
		self.boton_aceptar.set_posicion(punto=self.posicion_boton_aceptar)

		# Boton Cancelar
		(x,y) = (self.label.rect.x + self.label.rect.w - separador - self.boton_aceptar.rect.w, y)

		self.boton_cancelar = JAMButton(texto="Cancelar", tamanio_de_letra=30, tamanio_panel=self.tamanio_botones)
		self.posicion_boton_cancelar = (x,y)
		self.boton_cancelar.set_posicion(punto=self.posicion_boton_cancelar)

		# Frame interno
		self.tamanio_frame_interno = (self.label.rect.w + separador, separador + self.label.rect.h + separador + self.boton_aceptar.rect.h + separador)
		self.frame1 = JAMFrame(color_borde=(0,0,0,1), grosor_borde=3, color_relleno=(255,190,0,1), tamanio=self.tamanio_frame_interno)
		self.posicion_frame_interno = (self.posicion_label[0] - separador/2, self.posicion_label[1] - separador)
		self.frame1.set_posicion(punto=self.posicion_frame_interno)

		# Frame externo
		self.tamanio_frame_externo = (self.tamanio_frame_interno[0]+separador*2,self.tamanio_frame_interno[1]+separador*2)
		self.frame2 = JAMFrame(color_borde=(0,0,0,1), grosor_borde=6, color_relleno=(255,255,255,1), tamanio=self.tamanio_frame_externo)
		self.posicion_frame_externo = (self.posicion_frame_interno[0]-separador, self.posicion_frame_interno[1] - separador)
		self.frame2.set_posicion(punto=self.posicion_frame_externo)

		self.add(self.frame2)
		self.add(self.frame1)
		self.add(self.label)
		self.add(self.boton_aceptar)
		self.add(self.boton_cancelar)
