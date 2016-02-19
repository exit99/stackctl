import os

import paramiko
from colors import red

from errors import ConnectionFailure


class Connection(object):
    def __init__(self, host, **kwargs):
        """Connect to host via ssh.

        :param host: The ip or name of the host.
        :param kwargs: Requires at least `username` key. Can take any
            kwarg that :meth:`paramiko.SSHClient.connect` can take.
        """
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Remove keys with empty values.
        kwargs = dict((k, v) for k, v in kwargs.iteritems() if v)
        keyfile = os.path.expanduser(
            os.environ.get('STACKCTL_PRIVATE_KEY', '~/.ssh/id_rsa')
        )
        try:
            self.ssh.connect(host, key_filename=keyfile, **kwargs)
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            msg = red(e.strerror)
            msg += "\nAre you using the proper user and port?"
            raise ConnectionFailure(msg)
        except IOError as e:
            msg = red(e.strerror)
            msg += "\nIs your public key located at '{}'?".format(keyfile)
            raise ConnectionFailure(msg)

    def execute(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        for line in stderr.readlines():
            print line
        for line in stdout.readlines():
            print line

    def close(self):
        self.ssh.close()
