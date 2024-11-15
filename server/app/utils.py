import logging
from collections import defaultdict
from collections.abc import Iterable
from email.message import EmailMessage

import aiosmtplib

from app.config import settings
from app.yivi.models import Attribute

logger = logging.getLogger(__name__)


async def send_email(message: EmailMessage):
    if settings.smtp is None:
        logger.warning("No SMTP server is configured, but an email would have been sent.")
        return

    await aiosmtplib.send(
        message,
        hostname=settings.smtp.hostname,
        username=settings.smtp.username,
        password=settings.smtp.password,
        start_tls=True,
    )


def create_condiscon(
    attributes: Iterable[Attribute],
) -> list[list[list[Attribute]]]:
    """Create a ConDisCon where attributes are grouped into conjunctions by their credential.

    This prevents issues with the requirement that each inner conjunction can consist of
    attributes of at most one non-singleton credential, while still guaranteeing that all
    the disclosed values of all attributes of a credential come from the same single instance
    of that credential.
    """
    credentials: defaultdict[str, set[Attribute]] = defaultdict(set)
    for attribute in attributes:
        credential = attribute[: attribute.rfind(".")]
        credentials[credential].add(attribute)

    condiscon: list[list[list[Attribute]]] = []
    for key in credentials:
        condiscon.append([list(credentials[key])])

    return condiscon


ATTRIBUTE_DISPLAY_OPTIONS = [
    {
        "label": "Volledige naam",
        "required_attributes": {"pbdf.gemeente.personalData.fullname"},
        "display": lambda values: values["pbdf.gemeente.personalData.fullname"].nl,
    },
    {
        "label": "E-mailadres",
        "required_attributes": {"pbdf.sidn-pbdf.email.email"},
        "display": lambda values: values["pbdf.sidn-pbdf.email.email"].nl,
    },
    {
        "label": "Mobiel telefoonnummer",
        "required_attributes": {"pbdf.sidn-pbdf.mobilenumber.mobilenumber"},
        "display": lambda values: values["pbdf.sidn-pbdf.mobilenumber.mobilenumber"].nl,
    },
    {
        "label": "Geboortedatum",
        "required_attributes": {"pbdf.gemeente.personalData.dateofbirth"},
        "display": lambda values: values["pbdf.gemeente.personalData.dateofbirth"].nl,
    },
    {
        "label": "Woonadres",
        "required_attributes": {
            "pbdf.gemeente.address.street",
            "pbdf.gemeente.address.houseNumber",
            "pbdf.gemeente.address.zipcode",
            "pbdf.gemeente.address.city",
        },
        "display": lambda values: "{address} {house_number}, {zipcode} {city}".format(
            address=values["pbdf.gemeente.address.street"].nl,
            house_number=values["pbdf.gemeente.address.houseNumber"].nl,
            zipcode=values["pbdf.gemeente.address.zipcode"].nl,
            city=values["pbdf.gemeente.address.city"].nl,
        ),
    },
]
