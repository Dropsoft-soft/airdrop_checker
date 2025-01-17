from scr.odos import Odos
from scr.opzora import OpZora
import asyncio
from loguru import logger
from concurrent.futures import ThreadPoolExecutor
import sys
import questionary
from questionary import Choice

from scr.orbitrer import Orbitrer

'''Settings use or not use proxies and filename'''
def get_module():
    result = questionary.select(
        "\nSubscribe – https://t.me/web3sftwr\n\n\nSelect a method to get started",
        choices=[
            Choice("1) Check zora airdrop", OpZora('op-zora.xlsx')),
            Choice("2) Check Odos airdrop", Odos('odos.xlsx')),
            Choice("3) Check Orbitrer airdrop", Orbitrer('orbitrer.xlsx')),

            Choice("99) Exit", "exit"),
        ],
        qmark="⚙️ ",
        pointer="✅ "
    ).ask()
    if result == "exit":
        print("\nSubscribe – https://t.me/web3sftwr\n")
        sys.exit()
    return result

if __name__ == "__main__":
    checker = get_module()
    if sys.platform == 'win32':
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    wallets = checker.get_wallets()

    with ThreadPoolExecutor(max_workers=5) as executor:
        for _, account in enumerate(wallets, start=1):
            executor.submit(
                checker._async_run_module,
                account.get("key")
            )

    logger.info(f'{len(checker.success_array)} saving...')
    for i in checker.success_array.keys():
        checker.add_data(f'{i}', f'{checker.success_array[i]}')    
    logger.info(f'Finished')
        

