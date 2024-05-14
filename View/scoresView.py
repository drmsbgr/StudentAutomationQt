from typing import override
from PySide6 import QtCore, QtWidgets, QtGui
from Helper import dbhelper
from Data.score import Score
from Data.baseView import BaseView
from Data.scoreType import ScoreType
from Data.student import Student
from Data.exam import Exam


class ScoresView(QtWidgets.QWidget, BaseView):

    def __init__(self, mainApp, parent=None):
        super(ScoresView, self).__init__(parent)

        self.mainApp = mainApp
        self.stackWidget = mainApp.stackedWidget
        self.layout = QtWidgets.QVBoxLayout(self)

    def initUI(self):
        self.headerLabel = QtWidgets.QLabel("Notlar", alignment=QtCore.Qt.AlignCenter)

        self.listingOptionsGroup = QtWidgets.QGroupBox("Listeleme İşlemleri")
        self.listingOptionsGroup.layout = QtWidgets.QVBoxLayout(
            self.listingOptionsGroup
        )
        self.examInputLabel = QtWidgets.QLabel("Sınav Seçin")
        self.examInput = QtWidgets.QComboBox()
        self.examInput.currentIndexChanged.connect(self.refreshScores)

        self.listingOptionsGroup.layout.addWidget(self.examInputLabel)
        self.listingOptionsGroup.layout.addWidget(self.examInput)

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

        self.scoreOperationsGroup = QtWidgets.QGroupBox("Not İşlemleri")
        self.scoreOperationsGroup.layout = QtWidgets.QVBoxLayout(
            self.scoreOperationsGroup
        )

        self.studentInputLabel = QtWidgets.QLabel("Öğrenci Seçin")
        self.studentInput = QtWidgets.QComboBox()

        self.scoreInputLabel = QtWidgets.QLabel("Not Girin")
        self.scoreInput = QtWidgets.QSpinBox()
        self.scoreInput.setMinimum(0)
        self.scoreInput.setMaximum(100)

        self.scoreTypeInputLabel = QtWidgets.QLabel("Not Türü Seçin")
        self.scoreTypeInput = QtWidgets.QComboBox()

        self.createScoreBtn = QtWidgets.QPushButton("Not Ekle")
        self.deleteScoreBtn = QtWidgets.QPushButton("Seçilen Notu Sil")

        self.createScoreBtn.clicked.connect(self.createScore)
        self.deleteScoreBtn.clicked.connect(self.deleteScore)

        self.scoreOperationsGroup.layout.addWidget(self.studentInputLabel)
        self.scoreOperationsGroup.layout.addWidget(self.studentInput)
        self.scoreOperationsGroup.layout.addWidget(self.scoreInputLabel)
        self.scoreOperationsGroup.layout.addWidget(self.scoreInput)
        self.scoreOperationsGroup.layout.addWidget(self.scoreTypeInputLabel)
        self.scoreOperationsGroup.layout.addWidget(self.scoreTypeInput)
        self.scoreOperationsGroup.layout.addWidget(self.createScoreBtn)
        self.scoreOperationsGroup.layout.addWidget(self.deleteScoreBtn)

        self.backBtn = QtWidgets.QPushButton("Geri Dön")

        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        self.layout.addWidget(self.headerLabel)
        self.layout.addWidget(self.listingOptionsGroup)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.scoreOperationsGroup)
        self.layout.addWidget(self.backBtn)

        self.backBtn.clicked.connect(self.backToMenu)

    @QtCore.Slot()
    def updateInputs(self):
        if len(self.table.selectedItems()) == 0:
            return
        rowIndex = self.table.selectedItems()[0].row()
        s = self.scores[rowIndex]
        self.scoreInput.setValue(s.score)

        i = 0
        for student in self.loadedStudents:
            if student.id == s.student.id:
                break
            i += 1

        self.studentInput.setCurrentIndex(i)

        i = 0
        for scoreType in self.loadedScoreTypes:
            if scoreType.id == s.scoreType.id:
                break
            i += 1

        self.scoreTypeInput.setCurrentIndex(i)

    @QtCore.Slot()
    def createScore(self):
        sql = """INSERT INTO scores (score,scoreTypeId,scoreStudentId,scoreExamId) VALUES (?,?,?,?)"""
        dbhelper.executeSql(
            sql,
            params=(
                self.scoreInput.value(),
                self.loadedScoreTypes[self.scoreTypeInput.currentIndex()].id,
                self.loadedStudents[self.studentInput.currentIndex()].id,
                self.loadedExams[self.examInput.currentIndex()].id,
            ),
        )

        self.refreshScores()

    @QtCore.Slot()
    def deleteScore(self):
        if len(self.table.selectedItems()) == 0:
            return
        rowIndex = self.table.selectedItems()[0].row()
        s = self.scores[rowIndex]

        sql = f"""DELETE FROM scores WHERE scoreId={s.id}"""

        dbhelper.executeSql(sql, "")
        self.refreshScores()

    def refreshScores(self):

        sql = f"""
        SELECT scoreId,score,scoreTypes.scoreTypeId,scoreTypeName,studentId,studentName,studentSurname,studentNo,examId,examName FROM scores
        INNER JOIN scoreTypes ON scores.scoreTypeId=scoreTypes.scoreTypeId
        INNER JOIN students ON studentId=scoreStudentId
        INNER JOIN exams ON examId=scoreExamId
        WHERE examId={self.loadedExams[self.examInput.currentIndex()].id}
        ORDER BY scores.scoreTypeId"""

        conn = dbhelper.connectDB()
        cur = conn.cursor()

        l = cur.execute(sql).fetchall()

        self.scores = [
            Score(
                row[0],
                row[1],
                ScoreType(row[2], row[3]),
                Student(row[4], row[5], row[6], row[7], None, None),
                Exam(row[8], row[9]),
            )
            for row in l
        ]

        self.table.setRowCount(len(self.scores))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            [
                "Öğrenci Adı",
                "Öğrenci Soyadı",
                "Öğrenci No",
                "Not Türü",
                "Not",
            ]
        )

        for i, c in enumerate(self.scores):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(c.student.name)))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(c.student.surname)))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(c.student.no)))
            self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(c.scoreType.name)))
            self.table.setItem(i, 4, QtWidgets.QTableWidgetItem(str(c.score)))

        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                self.table.item(row, col).setFlags(
                    self.table.item(row, col).flags()
                    ^ QtCore.Qt.ItemFlag.ItemIsEditable
                )

    @override
    def initTitle(self):
        self.mainApp.setWindowTitle("Notlar")

        if (
            len(dbhelper.loadTable("students")) == 0
            or len(dbhelper.loadTable("scoreTypes")) == 0
            or len(dbhelper.loadTable("exams")) == 0
        ):
            self.warningLabel = QtWidgets.QLabel(
                "Not ekleyebilmek için önce lütfen en az bir öğrenci, not türü ve sınav oluşturun.",
                alignment=QtCore.Qt.AlignCenter,
            )
            self.backBtn = QtWidgets.QPushButton("Geri Dön")
            self.backBtn.clicked.connect(self.backToMenu)
            for i in reversed(range(self.layout.count())):
                self.layout.itemAt(i).widget().setParent(None)
            self.layout.addWidget(self.warningLabel)
            self.layout.addWidget(self.backBtn)
            return

        self.initUI()

        self.loadedExams = [Exam(row[0], row[1]) for row in dbhelper.loadTable("exams")]
        self.examInput.clear()
        self.examInput.addItems([e.name for e in self.loadedExams])

        self.loadedStudents = [
            Student(row[0], row[1], row[2], None, None, None)
            for row in dbhelper.loadTable("students")
        ]
        self.studentInput.clear()
        self.studentInput.addItems(
            [f"{s.name} {s.surname}" for s in self.loadedStudents]
        )

        self.loadedScoreTypes = [
            ScoreType(row[0], row[1]) for row in dbhelper.loadTable("scoreTypes")
        ]
        self.scoreTypeInput.clear()
        self.scoreTypeInput.addItems(st.name for st in self.loadedScoreTypes)

        self.refreshScores()

    @QtCore.Slot()
    def backToMenu(self):
        self.mainApp.menuView.initTitle()
        self.stackWidget.setCurrentWidget(self.mainApp.menuView)
