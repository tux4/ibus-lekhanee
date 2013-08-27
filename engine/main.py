# vim:set et sts=4 sw=4:
#
# ibus-lekhanee-Indic Input Method for IBus 
# Copyright (c) 2013 Prasanna Suman <prasanna.tux@gmail.com>
# Copyright (c) 2007-2012 Peng Huang <shawn.p.huang@gmail.com>
#  
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

from gi.repository import IBus
from gi.repository import GLib
from gi.repository import GObject

import os
import sys
import getopt
import locale

from gi.repository import Gtk

from engine import LekhaneeEngine 
   
class IMApp():
    def __init__(self):
        self.__lk_engine = LekhaneeEngine()
        #self.__lk_engine.set_im(self)
        self.__component = IBus.Component.new_from_file("lekhanee.xml") 
        self.__mainloop = GLib.MainLoop()
        self.__bus = IBus.Bus()
        self.__bus.connect("disconnected", self.__bus_disconnected_cb)
        self.__factory = IBus.Factory.new(self.__bus.get_connection())
        #self.__factory.add_engine("Lekhanee", GObject.type_from_name("Lekhanee"))
        self.__factory.add_engine("Lekhanee", self.__lk_engine)
        self.__bus.register_component(self.__component)
        self.__bus.set_global_engine_async("Lekhanee", -1, None, None, None)
        

    def run(self):
        IBus.init()
        self.__mainloop.run()

    def test_fun(self):
        print "Super Test Success"

    def __bus_disconnected_cb(self, bus):
        self.__mainloop.quit()


def launch_engine():
    win = IMApp()
    win.run()
    
if __name__ == "__main__":
    launch_engine()
