# Contributing to Doc-Agent

We love your input! We want to make contributing to Doc-Agent as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issue tracker](https://github.com/yourusername/doc-agent/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/yourusername/doc-agent/issues/new); it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can.
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Use a Consistent Coding Style

* 4 spaces for indentation rather than tabs
* 80 character line length
* Run `black` for Python code formatting
* Run `pylint` for code quality checks

## Code Review Process

The core team looks at Pull Requests on a regular basis. After feedback has been given we expect responses within two weeks. After two weeks we may close the PR if it isn't showing any activity.

## Testing

### Running Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run tests with coverage
pytest --cov=doc_agent --cov-report=term-missing
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with `test_` prefix
- Use descriptive test function names
- Include both positive and negative test cases
- Mock external services appropriately

## Documentation

### Code Documentation

- Use docstrings for all public modules, functions, classes, and methods
- Follow Google style for docstrings
- Include type hints for function arguments and return values
- Add inline comments for complex logic

Example:

```python
def process_text(content: str, max_length: int = 100) -> str:
    """Process and validate text content.

    Args:
        content: The text content to process.
        max_length: Maximum allowed length of the text.

    Returns:
        The processed text content.

    Raises:
        ValueError: If content exceeds max_length.
    """
    if len(content) > max_length:
        raise ValueError(f"Content exceeds maximum length of {max_length}")
    return content.strip()
```

### Project Documentation

- Keep README.md up to date
- Document all configuration options
- Provide examples for common use cases
- Update architecture.md for significant changes

## Setting Up Development Environment

1. Clone your fork:
```bash
git clone git@github.com:your-username/doc-agent.git
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: `.venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

4. Set up pre-commit hooks:
```bash
pre-commit install
```

## Branch Naming Convention

- Feature branches: `feature/description`
- Bug fixes: `fix/description`
- Documentation: `docs/description`
- Performance improvements: `perf/description`

## Commit Message Format

Use clear and descriptive commit messages:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- feat: A new feature
- fix: A bug fix
- docs: Documentation only changes
- style: Changes that do not affect the meaning of the code
- refactor: A code change that neither fixes a bug nor adds a feature
- perf: A code change that improves performance
- test: Adding missing tests or correcting existing tests
- chore: Changes to the build process or auxiliary tools

Example:
```
feat(evaluator): add tone analysis capability

- Implements tone analysis using OpenAI's API
- Adds configuration options for tone preferences
- Includes unit tests for the new feature

Closes #123
```

## License

By contributing, you agree that your contributions will be licensed under its MIT License. 