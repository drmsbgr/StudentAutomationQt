from PySide6 import QtCore, QtWidgets, QtGui


class MenuView(QtWidgets.QWidget):

    def __init__(self, mainApp, parent=None):
        super(MenuView, self).__init__(parent)

        self.mainApp = mainApp
        self.stackWidget = mainApp.stackedWidget

        self.mainApp.setWindowTitle("Ana Menü")

        self.headerLabel = QtWidgets.QLabel(
            "Tablo Seçin", alignment=QtCore.Qt.AlignCenter
        )
        self.studentsBtn = QtWidgets.QPushButton("Öğrenciler")
        self.examsBtn = QtWidgets.QPushButton("Sınavlar")
        self.scoresBtn = QtWidgets.QPushButton("Notlar")
        self.departmentsBtn = QtWidgets.QPushButton("Bölümler")
        self.citiesBtn = QtWidgets.QPushButton("Şehirler")
        self.quitBtn = QtWidgets.QPushButton("Çık")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.headerLabel)
        self.layout.addWidget(self.studentsBtn)
        self.layout.addWidget(self.examsBtn)
        self.layout.addWidget(self.scoresBtn)
        self.layout.addWidget(self.departmentsBtn)
        self.layout.addWidget(self.citiesBtn)
        self.layout.addWidget(self.quitBtn)

        self.studentsBtn.clicked.connect(
            lambda: self.openView(self.mainApp.studentsView)
        )
        self.examsBtn.clicked.connect(lambda: self.openView(self.mainApp.examsView))
        self.scoresBtn.clicked.connect(lambda: self.openView(self.mainApp.scoresView))
        self.departmentsBtn.clicked.connect(
            lambda: self.openView(self.mainApp.departmentsView)
        )
        self.citiesBtn.clicked.connect(lambda: self.openView(self.mainApp.citiesView))
        self.quitBtn.clicked.connect(quit)

    @QtCore.Slot()
    def openView(self, targetView):
        self.stackWidget.setCurrentWidget(targetView)
