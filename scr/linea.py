
from .request_gl import Request_main
from scr.helper import WALLET_PROXIES, decimalToInt
from user_data.settings import USE_PROXY, SLEEP_TIME
from scr.web_client import WebClient
from loguru import logger
import asyncio,random
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   

user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

class Linea(Request_main):
    def __init__(self, file_name: str):
        super().__init__(file_name=file_name)

    async def run_module(self, key):
        await super().run_module(key)
        try:
            proxy = None
            if USE_PROXY:
                proxy = WALLET_PROXIES[key]
            url = f'https://linea-xp-poh-api.linea.build/poh/{key}'
            headers = {
                'accept': 'application/json',
                'accept-language': 'en-US,en;q=0.9,uk;q=0.8',
                'cache-control': 'no-cache',
                'origin': 'https://poh.linea.build',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://poh.linea.build/',
                'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': user_agent_rotator.get_random_user_agent(),
            }
            status, result = await self.global_request(method='get', url=url, headers=headers, proxy=proxy)
            if 'poh' in result:
                val = result['poh']
                if val == True:
                    k = f'{key}'
                    logger.success(f'{k} poh: {val}')
                    self.success_array[k] = val
                else:
                    logger.warning(f'Skip {key} poh {val}')
            else:
                logger.warning(f'Wallet {key} not elligable')
            random_number = random.randint(SLEEP_TIME[0], SLEEP_TIME[1])
            await asyncio.sleep(random_number)
            
        except Exception as e:
            logger.error(e)