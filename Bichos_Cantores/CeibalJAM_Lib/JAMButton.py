#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMButton.py por:
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

# ----------- configuración default ----------- #

# texto
TEXTO = "JAMButton"
TIPO_DE_LETRA = "Arial"
TAMANIO_DE_LETRA = 20
COLOR_TEXTO = (0,0,0,1)

# Panel "Base"
TAMANIO_PANEL = (20,20)#(200, 50)
COLOR_PANEL = (128, 128 , 128, 1)		
COLOR_BORDE_PANEL = (179, 179 , 179, 1)		# Borde exterior del control puede tener otro interno con COLOR_BORDE_RELLENO

# Panel "Relleno"
COLOR_RELLENO = (242,242,242,1)			# Porque puede tener un objeto transparente encima pero con borde

# Separadores y Bordes
GROSOR_BORDE = 7
MINI_BORDE = 2

# Color Key para transparencia
MAGENTA  = (255, 0, 255)

# -------------------- INICIO DE la clase JAMButton -------------------- #

class JAMButton(pygame.sprite.Sprite):
	def __init__(self,
			color_relleno=COLOR_RELLENO,
			color_borde_relleno=None,
			color_panel=COLOR_PANEL,
			color_borde_panel=COLOR_BORDE_PANEL,
			tamanio_panel=TAMANIO_PANEL,
			grosor_borde=GROSOR_BORDE,
			imagen=None ,
			tamanio_imagen=(0,0),
			texto=TEXTO,
			tipo_de_letra=TIPO_DE_LETRA,
			tamanio_de_letra=TAMANIO_DE_LETRA,
			color=COLOR_TEXTO):

		pygame.sprite.Sprite.__init__(self)

		# variables de creación de la base del botón
		self.color_relleno=color_relleno
		self.color_borde_relleno=color_borde_relleno
		self.color_panel=color_panel
		self.color_borde_panel=color_borde_panel
		self.tamanio_panel=tamanio_panel
		self.grosor_borde=grosor_borde
		# variables de creación de la etiqueta del botón
		self.imagen=imagen
		self.tamanio_imagen=tamanio_imagen
		self.texto=texto
		self.tipo_de_letra=tipo_de_letra
		self.tamanio_de_letra=tamanio_de_letra
		self.color=color

		# variables del botón definitivo resultante
		self.Label = None
		self.Base = None
		self.sprite_select = None
		self.sprite_deselect = None
		self.image = None
		self.rect = None
		self.sonido_select = None
		self.callback = None
		self.center_imagen = False

		# verificar si es con solo imagen, con solo texto, o ambos
		self.verificar_tipo()

		# Construcción del botón
		self.construye_boton()
		self.recalcular_tamanios()
		self.set_button()
	
		self.select = False

	# -------------------- INICIO DE METODOS DE Construcción del Botón -------------------- #
	def verificar_tipo(self):
	# Bontó se ajusta al tamaño de la imagen SOLO SI NO HAY TEXTO, NO SE ESPECIFICA TAMAÑO PARA EL BOTÓN NI PARA LA IMAGEN

		if self.imagen and not self.texto:
		# Si solo hay una imagen, sin tamaño y el tamaño del panel es el default, el boton tendrá el tamaño de la imagen
			imagen = pygame.image.load(self.imagen)
			rect = imagen.get_rect()
			tamanio = (rect.w, rect.h)

			if self.tamanio_imagen == (0,0):
			# si no pasas tamaño a la imagen
				if self.tamanio_panel == TAMANIO_PANEL:
				# si no pasas tamaño al panel
					self.tamanio_imagen = tamanio
					self.tamanio_panel = tamanio
					return
				else:
				# si pasas tamaño al panel
					jambasebuton=JAMBaseButton(color_relleno=self.color_relleno,
						color_borde_relleno=self.color_borde_relleno,
						color_panel=self.color_panel,
						color_borde_panel=self.color_borde_panel,
						tamanio_panel=self.tamanio_panel,
						grosor_borde=self.grosor_borde)

					while tamanio[0] > jambasebuton.tamanio_relleno[0] or tamanio[1] > jambasebuton.tamanio_relleno[1]:
					# mientras las dimensiones de la imagen sean mayores a la del botón
						w, h = tamanio
						w -= 1 
						h -= 1
						tamanio = (w,h)

					self.tamanio_imagen = tamanio
					return
			else:
			# si le pasas tamaño a la imagen
				if self.tamanio_panel == TAMANIO_PANEL:
				# si no pasas tamaño al panel
					self.tamanio_panel = self.tamanio_imagen
				else:
				# si pasas tamaño al panel
					pass

		elif self.imagen and self.texto:
		# imagen y texto
			pass
		elif not self.imagen and self.texto:
		# solo hay texto
			pass

	def construye_boton(self):
	# genera los componentes internos del botón
		# La etiqueta
		self.Label = JAMLabel(imagen=self.imagen,
			tamanio_imagen=self.tamanio_imagen,
			texto=self.texto,
			tipo_de_letra=self.tipo_de_letra,
			tamanio_de_letra=self.tamanio_de_letra,
			color=self.color)
		# Base del Botón
		self.Base = JAMBaseButton(color_relleno=self.color_relleno,
			color_borde_relleno=self.color_borde_relleno,
			color_panel=self.color_panel,
			color_borde_panel=self.color_borde_panel,
			tamanio_panel=self.tamanio_panel,
			grosor_borde=self.grosor_borde)

	def recalcular_tamanios(self):
	# Ajustar tamaños (Agranda el botón si no hay lugar para la etiqueta, pero no lo achica)
		while self.Base.tamanio_relleno[0] < self.Label.rect.w + MINI_BORDE*4 or self.Base.tamanio_relleno[1] < self.Label.rect.h + MINI_BORDE*4:
			if self.Base.tamanio_relleno[0] < self.Label.rect.w + MINI_BORDE*4:
				# Calcula la diferencia de ancho
				diferencia = self.Label.rect.w + MINI_BORDE*4 - self.Base.tamanio_relleno[0]
				self.tamanio_panel = (self.tamanio_panel[0]+diferencia, self.tamanio_panel[1])

			if self.Base.tamanio_relleno[1] < self.Label.rect.h + MINI_BORDE*4:
				# Calcula la diferencia de ancho
				diferencia = self.Label.rect.h + MINI_BORDE*4 - self.Base.tamanio_relleno[1]
				self.tamanio_panel = (self.tamanio_panel[0], self.tamanio_panel[1]+diferencia)

			# Reconstruir el botón
			self.Base = JAMBaseButton(color_relleno=self.color_relleno,
				color_borde_relleno=self.color_borde_relleno,
				color_panel=self.color_panel,
				color_borde_panel=self.color_borde_panel,
				tamanio_panel=self.tamanio_panel,
				grosor_borde=self.grosor_borde)

	def set_button(self):
	# construye las imagenes definitivas del botón
		self.Base.posicion_relleno = (self.Base.posicion_relleno[0]+MINI_BORDE*2, self.Base.posicion_relleno[1]+MINI_BORDE*2)
		pos_x, pos_y = self.Base.relleno.get_rect().center 
		pos_x = pos_x - self.Label.rect.w/2 + self.grosor_borde
		pos_y = pos_y - self.Label.rect.h/2 + self.grosor_borde

		# Pintar etiqueta sobre el relleno
		if self.texto and not self.imagen:
		# si hay texto pero no imagen, se centra el texto
			self.Base.sprite_deselect.blit(self.Label.image, (pos_x, pos_y))
			self.Base.sprite_select.blit(self.Label.image, (pos_x, pos_y))

		elif not self.texto:
		# Si no hay texto se centra la imagen
			self.Base.sprite_deselect.blit(self.Label.image, (pos_x, pos_y))
			self.Base.sprite_select.blit(self.Label.image, (pos_x, pos_y))

		if self.texto and self.imagen:
		# Si hay texto e imagen, se alinea a la izquierda
			self.Base.sprite_deselect.blit(self.Label.image, (self.Base.posicion_relleno[0], pos_y))
			self.Base.sprite_select.blit(self.Label.image, (self.Base.posicion_relleno[0], pos_y))

		self.sprite_select = self.Base.sprite_select
		self.sprite_deselect = self.Base.sprite_deselect

		self.image = self.sprite_deselect.copy()
		self.rect = self.image.get_rect()
	# -------------------- FIN DE METODOS DE Construcción del Botón -------------------- #

	# -------------------- INICIO DE METODOS SETS -------------------- #
	def set_text(self, texto=None, tipo_de_letra=None, tamanio_de_letra=None, color=None):
	# permite cambiar atributos de texto
		# actualizar segun cambios
		if texto: self.texto=texto
		if tipo_de_letra: self.tipo_de_letra=str(tipo_de_letra)
		if tamanio_de_letra: self.tamanio_de_letra=int(tamanio_de_letra)
		if color: self.color=color
		# reconstruir el sprite
		self.re_init()
		return

	def set_imagen(self, imagen=None , tamanio_imagen=None):
	# permite cambiar atributos de texto
		# actualizar segun cambios
		if imagen: self.imagen=imagen
		if tamanio_imagen: self.tamanio_imagen=tamanio_imagen
		# reconstruir el sprite
		self.re_init()

	def set_colors(self,
		color_relleno=None,
	        color_borde_relleno=None,
        	color_panel=None,
            	color_borde_panel=None):
	# permite cambiar atributos de colores y bordes.

		# actualizar segun cambios
		if color_relleno > -1: self.color_relleno=color_relleno
		if color_borde_relleno > -1: self.color_borde_relleno=color_borde_relleno
		if color_panel > -1: self.color_panel=color_panel
		if color_borde_panel > -1: self.color_borde_panel=color_borde_panel
		# reconstruir el sprite
		self.re_init()

	def set_tamanios(self, tamanio_panel=TAMANIO_PANEL, grosor_borde=-1):
	# permite cambiar atributos de colores y bordes.
		# actualizar segun cambios
		if tamanio_panel: self.tamanio_panel=tamanio_panel
		if grosor_borde > -1: self.grosor_borde=grosor_borde
		# reconstruir el sprite
		self.re_init()

	def set_inclinacion(self, angulo):
	# Rota el botón
		if angulo == 0:
			self.image = self.sprite_deselect.copy()
        		self.rect = self.image.get_rect()
		else:
			tamanio_panel = self.rect.w, self.rect.h
			jambutton = JAMBaseButton()
			superficie = jambutton.get_surface(color_relleno=None, color_borde=None, tamanio_panel=tamanio_panel, grosor_borde=1)
			superficie.blit(self.sprite_deselect, (0,0))
			self.image = pygame.transform.rotate(superficie, -angulo)

	def set_posicion(self, punto=(0,0)):
	# Setea la posición del botón
		self.rect.x, self.rect.y = punto

	def connect(self, callback=None, sonido_select=None):
	# conecta el botón a una función y un sonido para select
		self.callback = callback
		self.sonido_select = sonido_select
	# -------------------- FIN DE METODOS SETS -------------------- #

	# -------------------- INICIO DE METODOS INTERNOS AUTOMÁTICOS -------------------- #
	def play_select(self):
	# reproduce un sonido cuando pasas el mouse sobre el botón
		if self.sonido_select:
			self.sonido_select.play()

	def re_init(self):
	# Construye nuevamente el sprite, se usa luego de cambiar algún atributo como el texto o la imagen
		callback = self.callback
		sonido_select = self.sonido_select

		self.__init__(color_relleno=self.color_relleno,
		color_borde_relleno=self.color_borde_relleno,
		color_panel=self.color_panel,
		color_borde_panel=self.color_borde_panel,
		tamanio_panel=self.tamanio_panel,
		grosor_borde=self.grosor_borde,
		imagen=self.imagen ,
		tamanio_imagen=self.tamanio_imagen,
		texto=self.texto,
		tipo_de_letra=self.tipo_de_letra,
		tamanio_de_letra=self.tamanio_de_letra,
		color=self.color)

		self.callback = callback
		self.sonido_select = sonido_select
		return

	def update(self):
	# responde a los eventos del mouse sobre el sprite
		posicion = pygame.mouse.get_pos()
		# Selecciona el botón cuando el mouse pasa encima de él
		if self.rect.collidepoint(posicion):
			if self.select == False:
				self.play_select()
				self.image = self.sprite_select.copy()
				self.select = True

			if  pygame.event.get(pygame.MOUSEBUTTONDOWN):
				if self.callback:
					return self.callback()
		else:
			if self.select == True:
				self.image = self.sprite_deselect.copy()
				self.select = False
	# -------------------- FIN DE METODOS INTERNOS AUTOMÁTICOS -------------------- #

# -------------------- FIN DE la clase JAMButton -------------------- #

# -------------------- INICIO DE la clase JAMBaseButton -------------------- #
class JAMBaseButton(pygame.sprite.Sprite):
# el texto del botón
	def __init__(self, color_relleno=COLOR_RELLENO, color_borde_relleno=None, color_panel=COLOR_PANEL, color_borde_panel=COLOR_BORDE_PANEL,
			tamanio_panel=TAMANIO_PANEL, grosor_borde=GROSOR_BORDE):

		pygame.sprite.Sprite.__init__(self)

		self.color_panel = color_panel
		self.color_relleno = color_relleno
		self.color_borde_relleno = color_borde_relleno
		self.color_borde_panel = color_borde_panel
		self.tamanio_panel = tamanio_panel
		self.grosor_borde = grosor_borde

		# Para luego poner una etiqueta
		self.relleno = None
		self.tamanio_relleno = None
		self.posicion_relleno = None

		# SPRITE
		self.sprite_deselect = self.get_JAMButtonBase(color_relleno=self.color_relleno, color_borde_relleno=self.color_borde_relleno, 					color_panel=self.color_panel, color_borde_panel=self.color_borde_panel,
				tamanio_panel=self.tamanio_panel, grosor_borde=self.grosor_borde)

		self.sprite_select = self.get_JAMButtonBase(color_relleno=self.color_borde_panel, color_borde_relleno=None, 						color_panel=self.color_panel, color_borde_panel=self.color_borde_panel,
				tamanio_panel=self.tamanio_panel, grosor_borde=self.grosor_borde)

		self.image = self.sprite_deselect.copy()
        	self.rect = self.image.get_rect()

		self.callback = None
		self.sonido_select = None
		self.select = False

	# -------------------- INICIO DE METODOS DE CONSTRUCCION DE JAMBaseButton -------------------- #
	def get_JAMButtonBase(self, color_relleno=None, color_borde_relleno=None, color_panel=None, color_borde_panel=None, tamanio_panel=None, 				grosor_borde=None):
	# Crea un JAMButton Rectangular

		# la base
		base = self.get_surface(color_relleno=color_panel, color_borde=color_borde_panel, tamanio_panel=tamanio_panel, grosor_borde=grosor_borde)
		(x, y, w, h) = base.get_rect()

		# damos como origen una posición mas adentro del origen de la base sumada al borde
		self.posicion_relleno = (x + grosor_borde, y + grosor_borde)

		# restamos bordes y separadores dando perspectiva
		self.tamanio_relleno = (w - self.posicion_relleno[0] - grosor_borde - MINI_BORDE * 3, h - self.posicion_relleno[1] - grosor_borde - MINI_BORDE * 3)

		# el relleno
		self.relleno = self.get_surface(color_relleno=color_relleno, color_borde=color_borde_relleno, tamanio_panel=self.tamanio_relleno, grosor_borde=7)
		
		# construimos el sprite
		base.blit(self.relleno, self.posicion_relleno)
	
		# devolvemos el resultado
		return base

	def get_surface(self, color_relleno=None, color_borde=None, tamanio_panel=TAMANIO_PANEL, grosor_borde=GROSOR_BORDE):
	# genera una superficie

		superficie = pygame.Surface( tamanio_panel, flags=HWSURFACE )

		# Si no se pasa un color, se hace transparente
		if not color_relleno:
			superficie.fill(MAGENTA)
			superficie.set_colorkey(MAGENTA, pygame.RLEACCEL)
		else:
		# Se pinta con el color de relleno
			superficie.fill(color_relleno)

		if color_borde and grosor_borde:
		# Si se especificó un color y un grosor para el borde
			rectangulo_borde = (0, 0, tamanio_panel[0], tamanio_panel[1])
			pygame.draw.rect(superficie, color_borde, rectangulo_borde, grosor_borde)
		return superficie
	# -------------------- FIN DE METODOS DE CONSTRUCCION DE JAMBaseButton -------------------- #

	# -------------------- INICIO DE METODOS SETS -------------------- #
	def set_posicion(self, punto=(0,0)):
	# Setea la posición del botón
		self.rect.x, self.rect.y = punto

	def set_tamanio(self, tamanio=TAMANIO_PANEL):
	# Setea el tamaño del botón
		self.image = pygame.transform.scale(self.sprite_deselect, tamanio)
		self.rect = self.image.get_rect()

	def connect(self, callback=None, sonido_select=None):
	# conecta el botón a una función y un sonido para select
		self.callback = callback
		self.sonido_select = sonido_select

	def set_inclinacion(self, angulo):
	# Rota el botón
		if angulo == 0:
			self.image = self.sprite_deselect.copy()
        		self.rect = self.image.get_rect()
		else:
			tamanio_panel = self.rect.w, self.rect.h
			superficie = self.get_surface(color_relleno=None, color_borde=None, tamanio_panel=tamanio_panel, grosor_borde=1)
			superficie.blit(self.sprite_deselect, (0,0))
			self.image = pygame.transform.rotate(superficie, -angulo)
	# -------------------- FIN DE METODOS SETS -------------------- #

	# -------------------- INICIO DE METODOS INTERNOS AUTOMÁTICOS -------------------- #
	def play_select(self):
	# reproduce un sonido cuando pasas el mouse sobre el botón
		if self.sonido_select:
			self.sonido_select.play()

	
	def update(self):
	# responde a los eventos del mouse sobre el sprite
		posicion = pygame.mouse.get_pos()
		# Selecciona el botón cuando el mouse pasa encima de él
		if self.rect.collidepoint(posicion):
			if self.select == False:
				self.play_select()
				self.image = self.sprite_select.copy()
				self.select = True

			if  pygame.event.get(pygame.MOUSEBUTTONDOWN):
				if self.callback:
					return self.callback()
		else:
			if self.select == True:
				self.image = self.sprite_deselect.copy()
				self.select = False

	# -------------------- FIN DE METODOS INTERNOS AUTOMÁTICOS -------------------- #
# -------------------- FIN DE la clase JAMBaseButton -------------------- #

# -------------------- INICIO DE la clase JAMLabel -------------------- #
class JAMLabel(pygame.sprite.Sprite):
# Botón con texto e imágen

	def __init__(self, imagen=None , tamanio_imagen=(30,30),
			texto=TEXTO, tipo_de_letra=TIPO_DE_LETRA, tamanio_de_letra=TAMANIO_DE_LETRA, color=COLOR_TEXTO):

		pygame.sprite.Sprite.__init__(self)

		# imagen
		if imagen != None:
			self.direccion_imagen = str(imagen)
		else:
			self.direccion_imagen = None
		self.imagen=imagen
		self.tamanio_imagen=tamanio_imagen

		# texto
		self.valor_texto = texto
		self.texto= texto
		self.tipo_de_letra=str(tipo_de_letra)
		self.tamanio_de_letra=int(tamanio_de_letra)
		self.color=color

		# Construyendo las superficies
		if self.imagen:
			self.imagen = self.construye_imagen(imagen=self.imagen , tamanio=self.tamanio_imagen)
		if self.texto:
			self.texto = self.construye_texto(texto=self.texto, tipo_de_letra=self.tipo_de_letra,
				tamanio_de_letra=self.tamanio_de_letra, color=self.color)

		# Si solo hay imagen
		if self.imagen and not self.texto:
			# SPRITE
			self.image = self.imagen
			self.rect = self.image.get_rect()
		# Si solo hay texto
		if self.texto and not self.imagen:
			# SPRITE
			self.image = self.texto
			self.rect = self.image.get_rect()
		# Si hay imagen y texto
		if self.texto and self.imagen:
			rectangulo_imagen = self.imagen.get_rect()
			rectangulo_texto = self.texto.get_rect()	
			altura = 0
			# Calculando altura
			if rectangulo_imagen.h > rectangulo_texto.h:
				altura = rectangulo_imagen.h
			else:
				altura = rectangulo_texto.h
			# Calculando largo
			largo = rectangulo_imagen.w + MINI_BORDE*2 + rectangulo_texto.w + MINI_BORDE*3
			# Creando una nueva superficie transparente para los nuevos objetos
			tamanio = (largo, altura)
			jambutton = JAMBaseButton()
			superficie = jambutton.get_surface(color_relleno=None, color_borde=(0,0,0,1), tamanio_panel=tamanio, grosor_borde=0)
			# centrado horizontal
			posicio_h_texto = altura/2 - rectangulo_texto.h/2
			posicio_h_imagen = altura/2 - rectangulo_imagen.h/2
			# creando nueva superficie
			superficie.blit(self.imagen, (0,posicio_h_imagen))
			superficie.blit(self.texto, (rectangulo_imagen.w+MINI_BORDE*2, posicio_h_texto))
			# SPRITE
			self.image = superficie
			self.rect = self.image.get_rect()

		self.imagen_original = self.image

		self.posicion = (0,0)
		self.angulo = 0

	# -------------------- INICIO DE METODOS DE CONSTRUCCION DE JAMLabel -------------------- #
	def construye_texto(self, texto=TEXTO, tipo_de_letra=TIPO_DE_LETRA, tamanio_de_letra=TAMANIO_DE_LETRA, color=COLOR_TEXTO):
	# setea texto
		pygame.font.init()
		fuente = pygame.font.Font(pygame.font.match_font(tipo_de_letra, True, False), tamanio_de_letra)

		string_to_render = unicode( str(texto).decode("utf-8") )
		imagen_fuente = fuente.render(string_to_render, 1, (color))

		return imagen_fuente

	def construye_imagen(self, imagen=None , tamanio=(50,50)):
	# setea texto e imagen para el botón
		imagen_original = pygame.transform.scale(pygame.image.load(imagen), tamanio).convert_alpha()

		return imagen_original
	# -------------------- FIN DE METODOS DE CONSTRUCCION DE JAMLabel -------------------- #

	# -------------------- INICIO DE METODOS SETS -------------------- #
	def set_posicion(self, punto=(0,0)):
	# permite cambiar la posición en pantalla
		self.rect.x, self.rect.y = punto
		self.posicion = punto


	def set_inclinacion(self, angulo):
	# permite rotar la etiqueta
		if angulo == 0:
			self.image = self.imagen_original.copy()
        		self.rect = self.image.get_rect()
		else:
			self.image = pygame.transform.rotate(self.imagen_original, -angulo)
		self.angulo = angulo

	def set_text(self, texto=None, tipo_de_letra=None, tamanio_de_letra=None, color=None):
	# permite cambiar atributos de texto
		# actualizar segun cambios
		if texto: self.valor_texto=texto
		if tipo_de_letra: self.tipo_de_letra=str(tipo_de_letra)
		if tamanio_de_letra: self.tamanio_de_letra=int(tamanio_de_letra)
		if color: self.color=color
		# reconstruir el sprite
		self.__init__(imagen=self.direccion_imagen , tamanio_imagen=self.tamanio_imagen,
			texto=self.valor_texto, tipo_de_letra=self.tipo_de_letra, tamanio_de_letra=self.tamanio_de_letra, color=self.color)

	def set_imagen(self, imagen=None , tamanio_imagen=None):
	# permite cambiar atributos de texto
		# actualizar segun cambios
		if imagen: self.direccion_imagen=imagen
		if tamanio_imagen: self.tamanio_imagen=tamanio_imagen
		# reconstruir el sprite
		self.__init__(imagen=self.direccion_imagen , tamanio_imagen=self.tamanio_imagen,
			texto=self.valor_texto, tipo_de_letra=self.tipo_de_letra, tamanio_de_letra=self.tamanio_de_letra, color=self.color)
	# -------------------- FIN DE METODOS SETS -------------------- #

# -------------------- FIN DE la clase JAMLabel -------------------- #
