from ssh import Connection


def remove_salt_minion(host, username):
    conn = Connection(host, username)
    pword = raw_input("Enter sudo password: ")
    conn.execute("echo {} | sudo apt-get remove salt-minion -y".format(pword))
    conn.close()
