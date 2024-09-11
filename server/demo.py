import json
import time

import click
import httpx
import qr2text  # type: ignore


def do_request(
    sender: str, method: str, url: str, body: dict | str | None = None, headers: dict | None = None
):
    click.secho(f"{sender}: {method.upper()} {url}", fg="blue")
    if body:
        click.secho(json.dumps(body, indent=2), fg="blue", dim=True)

    response = httpx.request(
        method,
        url,
        json=(body if isinstance(body, dict) else None),
        content=(body if isinstance(body, str) else None),
        headers=headers,
    )

    click.secho(f"response: {response.status_code}", fg="blue")
    if response.headers["Content-Type"] == "application/json" and response.content:
        click.secho(json.dumps(response.json(), indent=2), fg="blue", dim=True)
    else:
        click.secho(response.text, fg="blue", dim=True)
    return response


def demo(base_url: str):
    click.secho("Welcome to the demo!\n", fg="green", bold=True)
    click.secho(f"Starting exchange on {base_url}...\n")

    initiator_exchange_response = do_request(
        "initiator",
        "POST",
        f"{base_url}/api/exchanges/create/",
        body={
            "attributes": [[["irma-demo.gemeente.personalData.fullname"]]],
            "public_initiator_attributes": [["irma-demo.sidn-pbdf.mobilenumber.mobilenumber"]],
        },
    ).json()

    exchange_id = initiator_exchange_response["id"]

    click.secho("Initiating session on irma server...\n")

    irma_session_response = do_request(
        "initiator",
        "POST",
        f"{base_url}/yivi/session/",
        body=initiator_exchange_response["request_jwt"],
        headers={"Content-Type": "text/plain"},
    ).json()

    click.secho("Perform disclosure as initiator...\n")

    qr_content = json.dumps(irma_session_response["sessionPtr"])
    qr_text = qr2text.QR.from_text(qr_content).to_ascii_art()

    click.secho(qr_text)

    while True:
        time.sleep(3)

        session_status_response = do_request(
            "initiator",
            "GET",
            f"{base_url}/yivi/session/{irma_session_response['token']}/status",
        ).json()

        if session_status_response == "DONE":
            break

    click.secho("Getting result JWT and sending it to DIYivi\n")

    initiator_result_jwt = do_request(
        "initiator",
        "GET",
        f"{base_url}/yivi/session/{irma_session_response['token']}/result-jwt",
    ).text

    do_request(
        "initiator",
        "POST",
        f"{base_url}/api/exchanges/{exchange_id}/start/",
        body={
            "initiator_secret": initiator_exchange_response["initiator_secret"],
            "disclosure_result": initiator_result_jwt,
        },
    )

    recipient_url = f"{base_url}/exchange/{exchange_id}/respond/"
    click.secho(f"Initiator sends to recipient: {recipient_url}\n", bold=True)

    click.secho("Recipient opens exchange request...\n")
    recipient_exchange_response = do_request(
        "recipient", "GET", f"{base_url}/api/exchanges/{exchange_id}/"
    ).json()

    click.secho("Initiating recipient's session on irma server...\n")

    irma_session_response = do_request(
        "recipient",
        "POST",
        f"{base_url}/yivi/session/",
        body=recipient_exchange_response["request_jwt"],
        headers={"Content-Type": "text/plain"},
    ).json()

    click.secho("\nPerform disclosure as recipient...\n")

    qr_content = json.dumps(irma_session_response["sessionPtr"])
    qr_text = qr2text.QR.from_text(qr_content).to_ascii_art()

    click.secho(qr_text)

    while True:
        time.sleep(3)

        session_status_response = do_request(
            "recipient",
            "GET",
            f"{base_url}/yivi/session/{irma_session_response['token']}/status",
        ).json()

        if session_status_response == "DONE":
            break

    click.secho("Getting result JWT and sending it to DIYivi\n")

    recipient_result_jwt = do_request(
        "recipient",
        "GET",
        f"{base_url}/yivi/session/{irma_session_response['token']}/result-jwt",
    ).text

    do_request(
        "recipient",
        "POST",
        f"{base_url}/api/exchanges/{exchange_id}/respond/",
        body={
            "disclosure_result": recipient_result_jwt,
        },
    )

    click.secho("\nInitiator retrieves the result...\n")

    do_request(
        "initiator",
        "GET",
        f"{base_url}/api/exchanges/{exchange_id}/result/?secret={initiator_exchange_response['initiator_secret']}",
    ).json()


if __name__ == "__main__":
    demo("https://diyivi.ddoesburg.nl")
