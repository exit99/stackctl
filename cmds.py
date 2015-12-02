import os
from datetime import datetime

import progressbar
from colors import green, red
from novaclient import client, exceptions
from tabulate import tabulate

from errors import CommandExecutionError, InvalidCommandArgs


class AbstractCommand(object):
    min_args = 0
    needs_auth = True

    def execute(self, *args):
        self.valid_args(args)
        self.novaclient = self.authenticate() if self.needs_auth else None
        self.run(*args)

    def valid_args(self, args):
        if len(args) < self.min_args:
            msg = red("Too few arguments. {} Required.".format(self.min_args))
            raise InvalidCommandArgs(msg)

    def authenticate(self):
        return client.Client(
            os.getenv('OS_COMPUTE_API_VERSION', 2),
            os.getenv('OS_USERNAME'),
            os.getenv('OS_PASSWORD'),
            os.getenv('OS_TENANT_NAME'),
            os.getenv('OS_AUTH_URL'),
        )

    def run(self, *args):
        """Override this method in inherting class."""
        pass

    def get_server(self, name):
        servers = {s.name: s for s in self.novaclient.servers.list()}
        server = servers.get(name, False)
        if server:
            return server
        msg = red("'{}' is not an active instance.\n".format(name))
        msg += "Use 'stagingctl list' to view active instances."
        raise CommandExecutionError(msg)

    def valid_server(self, name):
        """Raise error if instance doesn't exist.

        Used for readability where you just need to check for validity
        and not get the entire server.
        """
        self.get_server(name)

    def wait(self, item, status="ACTIVE"):
        bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
        while item.progress < 100 and item.status != status:
            bar.update(item.progress)
            item.get()


class List(AbstractCommand):
    """Lists instances in the current tenant."""
    def run(self, *args):
        servers = sorted(self.novaclient.servers.list(), key=lambda x: x.name)
        for server in servers:
            # TODO: Add the floating IP of each instance.
            if server.status == u"ACTIVE":
                print green(server.name)
            else:
                print red(server.name)


class Images(AbstractCommand):
    """Lists all available images."""

    def run(self, *args):
        images = sorted(self.novaclient.images.list(), key=lambda x: x.name)
        print tabulate([self.get_image_data(image) for image in images])

    def get_image_data(self, image):
        if image.status == "ACTIVE":
            name = green(image.name)
        else:
            name = red(image.name)
        return [name, image.id, "{}%".format(image.progress)]


class Clone(AbstractCommand):
    """Clone an instance in the current tenant."""
    min_args = 2

    def run(self, *args):
        server = self.get_server(args[0])
        image = self.create_image(server)
        clone = self.create_instance(server, image, args[1])
        print "Deleting image."
        image.delete()
        print green("Success!")
        self.print_instance(clone)

    def create_image(self, server):
        image_name = self.create_image_name(server)
        print "Creating Image: {}".format(image_name)
        print "This may take a while..."

        try:
            id = self.novaclient.servers.create_image(server, image_name)
        except exceptions.NotFound:
            msg = red("'{}' not found.\n".format(server.name))
            msg += "Use 'stagingctl list' to view active instances."
            raise CommandExecutionError(msg)

        image = self.novaclient.images.get(id)
        self.wait(image)
        print green("Image creation successful!")
        return image

    def create_image_name(self, server):
        now = datetime.now()
        return "{}-clone-{}".format(server.name, now).replace(' ', '-')

    def create_instance(self, server, image, name):
        print "Creating instance: {}".format(name)
        print "This may take a while..."
        flavor = self.novaclient.flavors.get(server.flavor['id'])
        clone = self.novaclient.servers.create(
            name,
            image,
            flavor,
            security_groups=(item['name'] for item in server.security_groups),
            key_name=server.key_name,
        )
        self.wait(clone)
        print green("Instance creation successful!")
        self.add_floating_ip(clone)
        return clone

    def add_floating_ip(self, server):
        try:
            # BUG: This will remove the floating ip from whoever it is assigned
            # to. Therefore we must check to see if all floating ips are
            # assigned instead.
            ip = self.novaclient.floating_ips.list()[0].ip
        except IndexError:
            print red("No more floating IPs available! Skipping assignment.")
        else:
            print "Assigning floating IP."
            server.add_floating_ip(ip)

    def print_instance(self, server):
        server.get()
        ips = server.networks.values()[0]
        print tabulate([[green(server.name)] + ips])
