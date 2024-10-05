import logging
from email.message import EmailMessage

import aiosmtplib

from app.config import settings
from server.app.exchanges.models import Exchange

logger = logging.getLogger(__name__)


async def send_email(message: EmailMessage):
    if settings.smtp is None:
        logger.info("No SMTP server is configured, but an email would have been sent.")
        return

    await aiosmtplib.send(
        message,
        hostname=settings.smtp.hostname,
        username=settings.smtp.username,
        password=settings.smtp.password,
        start_tls=True,
    )


async def send_initiator_result_email(exchange: Exchange):
    message = EmailMessage()
    message["From"] = f"noreply@{settings.email_from_domain}"
    message["To"] = exchange.initiator_email_value
    message["Subject"] = "Antwoord via DIYivi"
    message.set_content("Er heeft iemand gereageerd op je uitnodiging met DIYivi.")

    await send_email(message)
