from Data.scoreType import ScoreType
from Data.student import Student
from Data.exam import Exam


class Score:
    def __init__(
        self, id: int, score: float, scoreType: ScoreType, student: Student, exam: Exam
    ):
        self.id = id
        self.score = score
        self.scoreType = scoreType
        self.student = student
        self.exam = exam
