from typing import override
from PySide6 import QtCore, QtWidgets, QtGui
from Helper import dbhelper
from Data.score import Score
from Data.baseView import BaseView


class ScoresView(QtWidgets.QWidget, BaseView):

    def __init__(self, mainApp, parent=None):
        super(ScoresView, self).__init__(parent)

        self.mainApp = mainApp
        self.stackWidget = mainApp.stackedWidget

        self.headerLabel = QtWidgets.QLabel("Notlar", alignment=QtCore.Qt.AlignCenter)
        self.table = QtWidgets.QTableWidget()

        self.table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        )
        self.table.setMinimumHeight(300)
        self.table.setMaximumHeight(600)

        self.refreshScores()

        self.backBtn = QtWidgets.QPushButton("Geri Dön")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.headerLabel)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.backBtn)

        self.backBtn.clicked.connect(self.backToMenu)

    def refreshScores(self):
        l = dbhelper.loadTable("scores")
        
        sql = """SELECT """

        self.exams = [Score()]

        for row in l:
            self.exams.append(Score(row[0], row[1], row[2], row[3]))

        self.table.setRowCount(len(self.exams))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Not", "Öğrenci Id", "Sınav Id"])

        for i, c in enumerate(self.exams):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(c.id))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(c.score))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(c.studentId))
            self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(c.examId))

    @override
    def initTitle(self):
        self.mainApp.setWindowTitle("Notlar")

    @QtCore.Slot()
    def backToMenu(self):
        self.mainApp.menuView.initTitle()
        self.stackWidget.setCurrentWidget(self.mainApp.menuView)
