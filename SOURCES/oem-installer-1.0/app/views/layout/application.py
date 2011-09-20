# Copyright (C) 2011 - Jonatas Teixeira <jonatast@mandriva.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.

from app.views.screen.show import ScreenShow
from app.controllers import *

from PyQt4 import QtCore, QtGui
import os
import sys
import locale
import gettext

class ApplicationLayout(object):

    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        self.domain = self.translate()
        self.screen_create()
        sys.exit(self.app.exec_())

    def screen_create(self):
        screen = self.solve_options()
        
        if screen:
            screen.show()
            screen.start()
        else:
            self.error()

    # Check params to choose who method to installer will be called   
    def solve_options(self):
        version = None
        mode = None
        debug = False
        
        for option in sys.argv:
            opt = option.replace("-", "")

            if opt == "d" or  opt == "debug":
                debug = True
            if opt == "positivo" or opt == "philco" or opt == "meego":
                version = opt
            if opt == "master" or opt == "installer" or opt == "disk":
                mode = opt

        if not mode or not version:
            self.error()

        if version == "positivo":
            if mode == "master": return ScreenShow(PositivoMaster, debug)
            if mode == "installer": return ScreenShow(PositivoInstaller, debug)
            if mode == "disk": return ScreenShow(PositivoDisk, debug)
        if version == "meego":
            if mode == "master": return ScreenShow(MeegoMaster, debug)
            if mode == "installer": return ScreenShow(MeegoInstaller, debug)
            if mode == "disk": return ScreenShow(MeegoDisk, debug)
        if version == "philco": 
            if mode == "master": return ScreenShow(PhilcoMaster, debug)
            if mode == "installer": return ScreenShow(PhilcoInstaller, debug)
            if mode == "disk": return ScreenShow(PhilcoDisk, debug)

        return None
            
    # Attention here, I'm not sure if this message is a good idea
    def error(self):
        print "Invalid parameter try:"
        print "\t", sys.argv[0], "-vendor -mode <option>"
        print "\t Vendors:"
        print "\t\t -positivo"
        print "\t\t -philco"
        print "\t\t -meego"
        print "\t Modes:"
        print "\t\t -master"
        print "\t\t -installer"
        print "\t\t -disk"
        print "\t Options:"
        print "\t\t -debug"
        sys.exit(1)
        
    #Not used yet, but if be necessary is just set in all strigns
    def translate(self):
        domain = "wizard"
        current_path = os.path.dirname(__file__)
        locale_path = os.path.join(current_path, "..", "..", "..", "config", "locale")

        langs = []
        lc, encoding = locale.getdefaultlocale()

        if (lc):
            langs = [lc]

        language = os.environ.get('LANGUAGE', None)

        if (language):
            langs += language.split(":")

        # TODO - Configuration file
        langs += ["pt_BR", "en_US"]

        gettext.bindtextdomain(domain, locale_path)
        gettext.textdomain(domain)
        lang = gettext.translation(domain, locale_path, languages=langs, fallback = True)

        gettext.install(domain, locale_path)

        return domain
