package openstack

import (
	"github.com/hivelocity/stagingctl/exceptions"
	"github.com/rackspace/gophercloud"
	"github.com/rackspace/gophercloud/openstack"
)

func OpenstackConnect() (*gophercloud.ServiceClient, error) {
	provider, err := OpenstackAuthenticate()
	if err == nil {
		return openstack.NewComputeV2(provider, gophercloud.EndpointOpts{
			Region: "RegionOne",
		})
	}
	return nil, err
}

func OpenstackAuthenticate() (*gophercloud.ProviderClient, error) {
	if opts, err := openstack.AuthOptionsFromEnv(); err == nil {
		if provider, err := openstack.AuthenticatedClient(opts); err == nil {
			return provider, nil
		}
	}
	msg := "Invalid Openstack Credentials"
	helper := "Did you `source internal-staging.openrc.sh`?"
	return nil, &exceptions.CliError{msg, helper}
}
