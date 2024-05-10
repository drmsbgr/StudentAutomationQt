import sys
from PySide6 import QtCore, QtWidgets, QtGui
from app import MainApp
from Helper import dbhelper

dbhelper.connectDB()
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
    "CREATE TABLE IF NOT EXISTS scores(scoreId INTEGER PRIMARY KEY, score FLOAT, scoreStudentId INTEGER, scoreExamId INTEGER)"
)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainApp()
    widget.resize(800, 600)

    sys.exit(app.exec())
