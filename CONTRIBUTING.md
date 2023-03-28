# Contributing

## Branches

- `main` for active development. Changes submitted via pull request.
- `vX` for public release of version X.

## Contributing Code

This project uses [hatch](https://hatch.pypa.io/latest/) as its Python project
manager.

Pre-commit is available to help you pass the pull request checks.

## Making a New Release

1. A new major release `X.0.0` will have a new branch `vX`. A minor and patch
release will use existing branch.
2. Create and increment Github releases.
3. Build and release to PyPI with hatch.
