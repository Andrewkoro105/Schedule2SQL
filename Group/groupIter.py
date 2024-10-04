from Group.group import Group


class GroupIter:
    def __init__(self, sheet, row=4, col=2):
        self.sheet = sheet
        self.row = row
        self.col = col

    def __iter__(self):
        return self

    def __next__(self):
        if self.col + 2 < self.sheet.ncols:
            result = Group(self.sheet, self.row, self.col)
            self.col += 2
            if self.get_name() == 'Дни нед.':
                self.col += 2
            return result
        raise StopIteration

    def get_name(self) -> str:
        cell = self.sheet[self.row, self.col]
        if cell is None:
            return ''
        return str(cell.value)
