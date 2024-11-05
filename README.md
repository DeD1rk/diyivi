[![Build](https://github.com/DeD1rk/diyivi/actions/workflows/build.yaml/badge.svg)](https://github.com/DeD1rk/diyivi/actions/workflows/build.yaml)
[![Linting and Testing](https://github.com/DeD1rk/diyivi/actions/workflows/ci.yaml/badge.svg)](https://github.com/DeD1rk/diyivi/actions/workflows/ci.yaml)

# Do It Yivi

Do It Yivi (DIYivi) is a tool that allows users to easily use [Yivi](https://www.yivi.app/) attributes for personal use cases. It provides the following functionality:

1. Getting to know one another (`exchanges`): a user can request to exchange attributes with another user. The initiator first discloses their attributes, and then sends a link to the recipient. The recipient, if she consents, then discloses her attributes, and both parties can see each other's attributes.
2. Creating and verifying attribute-based signatures: a user can create a signature on a plain-text message, using their Yivi attributes. Another user can then verify this signature, and see the attributes that were used to create it.
3. Requesting a signature from someone else: a user can request that another user creates a signature on a plain-text message, using their Yivi attributes. The initiator fills in a message and selects the desired attributes. Then, the initiator discloses their own email (used to send the result), and sends a link to the recipient. The recipient, if she consents, then creates a signature. This signature is presented to the recipient, and sent by email to the initiator. Verification can be done the same way as for self-created signatures.

For more information about the security, privacy, usability and implementation considerations, see the design documents:

- [docs/exchanges.md](docs/exchanges.md)
- [docs/signatures.md](docs/signatures.md)

## Getting started

This project consists of a front-end and a back-end.
The front-end is a in Vue.js single-page application, located in [`client`](client/).
The back-end is a in FastAPI REST API, located in [`server`](server/).

Additionally, DIYivi requires a Redis server to maintain state for the backend, and
an `irma server` for interaction with the user's Yivi app.


For development, I'm using an `irma server` I host at `https://diyivi.ddoesburg.nl/yivi/`.
The client is configured to use this via [`client/.env`](client/.env)).
This server is currently using the *unsafe* private key checked in at [`infra/irmaserver_private.pem`](infra/irmaserver_private.pem).
For a production setup, of course a fresh and actually secret key should be used.

To run the project locally, if you're using such a real deployed `irma server`,
you then only need to run the server and client at the same time. If the server is not
configured to use a Redis server, it will fall back to a (not production-ready) in-memory
storage.

### Server

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run:

```bash
# To run the server.
uv run fastapi dev

# To run the tests.
uv run pytest

# To manually run linting and formatting.
uv run ruff check .
uv run ruff format .
uv run mypy .

# To save the OpenAPI specification to a file.
uv run python -c "from app.main import output_schema; output_schema()" > schema.json

# Or, to get rid of `uv run` before all of these commands, activate the virtual environment:
source .venv/bin/activate
```

### Client

```sh
# Install dependencies.
npm install

# Run the development server.
npm run dev

# To compile and minify for production.
npm run build

# To manually run linting.
npm run lint
```
