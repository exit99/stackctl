import sys

from tabulate import tabulate
from novaclient.exceptions import AuthorizationFailure, Unauthorized

from cmds import Clone, Images, List, Desalt, Emancipate, Delete
from colors import red

from errors import (
    CommandExecutionError,
    ConnectionFailure,
    InvalidCommandArgs,
    WrapperFailure,
)


CMDS = {
    'clone': Clone,
    'de-salt': Desalt,
    'emancipate': Emancipate,
    'images': Images,
    'list': List,
    'rm': Delete,
}


def fetch_command(cmd, **kwargs):
    if cmd == "--help":
        print "usage: stackctl [--help] <command> [<args>]\n"
        print tabulate([[name, cmd.__doc__ ] for name, cmd in CMDS.iteritems()])
    elif cmd in CMDS:
        return CMDS[cmd](**kwargs)
    else:
        print red("'{}' is not a valid command.".format(cmd))


def main(args, cli=True, **kwargs):
    cmd = fetch_command(args.pop(0), **kwargs)
    errors = (InvalidCommandArgs, CommandExecutionError,
              ConnectionFailure, WrapperFailure)
    source_msg = "Did you 'source TENANT_NAME.openrc.sh' with a valid password?"
    if cli:
        try:
            cmd.execute(*args)
        except AttributeError:
            pass
        except (AuthorizationFailure, Unauthorized):
            print red("Authentication Failed!")
            print source_msg
        except errors as e:
            print e.message
    else:
        try:
            cmd.execute(*args)
        except (AuthorizationFailure, Unauthorized):
            raise RuntimeError("AUTH_FAILED: " + source_msg)


def run(cmd, *args, **kwargs):
    main(list((cmd,) + args), cli=False, **kwargs)


def cli():
    if len(sys.argv) > 1:
        main(sys.argv[1:])
