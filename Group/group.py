from Lecture.lectureIter import LectureIter


class Group:
    def __init__(self, sheet, row=4, col=2):
        self.sheet = sheet
        self.row = row
        self.col = col

    def get_name(self) -> str:
        cell = self.sheet[self.row, self.col]
        if cell is None:
            return ''
        return str(cell.value)

    def get_lecture_iter(self):
        return LectureIter(self.sheet, self.row + 1, self.col, self.get_name())

