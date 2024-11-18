import base64
import logging
from email.message import EmailMessage

from app.config import settings
from app.signatures.models import SignatureRequest
from app.utils import send_email
from app.yivi.models import SignatureSessionResultJWT

logger = logging.getLogger(__name__)


async def send_initiator_signature_result_email(
    signature_request: SignatureRequest, result: SignatureSessionResultJWT
):
    message = EmailMessage()
    message["From"] = f"noreply@{settings.email_from_domain}"
    message["To"] = signature_request.initiator_email_value
    message["Subject"] = "Antwoord via DIYivi"

    signature_content = base64.b64encode(
        result.signature.model_dump_json(by_alias=True).encode()
    ).decode()

    signature = f"{settings.client_origin}/signature/verify/#{signature_content}"

    message.set_content(
        f"""Beste gebruiker van DIYivi,

Gefeliciteerd! Iemand heeft gereageerd op je verzoek om een afspraak te ondertekenen.
Hier is het ondertekende bericht. Open de lange link hieronder of kopieer hem en vul hem
in op {settings.client_origin}/signature/verify/ om de handtekening te bekijken.

{signature}

Dit is een automatisch gegenereerd bericht. U kunt hier niet op reageren.
"""
    )

    await send_email(message)
