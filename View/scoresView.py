from PySide6 import QtCore, QtWidgets, QtGui
from Helper import dbhelper
from Data.score import Score


class ScoresView(QtWidgets.QWidget):

    def __init__(self, mainApp, parent=None):
        super(ScoresView, self).__init__(parent)

        self.mainApp = mainApp
        self.stackWidget = mainApp.stackedWidget

        self.mainApp.setWindowTitle("Notlar")

        self.headerLabel = QtWidgets.QLabel("Notlar", alignment=QtCore.Qt.AlignCenter)
        self.table = QtWidgets.QTableWidget()

        l = dbhelper.loadTable("scores")

        self.exams = []

        for row in l:
            self.exams.append(Score(row[0], row[1], row[2], row[3]))

        self.table.setRowCount(len(self.exams))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Not", "Öğrenci Id", "Sınav Id"])

        for i, c in enumerate(self.exams):
            self.table.setItem(i, 0, c.id)
            self.table.setItem(i, 1, c.score)
            self.table.setItem(i, 2, c.studentId)
            self.table.setItem(i, 3, c.examId)

        self.backBtn = QtWidgets.QPushButton("Geri Dön")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.headerLabel)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.backBtn)

        self.backBtn.clicked.connect(self.backToMenu)

    @QtCore.Slot()
    def backToMenu(self):
        self.stackWidget.setCurrentWidget(self.mainApp.menuView)
