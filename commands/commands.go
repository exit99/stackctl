package commands

import (
	"fmt"
	"github.com/hivelocity/stagingctl/helpers"
	"github.com/hivelocity/stagingctl/openstack"
	"github.com/rackspace/gophercloud/openstack/compute/v2/servers"
	"os"
	//"os/exec"
)

func TerraformApply(args []string) {
	//cmd := "touch hey.py"
	fmt.Println(args[0])
	fmt.Println(args)
	//if err := exec.Command(cmd, args).Run(); err != nil {
	//	fmt.Fprintln(os.Stderr, err)
	//	os.Exit(1)
	//}
	fmt.Println("Successfully halved image in size")
}

func TerraformDestroy(args []string) {
	fmt.Println("NOT IMPLEMENTED")
}

func Instances(args []string) {
	client, err := openstack.OpenstackConnect()
	if err != nil {
		err.Error()
		os.Exit(1)
	}
	opts := servers.ListOpts{}
	pager := servers.List(client, opts)
	pages, err := pager.AllPages()
	all, err := servers.ExtractServers(pages)
	var color string
	for _, instance := range all {
		if instance.Status == "ACTIVE" {
			color = "green"
		} else {
			color = "red"
		}
		helpers.PrintColor(color, instance.Name)
	}
}
