# DIYivi Server

The DIYivi server is a simple REST API based on FastAPI. This allows for rapid development, with a precise OpenAPI specification.

## Development

Install [poetry](https://python-poetry.org/docs/#installation) >= 1.8.0, then run:

```bash
# To install the dependencies.
poetry install

# To open a shell in the virtual environment.
poetry shell

# Then, in the virtual environment:

# To run the server.
fastapi dev

# To run the tests.
pytest

# To manually run linting and formatting.
ruff check .
ruff format .
mypy .

# To save the OpenAPI specification to a file.
python -c "from app.main import output_schema; output_schema()" > schema.json     
```
