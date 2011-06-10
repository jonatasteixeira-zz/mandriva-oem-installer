from app.views.wait.show_ui import Ui_WaitShow

from PyQt4 import QtCore, QtGui

class WaitShow(QtGui.QDialog):
    def __init__(self, message):
        QtGui.QMainWindow.__init__(self)
        
        self.wait_show = Ui_WaitShow()
        self.wait_show.setupUi(self)

        self.progress_bar = self.wait_show.progress_bar
        self.button_box = self.wait_show.button_box
        
        self.progress_bar.setFormat(message)

        self.ctimer = QtCore.QTimer()
        self.ctimer.start(100)
#		QtCore.QMetaObject.connectSlotsByName(self)

        self.connect_signals()
    
    def connect_signals(self):
        self.connect(self.button_box, QtCore.SIGNAL("accepted()"), self.button_box_accepted)
        self.connect(self.button_box, QtCore.SIGNAL("rejected()"), self.button_box_rejected)
 
 		# constant timer
        QtCore.QObject.connect(self.ctimer, QtCore.SIGNAL("timeout()"), self.progress_bar_update)

    
    def button_box_accepted(self):
        print "Ok"
        
    def button_box_rejected(self):
        print "Cancel"
        
		
    def progress_bar_update(self):
        val = self.progress_bar.value() + 10
        if val > 100:
            val = 0
        self.progress_bar.setValue(val)


"""
    # Interface Method can't be here
    def wait_for_it(self, message):
    	(while true; do echo ; sleep 1; done) |  $DIALOG --progress --pulsate --text="$1" &
    	killpid=$!

    # Interface Method can't be here
    def error_message(self):
	    $DIALOG --error --text="Ocorreu um erro durante a instalacao, verifique a midia e tente novamente." 
	    reboot
"""
