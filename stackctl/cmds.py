import re
from getpass import getpass

from colors import green, red
from tabulate import tabulate

import ssh
from errors import InvalidCommandArgs
from nova_wrapper import NovaWrapper


class AbstractCommand(object):
    min_args = 0
    needs_auth = True

    def __init__(self, **kwargs):
        self.extra_flags = kwargs
        return super(AbstractCommand, self).__init__()

    def execute(self, *args):
        self.valid_args(args)
        self.flags = self.extract_flags(args)
        self.nova = NovaWrapper() if self.needs_auth else None
        if 'force' in self.flags or self.safety_check(*args):
            self.run(*args)
        else:
            print red("Cancelled.")

    def valid_args(self, args):
        if len(args) < self.min_args:
            msg = red("Too few arguments. {} Required.".format(self.min_args))
            raise InvalidCommandArgs(msg)

    def safety_check(self, *args):
        """Override this method in inherting class."""
        return True

    def run(self, *args):
        """Override this method in inherting class."""
        pass

    def extract_flags(self, args):
        flags = {}
        for arg in args:
            if re.match("--.*?", arg):
                try:
                    index = arg.index('=')
                except ValueError:
                    flags[arg.strip('-')] = True
                else:
                    flags[arg[:index].strip('-')] = arg[index+1:]
        flags.update(self.extra_flags)
        return flags

    def ssh_connect(self, server):
        user = self.flags.get('user')
        host = self.nova.floating_ip(server)
        try:
            port = int(self.flags.get('port', 22))
        except ValueError:
            port = 22
        print "Connecting to {}@{} -p {}".format(user, host, port)
        conn = ssh.Connection(host, username=user, port=port)
        return conn

    def remote_command(self, cmds, *args):
        if not isinstance(cmds, list):
            cmds = [cmds]
        target = args[0]
        server = self.nova.server(target)
        conn = self.ssh_connect(server)
        pword = self.flags.get('sudopass') or getpass("Enter sudo password: ")
        for cmd in cmds:
            print "Executing: {}".format(cmd)
            cmd = "echo {} | sudo -S {}".format(pword, cmd)
            conn.execute(cmd)


class List(AbstractCommand):
    """Lists instances in the current tenant."""
    def run(self, *args):
        servers = self.nova.servers()
        for server in self.nova.servers():
            # TODO: Add the IPs of each instance.
            if server.status == u"ACTIVE":
                print green(server.name)
            else:
                print red(server.name)
        return servers


class Start(AbstractCommand):
    """Start an instance in the current tenant."""
    def run(self, *args):
        server = self.nova.server(args[0])
        server.start()
        print green("{} started!".format(server.name))


class Stop(AbstractCommand):
    """Stop an instance in the current tenant."""
    def run(self, *args):
        server = self.nova.server(args[0])
        server.stop()
        print green("{} stopped!".format(server.name))


class Delete(AbstractCommand):
    """Delete an instance in the current tenant."""
    def safety_check(self, *args):
        msg = "Are you sure you want to delete {}? This cannot be undone. Y/n\n".format(args[0])
        return raw_input(msg) == "Y"

    def run(self, *args):
        server = self.nova.server(args[0])
        server.delete()
        print green("{} removed!".format(server.name))


class Images(AbstractCommand):
    """Lists all available images."""

    def run(self, *args):
        images = self.nova.images()
        print tabulate([self.nova.image_data(i) for i in images])
        return images


class Clone(AbstractCommand):
    """Clone an instance in the current tenant."""
    min_args = 2

    def run(self, *args):
        server = self.nova.server(args[0])
        clone = self.nova.clone(server, args[1])
        self.nova.print_server(clone)
        print green("Success!")


class Desalt(AbstractCommand):
    """Turns off salt minion. [--user, --port, --sudopass]."""
    min_args = 1

    def run(self, *args):
        self.remote_command("service salt-minion stop", *args)


class Emancipate(AbstractCommand):
    """Turns slave mysql server to master, removes read-only. [--user, --port, --dbuser, --sudopass]."""
    min_args = 1

    def safety_check(self, *args):
        msg = "Are you sure you want to emancipate '{}'? This cannot be undone. Y/n\n".format(args[0])
        return raw_input(msg) == "Y"

    def run(self, *args):
        dbuser = self.flags.get('dbuser', '')
        cmds = [
            "sed -i 's/read-only//g' /etc/mysql/my.cnf",
            'mysql -u {} -e "stop slave;"'.format(dbuser),
        ]
        self.remote_command(cmds, *args)
