from typing import override
from PySide6 import QtCore, QtWidgets, QtGui
from Helper import dbhelper
from Data.scoreType import ScoreType
from Data.baseView import BaseView


class ScoreTypesView(QtWidgets.QWidget, BaseView):

    def __init__(self, mainApp, parent=None):
        super(ScoreTypesView, self).__init__(parent)

        self.mainApp = mainApp
        self.stackWidget = mainApp.stackedWidget

        self.headerLabel = QtWidgets.QLabel(
            "Not Türleri", alignment=QtCore.Qt.AlignCenter
        )
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

        self.createScoreTypeGroup = QtWidgets.QGroupBox("Not Türü İşlemleri")
        self.createScoreTypeGroup.layout = QtWidgets.QVBoxLayout(
            self.createScoreTypeGroup
        )

        self.scoreTypeNameLabel = QtWidgets.QLabel("Not Türü Adı")
        self.scoreTypeNameInput = QtWidgets.QPlainTextEdit()
        self.createScoreTypBtn = QtWidgets.QPushButton("Not Türü Ekle")
        self.overwriteScoreTypBtn = QtWidgets.QPushButton(
            "Seçili Not Türünün Üzerine Kaydet"
        )
        self.deleteScoreTypBtn = QtWidgets.QPushButton("Seçili Not Türünü Sil")

        self.table.itemSelectionChanged.connect(self.updateInputs)

        self.createScoreTypeGroup.layout.addWidget(self.scoreTypeNameLabel)
        self.createScoreTypeGroup.layout.addWidget(self.scoreTypeNameInput)
        self.createScoreTypeGroup.layout.addWidget(self.createScoreTypBtn)
        self.createScoreTypeGroup.layout.addWidget(self.overwriteScoreTypBtn)
        self.createScoreTypeGroup.layout.addWidget(self.deleteScoreTypBtn)

        self.createScoreTypBtn.clicked.connect(self.createScoreType)
        self.overwriteScoreTypBtn.clicked.connect(self.overwriteScoreType)
        self.deleteScoreTypBtn.clicked.connect(self.deleteScoreType)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.headerLabel)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.createScoreTypeGroup)
        self.layout.addWidget(self.backBtn)

        self.backBtn.clicked.connect(self.backToMenu)

    @override
    def initTitle(self):
        self.mainApp.setWindowTitle("Not Türleri")
        self.refreshScoreTypes()

    @QtCore.Slot()
    def createScoreType(self):

        if self.scoreTypeNameInput.toPlainText() == "":
            return

        sql = """INSERT INTO scoreTypes (scoreTypeName) VALUES (?)"""

        dbhelper.executeSql(sql, (self.scoreTypeNameInput.toPlainText(),))

        self.refreshScoreTypes()

    @QtCore.Slot()
    def overwriteScoreType(self):
        if self.scoreTypeNameInput.toPlainText() == "":
            return
        rowIndex = self.table.selectedItems()[0].row()
        st = self.scoreTypes[rowIndex]

        sql = f"""UPDATE scoreTypes SET scoreTypeName='{self.scoreTypeNameInput.toPlainText()}' WHERE scoreTypeId={st.id}"""

        dbhelper.executeSql(sql, "")

        self.refreshScoreTypes()

    @QtCore.Slot()
    def deleteScoreType(self):
        rowIndex = self.table.selectedItems()[0].row()
        st = self.scoreTypes[rowIndex]

        sql = f"""DELETE FROM scoreTypes WHERE scoreTypeId={st.id}"""

        dbhelper.executeSql(sql, "")

        self.refreshScoreTypes()

    @QtCore.Slot()
    def updateInputs(self):
        rowIndex = self.table.selectedItems()[0].row()
        st = self.scoreTypes[rowIndex]
        self.scoreTypeNameInput.setPlainText(st.name)

    def refreshScoreTypes(self):
        l = dbhelper.loadTable("scoreTypes")

        self.scoreTypes = [ScoreType(row[0], row[1]) for row in l]

        self.table.setRowCount(len(self.scoreTypes))
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(["Not Türü"])

        for i, c in enumerate(self.scoreTypes):
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
