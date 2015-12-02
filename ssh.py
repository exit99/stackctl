import paramiko


class Connection():
    def connect(self, host, username):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host, username=username, key_filename='~/.ssh/id_rsa')

    def execute(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        print stdout.readlines()

    def close(self):
        self.ssh.close()
