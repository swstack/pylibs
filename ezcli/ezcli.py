"""Yet another wrapper around command line interfaces

This started as a fun/toy project and actually ended up to be very much
like what fabric offers.  Anyway, I kind of enjoy the decorator syntax.
"""

import argparse
import sys
import threading


# public
class command(object):
    """Decorator for adding a command to EZCLI"""
    def __init__(self, description=None):
        self._description = description

    def __call__(self, fn):
        EZCLI.add_command(fn.__name__, self._description, fn)
        return fn


# public
class positional_argument(object):
    """Decorator for adding a positional argument to an EZCLI command

    Implements the same interface as argparse.add_argument.
    """
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    def __call__(self, fn):
        EZCLI.add_argument(fn.__name__, *self._args, **self._kwargs)
        return fn


# public
class optional_argument(positional_argument):
    """Decorator for adding an optional argument to an EZCLI command"""


# public
class EZCLI(object):
    """Core component of the ezcli library

    Implements the Singleton pattern because, although unlikely, there should
    only be one of these instances in the system.  There are class level methods
    that expose interfaces for adding commands and subcommands that we need
    to make sure are added to the same CLI, in case of abuse.

    The EZCLI is inherently meant to implement a subparser, to offer a fabric-like
    interface.  If you'd like to alter the "root" lever parser there are utilities
    to do so.  See the usage for more details:

        $ bin/ezcli [root options] command [command options]

    """

    _construction_lock = threading.RLock()
    _singleton = None

    # thread safe
    def __new__(cls, *args, **kwargs):
        with cls._construction_lock:
            if not cls._singleton:
                cls._singleton = super(EZCLI, cls).__new__(cls, *args, **kwargs)
        return cls._singleton

    def __init__(self):
        self._root_parser = argparse.ArgumentParser()
        self._sub_parser = self._root_parser.add_subparsers(help="Commands")
        self._ezcli = {}

    #---------------------------------------------------------------------------
    # Class methods used by decorators
    #---------------------------------------------------------------------------
    @classmethod
    def add_command(cls, command_name, command_help, handler):
        """Extend EZCLI with a command"""
        cls._singleton._ezcli[command_name] = {
                                                "help": command_help,
                                                "handler": handler,
                                                "args": [],  # arg/kwarg pairs
                                              }

    @classmethod
    def add_argument(cls, command_name, *args, **kwargs):
        """Add an argument to a previously added command"""
        command = cls._singleton._ezcli[command_name]
        command.update("args", (args, kwargs))

    #---------------------------------------------------------------------------
    # Public
    #---------------------------------------------------------------------------
    def load(self):
        """Load the EZCLI from decorated functions"""
        for command, details in self._ezcli.items():
            self._sub_parser.add_parser(command, help=details.get("help"))
            for args, kwargs in details.get("args"):
                self._sub_parser.add_argument(*args, **kwargs)

    def execute(self):
        """Execute EZCLI, ultimately excecuting a command"""

        fn = self._args.sub_handler
        fn(self._args)

    def add_root_argument(self, *args, **kwargs):
        """Add an argument to the root argument parser, typically not used"""
        self._root_parser.add_argument(*args, **kwargs)
