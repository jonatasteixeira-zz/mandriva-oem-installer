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

    # Check params to choose who method to installer will be called   
    def screen_create(self):
        screen = None
        if len(sys.argv) > 1:
            if sys.argv[1] == "positivo-master":
                screen = ScreenShow(PositivoMaster)
            elif sys.argv[1] == "positivo-installer":
                screen = ScreenShow(PositivoInstaller)
            elif sys.argv[1] == "positivo-disk":
                screen = ScreenShow(PositivoDisk)
            elif sys.argv[1] == "meego-master":
                screen = ScreenShow(MeegoMaster)
            elif sys.argv[1] == "meego-installer":
                screen = ScreenShow(MeegoInstaller)
            elif sys.argv[1] == "meego-disk":
                screen = ScreenShow(MeegoDisk)
            else:
                self.error()
        else:
            self.error()

        if screen:
            screen.show()
            screen.start()

            
            
    # Attention here, I'm not sure if this message is a good idea
    def error(self):
        print "Invalid parameter try:"
        print "\t", sys.argv[0], "positivo-master"
        print "\t", sys.argv[0], "positivo-installer"
        print "\t", sys.argv[0], "positivo-disk"
        print "\t", sys.argv[0], "meego-master"
        print "\t", sys.argv[0], "meego-installer"
        print "\t", sys.argv[0], "meego-disk"
        print "\t", sys.argv[0], "philco-master"
        print "\t", sys.argv[0], "philco-installer"
        print "\t", sys.argv[0], "philco-disk"
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
