from PySide6 import QtCore, QtWidgets, QtGui
from Helper import dbhelper
from Data.student import Student


class StudentsView(QtWidgets.QWidget):

    def __init__(self, mainApp, parent=None):
        super(StudentsView, self).__init__(parent)

        self.mainApp = mainApp
        self.stackWidget = mainApp.stackedWidget

        self.mainApp.setWindowTitle("Öğrenciler")

        self.headerLabel = QtWidgets.QLabel(
            "Öğrenciler", alignment=QtCore.Qt.AlignCenter
        )
        self.table = QtWidgets.QTableWidget()
        self.refreshStudents()

        self.backBtn = QtWidgets.QPushButton("Geri Dön")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.headerLabel)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.backBtn)

        self.backBtn.clicked.connect(self.backToMenu)

    def refreshStudents(self):

        l = dbhelper.loadTable("students")

        self.students = []

        for row in l:
            self.students.append(
                Student(row[0], row[1], row[2], row[3], row[4], row[5])
            )

        self.table.setRowCount(len(self.students))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Ad", "Soyad", "Öğrenci No", "Şehir", "Bölüm"]
        )

        for i, s in enumerate(self.students):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(s.id)))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(s.name)))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(s.surname)))
            self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(s.no)))
            self.table.setItem(i, 4, QtWidgets.QTableWidgetItem(str(s.cityId)))
            self.table.setItem(i, 5, QtWidgets.QTableWidgetItem(str(s.departmentId)))

    @QtCore.Slot()
    def backToMenu(self):
        self.stackWidget.setCurrentWidget(self.mainApp.menuView)
