from typing import override
from PySide6 import QtCore, QtWidgets, QtGui
from Helper import dbhelper
from Data.department import Department
from Data.baseView import BaseView


class DepartmentsView(QtWidgets.QWidget, BaseView):

    def __init__(self, mainApp, parent=None):
        super(DepartmentsView, self).__init__(parent)

        self.mainApp = mainApp
        self.stackWidget = mainApp.stackedWidget

        self.headerLabel = QtWidgets.QLabel("Bölümler", alignment=QtCore.Qt.AlignCenter)
        self.table = QtWidgets.QTableWidget()

        self.table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        )
        self.table.setMinimumHeight(300)
        self.table.setMaximumHeight(600)

        self.createDepartmentGroup = QtWidgets.QGroupBox("Bölüm İşlemleri")

        self.createDepartmentGroup.layout = QtWidgets.QVBoxLayout(
            self.createDepartmentGroup
        )

        self.departmentNameLabel = QtWidgets.QLabel("Bölüm Adı")
        self.depNameInput = QtWidgets.QPlainTextEdit()

        self.departmentDescLabel = QtWidgets.QLabel("Bölüm Açıklaması")
        self.depDescInput = QtWidgets.QPlainTextEdit()

        self.table.itemSelectionChanged.connect(self.updateInputs)

        self.createDepBtn = QtWidgets.QPushButton("Bölümü Ekle")
        self.overwriteDepBtn = QtWidgets.QPushButton("Seçilen Bölümün Üzerine Kaydet")
        self.deleteDepBtn = QtWidgets.QPushButton("Seçilen Bölümü Sil")
        self.createDepBtn.clicked.connect(self.createDepartment)
        self.overwriteDepBtn.clicked.connect(self.overwriteDepartment)
        self.deleteDepBtn.clicked.connect(self.deleteDepartment)

        self.createDepartmentGroup.layout.addWidget(self.departmentNameLabel)
        self.createDepartmentGroup.layout.addWidget(self.depNameInput)
        self.createDepartmentGroup.layout.addWidget(self.departmentDescLabel)
        self.createDepartmentGroup.layout.addWidget(self.depDescInput)
        self.createDepartmentGroup.layout.addWidget(self.createDepBtn)
        self.createDepartmentGroup.layout.addWidget(self.overwriteDepBtn)
        self.createDepartmentGroup.layout.addWidget(self.deleteDepBtn)

        self.backBtn = QtWidgets.QPushButton("Geri Dön")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.headerLabel)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.createDepartmentGroup)
        self.layout.addWidget(self.backBtn)

        self.backBtn.clicked.connect(self.backToMenu)

    @override
    def initTitle(self):
        self.mainApp.setWindowTitle("Bölümler")
        self.refreshDepartments()

    @QtCore.Slot()
    def updateInputs(self):
        if len(self.table.selectedItems()) == 0:
            return
        selectedRow = self.table.selectedItems()
        self.depNameInput.setPlainText(selectedRow[0].text())
        self.depDescInput.setPlainText(selectedRow[1].text())

    @QtCore.Slot()
    def createDepartment(self):

        if (
            self.depNameInput.toPlainText() == ""
            or self.depDescInput.toPlainText() == ""
        ):
            return

        sql = """INSERT INTO departments (departmentName,departmentDesc) VALUES (?,?)"""

        dbhelper.executeSql(
            sql, (self.depNameInput.toPlainText(), self.depDescInput.toPlainText())
        )

        self.refreshDepartments()

    @QtCore.Slot()
    def overwriteDepartment(self):

        if (
            self.depNameInput.toPlainText() == ""
            or self.depDescInput.toPlainText() == ""
        ):
            return

        rowIndex = self.table.selectedItems()[0].row()
        selectedDepartment = self.departments[rowIndex]
        sql = f"""UPDATE departments SET departmentName='{self.depNameInput.toPlainText()}',departmentDesc='{self.depDescInput.toPlainText()}' WHERE departmentId={selectedDepartment.id}"""
        dbhelper.executeSql(sql)
        self.refreshDepartments()

    @QtCore.Slot()
    def deleteDepartment(self):
        if len(self.table.selectedItems()) == 0:
            return
        rowIndex = self.table.selectedItems()[0].row()
        selectedDepartment = self.departments[rowIndex]
        sql = f"""DELETE FROM departments WHERE departmentId={selectedDepartment.id}"""
        dbhelper.executeSql(sql, "")
        self.refreshDepartments()

    def refreshDepartments(self):
        l = dbhelper.loadTable("departments")

        self.departments = [Department(row[0], row[1], row[2]) for row in l]

        self.table.setRowCount(len(self.departments))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(
            ["Bölüm Adı", "Bölüm Açıklaması", "Öğrenci Sayısı"]
        )

        for i, c in enumerate(self.departments):
            # self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(c.id)))
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(c.name)))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(c.desc)))
            sql1 = f"""SELECT * FROM students WHERE studentDepartmentId={c.id}"""
            conn = dbhelper.connectDB()
            cur = conn.cursor()
            students = cur.execute(sql1).fetchall()
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(len(students))))
            conn.close()

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
