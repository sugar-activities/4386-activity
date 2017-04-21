#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMFrame.py por:
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

# configuración default
TAMANIO = (200, 300)
GROSOR = 7
COLOR_RELLENO = (255, 255 , 255, 1)
COLOR_BORDE = (150, 150 , 150, 1)
#COLOR_TEXTO = (0,0,0,1)
MINI_BORDE = 2

MAGENTA  = (255, 0, 255) # usa en transparencia, no lo uses para pintar controles
from JAMButton import JAMBaseButton

# -------------------- INICIO DE la clase JAMFrame -------------------- #

class JAMFrame(pygame.sprite.OrderedUpdates):
# Un Botón en pygame
	def __init__(self, color_borde=COLOR_BORDE, grosor_borde=GROSOR, color_relleno=None, tamanio=TAMANIO):

		pygame.init()
		pygame.sprite.OrderedUpdates.__init__(self)

		# variables del panel
		self.color_borde = color_borde
		self.tamanio = tamanio
		self.grosor_borde = grosor_borde
		self.color_relleno = color_relleno

		self.panel = Panel(color_borde=self.color_borde, color_relleno=self.color_relleno, tamanio=self.tamanio, grosor_borde=self.grosor_borde)

		# grupo de sprit - widgets contenidos en el panel
		self.widgets = pygame.sprite.OrderedUpdates()

		# diccionario de widgets:(tamaño,posicion)
		self.dict_widgets_tamanio_posicion = {}

		# variables de alineación y escalado automático
		self.posicion = (0,0)
		self.tipo = "expand"
		self.alineacion = "izquierda"
		self.orientacion = "vertical"

		self.separador = GROSOR
		self.margen = MINI_BORDE

		self.add(self.panel)

	# -------------------- INICIO DE METODOS SETS -------------------- #
	def set_separador(self, separador=0):
		self.separador = separador
		self.set_automatic_expand(orientacion=self.orientacion, alineacion=self.alineacion)

	def set_colors_frame(self, color_borde=None, grosor_borde=None, color_relleno=None):
	# Setea bordes y relleno
		if color_borde != None:
			self.color_borde = color_borde

		if color_relleno != None:
			self.color_relleno = color_relleno
		if color_relleno == -1:
			self.color_relleno = None

		if grosor_borde != None and grosor_borde > -1:
			self.grosor_borde = grosor_borde

		self.panel.kill()
		self.empty()
		self.panel = Panel(color_borde=self.color_borde, color_relleno=self.color_relleno,
				tamanio=self.tamanio, grosor_borde=self.grosor_borde)

		self.add(self.panel)
		self.set_posicion(punto=self.posicion)

	def set_posicion(self, punto=(0,0)):
	# Setea la posición del Frame
		# revisar, los widgets se siguen dibujando bien
		# pero el area de captura del mouse se mantiene invariable.
		self.posicion = punto
		self.panel.set_posicion(punto=punto)

	def set_tamanio(self, tamanio=(0,0)):
	# Setea el tamaño del Frame
		if tamanio[0] > 20 and tamanio[1] > 20:
			self.tamanio = tamanio
			self.panel.kill()
			self.empty()
			self.panel = Panel(color_borde=self.color_borde, color_relleno=self.color_relleno,
				tamanio=self.tamanio, grosor_borde=self.grosor_borde)
			self.add(self.panel)
		self.set_posicion(punto=self.posicion)

	def agregar(self, JAMwidget=None, punto=(0,0)):
	# Agrega los JAMwidgets dentro del frame
		if JAMwidget in self.widgets:
			return
		elif JAMwidget != None:
			JAMwidget.set_posicion(punto=punto)
			# inicio - modificado 7-11-2010
			#rectangulo = (punto[0], punto[1], JAMwidget.rect.w, JAMwidget.rect.h)
			#JAMwidget.rect.clip(rectangulo)
			# fin - modificado 7-11-2010
			self.widgets.draw(self.panel.image)
			self.widgets.add(JAMwidget)

			# guardamos tamaño y posicion de los widget para controlar sus cambios en update()
			tamanio = (JAMwidget.rect.w, JAMwidget.rect.h)
			posicion = (JAMwidget.rect.x, JAMwidget.rect.y)
			self.dict_widgets_tamanio_posicion[JAMwidget] = (tamanio, posicion)

			if self.tipo == "expand":
			# El Frame se expande al ancho del widget con más ancho y toma la altura adecuada según los widgets contenidos.
				self.set_automatic_expand(orientacion=self.orientacion, alineacion=self.alineacion)
			elif self.tipo == "libre":
				return
			else:
				pass

	def set_automatic_expand(self, orientacion="vertical", alineacion="izquierda"):
	# El Frame se expande o contrae para que todos los widget queden dentro, visibles y alineados
		if orientacion == None or alineacion == None:
		# Sin orientacion ni alineación queda libre, no se controla ni tamaños ni posiciones.
			self.tipo = "libre"
			return
		else:
		# Si hay alineación u orientación, se interpreta que quieres "expand"
			self.tipo = "expand"
			if orientacion == "vertical" or orientacion == "horizontal":
				self.orientacion = orientacion
			if alineacion == "centro" or alineacion == "izquierda" or alineacion == "derecha":
				self.alineacion = alineacion

		if self.orientacion == "vertical":
		# Como un gtk.VBox
			# Calcula y obtiene el tamaño del frame
			tamanio_para_frame = self.get_dimension_frame_vertical()
			self.alineacion = alineacion
			self.orientacion = orientacion
			self.set_tamanio(tamanio=tamanio_para_frame)
			self.set_posicion(punto=self.posicion)
			# alinea los widgets para frame vertical
			self.set_vertical_aling(alineacion=self.alineacion)

		elif self.orientacion == "horizontal":
		# Como un gtk.HBox
			# Calcula y obtiene el tamaño del frame
			tamanio_para_frame = self.get_dimension_frame_horizontal()
			self.alineacion = alineacion
			self.orientacion = orientacion
			self.set_tamanio(tamanio=tamanio_para_frame)
			self.set_posicion(punto=self.posicion)
			# alinea los widgets para frame vertical
			self.set_horizontal_aling(alineacion=self.alineacion)
			pass
		else:
			pass


# -------------------- FIN DE METODOS SETS -------------------- #

# -------------------- INICIO DE METODOS INTERNOS DE JAMFRAME -------------------- #
	def get_dimension_frame_horizontal(self):
	# Calculando tamaño para Frame
		alto = 0
		ancho_frame = self.margen * 2 + self.grosor_borde * 2

		for widget in list(self.widgets):
			ancho_frame += widget.rect.w + self.separador

			if widget.rect.h > alto:
				alto = widget.rect.h

		ancho_frame -= self.separador
		alto_frame = alto + self.margen * 2 + self.grosor_borde * 2
		return (ancho_frame, alto_frame)

	def get_dimension_frame_vertical(self):
	# Calculando tamaño para Frame
		ancho = 0
		alto_frame = self.margen * 2 + self.grosor_borde * 2

		for widget in list(self.widgets):
			alto_frame += widget.rect.h + self.separador

			if widget.rect.w > ancho:
				ancho = widget.rect.w

		alto_frame -= self.separador
		ancho_frame = ancho + self.margen * 2 + self.grosor_borde * 2
		return (ancho_frame, alto_frame)

	def set_horizontal_aling(self, alineacion=None):
	# Alinea los widgets en un label de orienctacion vertical
		if alineacion == "centro":
		# centrando los widget en la horizontal
			posicion_x = self.grosor_borde + self.margen
			for widget in list(self.widgets):
			# centrado horizontal
				y = self.panel.rect.h/2 - widget.rect.h/2
				x =  posicion_x
				widget.set_posicion(punto=(x,y))
				posicion_x += self.separador + widget.rect.w
				# almacenar cambios
				(tamanio, posicion) = (widget.rect.w, widget.rect.h), (widget.rect.x, widget.rect.y)
				self.dict_widgets_tamanio_posicion[widget] = (tamanio, posicion)
		
		if alineacion == "izquierda":
		# alineando los widgets a la izquierda
			y = self.grosor_borde + self.margen
			x = self.grosor_borde + self.margen
			for widget in list(self.widgets):
				widget.set_posicion(punto=(x,y))
				x += self.separador + widget.rect.w
				# almacenar cambios
				(tamanio, posicion) = (widget.rect.w, widget.rect.h), (widget.rect.x, widget.rect.y)
				self.dict_widgets_tamanio_posicion[widget] = (tamanio, posicion)
		
		if alineacion == "derecha":
		# alineando los widgets a la derecha
			x = self.grosor_borde + self.margen
			for widget in list(self.widgets):
				y = self.panel.rect.h - widget.rect.h - self.grosor_borde # - self.margen
				widget.set_posicion(punto=(x,y))
				x += self.separador + widget.rect.w
				# almacenar cambios
				(tamanio, posicion) = (widget.rect.w, widget.rect.h), (widget.rect.x, widget.rect.y)
				self.dict_widgets_tamanio_posicion[widget] = (tamanio, posicion)

	def set_vertical_aling(self, alineacion=None):
	# Alinea los widgets en un label de orienctacion vertical
		if alineacion == "centro":
		# centrando los widget en la horizontal
			posicion_y = self.grosor_borde + self.margen
			for widget in list(self.widgets):
			# centrado horizontal
				x = self.panel.rect.w/2 - widget.rect.w/2
				y =  posicion_y
				widget.set_posicion(punto=(x,y))
				posicion_y += self.separador + widget.rect.h
				# almacenar cambios
				(tamanio, posicion) = (widget.rect.w, widget.rect.h), (widget.rect.x, widget.rect.y)
				self.dict_widgets_tamanio_posicion[widget] = (tamanio, posicion)

		if alineacion == "izquierda":
		# alineando los widgets a la izquierda
			y = self.grosor_borde + self.margen
			x = self.grosor_borde + self.margen
			for widget in list(self.widgets):
				widget.set_posicion(punto=(x,y))
				y += self.separador + widget.rect.h
				# almacenar cambios
				(tamanio, posicion) = (widget.rect.w, widget.rect.h), (widget.rect.x, widget.rect.y)
				self.dict_widgets_tamanio_posicion[widget] = (tamanio, posicion)

		if alineacion == "derecha":
		# alineando los widgets a la derecha
			y = self.grosor_borde + self.margen
			for widget in list(self.widgets):
				x = self.panel.rect.w - widget.rect.w - self.grosor_borde # - self.margen
				widget.set_posicion(punto=(x,y))
				y += self.separador + widget.rect.h
				# almacenar cambios
				(tamanio, posicion) = (widget.rect.w, widget.rect.h), (widget.rect.x, widget.rect.y)
				self.dict_widgets_tamanio_posicion[widget] = (tamanio, posicion)

	def update(self):
	# redibuja todos los controles
		self.panel.image = self.panel.imagen_original.copy()
		self.widgets.clear(self.panel.get_surface(), self.panel.image)

		if self.tipo == "expand":
		# Control de alineacion de widgets y tamaño de frame
			for widget in self.dict_widgets_tamanio_posicion.keys():
			# Si somos expand controlamos los tamaños, alineaciones y posiciones de los widgets contenidos
				(tamanio, posicion) = self.dict_widgets_tamanio_posicion[widget]
				if tamanio != (widget.rect.w, widget.rect.h) or posicion != (widget.rect.x, widget.rect.y):
					#print "Cambios tamaño:", "Almacenado:", tamanio, "Widget", (widget.rect.w, widget.rect.h)
					#print "Cambios posicion:", "Almacenado:", tamanio, "posicion", (widget.rect.x, widget.rect.y)
					self.set_automatic_expand(orientacion=self.orientacion, alineacion=self.alineacion)
					break
		self.widgets.update()
		self.widgets.draw(self.panel.image)
# -------------------- FIN DE METODOS INTERNOS DE JAMFRAME -------------------- #

# -------------------- FIN DE la clase JAMFrame -------------------- #

class Panel(pygame.sprite.Sprite):
# el texto del botón
	def __init__(self, color_borde=COLOR_BORDE, color_relleno=None, tamanio=TAMANIO, grosor_borde=GROSOR):

		pygame.sprite.Sprite.__init__(self)

		self.tamanio = tamanio
		self.color_relleno = color_relleno
		self.grosor_borde = grosor_borde
		self.color_borde = color_borde

		self.imagen_original = self.get_surface(color_borde=self.color_borde, color_relleno=self.color_relleno,
			tamanio=self.tamanio, grosor_borde=self.grosor_borde)
		#self.imagen_original.set_colorkey(MAGENTA, pygame.RLEACCEL)
		self.image = self.imagen_original.copy()
        	self.rect = self.image.get_rect()

	def get_surface(self, color_borde=COLOR_BORDE, color_relleno=None, tamanio=TAMANIO, grosor_borde=GROSOR):
	# genera una superficie transparente sobre la que dibuja una elipse de color para la base del botón
		superficie = pygame.Surface( tamanio, flags=HWSURFACE )
		if not color_relleno:
			superficie.fill(MAGENTA)
			superficie.set_colorkey(MAGENTA, pygame.RLEACCEL)
		else:
			superficie.fill(color_relleno)

		rectangulo_marco = (0,0,tamanio[0], tamanio[1])
		pygame.draw.rect(superficie, color_borde, rectangulo_marco, grosor_borde)
		return superficie

	def set_posicion(self, punto=(0,0)):
	# Setea la posición del botón
		self.rect.x, self.rect.y = punto


