# vim:set et sts=4 sw=4:
#
# ibus-tmpl - The Input Bus template project
#
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

import enchant
import full_map_np
import trans
from gi.repository import GLib
from gi.repository import IBus
from gi.repository import Pango
#import panel
#from panel import HelloWorld
#from main import IMApp

keysyms = IBus

class LekhaneeEngine(IBus.Engine):
    __gtype_name__ = 'Lekhanee'
    __dict = enchant.Dict("en")

    def __init__(self):
        super(LekhaneeEngine, self).__init__()
        self.__is_invalidate = False
        self.__preedit_string = u""
        self.__lookup_table = IBus.LookupTable.new(10, 0, True, True)
        self.__prop_list = IBus.PropList()
        self.__prop_list.append(IBus.Property(key="test", icon="ibus-local"))
        print "Create IBus Lekhanee OK"
        print "Transliterator Creation Done"
        self.__transliterator = trans.transliterator(full_map_np.default)


    def do_process_key_event(self, keyval, keycode, state):
        #print "process_key_event(%04x, %04x, %04x)" % (keyval, keycode, state)
        # ignore key release events
        is_press = ((state & IBus.ModifierType.RELEASE_MASK) == 0)
        if not is_press:
            return False

        if self.__preedit_string:
            if keyval == keysyms.Return:
                print type(self.__preedit_string)
                self.__commit_string(self.__preedit_string)
                return True
            elif keyval == keysyms.Escape:
                self.__preedit_string = u""
                self.__update()
                return True
            elif keyval == keysyms.BackSpace:
                self.__preedit_string = self.__preedit_string[:-1]
                self.__invalidate()
                return True
            elif keyval == keysyms.space:
                if self.__lookup_table.get_number_of_candidates() > 0:
                    cur_pos = self.__lookup_table.get_cursor_pos()
                    text = IBus.Text.get_text(self.__lookup_table.get_candidate(cur_pos))
                    self.__commit_string(text)
                else:
                      self.__commit_string(self.__transliterator.transliterate(self.__preedit_string))
                #self.__commit_string(self.__preedit_string)
                return False
            elif keyval >= 49 and keyval <= 57:
                #keyval >= keysyms._1 and keyval <= keysyms._9
                index = keyval - 49 #keysyms.1
                candidates = self.__lookup_table.get_canidates_in_current_page()
                if index >= len(candidates):
                    return False
                candidate = candidates[index].text
                self.__commit_string(candidate)
                return True
            elif keyval == keysyms.Page_Up or keyval == keysyms.KP_Page_Up:
                self.do_page_up()
                return True
            elif keyval == keysyms.Page_Down or keyval == keysyms.KP_Page_Down:
                self.do_page_down()
                return True
            elif keyval == keysyms.Up:
                self.do_cursor_up()
                return True
            elif keyval == keysyms.Down:
                self.do_cursor_down()
                return True
            elif keyval == keysyms.Left or keyval == keysyms.Right:
                print "table"
                self.show_lookup_table()
                return True
        if keyval in xrange(keysyms.a, keysyms.z + 1) or \
            keyval in xrange(keysyms.A, keysyms.Z + 1):
            if state & (IBus.ModifierType.CONTROL_MASK | IBus.ModifierType.MOD1_MASK) == 0:
                self.__preedit_string += unichr(keyval)
                self.__invalidate()
                return True
        else:
            if keyval < 128 and self.__preedit_string:
                self.__commit_string(self.__preedit_string)

        return False

    def __invalidate(self):
        if self.__is_invalidate:
            return
        self.__is_invalidate = True
        GLib.idle_add(self.__update)


    def do_page_up(self):
        if self.__lookup_table.page_up():
            #self.page_up_lookup_table()
            return True
        return False

    def do_page_down(self):
        if self.__lookup_table.page_down():
            #self.page_down_lookup_table()
            return True
        return False

    def do_cursor_up(self):
        self.__lookup_table.cursor_up()
        print self.__lookup_table.get_candidate()
        #if self.__lookup_table.cursor_up():
            #self.cursor_up_lookup_table()
        #    return True
        #return False

    def do_cursor_down(self):
        self.__lookup_table.cursor_down()
        print self.__lookup_table.is_cursor_visible()
        self.__lookup_table.set_cursor_visible(True)
        cur_pos = self.__lookup_table.get_cursor_pos()
        print IBus.Text.get_text(self.__lookup_table.get_candidate(cur_pos))
        #if self.__lookup_table.cursor_down():
            #self.cursor_down_lookup_table()
            #return True
        #return False

    def __commit_string(self, text):
        
        self.commit_text(IBus.Text.new_from_string(text))
        #self.commit_text(IBus.Text.new_from_string(self.__transliterator.transliterate(text)))
        self.__preedit_string = u""
        self.__update()

    def __update(self):
        preedit_len = len(self.__preedit_string)
        attrs = IBus.AttrList()
        self.__lookup_table.clear()
        if preedit_len > 0:
            for text in self.__transliterator.anm(self.__transliterator.transliterate(self.__preedit_string)):
                self.__lookup_table.append_candidate(IBus.Text.new_from_string(text))
            #if not self.__dict.check(self.__preedit_string):
            #    attrs.append(IBus.Attribute.new(IBus.AttrType.FOREGROUND,
            #            0xff0000, 0, preedit_len))
                #for text in self.__dict.suggest(self.__preedit_string):
                #    self.__lookup_table.append_candidate(IBus.Text.new_from_string(text))
        text = IBus.Text.new_from_string(self.__preedit_string)
        text.set_attributes(attrs)
        self.update_auxiliary_text(text, preedit_len > 0)

        attrs.append(IBus.Attribute.new(IBus.AttrType.UNDERLINE,
                IBus.AttrUnderline.SINGLE, 0, preedit_len))
        text = IBus.Text.new_from_string(self.__preedit_string)
        text.set_attributes(attrs)
        self.update_preedit_text(text, preedit_len, preedit_len > 0)
        self.__update_lookup_table()
        self.__is_invalidate = False

    def __update_lookup_table(self):
        visible = self.__lookup_table.get_number_of_candidates() > 0
        self.update_lookup_table(self.__lookup_table, visible)


    def do_focus_in(self):
        print "focus_in"
        self.register_properties(self.__prop_list)

    def do_focus_out(self):
        print "focus_out"

    def do_reset(self):
        print "reset"

    def do_property_activate(self, prop_name):
        print "PropertyActivate(%s)" % prop_name

