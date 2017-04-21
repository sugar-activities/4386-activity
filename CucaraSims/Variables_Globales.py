#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   VariablesGlobales.py por:
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

import os

RESOLUCION_MONITOR = (1200,900)

from sugar.activity import activity
DIRECTORIO_DATOS = os.path.join(activity.get_activity_root(), 'data/')

#DIRECTORIO_DATOS = os.path.join(os.getcwd(), 'data/')

# -------------------------------- Cria de Cucarachas -------------------------------- #
VELOCIDADJUEGO = 3
MAXIMOCUCAS = 15

# Datos Vitales
ESCALASMUDAS = [(73,60),(83,70),(93,80),(103,90)]
DIASMUDAS = [9,21,32,43]
DIASREPRO = [51, 62, 73]
DIASCADAVER = 3
UNIDADALIMENTO = 333
UNIDADAGUA = 333
AUMENTAHAMBRE = 2 # por dia
AUMENTASED = 2 # por dia
RINDEALIMENTO = 5 # cada 30 pasadas update
RINDEAGUA = 5
CONSUMOALIMENTO = 10 # resta cuando come
CONSUMOAGUA = 10
NACER = 9 # incubacion de ooteca en dias
# Limites vitales
LIMITEHAMBRE = -126
LIMITESED = -126
LIMITEVIDA = 84 # DIAS

CUCARACHA1 = os.getcwd() + "/CucaraSims/CUCARACHA/Imagenes/cucaracha1.png"
CUCARACHA2 = os.getcwd() + "/CucaraSims/CUCARACHA/Imagenes/cucaracha2.png"
CUCARACHA3 = os.getcwd() + "/CucaraSims/CUCARACHA/Imagenes/cucaracha3.png"
CUCARACHA4 = os.getcwd() + "/CucaraSims/CUCARACHA/Imagenes/cucaracha4.png"
SONIDOCUCARACHA = os.getcwd() + "/CucaraSims/CUCARACHA/Sonidos/cucaracha.ogg"
MUDAS = os.getcwd() + "/CucaraSims/CUCARACHA/Muda/"
MUDA1 = os.getcwd() + "/CucaraSims/CUCARACHA/Imagenes/muda1.png"
MUDA2 = os.getcwd() + "/CucaraSims/CUCARACHA/Imagenes/muda2.png"
OOTECA = os.getcwd() + "/CucaraSims/CUCARACHA/Imagenes/huevos.png"
REPRODUCCION1 = os.getcwd() + "/CucaraSims/CUCARACHA/Imagenes/reproduccion1.png"
REPRODUCCION2 = os.getcwd() + "/CucaraSims/CUCARACHA/Imagenes/reproduccion2.png"
CICLO1 = os.getcwd() + "/CucaraSims/CUCARACHA/Imagenes/ciclo_vital1.png"
CICLO2 = os.getcwd() + "/CucaraSims/CUCARACHA/Imagenes/ciclo_vital2.png"
CADAVER = os.getcwd() + "/CucaraSims/CUCARACHA/Imagenes/muerta.png"
MUERTE = os.getcwd() + "/CucaraSims/CUCARACHA/Imagenes/muerte1.png"
MUSICA1 = os.getcwd() + "/CucaraSims/CUCARACHA/Sonidos/musica.ogg"
MUSICA2 = os.getcwd() + "/CucaraSims/CUCARACHA/Sonidos/musica2.ogg"
FONDO4 = os.getcwd() + "/CucaraSims/CUCARACHA/Imagenes/fondo4.png"
LOGO = os.getcwd() + "/CucaraSims/CUCARACHA/Imagenes/logo.png"

# Interfaz
FONDO = os.getcwd() + "/CucaraSims/CUCARACHA/Imagenes/fondo.png"
PAN = os.getcwd() + "/CucaraSims/CUCARACHA/Imagenes/pan.png"
JARRA = os.getcwd() + "/CucaraSims/CUCARACHA/Imagenes/jarra.png"
AGUA = os.getcwd() + "/CucaraSims/CUCARACHA/Imagenes/agua.png"

# Libreta de lectura
FONDO_LIBRO = os.getcwd() + "/CucaraSims/Iconos/libreta.png"
# Iconos generales
SIGUIENTE = os.getcwd() + "/CucaraSims/Iconos/siguiente.png"
ANTERIOR = os.getcwd() + "/CucaraSims/Iconos/anterior.png"
PLAY = os.getcwd() + "/CucaraSims/Iconos/play.png"
CERRAR = os.getcwd() + "/CucaraSims/Iconos/cerrar.png"

JAM = os.getcwd() + "/CucaraSims/Iconos/icono_jam.png"
ICONOSAUDIO = [os.getcwd() + "/CucaraSims/Iconos/audio1.png", os.getcwd() + "/CucaraSims/Iconos/audio2.png"]

# Lecturas
import CUCARACHA
from CUCARACHA.Lectura import MUDA as leccionmuda
from CUCARACHA.Lectura import REPRODUCCION as leccionreproduccion
from CUCARACHA.Lectura import LECTURACICLOVITAL as lecturaciclovital
from CUCARACHA.Lectura import LECTURAMUERTE as lecturamuerte
from CUCARACHA.Lectura import LECTURAPLAGA as LecturaPlaga
from CUCARACHA.Lectura import LECTURAENDGAME as endgame
from CUCARACHA.Lectura import LECTURASEXTRAS as lecturasextras

LECTURAMUDA = leccionmuda
LECTURAREPRODUCCION = leccionreproduccion
LECTURACICLOVITAL = lecturaciclovital
LECTURAMUERTE = lecturamuerte
LECTURAPLAGA = LecturaPlaga
LECTURAENDGAME = endgame
LECTURASEXTRAS = lecturasextras
