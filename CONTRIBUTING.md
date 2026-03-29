# Contributing to AxomiScript

Thank you for your interest in contributing! AxomiScript is a community-driven project and welcomes contributions of all kinds — new language frontends, bug fixes, documentation improvements, and more.

---

## Setting Up the Development Environment

1. **Clone the repository**

   ```bash
   git clone https://github.com/leonkaushikdeka/AxomiScript.git
   cd AxomiScript
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python -m venv .venv
   # On Linux / macOS:
   source .venv/bin/activate
   # On Windows:
   .venv\Scripts\activate
   ```

3. **Install in editable mode with dev dependencies**

   ```bash
   pip install -e ".[dev]"
   ```

   This installs `lark`, `pytest`, `pytest-cov`, `ruff`, and `mypy` alongside the package itself.

---

## Running the Tests

```bash
pytest
```

To see coverage:

```bash
pytest --cov=axomiscript --cov-report=term-missing
```

To run a specific test class:

```bash
pytest tests/test_assamese.py::TestParser -v
```

All tests must pass before opening a pull request.

---

## Code Style

AxomiScript uses **ruff** for linting and formatting.

**Check for issues:**

```bash
ruff check axomiscript/ tests/
```

**Auto-fix safe issues:**

```bash
ruff check --fix axomiscript/ tests/
```

**Key style rules:**

- Line length: 100 characters
- Target Python version: 3.8+
- All `.py` source files must include `# -*- coding: utf-8 -*-` as the first line
- Docstrings on all public functions and classes
- No bare `except:` clauses — always catch a specific exception type

---

## Adding a New Language

Adding a new natural-language frontend (Hindi, Bengali, Bodo, Odia, etc.) is the most impactful contribution you can make to AxomiScript.

See the full step-by-step guide: **[docs/adding_a_language.md](docs/adding_a_language.md)**

In short:

1. Create `axomiscript/languages/<name>/` with `keywords.py`, `preprocessor.py`, `grammar.py`, `transformer.py`, `parser.py`, and `__init__.py`.
2. Register your parser in `axomiscript/languages/__init__.py`.
3. Add tests under `tests/test_<name>.py`.
4. Add example `.as` files under `examples/`.

---

## Pull Request Checklist

Before submitting a pull request, please confirm the following:

- [ ] All existing tests pass: `pytest`
- [ ] No ruff linting errors: `ruff check axomiscript/ tests/`
- [ ] Every new public function and class has a docstring
- [ ] All new `.py` files begin with `# -*- coding: utf-8 -*-`
- [ ] New language frontends include at least one test file
- [ ] Example `.as` files are included for any new language
- [ ] `docs/adding_a_language.md` is updated if the plugin interface changes
- [ ] The PR description explains **what** changed and **why**

---

## Reporting Issues

Please open a GitHub issue for:

- Bugs (include a minimal reproducible example)
- Feature requests
- Incorrect or missing documentation

Use the issue tracker at: https://github.com/leonkaushikdeka/AxomiScript/issues

---

## Code of Conduct

Be respectful, patient, and constructive. This project exists to make programming accessible to speakers of Assamese and other languages — contributors from all linguistic backgrounds are welcome.
