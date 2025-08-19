# Contributing

## Branches

All active development are on the `main` branch and releases are on git tags.

## Recommended Project Manager

This project uses [hatch](https://hatch.pypa.io/latest/) and [uv](https://docs.astral.sh/uv) as its Python project manager.

## Commit Messages

All commit messages must pass pre-commit check following [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

## Linting and Testing

All PRs must pass CI checks running linter, tests, and test coverage.

```
# Run lint checks
pre-commit run --all-files
```
```
# Run tests
hatch -e test run test-cov
```

## Making a New Release

Create new release in the GitHub Releases page. GitHub Actions CI will automatically build and publish the package to PyPI.
