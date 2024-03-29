from typing import Any
from blacksheep import Content, Response
from orjson import dumps,OPT_INDENT_2

JSON_RESPONSE = b"application/json"
def json(data: Any, status: int = 200) -> Response:
    """
    Returns a response with application/json content,
    and given status (default HTTP 200 OK).
    """
    return Response(
        status,
        None,
        Content(
            JSON_RESPONSE,
            dumps(data)
        ),
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
            dumps(data,option=OPT_INDENT_2)
        ),
    )
