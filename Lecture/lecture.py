import re


class Lecture:
    def __init__(self, week_day, week_type, star, finish, rooms, text, dates=None):
        if dates is None:
            dates = []
        self.week_day = week_day
        self.week_type = week_type
        self.star = star
        self.finish = finish
        self.rooms = rooms
        self.text = text
        self.dates = dates

    def copy(self, text):
        return Lecture(self.week_day, self.week_type, self.star, self.finish, self.rooms, text, self.dates)

    @staticmethod
    def new(week_day, week_type, star, finish, rooms, text):
        lectures = [Lecture(week_day, week_type, star, finish, rooms, text)]

        lectures[0].text2time()
        lectures[0].text2room()

        data_match = re.match(r'(.*?) (\((.+?) - ((\d\d\.\d\d)(, |))+\)(, \w+\d+|)(; |))+', lectures[0].text)
        if data_match is not None:
            i = 0
            for lecture_type_data, lecture_type, _, _, _, _ in re.findall(r'(\((.*?) - ((\d\d\.\d\d)(, |))+\)(, \w+\d+|))', lectures[0].text):
                if i == 0:
                    lectures[0].text = f'{data_match[1]} ({lecture_type})'
                else:
                    lectures.append(lectures[0].copy(f'{data_match[1]} ({lecture_type})'))

                lectures[i].set_dates_from_text(lecture_type_data)
                lectures[i].set_room_from_text(lecture_type_data)
                i += 1

        return iter(lectures)

    def text2time(self):
        time_match = re.match(r'(\d{1,2}:\d{2})-(\d{1,2}:\d{2}) (.*)', self.text)
        if time_match is not None:
            self.star = time_match[1]
            self.finish = time_match[2]
            self.text = time_match[3]

    def text2room(self):
        room_match = re.match(r'(.*), ул. (.+), д. (\d+)', self.text)
        if room_match is not None:
            self.text = room_match[1]
            self.rooms = room_match[2][0] + room_match[3]

    def set_dates_from_text(self, lecture_type_data):
        self.dates = re.findall(r'\d\d\.\d\d', lecture_type_data)

    def set_room_from_text(self, lecture_type_data):
        new_room = re.findall(r'\), \w+\d+', lecture_type_data)
        if len(new_room) != 0:
            self.rooms = new_room[0][3:]

    def __str__(self):
        return self.text
        if self.text == '':
            return (
                    "'" +
                    str(self.week_day) + "' '" +
                    str(self.week_type) + "' " +
                    'class window'
            )
        else:
            return (
                    "'" +
                    str(self.week_day) + "' '" +
                    str(self.week_type) + "' '" +
                    str(self.star) + "' '" +
                    str(self.finish) + "' '" +
                    str(self.rooms) + "' '" +
                    str(self.text) + "' '" +
                    str(self.dates) + "'"
            )
