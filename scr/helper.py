
with open("user_data/addresses.txt", "r") as f:
    WALLETS = [row.strip() for row in f]

with open("user_data/proxies.txt", "r") as f:
    PROXIES = [row.strip() for row in f]

def decimalToInt(qty, decimal):
    return qty/ int("".join((["1"]+ ["0"]*decimal)))

def get_wallet_proxies(wallets, proxies):
    try:
        result = {}
        for i in range(len(wallets)):
            result[wallets[i]] = proxies[i % len(proxies)]
        return result
    except: None

WALLET_PROXIES  = get_wallet_proxies(WALLETS, PROXIES)