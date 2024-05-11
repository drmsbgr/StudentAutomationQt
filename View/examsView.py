from typing import override
from PySide6 import QtCore, QtWidgets, QtGui
from Helper import dbhelper
from Data.exam import Exam
from Data.baseView import BaseView


class ExamsView(QtWidgets.QWidget, BaseView):

    def __init__(self, mainApp, parent=None):
        super(ExamsView, self).__init__(parent)

        self.mainApp = mainApp
        self.stackWidget = mainApp.stackedWidget

        self.headerLabel = QtWidgets.QLabel("Sınavlar", alignment=QtCore.Qt.AlignCenter)
        self.table = QtWidgets.QTableWidget()
        self.table.itemSelectionChanged.connect(self.updateInputs)

        self.table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        )
        self.table.setMinimumHeight(300)
        self.table.setMaximumHeight(600)

        self.examOperationsGroup = QtWidgets.QGroupBox("Sınav İşlemleri")
        self.examOperationsGroup.layout = QtWidgets.QVBoxLayout(
            self.examOperationsGroup
        )

        self.examNameInputLabel = QtWidgets.QLabel("Sınav Adı")
        self.examNameInput = QtWidgets.QPlainTextEdit()
        self.createExamBtn = QtWidgets.QPushButton("Sınav Ekle")
        self.overwriteExamBtn = QtWidgets.QPushButton("Seçili Sınavın Üzerine Kaydet")
        self.deleteExamBtn = QtWidgets.QPushButton("Seçili Sınavı Sil")

        self.examOperationsGroup.layout.addWidget(self.examNameInputLabel)
        self.examOperationsGroup.layout.addWidget(self.examNameInput)
        self.examOperationsGroup.layout.addWidget(self.createExamBtn)
        self.examOperationsGroup.layout.addWidget(self.overwriteExamBtn)
        self.examOperationsGroup.layout.addWidget(self.deleteExamBtn)

        self.createExamBtn.clicked.connect(self.createExam)
        self.overwriteExamBtn.clicked.connect(self.overwriteExam)
        self.deleteExamBtn.clicked.connect(self.deleteExam)

        self.backBtn = QtWidgets.QPushButton("Geri Dön")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.headerLabel)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.examOperationsGroup)
        self.layout.addWidget(self.backBtn)

        self.backBtn.clicked.connect(self.backToMenu)

    @override
    def initTitle(self):
        self.mainApp.setWindowTitle("Sınavlar")
        self.refreshExams()

    @QtCore.Slot()
    def createExam(self):
        if self.examNameInput.toPlainText() == "":
            return

        sql = f"""INSERT INTO exams (examName) VALUES (?)"""
        dbhelper.executeSql(sql, params=(self.examNameInput.toPlainText(),))
        self.refreshExams()

    @QtCore.Slot()
    def overwriteExam(self):
        if self.examNameInput.toPlainText() == "":
            return
        rowIndex = self.table.selectedItems()[0].row()
        e = self.exams[rowIndex]

        sql = f"""UPDATE exams SET examName='{self.examNameInput.toPlainText()}' WHERE examId={e.id}"""
        dbhelper.executeSql(sql, "")
        self.refreshExams()

    @QtCore.Slot()
    def deleteExam(self):
        rowIndex = self.table.selectedItems()[0].row()
        e = self.exams[rowIndex]

        sql = f"""DELETE FROM scores WHERE scoreExamId={e.id}"""
        dbhelper.executeSql(sql, "")

        sql = f"""DELETE FROM exams WHERE examId={e.id}"""
        dbhelper.executeSql(sql, "")
        self.refreshExams()

    @QtCore.Slot()
    def updateInputs(self):
        rowIndex = self.table.selectedItems()[0].row()
        e = self.exams[rowIndex]

        self.examNameInput.setPlainText(e.name)

    def refreshExams(self):
        l = dbhelper.loadTable("exams")

        self.exams = [Exam(row[0], row[1]) for row in l]

        self.table.setRowCount(len(self.exams))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(
            ["Sınav Adı", "Sınava Giren Öğrenci Sayısı", "Ortalama"]
        )

        for i, c in enumerate(self.exams):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(c.name))
            sql = f"""SELECT score FROM scores WHERE scoreExamId={c.id}"""
            conn = dbhelper.connectDB()
            cur = conn.cursor()
            scores = cur.execute(sql).fetchall()

            participant = len(scores)

            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(participant)))

            average = 0

            for item in scores:
                average += item[0]

            if participant > 0:
                average /= participant

            self.table.setItem(
                i,
                2,
                QtWidgets.QTableWidgetItem(str(average)),
            )

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
