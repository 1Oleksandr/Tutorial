from datetime import date

# users = [{"name": "Олександр Перший", "birthday": datetime(1955, 1, 2).date()},
#          {"name": "Дмитро Онищенко", "birthday": datetime(2001, 1, 1).date()},
#          {"name": "Петро Другий ", "birthday": datetime(1970, 12, 30).date()},
#          {"name": "Василь Третий", "birthday": datetime(2001, 1, 3).date()},
#          {"name": "Констянтин Пилипець", "birthday": datetime(2003, 9, 25).date()}]

week_days = {0: "Monday",
             1: "Tuesday",
             2: "Wednesday",
             3: "Thursday",
             4: "Friday",
             5: "Monday",
             6: "Monday"}


def is_birthday_in_range(birthday, days_between):
    is_birthday = False
    over_year = False
    current_date = date.today()
    if (current_date.year % 4 == 0 and current_date.year % 100 != 0) or current_date.year % 400 == 0:
        leap_year = True
    else:
        leap_year = False
    if (leap_year and -365 <= days_between <= -359 and birthday.month == 1) or \
            (not leap_year and -364 <= days_between <= -358 and birthday.month == 1):
        is_birthday = True
        over_year = True
    elif 0 <= days_between <= 6:
        is_birthday = True
        over_year = False
    return is_birthday, over_year


def get_birthdays_per_week(users):
    current_date = date.today()
    users_birthday = {}
    if not users:
        return users_birthday
    for user in users:
        birthday = user["birthday"].replace(year=current_date.year)
        days_between = birthday - current_date
        is_birthday, over_year = is_birthday_in_range(
            birthday, days_between.days)
        if is_birthday:
            if over_year:
                birthday = user["birthday"].replace(year=current_date.year+1)

            if users_birthday.get(week_days[birthday.weekday()]):
                users_birthday[week_days[birthday.weekday()]].append(
                    user["name"])
            else:
                users_birthday[week_days[birthday.weekday()]] = [user["name"]]

    return users_birthday
