from inspect import cleandoc
from aiohttp import ClientResponse


class BinanceApiException(Exception):
    def __init__(
        self,
        response: ClientResponse,
        error_msg: str
    ) -> None:
        super().__init__(
            "\n" + cleandoc(f"""
                {response.method} {response.status} {response.url}
                {error_msg}
            """)
        )
