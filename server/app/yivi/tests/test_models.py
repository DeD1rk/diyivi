from datetime import UTC, datetime

from app.yivi.models import (
    Attribute,
    AttributeProofStatus,
    AttributeValue,
    DisclosedAttribute,
    DisclosureSessionResultJWT,
    ProofStatus,
    SessionStatus,
)

_issuance_time = datetime.fromtimestamp(1720051200, tz=UTC)


def test_disclosed_attributes_satisfies():
    disclosed_housenumber = DisclosedAttribute.model_validate_json(
        """
        {
            "rawvalue": "123",
            "value": {
                "": "123",
                "en": "123",
                "nl": "123"
            },
            "id": "pbdf.gemeente.address.houseNumber",
            "status": "PRESENT",
            "issuancetime": 1720051200
        }
        """
    )
    assert disclosed_housenumber.satisfies("pbdf.gemeente.address.houseNumber")
    assert not disclosed_housenumber.satisfies("pbdf.gemeente.address.street")

    assert disclosed_housenumber.satisfies(
        AttributeValue(type="pbdf.gemeente.address.houseNumber", value="123")
    )
    assert not disclosed_housenumber.satisfies(
        AttributeValue(type="pbdf.gemeente.address.houseNumber", value="456")
    )
    assert not disclosed_housenumber.satisfies(
        AttributeValue(type="pbdf.gemeente.address.street", value="123")
    )

    assert disclosed_housenumber.satisfies(
        AttributeValue(type="pbdf.gemeente.address.houseNumber", notNull=True)
    )
    assert not disclosed_housenumber.satisfies(
        AttributeValue(type="pbdf.gemeente.address.houseNumber", notNull=False)
    )


def test_disclosure_result_satisfies():
    condiscon: list[list[list[Attribute | AttributeValue]]] = [
        [["pbdf.gemeente.address.houseNumber", "pbdf.gemeente.address.street"]],
        [
            [AttributeValue(type="pbdf.gemeente.address.city", value="Nijmegen")],
            [AttributeValue(type="other.issuer.address.city", value="Nijmegen")],
        ],
        [
            [
                AttributeValue(
                    type="pbdf.gemeente.personalData.firstnames",
                    value="Foo Bar",
                ),
                "pbdf.gemeente.personalData.familyname",
            ],
            [],
        ],
    ]

    housenumber = DisclosedAttribute(
        rawvalue="1",
        value={"": "1", "en": "1", "nl": "1"},
        id="pbdf.gemeente.address.houseNumber",
        status=AttributeProofStatus.PRESENT,
        issuancetime=_issuance_time,
    )
    street = DisclosedAttribute(
        rawvalue="Foo Avenue",
        value={"": "Foo Avenue", "en": "Foo Avenue", "nl": "Foo Avenue"},
        id="pbdf.gemeente.address.street",
        status=AttributeProofStatus.PRESENT,
        issuancetime=_issuance_time,
    )
    city = DisclosedAttribute(
        rawvalue="Nijmegen",
        value={"": "Nijmegen", "en": "Nijmegen", "nl": "Nijmegen"},
        id="other.issuer.address.city",
        status=AttributeProofStatus.PRESENT,
        issuancetime=_issuance_time,
    )
    firstnames = DisclosedAttribute(
        rawvalue="Foo Bar",
        value={"": "Foo Bar", "en": "Foo Bar", "nl": "Foo Bar"},
        id="pbdf.gemeente.personalData.firstnames",
        status=AttributeProofStatus.PRESENT,
        issuancetime=_issuance_time,
    )
    familyname = DisclosedAttribute(
        rawvalue="Baz",
        value={"": "Baz", "en": "Baz", "nl": "Baz"},
        id="pbdf.gemeente.personalData.familyname",
        status=AttributeProofStatus.PRESENT,
        issuancetime=_issuance_time,
    )

    valid_result_base_fields = {
        "iss": "irmaserver",
        "iat": 1720051200,
        "exp": 1720051320,
        "sub": "disclosing_result",
        "type": "disclosing",
        "status": SessionStatus.DONE,
        "token": "1234567890",
        "proofStatus": ProofStatus.VALID,
    }

    assert DisclosureSessionResultJWT(
        **valid_result_base_fields,
        disclosed=[
            [housenumber, street],
            [city],
            [],
        ],
    ).satisfies_condiscon(condiscon)

    assert not DisclosureSessionResultJWT(
        **valid_result_base_fields,
        disclosed=[
            [housenumber],
            [city],
            [],
        ],
    ).satisfies_condiscon(condiscon), "missing 'street'"

    assert not DisclosureSessionResultJWT(
        **valid_result_base_fields,
        disclosed=[
            [city],
            [housenumber, street],
            [],
        ],
    ).satisfies_condiscon(
        condiscon
    ), "`disclosed` elements must match request's disjunctions"

    assert DisclosureSessionResultJWT(
        **valid_result_base_fields,
        disclosed=[
            [housenumber, street],
            [city],
            [firstnames, familyname],
        ],
    ).satisfies_condiscon(condiscon)

    assert DisclosureSessionResultJWT(
        **valid_result_base_fields,
        disclosed=[
            [street, housenumber],
            [city],
            [familyname, firstnames],
        ],
    ).satisfies_condiscon(condiscon)

    assert not DisclosureSessionResultJWT(
        **valid_result_base_fields,
        disclosed=[
            [street, housenumber],
            [city],
            [familyname, firstnames],
            [familyname, firstnames],
        ],
    ).satisfies_condiscon(
        condiscon
    ), "`disclosed` elements must match request's disjunctions"

    assert not DisclosureSessionResultJWT(
        **valid_result_base_fields,
        disclosed=[
            [street, housenumber, city, familyname, firstnames],
        ],
    ).satisfies_condiscon(
        condiscon
    ), "`disclosed` elements must match request's disjunctions"

    assert not DisclosureSessionResultJWT(
        **{**valid_result_base_fields, "proofStatus": ProofStatus.EXPIRED},
        disclosed=[
            [housenumber, street],
            [city],
            [firstnames],
        ],
    ).satisfies_condiscon(condiscon)
