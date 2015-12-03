# Usage

## Commands

### Get list of instances
`stagingctl list`

### Get list of images
`stagingctl images`

### Clone instance
`stagingctl clone INSTANCE_NAME CLONE_NAME`

### Sanitize instance
Turns off salt minion.
`stagingctl sanitize INSTANCE_NAME`
Options flags: `--user=USERNAME --port=PORT`

### Help
`stagingctl --help`



# TODO

`cmds.py` `add_floating_ip`.
