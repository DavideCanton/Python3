__author__ = 'davide'

__author__ = 'davide'

import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QLabel
from gui import Ui_MainWindow
from queens_csp import *
from time import sleep
from functools import partial

W = "QLabel { background-color : white; color : black; }"
B = "QLabel { background-color : black; color : white; }"
R = "QLabel { background-color : red; color : black; }"


class QueenThread(QtCore.QThread):
    changeSS = QtCore.pyqtSignal(int, int, str, name="changeSS")

    def __init__(self, gui, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.gui = gui
        self.old = None
        self.new = None
        self.finished.connect(self.gui.endWork)

    def run(self):
        min_conflicts(self.gui.n, self.change, self.startCB)

    def startCB(self, sol, nc):
        self.gui.status.setText("Starting from {} [conflicts={}]".format(sol, nc))

    def change(self, var, value, sol):
        sleep(.1)
        for i in range(self.gui.n):
            for j in range(self.gui.n):
                if sol[j] == i + 1:
                    styleSheet = R
                else:
                    styleSheet = W if (i + j) % 2 else B
                self.changeSS.emit(i, j, styleSheet)


class QueensGUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.n = 0
        self.start.clicked.connect(self.start_alg)

    def reshape(self, old_n, new_n):
        for i in range(old_n):
            for j in range(old_n):
                self.gridLayout.removeWidget(self.squares[i, j])
                self.squares[i, j].hide()

        self.squares = {}
        for i in range(new_n):
            for j in range(new_n):
                square = QLabel()
                self.gridLayout.addWidget(square, i, j)
                square.setStyleSheet(W if (i + j) % 2 else B)
                self.squares[i, j] = square

    @QtCore.pyqtSlot(int, int, str)
    def changeStyleSheet(self, i, j, s):
        self.squares[i, j].setStyleSheet(s)

    @QtCore.pyqtSlot()
    def endWork(self):
        QMessageBox.information(self, "Finito!", "Soluzione trovata!")
        self.start.setEnabled(True)

    def start_alg(self):
        try:
            n = int(self.num_text.text())
            if n <= 0 or n in [2, 3]:
                return
        except ValueError:
            QMessageBox.critical(self, "Errore", "Dati non validi!", )
        else:
            self.start.setEnabled(False)
            if n != self.n:
                self.reshape(self.n, n)
            self.n = n
            self.thread = QueenThread(self)
            self.thread.changeSS.connect(self.changeStyleSheet)
            self.thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QueensGUI()
    window.show()
    sys.exit(app.exec_())
