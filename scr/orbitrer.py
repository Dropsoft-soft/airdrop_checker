
from .request_gl import Request_main
from scr.helper import WALLET_PROXIES, decimalToInt
from user_data.settings import USE_PROXY, SLEEP_TIME
from scr.web_client import WebClient
from loguru import logger
import asyncio,random

class Orbitrer(Request_main):
    def __init__(self, file_name: str):
        super().__init__(file_name=file_name, use_addresses=False)

    async def run_module(self, key):
        await super().run_module(key)
        web3 = WebClient(id=0, key=key, chain='linea')
        message_signed = await web3.sign_message(message_text='Orbiter Airdrop')
        try:
            proxy = None
            if USE_PROXY:
                proxy = WALLET_PROXIES[key]
            url = f'https://airdrop-api.orbiter.finance/airdrop/snapshot'
            headers = {
                'token': message_signed,
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
            }
            status, result = await self.global_request(method='post', url=url, headers=headers, proxy=proxy)
            if 'result' in result and result['result'] != None:
                val = float(result['result']['amount'])
                if val > 0:
                    k = f'{web3.address}'
                    logger.success(f'{k} amount:{val}')
                    self.success_array[k] = val
                else:
                    logger.warning(f'Skip {web3.address} amount {val}')
            else:
                logger.warning(f'Wallet {web3.address} not elligable')
            random_number = random.randint(SLEEP_TIME[0], SLEEP_TIME[1])
            await asyncio.sleep(random_number)
            
        except Exception as e:
            logger.error(e)