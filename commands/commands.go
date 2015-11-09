package commands

import (
	"fmt"
	"os"
	"os/exec"
)

func TerraformApply(args ...[]string) {
	cmd := "touch hey.py"
	fmt.Println(args[0])
	fmt.Println(args)
	if err := exec.Command(cmd, args).Run(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println("Successfully halved image in size")
}

func TerraformDestroy(args ...interface{}) {
}
