# Copilot instructions

## Repository shape

This is a course-submission repository, not one single application. Work is grouped by
course week (`viikko1` through `viikko6`), and most exercise directories are independent
Python projects with their own `pyproject.toml`, `uv.lock`, `.python-version`, and source
layout. Run commands from the exercise directory you are changing; there is no
repository-wide Python package or test runner.

The exercises progress from small command-line/domain programs to Flask applications and
Robot Framework browser tests:

- Weeks 1–2 contain NHL readers/statistics and dependency-injection exercises. Their
  services consume reader abstractions, and tests commonly replace network readers with
  in-memory stubs.
- Week 3 contains Robot Framework exercises. `hello-robot` tests a Python counter
  library directly; `webcounter` and `login` exercise Flask apps through the browser.
  The Flask entry point is normally `src/index.py` and listens on port 5001.
- Weeks 4–5 focus on domain design, TDD, mocks, and collection/game implementations.
  Tests are mostly `unittest.TestCase` classes run by pytest; mock-based exercises
  verify collaborator calls and arguments.
- Week 6 contains standalone calculator and query-language exercises, with code under
  `src/` where present.

Keep each exercise self-contained. Do not move shared code into a repository-level
package unless the exercise explicitly requires it. Preserve the existing Finnish
names and the public interfaces used by the exercise tests.

## Environment and dependencies

Projects use `uv` and require Python 3.14. In the directory for an exercise, install or
refresh its environment with:

```bash
uv sync
```

Do not run `uv` commands from the repository root expecting them to discover every
exercise; select the relevant `viikkoN/<exercise>` directory first. The lockfile belongs
to that exercise and should be updated only when its `pyproject.toml` dependencies
change.

## Tests and linting

For a pytest-based exercise, run the full local suite from that exercise directory:

```bash
uv run pytest
```

Run one test by passing pytest's node id, for example:

```bash
uv run pytest src/tests/test_statistics_service.py::TestStatisticsService::test_team_returns_players_from_requested_team
```

The tests are usually written in `unittest` style even though pytest runs them. Prefer
the existing reader stubs and mocks so unit tests do not make network calls. The NHL
reader project has `pythonpath = ["src"]` in its `pyproject.toml`; follow that pattern
if a new exercise needs imports from its `src` directory.

`viikko2/nhl-reader` also declares Pylint as a development dependency. From that
directory, run:

```bash
uv run pylint src
```

For `viikko3/hello-robot`, run the Robot suites from the project directory:

```bash
uv run robot src/tests
```

For the Flask browser projects, install the Chromium browser once in the project
environment:

```bash
uv run rfbrowser install --with-deps chromium
```

Start the app in one terminal, then run the suites in another. For example, in
`viikko3/login`:

```bash
uv run python src/index.py
uv run robot --variable HEADLESS:true src/tests
```

The same commands apply to `viikko3/webcounter`. Its
`run_robot_tests.sh` script is the canonical end-to-end wrapper: it starts the Flask
server, waits for port 5001 to respond, runs headless Robot tests, and stops the server.
The webcounter GitHub Actions workflow follows the sequence `uv sync`, browser
installation, and `bash run_robot_tests.sh`.

To run one Robot test, select the suite and test name:

```bash
uv run robot --variable HEADLESS:true --test "Login With Correct Credentials" src/tests/login.robot
```

When changing a browser-tested app, preserve the `/ping` health endpoint and any
`/tests/reset` endpoint used by the Robot resources unless the tests are updated
together.

## Conventions that matter here

- Keep application composition at the exercise entry point. Flask routes import the
  app-layer services/repositories, while domain classes remain usable independently in
  unit tests.
- External data access is separated behind reader/repository objects. Test doubles are
  passed into statistics or service classes rather than patching network calls.
- In the web exercises, Robot resource files own browser setup and reusable keywords;
  suite files describe scenarios and use suite/test setup for state reset. Use
  `HEADLESS:true` in automation and keep the default interactive mode useful locally.
- Flask templates are in each app's `src/templates` directory and use the existing
  layout/template inheritance. Keep route names and form field IDs aligned with the
  Robot selectors.
- Domain exercises intentionally expose the interfaces required by their assignment
  tests (including Finnish method/class names). Avoid broad refactors or renaming public
  methods just to make style uniform across weeks.
- Existing tests often assert exact ordering, return values, and mock call arguments.
  Preserve those observable contracts when refactoring implementations.

