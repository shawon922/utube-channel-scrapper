"""
    function's params checker.
"""
import logging

from typing import Optional, Union

from utube.utilz.constants import RESOURCE_PARTS_MAPPING

logger = logging.getLogger(__name__)


def enf_comma_separated(
    field: str, value: Optional[Union[str, list, tuple, set]],
):
    """
    Check to see if field's value type belong to correct type.
    If it is, return api need value, otherwise, raise a PyYouTubeException.

    Args:
        field (str):
            Name of the field you want to do check.
        value (str, list, tuple, set, Optional)
            Value for the field.

    Returns:
        Api needed string
    """
    if value is None:
        return None
    try:
        if isinstance(value, str):
            return value
        elif isinstance(value, (list, tuple, set)):
            if isinstance(value, set):
                logging.warning(f"Note: The order of the set is unreliable.")
            return ",".join(value)
        else:
            raise Exception("Parameter ({field}) must be single str,comma-separated str,list,tuple or set")
    except (TypeError, ValueError):
        raise Exception("Parameter ({field}) must be single str,comma-separated str,list,tuple or set")


def enf_parts(resource: str, value: Optional[Union[str, list, tuple, set]]):
    """
    Check to see if value type belong to correct type, and if resource support the given part.
    If it is, return api need value, otherwise, raise a PyYouTubeException.

    Args:
        resource (str):
            Name of the resource you want to retrieve.
        value (str, list, tuple, set, Optional)
            Value for the part.

    Returns:
        Api needed part string
    """
    if value is None:
        parts = RESOURCE_PARTS_MAPPING[resource]
    elif isinstance(value, str):
        parts = set(value.split(","))
    elif isinstance(value, (list, tuple, set)):
        parts = set(value)
    else:
        raise Exception("Parameter (parts) must be single str,comma-separated str,list,tuple or set")

    # check parts whether support.
    support_parts = RESOURCE_PARTS_MAPPING[resource]
    if not support_parts.issuperset(parts):
        not_support_parts = ",".join(parts.difference(support_parts))
        raise Exception("Parts {not_support_parts} for resource {resource} not support")
    else:
        return ",".join(parts)
