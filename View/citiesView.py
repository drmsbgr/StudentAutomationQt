from typing import override
from PySide6 import QtCore, QtWidgets, QtGui
from Helper import dbhelper
from Data.city import City
from Data.baseView import BaseView


class CitiesView(QtWidgets.QWidget, BaseView):

    def __init__(self, mainApp, parent=None):
        super(CitiesView, self).__init__(parent)

        self.mainApp = mainApp
        self.stackWidget = mainApp.stackedWidget
        self.headerLabel = QtWidgets.QLabel("Şehirler", alignment=QtCore.Qt.AlignCenter)
        self.table = QtWidgets.QTableWidget()
        self.table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        )
        self.table.setMinimumHeight(300)
        self.table.setMaximumHeight(600)

        self.backBtn = QtWidgets.QPushButton("Geri Dön")

        self.createCityGroup = QtWidgets.QGroupBox("Şehir İşlemleri")
        self.createCityGroup.layout = QtWidgets.QVBoxLayout(self.createCityGroup)

        self.cityNameLabel = QtWidgets.QLabel("Şehir Adı")
        self.cityNameInput = QtWidgets.QPlainTextEdit()
        self.createCityBtn = QtWidgets.QPushButton("Şehir Ekle")
        self.overwriteCityBtn = QtWidgets.QPushButton("Seçili Şehrin Üzerine Kaydet")
        self.deleteCityBtn = QtWidgets.QPushButton("Seçili Şehri Sil")

        self.table.itemSelectionChanged.connect(self.updateInputs)

        self.createCityGroup.layout.addWidget(self.cityNameLabel)
        self.createCityGroup.layout.addWidget(self.cityNameInput)
        self.createCityGroup.layout.addWidget(self.createCityBtn)
        self.createCityGroup.layout.addWidget(self.overwriteCityBtn)
        self.createCityGroup.layout.addWidget(self.deleteCityBtn)

        self.createCityBtn.clicked.connect(self.createCity)
        self.overwriteCityBtn.clicked.connect(self.overwriteCity)
        self.deleteCityBtn.clicked.connect(self.deleteCity)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.headerLabel)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.createCityGroup)
        self.layout.addWidget(self.backBtn)

        self.backBtn.clicked.connect(self.backToMenu)

    @override
    def initTitle(self):
        self.mainApp.setWindowTitle("Şehirler")
        self.refreshCities()

    @QtCore.Slot()
    def updateInputs(self):
        rowIndex = self.table.selectedItems()[0].row()
        c = self.cities[rowIndex]
        self.cityNameInput.setPlainText(c.name)

    @QtCore.Slot()
    def createCity(self):
        if self.cityNameInput.toPlainText() == "":
            return

        sql = """INSERT INTO cities (cityName) VALUES (?)"""

        dbhelper.executeSql(sql, (self.cityNameInput.toPlainText(),))

        self.refreshCities()

    @QtCore.Slot()
    def overwriteCity(self):
        if self.cityNameInput.toPlainText() == "":
            return
        rowIndex = self.table.selectedItems()[0].row()
        c = self.cities[rowIndex]

        sql = f"""UPDATE cities SET cityName='{self.cityNameInput.toPlainText()}' WHERE cityId={c.id}"""

        dbhelper.executeSql(sql, "")

        self.refreshCities()

    @QtCore.Slot()
    def deleteCity(self):
        rowIndex = self.table.selectedItems()[0].row()
        c = self.cities[rowIndex]

        sql = f"""DELETE FROM cities WHERE cityId={c.id}"""

        dbhelper.executeSql(sql, "")

        self.refreshCities()

    def refreshCities(self):
        l = dbhelper.loadTable("cities")

        self.cities = [City(row[0], row[1]) for row in l]

        self.table.setRowCount(len(self.cities))
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(["Şehir Adı"])

        for i, c in enumerate(self.cities):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(c.name)))

        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                self.table.item(row, col).setFlags(
                    self.table.item(row, col).flags()
                    ^ QtCore.Qt.ItemFlag.ItemIsEditable
                )

    @QtCore.Slot()
    def backToMenu(self):
        self.mainApp.menuView.initTitle()
        self.stackWidget.setCurrentWidget(self.mainApp.menuView)
