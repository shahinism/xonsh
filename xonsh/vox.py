from os.path import join, basename, exists
import os
from shutil import rmtree
import venv

import builtins


class Vox:
    """Vox is a virtual environment manager for xonsh."""

    def __init__(self):
        """Ensure that $VIRTUALENV_HOME is defined and declare the available vox commands"""

        if not builtins.__xonsh_env__.get('VIRTUALENV_HOME'):
            if os.name == 'nt':
                home_path = builtins.__xonsh_env__['USERPROFILE']

            elif os.name == 'posix':
                home_path = builtins.__xonsh_env__['HOME']

            else:
                print('This OS is not supported.')
                return None

            builtins.__xonsh_env__['VIRTUALENV_HOME'] = join(home_path, '.virtualenvs')

        self.commands = {
            ('new',): self.new,
            ('activate', 'workon', 'enter'): self.activate,
            ('deactivate', 'exit'): self.deactivate,
            ('list', 'ls'): self.list,
            ('remove', 'rm', 'delete', 'del'): self.remove,
            ('help', '-h', '--help'): self.help
        }

    def __call__(self, args, stdin=None):
        """Call the right handler method for a given command."""

        if not args:
            self.help()
            return None

        command_name, params = args[0], args[1:]

        try:
            command = [
                self.commands[aliases] for aliases in self.commands
                if command_name in aliases
            ][0]

            command(*params)

        except IndexError:
            print('Command "%s" doesn\'t exist.\n' % command_name)
            self.print_commands()

    @staticmethod
    def new(name):
        """Create a virtual environment in $VIRTUALENV_HOME with ``python3 -m venv``.

        :param name: virtual environment name
        """

        env_path = join(builtins.__xonsh_env__['VIRTUALENV_HOME'], name)

        print('Creating environment...')

        vbuiltins.__xonsh_env__.create(env_path, with_pip=True)

        print('Environment "%s" created. Activate it with "vox activate %s".\n' % (name, name))

    @staticmethod
    def activate(name):
        """Activate a virtual environment.

        :param name: virtual environment name
        """

        env_path = join(builtins.__xonsh_env__['VIRTUALENV_HOME'], name)

        if not exists(env_path):
            print('This environment doesn\'t exist. Create it with "vox new %s".\n' % name)
            return None

        if os.name == 'nt':
            bin_dir = 'Scripts'

        elif os.name == 'posix':
            bin_dir = 'bin'

        else:
            print('This OS is not supported.')
            return None

        bin_path = join(env_path, bin_dir)

        builtins.__xonsh_env__['PATH'].insert(0, bin_path)
        builtins.__xonsh_env__['VIRTUAL_ENV'] = env_path

        print('Activated "%s".\n' % name)

    @staticmethod
    def deactivate():
        """Deactive the active virtual environment."""

        if 'VIRTUAL_ENV' not in ENV:
            print('No environment currently active. Activate one with "vox activate".\n')
            return None

        env_path = builtins.__xonsh_env__['VIRTUAL_ENV']

        env_name = basename(env_path)

        if os.name == 'nt':
            bin_dir = 'Scripts'

        elif os.name == 'posix':
            bin_dir = 'bin'

        else:
            print('This OS is not supported.')
            return None

        bin_path = join(env_path, bin_dir)

        while bin_path in builtins.__xonsh_env__['PATH']:
            builtins.__xonsh_env__['PATH'].remove(bin_path)

        builtins.__xonsh_env__.pop('VIRTUAL_ENV')

        print('Deactivated "%s".\n' % env_name)

    @staticmethod
    def list():
        """List available virtual environments."""

        env_names = os.listdir(builtins.__xonsh_env__['VIRTUALENV_HOME'])

        if not env_names:
            print('No environments evailable. Create one with "vox new".\n')
            return None

        print('Available environments:')

        for env_name in env_names:
            print('    %s' % env_name)

        else:
            print()

    @staticmethod
    def remove(name):
        """Remove virtual environment.

        :param name: virtual environment name
        """

        if 'VIRTUAL_ENV' in ENV:
            print('This environment is currently active. If you really want to remove it, deactivate it first with "vox deactivate %s".\n' % name)
            return None

        env_path = join(builtins.__xonsh_env__['VIRTUALENV_HOME'], name)

        rmtree(env_path)

        print('Environment "%s" removed.\n' % name)

    def help(self):
        """Show help."""

        print(self.__doc__, '\n')
        self.print_commands()

    @staticmethod
    def print_commands():
        """Print available vox commands."""

        print("""Available commands:
    vox new <env>
        Create new virtual environment in $VIRTUALENV_HOME

    vox activate (workon, enter) <env>
        Activate virtual environment

    vox deactivate (exit)
        Deactivate current virtual environment

    vox list (ls)
        List all available environments

    vox remove (rm, delete, del) <env>
        Remove virtual environment

    vox help (-h, --help)
        Show help
""")
