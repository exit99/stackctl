package commands

import (
	"fmt"
	"github.com/hivelocity/stagingctl/exceptions"
	"github.com/hivelocity/stagingctl/helpers"
	"github.com/hivelocity/stagingctl/openstack"
	"github.com/rackspace/gophercloud/openstack/compute/v2/servers"
	"os"
	"os/exec"
	"path/filepath"
	"reflect"
	"runtime"
	"strings"
)

func printCommand(cmd *exec.Cmd) {
	msg := fmt.Sprintf("==> Executing: %s\n", strings.Join(cmd.Args, " "))
	helpers.PrintColor("blue", msg)
}

func printError(err error) {
	if err != nil {
		os.Stderr.WriteString(fmt.Sprintf("==> Error: %s\n", err.Error()))
	}
}

func printOutput(outs []byte) {
	if len(outs) > 0 {
		fmt.Printf("==> Output: %s\n", string(outs))
	}
}

func DirExists(path string) bool {
	if _, err := os.Stat(path); err != nil {
		return false
	}
	return true
}

func ConfigurationsDir() string {
	dir := os.Getenv("STAGINGCTL_CONFIGURATIONS_DIR")
	if dir != "" {
		return dir
	}
	dir, err := filepath.Abs(filepath.Dir(os.Args[0]))
	if err != nil {
		return ""
	} else {
		return filepath.Join(dir, "configurations")
	}
}

func RunCmd(dir, command, args string) {
	cwd, err := os.Getwd()
	os.Chdir(dir)

	cmd := exec.Command(command, args)
	printCommand(cmd)
	output, err := cmd.CombinedOutput()
	printError(err)
	printOutput(output)

	os.Chdir(cwd)
}

func Create(args []string) {
	conf_dir := filepath.Join(ConfigurationsDir(), args[0])
	if ok := DirExists(conf_dir); ok {
		RunCmd(conf_dir, "terraform", "apply")
	} else {
		exceptions.ConfDoesNotExist(conf_dir)
	}
}

func Destroy(args []string) {
	project := args[0]
	conf_dir := filepath.Join(ConfigurationsDir(), project)
	if ok := DirExists(conf_dir); ok {
		msg := fmt.Sprintf("\nAre you sure to want to delete %s? y/n: ", project)
		if resp := helpers.GetInput(msg); resp == "y" {
			RunCmd(conf_dir, "terraform", "destroy")
		} else {
			fmt.Println(len(resp))
			fmt.Println(resp[1])
			fmt.Println(resp == "\ny")
			runtime.Breakpoint()
			fmt.Println(reflect.TypeOf(resp))
			fmt.Println(reflect.TypeOf("y"))
			helpers.PrintColor("red", "Destroy aborted.")
		}
	} else {
		exceptions.ConfDoesNotExist(conf_dir)
	}
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
