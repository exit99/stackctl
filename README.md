# Installation

`pip install stackctl`

# Usage

Stackctl can be used from as a CLI tool by using `stackctl [--help] <command> [args]`
or imported into python projects.

Python Example:
```python
import stackctl

stackctl.main('COMMAND', *args)
```

## Commands

- `stackctl --help`
- `stackctl list`: Get list of instances.
- `stackctl images`: Get list of images.
- `stackctl clone INSTANCE_NAME CLONE_NAME`: Clone instance.
- `stackctl de-salt INSTANCE_NAME [--user, --port]`: Turn off salt minion.
- `stackctl de-salt INSTANCE_NAME [--user, --port]`: Change slave mysql to master.

# TODO

`cmds.py` `add_floating_ip`.
