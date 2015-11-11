package main

import (
	"fmt"
	"github.com/hivelocity/stagingctl/commands"
	"github.com/hivelocity/stagingctl/helpers"
	"os"
)

var cmds = map[string]interface{}{
	"create":  commands.Create,
	"destroy": commands.Destroy,
	"list":    commands.Instances,
}

var required_args = map[string]int{
	"create":  1,
	"destroy": 1,
	"list":    0,
}

func main() {
	args := os.Args[1:]
	cmd := args[0]
	if ok := ValidCommand(cmd); ok {
		if ok := ValidArgLength(cmd, args); ok {
			cmds[cmd].(func([]string))(args[1:])
		} else {
			helpers.PrintColor("red", "ERROR: Invalid argument length!")
			os.Exit(1)
		}
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

func ValidArgLength(cmd string, args []string) bool {
	return len(args) >= required_args[cmd]+1
}
