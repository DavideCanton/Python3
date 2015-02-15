__author__ = 'davide'

import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from finestra import Ui_finestra

class ProvaFinestra(QMainWindow, Ui_finestra):
    def __init__(self):
        QMainWindow.__init__(self)

        # Set up the user interface from Designer.
        self.setupUi(self)

        # Connect up the buttons.
        self.saluta.clicked.connect(self.saluta_fun)

    def saluta_fun(self):
        name = self.name_edit.toPlainText()
        QMessageBox.information(self, "Saluto", "Ciao, {}!".format(name))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProvaFinestra()

    window.show()
    sys.exit(app.exec_())