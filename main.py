import xlrd
import os.path
import time
import requests
from Group.groupIter import GroupIter


def main():
    e_tag_path = 'ETags.txt'
    if not os.path.exists(e_tag_path):
        with open(e_tag_path, 'w'):
            pass

    while True:
        url = "https://sutd.ru/upload/raspisanie/raspisanie_o_vshpm_ipto_24_25.xls"
        e_tag = requests.head(url).headers['ETag']
        with open(e_tag_path, 'r') as file:
            content = file.read()
        if content != e_tag:
            with open(e_tag_path, 'w') as file:
                file.write(e_tag)

            response = requests.get(url)
            with open('schedule.xls', 'wb') as file:
                file.write(response.content)
            print('Downloaded')

            wb = xlrd.open_workbook('schedule.xls')
            main_sheet = wb.sheet_by_index(0)
            for group_iter in GroupIter(main_sheet):
                print(group_iter.get_name())
                for lecture in group_iter.get_lecture_iter():
                    if lecture.__str__() != '':
                        print('\t', lecture)
        else:
            print('The file already exists')
        time.sleep(5)


if __name__ == '__main__':
    main()
