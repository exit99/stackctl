package helpers

import (
	"bufio"
	"fmt"
	"os"
)

var colors = map[string]string{
	"red":    "\x1b[31;1m",
	"green":  "\x1b[32;1m",
	"yellow": "\x1b[33;1m",
	"blue":   "\x1b[34;1m",
	"maroon": "\x1b[35;1m",
	"cyan":   "\x1b[36;1m",
	"white":  "\x1b[37;1m",
	"end":    "\x1b[0m",
}

func PrintColor(color, msg string) {
	if val, ok := colors[color]; ok {
		color = val
	} else {
		color = colors["red"]
	}
	fmt.Println(color, msg, colors["end"])
}

func GetInput(msg string) string {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print(msg)
	text, _ := reader.ReadString('\n')
	return text
}
