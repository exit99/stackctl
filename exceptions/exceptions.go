package exceptions

import (
	"fmt"
	"github.com/hivelocity/stagingctl/helpers"
)

type CliError struct {
	Msg    string
	Helper string
}

func (e *CliError) Error() string {
	msg := fmt.Sprintf("ERROR: %s", e.Msg)
	helpers.PrintColor("red", msg)
	fmt.Println(e.Helper)
	return fmt.Sprintf("%s%s", e.Msg, e.Helper)
}
