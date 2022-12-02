<p align="center">
  <img src="./assets/binance4py_logo.png" alt="binance4py logo" width="480">
</p>

<p align="center">
  <a href="https://github.com/ren3104/binance4py/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/ren3104/binance4py"></a>
  <a href="https://pypi.org/project/binance4py"><img src="https://img.shields.io/pypi/v/binance4py?color=blue&logo=pypi&logoColor=FFE873" alt="PyPi package version"></a>
  <a href="https://pypi.org/project/binance4py"><img src="https://img.shields.io/pypi/pyversions/binance4py.svg?logo=python&logoColor=FFE873" alt="Supported python versions"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
</p>

This is an asynchronous Python wrapper for Binance exchange API.

## Features
- Implementation of all general, market, spot and websocket endpoints
- Easy to contribute and use
- Fully typed

## Installation
```bash
pip install -U binance4py
```

## Quick Start
```python
import asyncio
from binance4py import Binance


async def handle_kline(k):
    print(k)


async def main():
    client = Binance("<API_KEY>", "<API_SECRET>")
    async with client:
        print(await client.general.server_time())
        client.ws.kline("btcbusd", "1m", handle_kline)
        await client.ws.start()


asyncio.run(main())
```
