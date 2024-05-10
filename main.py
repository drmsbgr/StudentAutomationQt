import sys
from PySide6 import QtCore, QtWidgets, QtGui
from app import MainApp
from Helper import dbhelper

dbhelper.connectDB()
dbhelper.createTable(
    "CREATE TABLE IF NOT EXISTS scoreTypes(scoreTypeId INTEGER, scoreTypeName VARCHAR(255))"
)

scoreTypes = dbhelper.loadTable("scoreTypes")
labels = [row[1] for row in scoreTypes]

if "MIDTERM" not in labels:
    dbhelper.executeSql(
        "INSERT INTO scoreTypes (scoreTypeId,scoreTypeName) VALUES (1,'MIDTERM')"
    )


if "FINAL" not in labels:
    dbhelper.executeSql(
        "INSERT INTO scoreTypes (scoreTypeId,scoreTypeName) VALUES (2,'FINAL')"
    )

dbhelper.createTable(
    "CREATE TABLE IF NOT EXISTS students(studentId INTEGER PRIMARY KEY,studentName VARCHAR(255) ,studentSurname VARCHAR(255),studentNo INTEGER,studentCityId INTEGER,studentDepartmentId INTEGER)"
)
dbhelper.createTable(
    "CREATE TABLE IF NOT EXISTS departments(departmentId INTEGER PRIMARY KEY,departmentName VARCHAR(255),departmentDesc VARCHAR(255))"
)
dbhelper.createTable(
    "CREATE TABLE IF NOT EXISTS cities(cityId INTEGER PRIMARY KEY, cityName VARCHAR(255))"
)
dbhelper.createTable(
    "CREATE TABLE IF NOT EXISTS exams(examId INTEGER PRIMARY KEY, examName VARCHAR(255))"
)
dbhelper.createTable(
    "CREATE TABLE IF NOT EXISTS scores(scoreId INTEGER PRIMARY KEY, score FLOAT, scoreTypeId INTEGER, scoreStudentId INTEGER, scoreExamId INTEGER)"
)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainApp()
    widget.resize(800, 600)

    sys.exit(app.exec())
