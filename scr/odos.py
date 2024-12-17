
from .request_gl import Request_main
from scr.helper import WALLET_PROXIES, decimalToInt
from user_data.settings import USE_PROXY

from loguru import logger

class Odos(Request_main):
    def __init__(self, file_name: str):
        super().__init__(file_name)

    async def run_module(self, key):
        await super().run_module(key)
        try:
            proxy = None
            if USE_PROXY:
                proxy = WALLET_PROXIES[key]
            lowercased = key.lower()
            url = f'https://api.odos.xyz/loyalty/users/{lowercased}/balances'
            headers = {
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9,uk;q=0.8',
                'cache-control': 'no-cache',
                'origin': 'https://app.odos.xyz',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://app.odos.xyz/',
                'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
            }
            status, result = await self.global_request(url=url, headers=headers, proxy=proxy)
            if result['data']['pendingTokenBalance'] != None:
                val = int(result['data']['pendingTokenBalance'])
                if val > 0:
                    val = decimalToInt(val, 18)
                    k = f'{key}'
                    logger.success(f'{k} amount:{val}')
                    self.success_array[k] = val
                else:
                    logger.warning(f'Skip {key} not elligable')
        
        except Exception as e:
            logger.error(e)