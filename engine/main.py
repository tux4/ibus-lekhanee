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

from engine import EngineEnchant

class IMApp:
    def __init__(self, exec_by_ibus):
        engine_name = "IBus Lekhanee (dbg)"
        
        """
        self.__component = \
                IBus.Component.new("org.freedesktop.IBus.Lekhanee",
                                   "IBus Lekhanee",
                                   "0.1.0",
                                   "GPL",
                                   "Prasanna Suman <prasanna.tux@gmail.com>",
                                   "http://github.com/tux4/ibus-lekhanee",
                                   "/usr/bin/exec",
                                   "ibus-lekhanee")

        engine = IBus.EngineDesc.new("IBus-Lekhanee",
                                     engine_name,
                                     "IBus Input Method for Indic Languages",
                                     "Indic",
                                     "GPL",
                                     "Prasanna Suman <prasanna.tux@gmail.com>",
                                     "ibus-lekhanee.svg",
                                     "np")
        self.__component.add_engine(engine)
        """
        self.__component = IBus.Component.new_from_file("lekhanee.xml") 
        self.__mainloop = GLib.MainLoop()
        self.__bus = IBus.Bus()
        self.__bus.connect("disconnected", self.__bus_disconnected_cb)
        self.__factory = IBus.Factory.new(self.__bus.get_connection())
        self.__factory.add_engine("Lekhanee",
                GObject.type_from_name("Lekhanee"))
        self.__bus.register_component(self.__component)
        self.__bus.set_global_engine_async(
            "Lekhanee", -1, None, None, None)

    def run(self):
        self.__mainloop.run()

    def __bus_disconnected_cb(self, bus):
        self.__mainloop.quit()


def launch_engine(exec_by_ibus):
    IBus.init()
    IMApp(exec_by_ibus).run()

if __name__ == "__main__":
    launch_engine(False)
