#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
import pygtk
pygtk.require("2.0")

from sugar.activity import activity

from Insectos_Main import Insectos_Main

class InsectosActivity(activity.Activity):
	def __init__(self, handle):
		activity.Activity.__init__(self, handle, False)
		Juego = Insectos_Main()
		Juego.Run()
		gtk.Widget.destroy(self)
		gtk.main_quit()
