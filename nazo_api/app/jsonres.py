from typing import Any
from blacksheep import Content, Response

from msgspec import json as m_json

JSON_RESPONSE = b"application/json"

ENCODER = m_json.Encoder()


def json(data: Any, status: int = 200) -> Response:
    """
    Returns a response with application/json content,
    and given status (default HTTP 200 OK).
    """
    return Response(
        status,
        None,
        Content(JSON_RESPONSE, ENCODER.encode(data)),
    )


def pretty_json(
    data: Any,
    status: int = 200,
) -> Response:
    """
    Returns a response with indented application/json content,
    and given status (default HTTP 200 OK).
    """
    return Response(
        status,
        None,
        Content(
            JSON_RESPONSE,
            m_json.format(ENCODER.encode(data)),
        ),
    )
