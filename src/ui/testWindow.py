import sys
from PyQt4 import QtCore, QtGui, uic

form_class = uic.loadUiType("ui/testUI.ui")[0]                 # Load the UI

class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.btn1.clicked.connect(self.btn_clicked)
        self.text.textChanged.connect(self.textChanged)

        # self.btn_CtoF.clicked.connect(self.btn_CtoF_clicked)  # Bind the event handlers
        # self.btn_FtoC.clicked.connect(self.btn_FtoC_clicked)  #   to the buttons

    # def btn_CtoF_clicked(self):                  # CtoF button event handler
    #     cel = float(self.editCel.text())         #
    #     fahr = cel * 9 / 5.0 + 32                #
    #     self.spinFahr.setValue(int(fahr + 0.5))  #
    #
    # def btn_FtoC_clicked(self):                  # FtoC button event handler
    #     fahr = self.spinFahr.value()             #
    #     cel = (fahr - 32) *                      #
    #     self.editCel.setText(str(cel))           #

    def btn_clicked(self):
        print "button Clicked!"

    def textChanged(self):
        self.label.setText(self.text.toPlainText())

# app = QtGui.QApplication(sys.argv)
# myWindow = MyWindowClass(None)
# myWindow.show()
# app.exec_()