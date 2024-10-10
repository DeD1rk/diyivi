import logging
from email.message import EmailMessage

import aiosmtplib

from app.config import settings
from app.exchanges.models import Exchange, ExchangeReply

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


async def send_initiator_result_email(exchange: Exchange, reply: ExchangeReply):
    message = EmailMessage()
    message["From"] = f"noreply@{settings.email_from_domain}"
    message["To"] = exchange.initiator_email_value
    message["Subject"] = "Antwoord via DIYivi"

    values = {dv.id: dv.value for dv in reply.attribute_values}
    attributes = set(values.keys())

    attributes_display = "\n".join(
        f"- {option['label']}: {option['display'](values)}"  # type: ignore
        for option in ATTRIBUTE_DISPLAY_OPTIONS
        if option["required_attributes"].issubset(attributes)  # type: ignore
    )

    message.set_content(
        f"""Beste gebruiker van DIYivi,

Gefeliciteerd! Iemand heeft gereageerd op je verzoek om gegevens uit te wisselen.
Dit zijn de gegevens die je hebt ontvangen:

{attributes_display}

Al deze gegevens worden vanzelf binnen 48 uur van DIYivi verwijderd.
Dit is een automatisch gegenereerd bericht. U kunt hier niet op reageren.
"""
    )

    await send_email(message)


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
