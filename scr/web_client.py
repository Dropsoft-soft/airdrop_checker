import asyncio
import random
import time
from eth_utils import keccak
from eth_abi import encode
from scr.helper import WALLET_PROXIES
from scr.data import DATA
from user_data.settings import USE_PROXY
from loguru import logger
from web3 import Web3, AsyncHTTPProvider
from web3.eth import AsyncEth
from eth_account.messages import encode_defunct

class WebClient():
    def __init__(self, id:int, key: str, chain: str):
        self.proxy = None
        self.id = id
        self.key = key
        self.chain = chain
        self.web3 = self._initialize_web3()
        self.address = self._get_account_address()
        self.chain_id = self._get_chain_id()

    def _initialize_web3(self) -> Web3:
        rpc = DATA[self.chain]['rpc']
        web3 = Web3(AsyncHTTPProvider(rpc), modules={"eth": (AsyncEth)}, middlewares=[])

        if (USE_PROXY and WALLET_PROXIES):
            try:
                self.proxy = WALLET_PROXIES[self.key]
                web3 = Web3(AsyncHTTPProvider(rpc, request_kwargs={"proxy": self.proxy}), modules={"eth": (AsyncEth)}, middlewares=[])
            except Exception as error:
                logger.error(f'{error}. Use web3 without proxy')
        return web3

    def _get_account_address(self) -> str:
        return self.web3.eth.account.from_key(self.key).address

    def _get_chain_id(self) -> int:
        return DATA[self.chain]['chain_id']

    async def sign_message(self, message_text: str) -> str:
        message = encode_defunct(text=message_text)
        signed_message = self.web3.to_hex(
            self.web3.eth.account.sign_message(message, private_key=self.key).signature)
        return signed_message