import requests
import re
from bs4 import BeautifulSoup as BS


# def is_one_equal(item, values_tuple):
#     is_equal = False
#     for time in values_tuple:
#         if item == time:
#             is_equal = True
#             break
#     return is_equal


def findCurrentWeek(htmlBody):
    return htmlBody.find("span", {"class": "schedule__title-label"}).text


def write_content_to_txt(text):
    with open('content.txt', 'w') as file_content:
        file_content.write(text)


def clearList(content_str):
    list = [item.strip() for item in content_str.split('\n')]
    list = [item for item in list if item != '']
    return list


def find_next_day(previous_day, list_of_values):
    next_day = -1

    previous_day += 1
    short_list = list_of_values[previous_day:]
    try:
        next_day = short_list.index(TIMING[0])
    except:
        return

    return next_day + previous_day - 1


def fill_week_dict(list_of_values, monday_index, tuesday_index):
    week_dict = {}
    start = monday_index
    for item in DAYS:
        next_day = find_next_day(start + 1, list_of_values)
        week_dict[item] = list_of_values[start:next_day]
        start = next_day

    return week_dict


def extract_lesson(list_of_items):
    tmp_list = list_of_items.copy()
    for idx, item in enumerate(list_of_items):
        if item in TIMING:
            return tmp_list[:idx]


def divide_to_components(day_list):
    edited_list = day_list.copy()
    edited_list.append('21')
    day_schedule = dict.fromkeys(TIMING)
    for index in range(len(edited_list)):
        item = edited_list[index]
        if item in TIMING:
            this_lesson = extract_lesson(edited_list[index + 1:])
            # if day_list[index + 1] in PERIODS:
            #     day_schedule[item] = []
            #     day_schedule[item].append(edited_list[index + 1])
            # else:
            #     edited_list.insert(index + 1, '')
            #     day_schedule[item] = []
            #     day_schedule[item].append('every')
            day_schedule[item] = []
            day_schedule[item].append(this_lesson)
    return day_schedule


TIMING = ('08:30-10:00', '10:15-11:45', '12:00-13:30', '14:00-15:30', '15:45-17:15', '17:30-19:00', '19:15-20:45', '21')

PERIODS = ('по чётным', 'по нечётным', 'недели 4 8 12 16', '')

DAYS = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')

URL = 'https://www.nstu.ru/studies/schedule/schedule_classes/schedule?group=%D0%90%D0%92%D0%A2-816&print=true'

PAGE = requests.get(URL).text

schedule_soup = BS(PAGE, 'html.parser')

# current_week = findCurrentWeek(schedule_soup)

schedule = schedule_soup.html.body.find("div", {"class": "schedule"})

content = schedule.text

content_list = clearList(content)

monday = 0
tuesday = 0

for index in range(len(content_list)):
    if content_list[index] == 'пн':
        monday = index
        break

for index in range(len(content_list)):
    if content_list[index] == 'вт':
        tuesday = index
        break

rows_amount_per_day = tuesday - monday

# content_dict = {index: content_list[index] for index in range(len(content_list))}

content = '\n'.join(content_list)

# write_content_to_txt(content)

week = fill_week_dict(content_list, monday, tuesday)

for item in week:
    week[item] = divide_to_components(week[item])

for day in DAYS:
    these_lessons = week[day]
    for lesson in these_lessons:
        row = these_lessons[lesson]
        try:
            if (row[0][0] not in PERIODS) or (row == [[]] ):
                row[0].insert(0, 'every')
        except:
            continue

print(week['wednesday'])
# with open('content_dict.txt', 'a') as file:
#     for item in week:
#         str = item + '\t' + " ".join(week[item])
#         str += '\n'
#         file.write(str)
