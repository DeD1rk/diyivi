from datetime import UTC, datetime

import jwt
from fastapi.testclient import TestClient

from app.config import settings
from app.exchanges.dependencies import _storage
from app.exchanges.models import Exchange, ExchangeReply
from app.main import app
from app.yivi.models import (
    AttributeProofStatus,
    DisclosedAttribute,
    DisclosureRequestJWT,
)

client = TestClient(app)


_irmaserver_jwt_private_key = b"""-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCPOH1dIMwquLaE
nmOmBJEbJKIAnxKV8zCVMd4c2gpTMWUCBE3oIbNlZPYtVTfQJaZHB+tlve/UU8WS
vZPI+eYtTLcbAyx9yVuMZ3qjLOxJj6VESzJ5gsoQ3eAtvXh2bwlNMguVyaQkSeaA
iJ2IiuCYFigyMwMWj7U4HVoFMyeh7tc/xarsxtI2D1QpBuWwd0gfV2QhWMjhlcuB
501ZqQNqhVbTCEr2hTD13EqMoLGJR3+9TblHY4avSKkrpp8yJpQU5ermS7v3Brtl
uYPopml3MahTrcJMJBms/D+Dy+A1c2vrkntcpAG4TMk6H/einDEdWOPJvvtd5ZA5
MhDE1w/zAgMBAAECggEABKXxs6cP2UcbbVxyoX2+c+IRe/Gtub4l0oHG0qrk8ORG
gfU/zgvh9aV8M+ZzJEdEiUOhiTDL6tk5LVUHydsKdGfr/W1x8TcqyHjHSyp3FMAb
vgauwbDT/A4na3Sdx0I9TAsWwyrDMAZR+9PzQO448dauQUrUi9PoLsUNGeQaIjBA
y15K1oqbXaYGuK3uaLOcU2/B7KscleMzzf6QlFYS9ohHQMOnpaEMRmSnSAtDdQJh
q/Ozt0hTm5+/5wpZn9xFvKHcaiPgyElorD17JYfPTO1p+xSvJOnxiAg6tTzEpZ9c
yNnxUvdTPf4nHKssDkY1Dul72CFo08vPVpZqDW+egQKBgQDKc9nyL6Z+e0yDGgwG
liiT7wVEwsgxZ5P9iN76wGnJHDAAPL9baELcwtKZ6ELrX5taFEx871RxiYdFaySv
+GzyPywF9H/FGW7e+ppXv/+hn1qwAKLkyCAsjN+8idm2wGgljMGoGg8txTczEs6a
pUocGuSpFo7/iyGbtpBjMiRbswKBgQC1GgWxqF8LXTI5FSj1LB4yUUnlELB0sYRt
52p3FCxqfwyMQuNs0EBqK/IEzug+ulyCS5AE+0Igll3pQOX94jzev0SKULkyqdEJ
HP3JduOU19/EZA2bP0ff45m26h8wguJN7VoC7rwKEnM2QBPGAfugINbUzcGAMQyD
sAk6h4tawQKBgGOWZYl64x2orVR4RZ4f00oh86eFYVDcMLIw1+7lI6RoFzympULj
oLBTraFD3VdHKnY/MfjrCdDn5ADD2cIuI/luFcvAH/HmtuE8yRuNOMRaTRPy3C5K
O3luushVzyDUuOZvvPtiBkFvl92pzLPJxxDYMc7zZ9hQqnGcdp41Fil9AoGACxsc
bEeqBHVjphKBH3/kHivT/0MlvxI/z8mYQtMu4h0GdPeJINwohxpIzjiuD2K4V5kw
rM2HwZ3XBn3fXNFp8DMEjgLjSJMXaZqoiZlL3Y3bgByupO2dh8JaY9g5r2znWeYL
VhCz4V4+SH5neAYZGznIUuaHTkgzv0OlXTyAtEECgYBu9QCPT05aB5JiYuDih2U7
KRzRCEEFn6Ks8OCTeQYt1VSusRf+ZWqyK2Wygx9hpMxiADrgHXWUQZb7+giS4C10
pIQ8Xhyw2BrVvzhDuDGkLuOsJmvYbkB1w+8SihlkHnBMJSmgVMVYJL1Fo31Xp6rF
6KG1AOItgKJGFxFePSmPYw==
-----END PRIVATE KEY-----
"""

_issuance_time = datetime.fromtimestamp(1720051200, tz=UTC)

_common_result_jwt_fields = {
    "exp": datetime.now(UTC).timestamp() + 110,
    "iat": datetime.now(UTC).timestamp() - 10,
    "iss": "irmaserver",
    "sub": "disclosing_result",
    "token": "559RWzTITedKce9uxIJw",
    "status": "DONE",
    "type": "disclosing",
    "proofStatus": "VALID",
}


class TestCreateExchange:
    def test_create_exchange(self):
        _storage._exchanges.clear()

        response = client.post(
            "/exchanges/create/",
            json={
                "attributes": [
                    [["irma-demo.sidn-pbdf.email.email"]],
                    [
                        ["pbdf.gemeente.personalData.fullname"],
                        [
                            "pbdf.gemeente.personalData.initials",
                            "pbdf.gemeente.personalData.surname",
                        ],
                    ],
                ],
                "public_initiator_attributes": [["irma-demo.sidn-pbdf.mobilenumber.mobilenumber"]],
            },
        )

        assert response.status_code == 200
        response_data = response.json()

        # Check the response content.
        disclosure_request = DisclosureRequestJWT.model_validate(
            jwt.decode(
                response_data["request_jwt"],
                key=settings.irma.session_request_secret_key.get_secret_value(),
                issuer=settings.irma.session_request_issuer_id,
                algorithms=["HS256"],
            )
        )
        assert disclosure_request.sprequest.request.disclose == [
            [["irma-demo.sidn-pbdf.mobilenumber.mobilenumber"]],
            [["irma-demo.sidn-pbdf.email.email"]],
            [
                ["pbdf.gemeente.personalData.fullname"],
                [
                    "pbdf.gemeente.personalData.initials",
                    "pbdf.gemeente.personalData.surname",
                ],
            ],
        ]
        assert disclosure_request.sprequest.request.client_return_url == (
            f"{settings.base_url}exchanges/{response_data['id']}/"
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
            ["irma-demo.sidn-pbdf.mobilenumber.mobilenumber"]
        ]
        assert exchange.attributes == [
            [["irma-demo.sidn-pbdf.email.email"]],
            [
                ["pbdf.gemeente.personalData.fullname"],
                [
                    "pbdf.gemeente.personalData.initials",
                    "pbdf.gemeente.personalData.surname",
                ],
            ],
        ]

    # TODO: test validation on the selection of attributes.


class TestStartExchange:
    exchange = Exchange(
        initiator_secret="a" * 32,
        attributes=[[["irma-demo.sidn-pbdf.email.email"]]],
        public_initiator_attributes=[["irma-demo.sidn-pbdf.mobilenumber.mobilenumber"]],
    )

    phonenumber = DisclosedAttribute(
        rawvalue="31612345678",
        value={"": "31612345678", "en": "31612345678", "nl": "31612345678"},
        id="irma-demo.sidn-pbdf.mobilenumber.mobilenumber",
        status=AttributeProofStatus.PRESENT,
        issuancetime=_issuance_time,
    )

    email = DisclosedAttribute(
        rawvalue="foo@example.com",
        value={"": "foo@example.com", "en": "foo@example.com", "nl": "foo@example.com"},
        id="irma-demo.sidn-pbdf.email.email",
        status=AttributeProofStatus.PRESENT,
        issuancetime=_issuance_time,
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
        _storage._exchanges = {self.exchange.id: exchange.model_dump_json()}

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

    def test_incorrect_attributes(self):
        _storage._exchanges = {self.exchange.id: self.exchange.model_dump_json()}

        # Real disclosure result JWT but without email attribute.
        disclosure_result = jwt.encode(
            {
                "exp": datetime.now(UTC).timestamp() + 60,
                "iat": datetime.now(UTC).timestamp() - 60,
                "iss": "irmaserver",
                "sub": "disclosing_result",
                "token": "559RWzTITedKce9uxIJw",
                "status": "DONE",
                "type": "disclosing",
                "proofStatus": "VALID",
                "disclosed": [
                    [self.phonenumber.model_dump(mode="json")],
                ],
            },
            key=_irmaserver_jwt_private_key,
            algorithm="RS256",
        )

        response = client.post(
            f"/exchanges/{self.exchange.id}/start/",
            json={
                "initiator_secret": self.exchange.initiator_secret,
                "disclosure_result": disclosure_result,
            },
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid session result"}

    def test_invalid_timestamp(self):
        _storage._exchanges = {self.exchange.id: self.exchange.model_dump_json()}

        disclosure_result = jwt.encode(
            {
                **_common_result_jwt_fields,
                "exp": int(datetime.now(UTC).timestamp() - 60),
                "iat": int(datetime.now(UTC).timestamp() - 180),
                "disclosed": [
                    [self.phonenumber.model_dump(mode="json")],
                    [self.email.model_dump(mode="json")],
                ],
            },
            key=_irmaserver_jwt_private_key,
            algorithm="RS256",
        )

        response = client.post(
            f"/exchanges/{self.exchange.id}/start/",
            json={
                "initiator_secret": self.exchange.initiator_secret,
                "disclosure_result": disclosure_result,
            },
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid JWT"}

    def test_successful_start(self):
        _storage._exchanges = {self.exchange.id: self.exchange.model_dump_json()}

        disclosure_result = jwt.encode(
            {
                **_common_result_jwt_fields,
                "disclosed": [
                    [self.phonenumber.model_dump(mode="json")],
                    [self.email.model_dump(mode="json")],
                ],
            },
            key=_irmaserver_jwt_private_key,
            algorithm="RS256",
        )

        response = client.post(
            f"/exchanges/{self.exchange.id}/start/",
            json={
                "initiator_secret": self.exchange.initiator_secret,
                "disclosure_result": disclosure_result,
            },
        )

        assert response.status_code == 204
        assert response.content == b""

        exchange = Exchange.model_validate_json(_storage._exchanges[self.exchange.id])
        assert exchange.public_initiator_attribute_values == [self.phonenumber]
        assert exchange.initiator_attribute_values == [[self.email]]


class TestGetExchangeInfo:
    exchange = Exchange(
        attributes=[[["irma-demo.sidn-pbdf.email.email"]]],
        public_initiator_attributes=[["irma-demo.sidn-pbdf.mobilenumber.mobilenumber"]],
    )

    def test_exchange_not_found(self):
        _storage._exchanges = {self.exchange.id: self.exchange.model_dump_json()}

        response = client.get("/exchanges/0000000000000000/")
        assert response.status_code == 404

    def test_exchange_not_started(self):
        _storage._exchanges = {self.exchange.id: self.exchange.model_dump_json()}

        response = client.get(f"/exchanges/{self.exchange.id}/")
        assert response.status_code == 404

    def test_successful(self):
        exchange = self.exchange.model_copy()
        exchange.public_initiator_attribute_values = [
            DisclosedAttribute(
                rawvalue="31612345678",
                value={"": "31612345678", "en": "31612345678", "nl": "31612345678"},
                id="irma-demo.sidn-pbdf.mobilenumber.mobilenumber",
                status=AttributeProofStatus.PRESENT,
                issuancetime=_issuance_time,
            )
        ]
        exchange.initiator_attribute_values = [
            [
                DisclosedAttribute(
                    rawvalue="foo@example.com",
                    value={
                        "": "foo@example.com",
                        "en": "foo@example.com",
                        "nl": "foo@example.com",
                    },
                    id="irma-demo.sidn-pbdf.email.email",
                    status=AttributeProofStatus.PRESENT,
                    issuancetime=_issuance_time,
                )
            ]
        ]

        _storage._exchanges = {self.exchange.id: exchange.model_dump_json()}

        response = client.get(f"/exchanges/{self.exchange.id}/")

        assert response.status_code == 200
        response_data = response.json()

        # Check the response content.
        disclosure_request = DisclosureRequestJWT.model_validate(
            jwt.decode(
                response_data["request_jwt"],
                key=settings.irma.session_request_secret_key.get_secret_value(),
                issuer=settings.irma.session_request_issuer_id,
                algorithms=["HS256"],
            )
        )
        assert disclosure_request.sprequest.request.disclose == [
            [["irma-demo.sidn-pbdf.email.email"]]
        ]
        assert disclosure_request.sprequest.request.client_return_url == (
            f"{settings.base_url}exchanges/{exchange.id}/"
        )
        assert disclosure_request.sprequest.request.augment_return_url is True
        assert disclosure_request.sprequest.request.labels is None

        assert response_data["attributes"] == disclosure_request.sprequest.request.disclose

        assert response_data["public_initiator_attribute_values"] == [
            {
                "rawvalue": "31612345678",
                "value": {"": "31612345678", "en": "31612345678", "nl": "31612345678"},
                "id": "irma-demo.sidn-pbdf.mobilenumber.mobilenumber",
                "status": "PRESENT",
                "issuancetime": _issuance_time.timestamp(),
            }
        ]

    def test_already_responded(self):
        pass  # TODO: expected result depends on whether multiple responses are allowed.


class TestRespond:
    exchange = Exchange(
        attributes=[[["irma-demo.sidn-pbdf.email.email"]]],
        public_initiator_attributes=[["irma-demo.sidn-pbdf.mobilenumber.mobilenumber"]],
    )

    phonenumber = DisclosedAttribute(
        rawvalue="31612345678",
        value={"": "31612345678", "en": "31612345678", "nl": "31612345678"},
        id="irma-demo.sidn-pbdf.mobilenumber.mobilenumber",
        status=AttributeProofStatus.PRESENT,
        issuancetime=_issuance_time,
    )

    email = DisclosedAttribute(
        rawvalue="foo@example.com",
        value={"": "foo@example.com", "en": "foo@example.com", "nl": "foo@example.com"},
        id="irma-demo.sidn-pbdf.email.email",
        status=AttributeProofStatus.PRESENT,
        issuancetime=_issuance_time,
    )

    def test_exchange_not_found(self):
        _storage._exchanges = {self.exchange.id: self.exchange.model_dump_json()}

        response = client.post("/exchanges/0000000000000000/respond/")
        assert response.status_code == 404
        assert response.json() == {"detail": "Exchange not found"}

    def test_exchange_not_started(self):
        _storage._exchanges = {self.exchange.id: self.exchange.model_dump_json()}

        response = client.post(
            f"/exchanges/{self.exchange.id}/respond/",
            json={"disclosure_result": "dummy"},
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Exchange not found"}

    def test_incorrect_attributes(self):
        exchange = self.exchange.model_copy()
        exchange.public_initiator_attribute_values = [self.phonenumber]
        exchange.initiator_attribute_values = [[self.email]]
        _storage._exchanges = {self.exchange.id: exchange.model_dump_json()}

        result = jwt.encode(
            {
                **_common_result_jwt_fields,
                "disclosed": [
                    [self.phonenumber.model_dump(mode="json")],
                ],
            },
            key=_irmaserver_jwt_private_key,
            algorithm="RS256",
        )

        response = client.post(
            f"/exchanges/{self.exchange.id}/respond/",
            json={"disclosure_result": result},
        )

        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid session result"}

    def test_successful(self):
        exchange = self.exchange.model_copy()
        exchange.public_initiator_attribute_values = [self.phonenumber]
        exchange.initiator_attribute_values = [[self.email]]
        _storage._exchanges = {self.exchange.id: exchange.model_dump_json()}

        result = jwt.encode(
            {
                **_common_result_jwt_fields,
                "disclosed": [
                    [self.email.model_dump(mode="json")],
                ],
            },
            key=_irmaserver_jwt_private_key,
            algorithm="RS256",
        )

        response = client.post(
            f"/exchanges/{self.exchange.id}/respond/",
            json={"disclosure_result": result},
        )

        assert response.status_code == 200
        assert response.json()["public_initiator_attribute_values"] == [
            self.phonenumber.model_dump()
        ]
        assert response.json()["initiator_attribute_values"] == [[self.email.model_dump()]]
        assert response.json()["response_attribute_values"] == [[self.email.model_dump()]]

        assert len(_storage._exchange_replies[exchange.id]) == 1
        saved_reply = ExchangeReply.model_validate_json(_storage._exchange_replies[exchange.id][0])

        assert response.json()["recipient_secret"] == saved_reply.recipient_secret

    def test_already_responded(self):
        pass  # TODO: expected result depends on whether multiple responses are allowed.


class TestGetExchangeResult:
    phonenumber = DisclosedAttribute(
        rawvalue="31612345678",
        value={"": "31612345678", "en": "31612345678", "nl": "31612345678"},
        id="irma-demo.sidn-pbdf.mobilenumber.mobilenumber",
        status=AttributeProofStatus.PRESENT,
        issuancetime=_issuance_time,
    )

    email1 = DisclosedAttribute(
        rawvalue="foo@example.com",
        value={"": "foo@example.com", "en": "foo@example.com", "nl": "foo@example.com"},
        id="irma-demo.sidn-pbdf.email.email",
        status=AttributeProofStatus.PRESENT,
        issuancetime=_issuance_time,
    )

    email2 = DisclosedAttribute(
        rawvalue="bar@example.com",
        value={"": "bar@example.com", "en": "bar@example.com", "nl": "bar@example.com"},
        id="irma-demo.sidn-pbdf.email.email",
        status=AttributeProofStatus.PRESENT,
        issuancetime=_issuance_time,
    )

    exchange = Exchange(
        attributes=[[["irma-demo.sidn-pbdf.email.email"]]],
        public_initiator_attributes=[["irma-demo.sidn-pbdf.mobilenumber.mobilenumber"]],
        initiator_attribute_values=[[email1]],
        public_initiator_attribute_values=[phonenumber],
    )

    reply = ExchangeReply(
        exchange_id=exchange.id,
        attribute_values=[[email2]],
    )

    def test_no_replies(self):
        _storage._exchanges = {self.exchange.id: self.exchange.model_dump_json()}

        response = client.get(
            f"/exchanges/{self.exchange.id}/result/",
            params={"secret": self.exchange.initiator_secret},
        )

        assert response.status_code == 200
        assert response.json()["replies"] == []

    def test_successful(self):
        _storage._exchanges = {self.exchange.id: self.exchange.model_dump_json()}
        _storage._exchange_replies[self.exchange.id] = [self.reply.model_dump_json()]

        response = client.get(
            f"/exchanges/{self.exchange.id}/result/",
            params={"secret": self.exchange.initiator_secret},
        )

        assert response.status_code == 200
        assert response.json()["public_initiator_attribute_values"] == [
            self.phonenumber.model_dump()
        ]
        assert response.json()["initiator_attribute_values"] == [[self.email1.model_dump()]]
        assert response.json()["replies"] == [[[self.email2.model_dump()]]]

    def test_invalid_secret(self):
        _storage._exchanges = {self.exchange.id: self.exchange.model_dump_json()}
        _storage._exchange_replies[self.exchange.id] = [self.reply.model_dump_json()]

        response = client.get(
            f"/exchanges/{self.exchange.id}/result/",
            params={"secret": "b" * 32},
        )

        assert response.status_code == 404
        assert response.json() == {"detail": "Exchange not found"}

    def test_using_recipient_secret(self):
        # TODO: This is the many-to-many case. In other scenarios, any other recipient's replies
        # should be filtered out.
        reply2 = ExchangeReply(
            exchange_id=self.exchange.id,
            attribute_values=[
                [
                    DisclosedAttribute(
                        rawvalue="baz@example.com",
                        value={
                            "": "baz@example.com",
                            "en": "baz@example.com",
                            "nl": "baz@example.com",
                        },
                        id="irma-demo.sidn-pbdf.email.email",
                        status=AttributeProofStatus.PRESENT,
                        issuancetime=_issuance_time,
                    )
                ]
            ],
        )

        _storage._exchanges = {self.exchange.id: self.exchange.model_dump_json()}
        _storage._exchange_replies[self.exchange.id] = [
            self.reply.model_dump_json(),
            reply2.model_dump_json(),
        ]

        response = client.get(
            f"/exchanges/{self.exchange.id}/result/",
            params={"secret": reply2.recipient_secret},
        )

        assert response.status_code == 200
        assert response.json()["public_initiator_attribute_values"] == [
            self.phonenumber.model_dump()
        ]
        assert response.json()["initiator_attribute_values"] == [[self.email1.model_dump()]]
        assert response.json()["replies"] == [
            [[self.email2.model_dump()]],
            [[reply2.attribute_values[0][0].model_dump()]],
        ]
