#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Archivos_y_Directorios.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Ceibal Jam - Uruguay - Plan Ceibal
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

import os
import sqlite3
import urllib
import string

class Archivos_y_Directorios():

	def __init__(self, DIRECTORIO_DATOS):
		self.directorio = DIRECTORIO_DATOS	
		self.set_directorio()

	def set_directorio(self):
	# Crear Directorio para la base de datos
		if not os.path.exists(self.directorio):
			os.mkdir(self.directorio)

	def get_juegos(self):
		return (self.directorio, os.listdir(self.directorio))

	def CrearBasededatos (self):
	# Crea la base de datos inicial
		import time
		numero_de_juegos = time.time()
		nombre = "Cucarasims%s.db" % (numero_de_juegos)
		nombre_de_base = os.path.join(self.directorio, nombre)
		try:
			coneccion = sqlite3.connect(nombre_de_base)
			basededatos = coneccion.cursor()

			basededatos.execute("""create table Cucas (id INTEGER PRIMARY KEY AUTOINCREMENT,
				sexo text, anios text, dias text, horas text, nutricion text, hidratacion text)""")
			coneccion.commit()

			basededatos.execute("""create table Juego (id INTEGER PRIMARY KEY AUTOINCREMENT,
				anios text, dias text, horas text, puntos text)""")
			coneccion.commit()

			basededatos.execute("""create table Ootecas (id INTEGER PRIMARY KEY AUTOINCREMENT,
				dias text, horas text, huevos text)""")
			coneccion.commit()

			basededatos.close()
			coneccion.close()

			os.chmod(os.path.join(self.directorio, nombre), 0666)
			return nombre_de_base
		except Exception, e:
			return False

	def RE_CrearBasededatos (self, base):
	# Crea la base de datos inicial
		nombre_de_base = os.path.join(self.directorio, base)
		try:
			coneccion = sqlite3.connect(nombre_de_base)
			basededatos = coneccion.cursor()

			basededatos.execute("""create table Cucas (id INTEGER PRIMARY KEY AUTOINCREMENT,
				sexo text, anios text, dias text, horas text, nutricion text, hidratacion text)""")
			coneccion.commit()

			basededatos.execute("""create table Juego (id INTEGER PRIMARY KEY AUTOINCREMENT,
				anios text, dias text, horas text, puntos text)""")
			coneccion.commit()

			basededatos.execute("""create table Ootecas (id INTEGER PRIMARY KEY AUTOINCREMENT,
				dias text, horas text, huevos text)""")
			coneccion.commit()

			basededatos.close()
			coneccion.close()

			os.chmod(os.path.join(self.directorio, nombre), 0666)

			return nombre_de_base
		except Exception, e:
			return False

	def guardar(self, base=None, datos=None):
		datos_de_juego = datos[0] # [anios, dias, horas, puntos]
		datos_de_cucas = datos[1] # [sexo, anios, dias, horas, hambre, sed]
		datos_de_ootecas = datos[2] # [dias, horas, huevos]

		self.borrar_tabla(base)
		self.RE_CrearBasededatos(base)

		# Guardando Datos de tiempo de juego en general
		try:
			coneccion = sqlite3.connect(base)
			basededatos = coneccion.cursor()

			try:
				coneccion.text_factory = str #(no funciona en sugar de uruguay)
			except:
				pass

			anios, dias, horas, puntos = datos_de_juego
			item = [0, anios, dias, horas, puntos]
			basededatos.execute ("insert into %s values (?,?,?,?,?)" % ("Juego"), item)
			coneccion.commit()
			basededatos.close()
			coneccion.close()
		except Exception, e:
			print "Ha Ocurrido un Error al Intentar Llenar la Tabla Juego"

		# Guardando Datos de Cucas
		try:
			coneccion = sqlite3.connect(base)
			basededatos = coneccion.cursor()

			try:
				coneccion.text_factory = str #(no funciona en sugar de uruguay)
			except:
				pass

			contador = 0
			for x in range(0, len(datos_de_cucas)):
				datos_bicho = datos_de_cucas[x] # [sexo, anios, dias, horas, hambre, sed]

				sexo = datos_bicho[0]
				anios = datos_bicho[1]
				dias = datos_bicho[2]
				horas = datos_bicho[3]
				hambre = datos_bicho[4]
				sed = datos_bicho[5]

				item = [contador, sexo, anios, dias, horas, hambre, sed]

				basededatos.execute ("insert into %s values (?,?,?,?,?,?,?)" % ("Cucas"), item)
				coneccion.commit()

				contador += 1

			basededatos.close()
			coneccion.close()
		except Exception, e:
			print "Ha Ocurrido un Error al Intentar Llenar la Tabla Cucas"

		# Guardando Datos de Ootecas
		try:
			coneccion = sqlite3.connect(base)
			basededatos = coneccion.cursor()

			try:
				coneccion.text_factory = str #(no funciona en sugar de uruguay)
			except:
				pass

			contador = 0
			for x in range(0, len(datos_de_ootecas)):
				datos_ootecas = datos_de_ootecas[x] # [dias, horas, huevos]

				dias = datos_ootecas[0]
				horas = datos_ootecas[1]
				huevos = datos_ootecas[2]

				item = [contador, dias, horas, huevos]

				basededatos.execute ("insert into %s values (?,?,?,?)" % ("Ootecas"), item)
				coneccion.commit()
				contador += 1

			basededatos.close()
			coneccion.close()
		except Exception, e:
			print "Ha Ocurrido un Error al Intentar Llenar la Tabla Ootecas"	

	def Leer_Base_de_Datos(self, nombre):
		base = os.path.join(self.directorio, nombre)
		datos_juego = None
		try:
			coneccion = sqlite3.connect(base)
			basededatos = coneccion.cursor()
			basededatos.execute("select * from %s" % ("Juego"))
			for dato in basededatos:
				datos_juego = dato
			basededatos.close()
			coneccion.close()
		except Exception, e:
			print "Ha Ocurrido un Error al Intentar Carga Tabla Juego"

	    	cucas = []
		try:
			coneccion = sqlite3.connect(base)
			basededatos = coneccion.cursor()
			basededatos.execute("select * from %s" % ("Cucas"))
			for item in basededatos:
				cucas.append(item)
			basededatos.close()
			coneccion.close()
		except Exception, e:
			print "Ha Ocurrido un Error al Intentar Carga Tabla Cucas"

	    	Ootecas = []	
		try:
			coneccion = sqlite3.connect(base)
			basededatos = coneccion.cursor()
			basededatos.execute("select * from %s" % ("Ootecas"))
			for item in basededatos:
				Ootecas.append(item)
			basededatos.close()
			coneccion.close()
		except Exception, e:
			print "Ha Ocurrido un Error al Intentar Carga Tabla Ootecas"

		return (base, datos_juego, cucas, Ootecas)

	def borrar_tabla(self, nombre):
		try:
			nombre_de_base = os.path.join(self.directorio, nombre)
			os.remove(nombre_de_base)
		except Exception, e:
			print "Ha Ocurrido un Error al Intentar Borarr un Juego"
			

	def verifica(self, base_abrir=None):
		base = os.path.join(self.directorio, base_abrir)
		datos_juego = None
		try:
			coneccion = sqlite3.connect(base)
			basededatos = coneccion.cursor()
			basededatos.execute("select * from %s" % ("Juego"))
			for dato in basededatos:
				datos_juego = dato
			basededatos.close()
			coneccion.close()
		except Exception, e:
			print "Ha Ocurrido un Error al verifica Tabla Juego"

		if not datos_juego:
			os.remove(base)

