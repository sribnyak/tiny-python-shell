"""An interactive shell with partial bash functionality
"""

import os
import shutil
from pathlib import Path

PROJECT_NAME = 'MyShell'
AUTHOR = 'Alexander Sribnyak'


class Command:
    """A class with all required information about a command:
    name, a number of arguments, description, and the command itself."""

    def __init__(self, name, arg_counter, action, description=None):
        """Construct a new Command.
        By default, the description is taken from `action` docstring"""
        self.name = name
        self.arg_counter = arg_counter
        self.action = action
        self.description = description if description else action.__doc__

    def run(self, *args):
        """Check if the number of arguments is correct and run the command.
        The command is runing in a try block to avoid crashing"""
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


def assure_directory_exists(path):
    """Raise an error if the directory does not exist"""
    if not os.path.exists(path):
        raise FileNotFoundError(f'no such directory: "{path}"')
    if not os.path.isdir(path):
        raise NotADirectoryError(f'not a directory: "{path}"')


def assure_file_exists(path):
    """Raise an error if the file does not exist"""
    if not os.path.exists(path):
        raise FileNotFoundError(f'no such file: "{path}"')
    if os.path.isdir(path):
        raise IsADirectoryError(f'is a directory: "{path}"')


def assure_can_create(path):
    """Raise an error if the path already exists or
    the parent directory does not exist"""
    if os.path.exists(path):
        raise FileExistsError(f'file exists: "{path}"')
    parent = Path(path).resolve().parent
    if not parent.exists():
        raise FileNotFoundError(f'no parent directory: "{parent}"')


def change_directory(path: str):
    """Change the current working directory"""
    assure_directory_exists(path)
    os.chdir(path)


def remove_file(path: str):
    """Remove a file"""
    assure_file_exists(path)
    os.remove(path)


def remove_directory(path: str):
    """Remove an empty directory"""
    assure_directory_exists(path)
    if os.listdir(path):
        raise OSError(f'directory not empty: "{path}"')
    os.rmdir(path)


def make_directory(path: str):
    """Make a directory"""
    assure_can_create(path)
    os.mkdir(path)


def hello(filename: str):
    """Make a text file with "Hello, world!" in it"""
    assure_can_create(filename)
    with open(filename, 'w') as file:
        print("Hello, world!", file=file)


def print_file(filename: str):
    """Print file contents"""
    assure_file_exists(filename)
    with open(filename, 'r') as file:
        print(file.read(), end='')


def copy_file(source: str, dest: str):
    """Copy a file"""
    assure_file_exists(source)
    assure_can_create(dest)
    shutil.copy2(source, dest)


def move_file(source: str, dest: str):
    """Move (rename) a file"""
    assure_file_exists(source)
    assure_can_create(dest)
    shutil.move(source, dest)


def my_help():
    """Print a help message with a list of all available commands"""
    print('Available commands:')
    for command in commands:
        print(command.name, '-', command.description)


commands = [
    Command('pwd', 0,
            lambda: print(os.getcwd()),
            'Print name of current/working directory'),
    Command('ls', 0,
            lambda: print(*sorted(os.listdir()), sep='  '),
            'List directory contents'),
    Command('cd', 1, change_directory),
    Command('cp', 2, copy_file),
    Command('mv', 2, move_file),
    Command('rm', 1, remove_file),
    Command('rmdir', 1, remove_directory),
    Command('mkdir', 1, make_directory),
    Command('hw', 1, hello),
    Command('cat', 1, print_file),
    Command('help', 0, my_help, 'Print this help message'),
    Command('exit', 0, lambda: None, 'Cause normal process termination'),
]

commands_dict = {command.name: command for command in commands}


def split_command(command):
    """Split a command string considering that spaces can be
    escaped with a backslash"""
    # (assuming '\b' and '\n' cannot be found in a command)
    # this solution is used to avoid writing a lexical analyzer
    return [word.replace('\b', '\\').replace('\n', ' ')
            for word in
            command.replace('\\\\', '\b').replace('\\ ', '\n').split(' ')
            if word]


def run_command(command: str):
    """Interpret a command given as a stripped string"""
    if not command:
        return
    command, *args = split_command(command)
    if command in commands_dict:
        commands_dict[command].run(*args)
    else:
        print(f'{PROJECT_NAME}: {command}: command not found')


def main():
    """An entry point to an interactive shell"""

    print(f'Welcome to {PROJECT_NAME} by {AUTHOR}')
    print('Type "help" for more information.')

    while True:
        command = input('$ ').strip()
        run_command(command)
        if command == 'exit':
            break


if __name__ == '__main__':
    main()
