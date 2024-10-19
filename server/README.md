# DIYivi Server

The DIYivi server is a simple REST API based on FastAPI. This allows for rapid development, with a precise OpenAPI specification.

## Development

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run:

```bash
# To install the dependencies.
uv sync

# To run the server.
uv run fastapi dev

# To run the tests.
uv run pytest

# To manually run linting and formatting.
uv run ruff check .
uv run ruff format .
uv run qmypy .

# To save the OpenAPI specification to a file.
uv run python -c "from app.main import output_schema; output_schema()" > schema.json

# Or, to get rid of `uv run` before all of these commands, activate the virtual environment:
source .venv/bin/activate
```
