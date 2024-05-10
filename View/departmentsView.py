from PySide6 import QtCore, QtWidgets, QtGui
from Helper import dbhelper
from Data.department import Department


class DepartmentsView(QtWidgets.QWidget):

    def __init__(self, mainApp, parent=None):
        super(DepartmentsView, self).__init__(parent)

        self.mainApp = mainApp
        self.stackWidget = mainApp.stackedWidget

        self.mainApp.setWindowTitle("Bölümler")

        self.headerLabel = QtWidgets.QLabel("Bölümler", alignment=QtCore.Qt.AlignCenter)
        self.table = QtWidgets.QTableWidget()

        l = dbhelper.loadTable("departments")

        self.departments = []

        for row in l:
            self.departments.append(Department(row[0], row[1], row[2]))

        self.table.setRowCount(len(self.departments))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Bölüm Adı", "Bölüm Açıklaması"])

        for i, c in enumerate(self.departments):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(c.id))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(c.name))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(c.desc))

        self.backBtn = QtWidgets.QPushButton("Geri Dön")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.headerLabel)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.backBtn)

        self.backBtn.clicked.connect(self.backToMenu)

    @QtCore.Slot()
    def backToMenu(self):
        self.stackWidget.setCurrentWidget(self.mainApp.menuView)
