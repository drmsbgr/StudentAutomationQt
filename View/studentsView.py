from typing import override
from PySide6 import QtCore, QtWidgets, QtGui
from Helper import dbhelper
from Data.student import Student
from Data.city import City
from Data.department import Department
from Data.baseView import BaseView


class StudentsView(QtWidgets.QWidget, BaseView):

    def __init__(self, mainApp, parent=None):
        super(StudentsView, self).__init__(parent)

        self.mainApp = mainApp
        self.stackWidget = mainApp.stackedWidget

        self.headerLabel = QtWidgets.QLabel(
            "Öğrenciler", alignment=QtCore.Qt.AlignCenter
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

        self.refreshStudents()

        self.backBtn = QtWidgets.QPushButton("Geri Dön")

        self.createStudentGroup = QtWidgets.QGroupBox("Öğrenci İşlemleri")

        self.nameLabel = QtWidgets.QLabel("Öğrenci Adı")
        self.nameInput = QtWidgets.QPlainTextEdit()
        self.surnameLabel = QtWidgets.QLabel("Öğrenci Soyadı")
        self.surnameInput = QtWidgets.QPlainTextEdit()
        self.noLabel = QtWidgets.QLabel("Öğrenci No")
        self.noInput = QtWidgets.QSpinBox()
        self.noInput.setMaximum(9999)
        self.cityLabel = QtWidgets.QLabel("Öğrenci Şehir")
        self.cityInput = QtWidgets.QComboBox()
        self.departmentLabel = QtWidgets.QLabel("Öğrenci Bölüm")
        self.departmentInput = QtWidgets.QComboBox()

        self.table.itemSelectionChanged.connect(self.updateInputs)

        self.createStudentBtn = QtWidgets.QPushButton("Öğrenci Ekle")
        self.overwriteStudentBtn = QtWidgets.QPushButton(
            "Seçilen Öğrencinin Üzerine Kaydet"
        )
        self.deleteStudentBtn = QtWidgets.QPushButton("Seçilen Öğrenciyi Sil")

        self.createStudentGroup.layout = QtWidgets.QVBoxLayout(self.createStudentGroup)
        self.createStudentGroup.layout.addWidget(self.nameLabel)
        self.createStudentGroup.layout.addWidget(self.nameInput)
        self.createStudentGroup.layout.addWidget(self.surnameLabel)
        self.createStudentGroup.layout.addWidget(self.surnameInput)
        self.createStudentGroup.layout.addWidget(self.noLabel)
        self.createStudentGroup.layout.addWidget(self.noInput)
        self.createStudentGroup.layout.addWidget(self.cityLabel)
        self.createStudentGroup.layout.addWidget(self.cityInput)
        self.createStudentGroup.layout.addWidget(self.departmentLabel)
        self.createStudentGroup.layout.addWidget(self.departmentInput)
        self.createStudentGroup.layout.addWidget(self.createStudentBtn)
        self.createStudentGroup.layout.addWidget(self.overwriteStudentBtn)
        self.createStudentGroup.layout.addWidget(self.deleteStudentBtn)

        self.createStudentBtn.clicked.connect(self.createStudent)
        self.overwriteStudentBtn.clicked.connect(self.createStudent)
        self.deleteStudentBtn.clicked.connect(self.deleteStudent)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.headerLabel)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.createStudentGroup)
        self.layout.addWidget(self.backBtn)

        self.backBtn.clicked.connect(self.backToMenu)

    @QtCore.Slot()
    def createStudent(self):
        if self.nameInput.toPlainText() == "" or self.surnameInput.toPlainText() == "":
            return

        sql = """INSERT INTO students VALUES(NULL,?,?,?,?,?)"""
        dbhelper.executeSql(
            sql,
            (
                self.nameInput.toPlainText(),
                self.surnameInput.toPlainText(),
                self.noInput.value(),
                self.loadedCities[self.cityInput.currentIndex()].id,
                self.loadedDepartments[self.departmentInput.currentIndex()].id,
            ),
        )

        self.refreshStudents()

    @QtCore.Slot()
    def deleteStudent(self):
        rowIndex = self.table.selectedItems()[0].row()
        s = self.students[rowIndex]

        sql = f"""DELETE FROM students WHERE studentId={s.id}"""
        dbhelper.executeSql(sql, "")
        self.refreshStudents()

    @override
    def initTitle(self):
        self.mainApp.setWindowTitle("Öğrenciler")
        self.refreshStudents()
        self.loadedCities = [
            City(row[0], row[1]) for row in dbhelper.loadTable("cities")
        ]
        self.cityInput.clear()
        self.cityInput.addItems([item.name for item in self.loadedCities])

        self.loadedDepartments = [
            Department(row[0], row[1], row[2])
            for row in dbhelper.loadTable("departments")
        ]
        self.departmentInput.clear()
        self.departmentInput.addItems([item.name for item in self.loadedDepartments])

    @QtCore.Slot()
    def updateInputs(self):
        rowIndex = self.table.selectedItems()[0].row()
        s = self.students[rowIndex]

        self.nameInput.setPlainText(s.name)
        self.surnameInput.setPlainText(s.surname)
        self.noInput.setValue(s.no)

        i = 0
        for city in self.loadedCities:
            if city.name == s.city.name:
                break
            i += 1

        self.cityInput.setCurrentIndex(i)

        i = 0

        for dep in self.loadedDepartments:
            if dep.name == s.department.name:
                break
            i += 1

        self.departmentInput.setCurrentIndex(i)

    def refreshStudents(self):

        sql = """
        SELECT studentId, studentName, studentSurname, studentNo, cityId, cityName , departmentId, departmentName, departmentDesc FROM students
        INNER JOIN cities ON students.studentCityId = cities.cityId
        INNER JOIN departments ON students.studentDepartmentId = departments.departmentId
        """

        conn = dbhelper.connectDB()
        cur = conn.cursor()

        l = cur.execute(sql).fetchall()

        conn.close()

        self.students = [
            Student(
                row[0],
                row[1],
                row[2],
                row[3],
                City(row[4], row[5]),
                Department(row[6], row[7], row[8]),
            )
            for row in l
        ]

        self.table.setRowCount(len(self.students))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Ad", "Soyad", "Öğrenci No", "Şehir", "Bölüm"]
        )

        for i, s in enumerate(self.students):
            # self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(s.id)))
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(s.name)))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(s.surname)))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(s.no)))
            self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(s.city.name)))
            self.table.setItem(i, 4, QtWidgets.QTableWidgetItem(str(s.department.name)))

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
