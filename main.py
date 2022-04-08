import os

PROJECT_NAME = 'MyShell'
AUTHOR = 'Alexander Sribnyak'


class Command:
    def __init__(self, name, arg_counter, action, doc):
        self.name = name
        self.arg_counter = arg_counter
        self.action = action
        self.doc = doc

    def run(self, *args):
        if len(args) != self.arg_counter:
            takes = f'{self.arg_counter} argument'
            if self.arg_counter != 1:
                takes += 's'
            print(f'{PROJECT_NAME}: {self.name}: command takes {takes}')
            return
        try:
            self.action(*args)
        except BaseException as error:
            print(f'{PROJECT_NAME}: {self.name}: an error occurred: {error}')


def my_help():
    print('Available commands:')
    for command in commands:
        print(command.name, '-', command.doc)


commands = [
    Command('pwd', 0,
            lambda: print(os.getcwd()),
            'print name of current/working directory'),
    Command('ls', 0,
            lambda: print(*sorted(os.listdir()), sep='  '),
            'list directory contents'),
    Command('cd', 1,
            os.chdir,
            'change the current working directory'),
    Command('help', 0, my_help, 'print this help message'),
    Command('exit', 0, lambda: None, 'cause normal process termination'),
]

commands_dict = {command.name: command for command in commands}


if __name__ == '__main__':
    print(f'Welcome to {PROJECT_NAME} by {AUTHOR}')
    print('Type "help" for more information.')

    while True:
        command = input('$ ').split()
        if not command:
            continue

        command, *args = command
        if command not in commands_dict:
            print(f'{PROJECT_NAME}: {command}: command not found')
            continue
        commands_dict[command].run(*args)

        if command == 'exit' and len(args) == 0:
            break
