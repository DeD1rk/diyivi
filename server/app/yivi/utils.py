from typing import Sequence

from app.yivi.models import Attribute, AttributeValue, DisclosedAttribute


def satisfies_disjunction(
    disjunction: Sequence[Sequence[Attribute | AttributeValue]],
    disclosed: Sequence[DisclosedAttribute],
) -> bool:
    return any(
        satisfies_conjunction(conjunction, disclosed) for conjunction in disjunction
    )


def satisfies_conjunction(
    conjunction: Sequence[Attribute | AttributeValue],
    disclosed: Sequence[DisclosedAttribute],
) -> bool:
    for required_attribute in conjunction:
        if any(attribute.satisfies(required_attribute) for attribute in disclosed):
            continue
        return False
    return True
