
from user_data.settings import USE_PROXY
from .request_gl import Request_main
from loguru import logger
from scr.helper import WALLET_PROXIES, decimalToInt

class OpZora(Request_main):
    def __init__(self, file_name: str):
        super().__init__(file_name=file_name)

    async def run_module(self, key):
        await super().run_module(key)
        try:
            proxy = None
            if USE_PROXY:
                proxy = WALLET_PROXIES[key]
            lowercased = key.lower()
            url = f'https://op.zora.co/api/on-allowlist'
            json = {
                "userAddress": lowercased
            }
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
            }
            status, result = await self.global_request(method='post', url=url, headers=headers, json=json, proxy=proxy)
            if 'data' in result:
                val = int(result['data']['amount'])
                if val > 0:
                    val = decimalToInt(val, 18)
                    k = f'{key}'
                    logger.success(f'{k} amount:{val}')
                    self.success_array[k] = val
                else:
                    logger.warning(f'Skip {key} amount {val}')
            else:
                logger.warning(f'Wallet {key} not elligable')
            
        except Exception as e:
            logger.error(e)