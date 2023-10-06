records = {}


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enough params. It needs to have 2 params (Name Phone): "
        except KeyError:
            return "This name doesn't have in the dictionary."
        except ValueError:
            return "The phone number must contains only digit."
    return inner


@input_error
def add_record(*args):
    rec_id = args[0].lower()
    rec_value = int(args[1])
    records[rec_id] = rec_value
    return f"Add record {rec_id = }, {rec_value = }"


@input_error
def change_record(*args):
    rec_id = args[0]
    new_value = int(args[1])
    rec = records[rec_id]
    if rec:
        records[rec_id] = new_value
        return f"Change record {rec_id = }, {new_value = }"


def unknown(*args):
    return "Unknown command. Try again."


def end_program(*args):
    return "Good Bye!"


def hello(*args):
    return "How can I help you?:"


def help(*args):
    message = '''Use next commands:
    add 'name' 'phone'  - add name and phone number to memory
    change 'name' 'phone' - change phone number in this name
    phone 'name' - show phone number for this name
    show all  -  show all records in memory
    exit - exit from bot'''
    return message


def show_all(*args):
    return records


@input_error
def phone(*args):
    name = args[0].lower()
    customer = records[name]
    if customer:
        return f'{name.capitalize()} has {records[name]} phone number.'


COMMANDS = {add_record: "add",
            change_record: "change",
            end_program: "exit",
            hello: "hello",
            help: "help",
            phone: "phone",
            show_all: "show all"}


def parser(text: str):
    for func, kw in COMMANDS.items():
        if text.lower().startswith(kw):
            return func, text[len(kw):].strip().split()
    return unknown, []


def main():
    while True:
        user_input = input(
            "Enter user name and phone number or 'help' for help: ")
        func, data = parser(user_input)
        print(func(*data))
        if user_input == 'exit':
            break


if __name__ == '__main__':
    main()
