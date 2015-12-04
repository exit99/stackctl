import os
from datetime import datetime

import progressbar
from colors import green, red
from novaclient import client, exceptions
from tabulate import tabulate

from errors import WrapperFailure


__all__ = ["NovaWrapper"]


class NovaWrapper():
    def __init__(self):
        self.client = self.authenticate()

    def authenticate(self):
        return client.Client(
            os.getenv('OS_COMPUTE_API_VERSION', 2),
            os.getenv('OS_USERNAME'),
            os.getenv('OS_PASSWORD'),
            os.getenv('OS_TENANT_NAME'),
            os.getenv('OS_AUTH_URL'),
        )

    def server(self, name):
        try:
            return self.client.servers.find(name=name)
        except exceptions.NotFound:
            msg = red("'{}' is not an active instance.\n".format(name))
            msg += "Use 'stackctl list' to view active instances."
            raise WrapperFailure(msg)

    def servers(self):
        return sorted(self.client.servers.list(), key=lambda x: x.name)

    def images(self):
        return sorted(self.client.images.list(), key=lambda x: x.name)

    def image_data(self, image):
        if image.status == "ACTIVE":
            name = green(image.name)
        else:
            name = red(image.name)
        return [name, image.id, "{}%".format(image.progress)]

    def clone(self, server, name):
        snapshot = self.snapshot(server)
        clone = self.create_instance(server, snapshot, name)
        self.add_floating_ip(clone)
        print "Deleting snapshot."
        snapshot.delete()
        return clone

    def snapshot(self, server):
        now = datetime.now()
        name = "{}-clone-{}".format(server.name, now).replace(' ', '-')
        print "Creating snapshot: {}".format(name)
        print "This may take a while..."
        try:
            id = self.client.servers.create_image(server, name)
        except exceptions.NotFound:
            msg = red("'{}' not found.\n".format(server.name))
            msg += "Use 'stackctl list' to view active instances."
            raise WrapperFailure(msg)
        image = self.client.images.get(id)
        self.wait(image)
        print green("Snapshot creation successful!")
        return image

    def create_instance(self, server, image, name):
        print "Creating instance: {}".format(name)
        print "This may take a while..."
        flavor = self.client.flavors.get(server.flavor['id'])
        instance = self.client.servers.create(
            name,
            image,
            flavor,
            security_groups=(item['name'] for item in server.security_groups),
            key_name=server.key_name,
        )
        self.wait(instance)
        print green("Instance creation successful!")
        return instance

    def add_floating_ip(self, server):
        ips = self.client.floating_ips.findall(instance_id=None)
        if ips:
            print "Assigning floating IP."
            server.add_floating_ip(ips[0])
            return
        print red("No more floating IPs available! Skipping assignment.")

    def floating_ip(self, server):
        try:
            return self.client.floating_ips.find(instance_id=server.id).ip
        except (exceptions.NotFound, AttributeError):
            return None

    def print_server(self, server):
        server.get()
        ips = server.networks.values()[0]
        print tabulate([[green(server.name)] + ips])

    def wait(self, item, status="ACTIVE"):
        bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
        while item.progress < 100 and item.status != status:
            bar.update(item.progress)
            item.get()
