package main

import (
	"fmt"
	"github.com/hivelocity/stagingctl/commands"
	"github.com/hivelocity/stagingctl/helpers"
	"os"
)

var cmds = map[string]interface{}{
	"create":  commands.TerraformApply,
	"destroy": commands.TerraformDestroy,
}

func main() {
	args := os.Args[1:]
	cmd := args[0]
	if ok := ValidCommand(cmd); ok {
		fmt.Println(args)
		cmds[cmd].(func(...[]string))(args[1:])
	} else {
		msg := fmt.Sprintf("ERROR: '%s' command does not exists!", cmd)
		helpers.PrintColor("red", msg)
	}
}

func ValidCommand(cmd string) bool {
	if _, ok := cmds[cmd]; ok {
		return true
	} else {
		return false
	}
}

func DirExists(path string) bool {
	if _, err := os.Stat(path); err != nil {
		return false
	}
	return true
}
