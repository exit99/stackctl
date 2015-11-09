provider "openstack" {
    tenant_name = "internal-staging"
    api_key = ""
    endpoint_type = ""
    auth_url = "http://10.42.45.5:5000/v2.0"
}

resource "openstack_compute_floatingip_v2" "floatip_1" {
  region = "RegionOne"
  pool = "nova"
}

resource "openstack_compute_keypair_v2" "test-keypair" {
    name = "zkazanski"
    public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC/luyMG6cxKVW+NvSbL0agcM9ccQwgPrQSJmgNOrVMdAfdCtSFo+OwqteZqThnVZFltTu5G/kDzkuFZYO4ZvmIFDev5TUV9C8saCoXTgBRCLlodYANI4NgAClyQWivz+MgE5I2YK/V04BJEMTfwL4KHCZtL3En6DQRSbUe+4Lt+0nXz7hIkE3ww/y5Evevx9cVAB4seEX5QUVhwtuRFKlKO0cXhdGLESIMYqAGPgUzM5zwMuQELWJpJjCOeQeAQFl1ehmMhnQ8SVBrytTCt7YCKzQmDeSiKeGSha1feI0xwGmqw1m9VVKJlY7eK+4ZkrL10eFLXH2GEMweGv9aw5S1 zachary@zachary-X9SCL-X9SCM"
}

resource "openstack_compute_instance_v2" "hvdb1-staging" {
    name = "hvdb1"
    image_id = "8acf7c04-ecd2-4b25-b519-f95b8ee0a2da"
    flavor_id = "17ce8627-bb55-49ca-bab9-40c9a05cd2a9"
    security_groups = ["default"]
    key_pair = "${openstack_compute_keypair_v2.test-keypair.name}"
    floating_ip = "${openstack_compute_floatingip_v2.floatip_1.address}"
    provisioner "remote-exec" {
        connection {
            type = "ssh"
            user = "ubuntu"
            key_file = "~/.ssh/id_rsa"
            agent = false
        }
        script = "provision_mysql.sh"
    }

}

