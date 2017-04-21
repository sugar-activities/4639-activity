# -*- coding: utf-8 -*-
# Copyright 2013 Elena Ramos
# Copyright 2013 Vladimir Espinola
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


import gtk
import logging
import gobject
import random
from datetime import datetime
from gettext import gettext as _
from sugar.activity import activity
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity.widgets import ActivityButton
from sugar.activity.widgets import ActivityToolbox
from sugar.activity.widgets import TitleEntry
from sugar.activity.widgets import StopButton
from sugar.activity.widgets import ShareButton
from ConfigParser import SafeConfigParser
from subprocess import Popen


class ElegirActivity(activity.Activity):

    def __init__(self, handle):

        activity.Activity.__init__(self, handle)

        self.max_participants = 1

        toolbar_box = ToolbarBox()

        activity_button = ActivityButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        title_entry = TitleEntry(self)
        toolbar_box.toolbar.insert(title_entry, -1)
        title_entry.show()

        share_button = ShareButton(self)
        toolbar_box.toolbar.insert(share_button, -1)
        share_button.show()
        
        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        image = gtk.Image()
        vbox = gtk.VBox()
        hbox = gtk.HBox()
        self.set_canvas(vbox)

        button_0 = gtk.Button()
        button_1 = gtk.Button()
        button_2 = gtk.Button()
        button_3 = gtk.Button()
      
        vbox.add(button_0)
        vbox.add(image)
        vbox.add(hbox)
        hbox.add(button_1)
        hbox.add(button_2)
        hbox.add(button_3)
        vbox.show_all()
        try:
            self.puntaje=self.metadata["puntaje"]
            self.total=self.metadata["total"]
            self.numero=self.metadata["numero"]
            self.anterior=self.metadata["anterior"]
            button_0.set_label(str(self.puntaje) + '/' +str( self.total))
        except KeyError:
            self.puntaje=0
            self.numero=random.randint(1,100)
            self.anterior=self.numero
            self.total=0
            button_0.set_label('click para saber tu puntaje')
        self.parser = SafeConfigParser()
        self.parser.read('config.ini')
        
        Popen(['espeak', '-v', 'es', self.parser.get('pregunta'+str(self.numero), 'enunciado')])
        pixbuf = gtk.gdk.pixbuf_new_from_file(self.parser.get('pregunta'+str(self.numero), 'imagen'))
        scaled_pixbuf = pixbuf.scale_simple(400,400,gtk.gdk.INTERP_BILINEAR)
        image.set_from_pixbuf(scaled_pixbuf)
        button_1.set_label(self.parser.get('pregunta'+str(self.numero), 'correcta'))
        button_2.set_label(self.parser.get('pregunta'+str (self.numero), 'incorrecta2'))
        button_3.set_label(self.parser.get('pregunta'+str (self.numero), 'incorrecta1'))
        
        button_1.connect('clicked',self.__cambiar_imagen_cb, button_2,button_3,button_0,image)
        button_2.connect('clicked',self.__cambiar_imagen_cb, button_3,button_1,button_0,image)
        button_3.connect('clicked',self.__cambiar_imagen_cb, button_2,button_1,button_0,image)
        button_0.connect('clicked',self.__decir_puntaje_cb)
 
     
    def __cambiar_imagen_cb(self,b1,b2=None,b3=None,b0=None,i=None):
        if b1.get_label()== self.parser.get('pregunta'+ str(self.anterior), 'correcta'):  
            text =self.parser.get('pregunta'+ str(self.anterior), 'correcta')+', es correcta, tienes un punto mas '
            p=1
        else:
            text ='La palabra seleccionada  es , incorrecta'
            p=0
      
        self.puntaje=int(self.puntaje) +p
        Popen(['espeak', '-v', 'es', text])
        self.numero=random.randint(1,100)
      
        if self.numero % 2 ==0:
            pixbuf = gtk.gdk.pixbuf_new_from_file(self.parser.get('pregunta'+str(self.numero), 'imagen'))
            scaled_pixbuf = pixbuf.scale_simple(400,400,gtk.gdk.INTERP_BILINEAR)
            i.set_from_pixbuf(scaled_pixbuf)
            b3.set_label(self.parser.get('pregunta'+str (self.numero), 'correcta'))
            b1.set_label(self.parser.get('pregunta'+str (self.numero), 'incorrecta1'))
            b2.set_label(self.parser.get('pregunta'+str(self.numero), 'incorrecta2'))
           
        else:
            pixbuf = gtk.gdk.pixbuf_new_from_file(self.parser.get('pregunta'+str(self.numero), 'imagen'))
            scaled_pixbuf = pixbuf.scale_simple(400,400,gtk.gdk.INTERP_BILINEAR)
            i.set_from_pixbuf(scaled_pixbuf)
            b3.set_label(self.parser.get('pregunta'+str (self.numero), 'incorrecta1'))
            b1.set_label(self.parser.get('pregunta'+str (self.numero), 'incorrecta2'))
            b2.set_label(self.parser.get('pregunta'+str(self.numero), 'correcta'))
          
        self.anterior=self.numero
        self.total= int(self.total)+1
        b0.set_label(str(self.puntaje) + '/' +str( self.total))

    def __decir_puntaje_cb(self,b):
        text= 'tu puntaje es '+  str (self.puntaje) + ' de, '+  str(self.total)
    	Popen(['espeak', '-v', 'es', text])
 
    def read_file(self, tmp_file):
        self.puntaje=self.metadata["puntaje"]
        self.total=self.metadata["total"]
        self.numero=self.metadata["numero"]
        self.anterior=self.metada["anterior"]  

    def write_file(self, tmp_file):
        self.metadata["numero"]=self.numero
        self.metadata["anterior"]=self.anterior
        self.metadata["total"]=self.total
        self.metadata["puntaje"]=self.puntaje
      
