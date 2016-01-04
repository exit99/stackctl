# Changelog
All notable changes will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).


## [0.2.1]- 1/4/16:
### feat

- List cmd can ignore server name written to ~/.stackctl_ignore or the env var STACKCTL_IGNORE.


## [0.2.0]- 1/4/16:
### Refactor

- When cloning, do not automatically use the keypair that created the vm.  Instead, create a stackctl keypair to use.


## [0.1.0]- 12/9/15:
### Feature

- Add force flag to `emancipate` and `rm` .
- Accept `kwargs` in all `run` functions of cmds.
- Add `start` and `stop` commands.


## [0.0.3]- 12/4/15:
### Refactor

- All errors are raised instead of being caught and printing a msg.


## [0.0.2] - 12/4/15:
### Refactor

- `NovaWrapper.servers` now uses `novaclient.find`
- `__init__.py` import modules for easier use when using `import `tackctl`.


## [0.0.1] - 12/4/15:
### Feature

- Initial Version
