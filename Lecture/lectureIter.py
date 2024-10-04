from Lecture.lecture import Lecture
import re


class LectureIter:
    def __init__(self, sheet, row, col, name):
        self.sheet = sheet
        self.row = row
        self.col = col
        self.name = name
        self.lecture_number = 0
        self.week_day = 0
        self.week_type = False
        self.lectures = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.lectures is not None:
            try:
                result = self.lectures.__next__()
                return result
            except StopIteration:
                self.lectures = None

        if self.lectures is None:
            if self.week_day == 6 and not self.week_type:
                raise StopIteration

            times = ''
            for current_col in range(self.col - 1, 0, -2):
                times_buf = str(self.sheet[self.row, current_col].value)
                if times_buf == '':
                    times_buf = str(self.sheet[self.row - 1, current_col].value)
                times_buf = re.match(r'(\d{1,2}:\d{2})-(\d{1,2}:\d{2})', times_buf)
                if times_buf is not None:
                    times = times_buf
                    break

            self.lectures = Lecture.new(
                self.week_day,
                self.week_type,
                times[1],
                times[2],
                ' '.join(str(self.sheet[self.row, self.col + 1].value).split()),
                str(self.sheet[self.row, self.col].value)
            )

            self.row += 1
            if self.lecture_number == 11:
                self.lecture_number = 0
                self.week_day += 1
            else:
                self.lecture_number += 1
            self.week_type = not self.week_type

            return self.lectures.__next__()
