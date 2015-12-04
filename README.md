# Installation

`pip install stackctl`

# Usage

Stackctl can be used from as a CLI tool, `stackctl [--help] <command> [args]`,
or imported into a python project.

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
- `stackctl emancipate-salt INSTANCE_NAME [--user, --port, --dbuser]`: Change slave mysql to master.

# TODO

`cmds.py` `add_floating_ip`.
