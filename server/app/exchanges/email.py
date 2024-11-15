import logging
from email.message import EmailMessage

from app.config import settings
from app.exchanges.models import Exchange, ExchangeReply
from app.utils import ATTRIBUTE_DISPLAY_OPTIONS, send_email

logger = logging.getLogger(__name__)


async def send_initiator_exchange_result_email(exchange: Exchange, reply: ExchangeReply):
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
