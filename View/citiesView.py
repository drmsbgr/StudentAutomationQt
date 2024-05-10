from PySide6 import QtCore, QtWidgets, QtGui
from Helper import dbhelper
from Data.city import City


class CitiesView(QtWidgets.QWidget):

    def __init__(self, mainApp, parent=None):
        super(CitiesView, self).__init__(parent)

        self.mainApp = mainApp
        self.stackWidget = mainApp.stackedWidget

        self.mainApp.setWindowTitle("Şehirler")

        self.headerLabel = QtWidgets.QLabel("Şehirler", alignment=QtCore.Qt.AlignCenter)
        self.table = QtWidgets.QTableWidget()

        l = dbhelper.loadTable("cities")

        self.cities = []

        for row in l:
            self.cities.append(City(row[0], row[1]))

        self.table.setRowCount(len(self.cities))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "Şehir Adı"])

        for i, c in enumerate(self.cities):
            self.table.setItem(i, 0, c.id)
            self.table.setItem(i, 1, c.name)

        self.backBtn = QtWidgets.QPushButton("Geri Dön")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.headerLabel)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.backBtn)

        self.backBtn.clicked.connect(self.backToMenu)

    @QtCore.Slot()
    def backToMenu(self):
        self.stackWidget.setCurrentWidget(self.mainApp.menuView)
