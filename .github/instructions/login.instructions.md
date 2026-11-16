---
applyTo: "viikko3/login/**"
---

# Login exercise

This is an independent Python/Flask `uv` project. Run all commands from
`viikko3/login` and use `uv run ...`:

```bash
uv sync
```

Start the application with:

```bash
uv run python src/index.py
```

It listens on port `5001`. The application must be running while Robot Framework tests
are executed:

```bash
uv run robot src/tests
```

For headless browser execution, use `--variable HEADLESS:true`. Install Chromium once
if needed with `uv run rfbrowser install --with-deps chromium`.

`src/app.py` defines routes. User input and authentication validation are implemented
in `src/services/user_service.py`: `validate` checks registration fields, while
`check_credentials` looks up users through `src/repositories/user_repository.py` and
verifies login credentials. Keep the `/ping` and `/tests/reset` endpoints and the
route/form/template interfaces used by the Robot tests.

