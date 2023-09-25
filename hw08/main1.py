from datetime import date


def is_birthday_in_range(birthday, days_between):
    is_birthday = False
    over_year = False
    current_date = date.today()
    if (current_date.year % 4 == 0 and current_date.year % 100 != 0) or current_date.year % 400 == 0:
        leap_year = True
    else:
        leap_year = False
        print(days_between, birthday.month)
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
        return {}
    for user in users:
        birthday = user["birthday"].replace(year=current_date.year)
        days_between = birthday - current_date
        is_birthday, over_year = is_birthday_in_range(
            birthday, days_between.days)
        if is_birthday:
            if over_year:
                birthday = user["birthday"].replace(year=current_date.year+1)
            print(birthday.weekday())
            wd = birthday.weekday()
            if wd in (5, 6):
                wd_str = "Monday"
            else:
                wd_str = birthday.strftime("%A")

            if users_birthday.get(wd_str):
                users_birthday[wd_str].append(user["name"])
            else:
                users_birthday[wd_str] = [user["name"]]
    return users_birthday