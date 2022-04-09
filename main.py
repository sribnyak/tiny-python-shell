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


def hello(filename: str):
    with open(filename, 'w') as file:
        print("Hello, world!", file=file)


def cat(filename: str):
    with open(filename, 'r') as file:
        print(file.read(), end='')


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
    Command('cd', 1, os.chdir, 'change the current working directory'),
    # todo cp
    # todo mv
    Command('rm', 1, os.remove, 'remove a file'),
    Command('rmdir', 1, os.rmdir, 'remove an empty directory'),
    Command('mkdir', 1, os.mkdir, 'make a directory'),
    Command('hw', 1, hello, 'make a text file with "Hello, world!" in it'),
    Command('cat', 1, cat, 'print file contents'),
    Command('help', 0, my_help, 'print this help message'),
    Command('exit', 0, lambda: None, 'cause normal process termination'),
]

commands_dict = {command.name: command for command in commands}


def run_command(command: str):
    if not command:
        return
    command, *args = command.split()
    if command in commands_dict:
        commands_dict[command].run(*args)
    else:
        print(f'{PROJECT_NAME}: {command}: command not found')


def main():
    print(f'Welcome to {PROJECT_NAME} by {AUTHOR}')
    print('Type "help" for more information.')

    while True:
        command = input('$ ').strip()
        run_command(command)
        if command == 'exit':
            break


if __name__ == '__main__':
    main()
