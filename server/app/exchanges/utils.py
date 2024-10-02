from collections import defaultdict
from typing import Iterable

from app.yivi.models import Attribute


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
