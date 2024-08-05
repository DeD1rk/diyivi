import jwt
from fastapi.testclient import TestClient

from app.config import settings
from app.exchanges.dependencies import _storage
from app.exchanges.models import Exchange
from app.main import app
from app.yivi.models import (
    AttributeProofStatus,
    AttributeValue,
    DisclosedAttribute,
    DisclosureRequestJWT,
)

client = TestClient(app)


def test_create_exchange():
    _storage._exchanges.clear()
    _storage._exchange_replies.clear()

    response = client.post(
        "/exchanges/create/",
        json={
            "attributes": [
                [["pbdf.pbdf.email.email"]],
                [
                    ["pbdf.gemeente.personalData.fullname"],
                    [
                        "pbdf.gemeente.personalData.initials",
                        "pbdf.gemeente.personalData.surname",
                    ],
                ],
            ],
            "public_initiator_attributes": [["pbdf.pbdf.mobilenumber.mobilenumber"]],
        },
    )

    assert response.status_code == 200
    response_data = response.json()

    # Check the response content.
    disclosure_request = DisclosureRequestJWT.model_validate(
        jwt.decode(
            response_data["request_jwt"],
            key=settings.irma.session_request_secret_key,
            issuer=settings.irma.session_request_issuer_id,
            algorithms=["HS256"],
        )
    )
    assert disclosure_request.sprequest.request.disclose == [
        [["pbdf.pbdf.mobilenumber.mobilenumber"]],
        [["pbdf.pbdf.email.email"]],
        [
            ["pbdf.gemeente.personalData.fullname"],
            [
                "pbdf.gemeente.personalData.initials",
                "pbdf.gemeente.personalData.surname",
            ],
        ],
    ]
    assert disclosure_request.sprequest.request.client_return_url == (
        f"https://diyivi.app/exchanges/{response_data['id']}/"
    )
    assert disclosure_request.sprequest.request.augment_return_url is True
    assert disclosure_request.sprequest.request.labels == {
        "0": {"en": "Known by the recipient", "nl": "Bekend bij de ontvanger"}
    }

    # Check what was saved in the storage.
    exchange = Exchange.model_validate_json(_storage._exchanges[response_data["id"]])
    assert exchange.initiator_attribute_values is None
    assert exchange.public_initiator_attribute_values is None
    assert exchange.public_initiator_attributes == [
        ["pbdf.pbdf.mobilenumber.mobilenumber"]
    ]
    assert exchange.attributes == [
        [["pbdf.pbdf.email.email"]],
        [
            ["pbdf.gemeente.personalData.fullname"],
            [
                "pbdf.gemeente.personalData.initials",
                "pbdf.gemeente.personalData.surname",
            ],
        ],
    ]


class TestStartExchange:
    exchange = Exchange(
        id="0123456789abcdef",
        initiator_secret="a" * 32,
        attributes=[[["pbdf.pbdf.email.email"]]],
        public_initiator_attributes=[["pbdf.pbdf.mobilenumber.mobilenumber"]],
    )

    phonenumber = DisclosedAttribute(
        rawvalue="31612345678",
        value={"": "31612345678", "en": "31612345678", "nl": "31612345678"},
        id="pbdf.pbdf.mobilenumber.mobilenumber",
        status=AttributeProofStatus.PRESENT,
        issuancetime=1720051200,
    )

    email = phonenumber = DisclosedAttribute(
        rawvalue="foo@example.com",
        value={"": "foo@example.com", "en": "foo@example.com", "nl": "foo@example.com"},
        id="pbdf.pbdf.email.email",
        status=AttributeProofStatus.PRESENT,
        issuancetime=1720051200,
    )

    def test_exchange_not_found(self):
        _storage._exchanges = {self.exchange.id: self.exchange.model_dump_json()}

        response = client.post("/exchanges/0000000000000000/start/")
        assert response.status_code == 404
        assert response.json() == {"detail": "Exchange not found"}

    def test_incorrect_initiator_secret(self):
        _storage._exchanges = {self.exchange.id: self.exchange.model_dump_json()}

        response = client.post(
            f"/exchanges/{self.exchange.id}/start/",
            json={
                "initiator_secret": "b" * 32,
                "disclosure_result": "dummy",
            },
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Incorrect initiator secret"}

    def test_exchange_already_started(self):
        exchange = self.exchange.model_copy()
        exchange.public_initiator_attribute_values = [self.phonenumber]
        exchange.initiator_attribute_values = [[self.email]]
        _storage._exchanges = {self.exchange.id: exchange.model_dump_json}

        response = client.post(
            f"/exchanges/{self.exchange.id}/start/",
            json={
                "initiator_secret": self.exchange.initiator_secret,
                "disclosure_result": "dummy",
            },
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Exchange already started"}

    def test_invalid_jwt(self):
        _storage._exchanges = {self.exchange.id: self.exchange.model_dump_json()}

        response = client.post(
            f"/exchanges/{self.exchange.id}/start/",
            json={
                "initiator_secret": self.exchange.initiator_secret,
                "disclosure_result": "dummy",
            },
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid JWT"}
