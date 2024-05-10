from PySide6 import QtCore, QtWidgets, QtGui
from View.menuView import MenuView
from View.studentsView import StudentsView
from View.citiesView import CitiesView
from View.departmentsView import DepartmentsView
from View.scoresView import ScoresView
from View.scoreTypesView import ScoreTypesView
from View.examsView import ExamsView


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.stackedWidget = QtWidgets.QStackedWidget()

        self.menuView = MenuView(self)
        self.studentsView = StudentsView(self)
        self.examsView = ExamsView(self)
        self.scoresView = ScoresView(self)
        self.scoreTypesView = ScoreTypesView(self)
        self.departmentsView = DepartmentsView(self)
        self.citiesView = CitiesView(self)

        self.setCentralWidget(self.stackedWidget)
        self.stackedWidget.addWidget(self.menuView)
        self.stackedWidget.addWidget(self.studentsView)
        self.stackedWidget.addWidget(self.examsView)
        self.stackedWidget.addWidget(self.scoresView)
        self.stackedWidget.addWidget(self.scoreTypesView)
        self.stackedWidget.addWidget(self.departmentsView)
        self.stackedWidget.addWidget(self.citiesView)
        self.stackedWidget.setCurrentWidget(self.menuView)
        self.show()
