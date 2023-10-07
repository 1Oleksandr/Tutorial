customers = {}


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
    name = args[0].lower()
    phone = int(args[1])
    customers[name] = phone
    return f"Add record {name = }, {phone = }"


@input_error
def change_record(*args):
    name = args[0].lower()
    new_phone = int(args[1])
    if customers[name]:
        customers[name] = new_phone
        return f"Change record {name = }, {new_phone = }"


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
    return customers


@input_error
def phone(*args):
    name = args[0].lower()
    if customers[name]:
        return f'{name.capitalize()} has {customers[name]} phone number.'


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
