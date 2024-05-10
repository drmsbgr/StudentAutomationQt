from Data.city import City
from Data.department import Department


class Student:

    def __init__(
        self,
        id: int,
        name: str,
        surname: str,
        no: int,
        city: City,
        department: Department,
    ):
        self.id = id
        self.name = name
        self.surname = surname
        self.no = no
        self.city = city
        self.department = department
