# Installation

`pip install stackctl`

# Usage

Before usage you must set the appropriate enviroment variables.
This is done easiest with the [OpenStack RC file](http://docs.openstack.org/cli-reference/content/cli_openrc.html).

You can use stackctl as a CLI tool, `stackctl [--help] <command> [args]`,
or import it into a python project.

Python Example:
```python
import stackctl

# args == INSTANCE_NAME etc...
# kwargs == flags...
stackctl.run('COMMAND', *args, **kwargs)

# Example
stackctl.run("de-salt", "INSTANCE_NAME", user="MYUSER", "PORT"=22)
```

*Note:* Some commands, such as clone, take a long time.  You may want to async call them if ran from inside a python script.

## Commands

- `stackctl --help`
- `stackctl list`: Get list of instances.
- `stackctl images`: Get list of images.
- `stackctl start INSTANCE_NAME`: Start an instances.
- `stackctl stop INSTANCE_NAME`: Stop an instances.
- `stackctl rm INSTANCE_NAME`: Remove instance.
- `stackctl clone INSTANCE_NAME CLONE_NAME`: Clone instance.
- `stackctl de-salt INSTANCE_NAME [--user, --port]`: Turn off salt minion.
- `stackctl emancipate-salt INSTANCE_NAME [--user, --port, --dbuser]`: Change slave mysql to master.
