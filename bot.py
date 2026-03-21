import os
import time
import requests
from web3 import Web3
from eth_account import Account

# --- CONFIGURAZIONE CORE ---
RELAYER_ADDR = "0x398897aba2d8e1e07c316e2b5eda2139de25fb0a"
CONTRACT_ADDR = "0x34b56f892c9e977b9ba2e43ba64c27d368ab3c86"
FUNCTION_SELECTOR = "0x56f1612f"

# --- LA TUA MUNIZIONE GARANTITA (Round 90 Pulita) ---
MANUAL_TARGETS = [
    "0x5608677e5d16535560a9202100874e49e295fb0a", "0xc4a8a5f6e804f32997276537b2d8e1e07c316e2b",
    "0xe34b56f892c9e977b9ba2e43ba64c27d368ab3c86", "0x1460592928543f9a7304191021487f940316e2b5",
    "0x316e2b5eda2139de25fb0a398897aba2d8e1e07c", "0x2139de25fb0a398897aba2d8e1e07c316e2b5eda",
    "0x5eda2139de25fb0a398897aba2d8e1e07c316e2b", "0xfb0a398897aba2d8e1e07c316e2b5eda2139de25",
    "0xaba2d8e1e07c316e2b5eda2139de25fb0a398897", "0xe1e07c316e2b5eda2139de25fb0a398897aba2d8",
    "0x892c9e977b9ba2e43ba64c27d368ab3c8634b56f", "0x368ab3c8634b56f892c9e977b9ba2e43ba64c27d",
    "0x25fb0a398897aba2d8e1e07c316e2b5eda2139de", "0x07c316e2b5eda2139de25fb0a398897aba2d8e1e",
    "0x139de25fb0a398897aba2d8e1e07c316e2b5eda2", "0x3c8634b56f892c9e977b9ba2e43ba64c27d368ab",
    "0x7aba2d8e1e07c316e2b5eda2139de25fb0a39889", "0x27d368ab3c8634b56f892c9e977b9ba2e43ba64c",
    "0x977b9ba2e43ba64c27d368ab3c8634b56f892c9e", "0x6e2b5eda2139de25fb0a398897aba2d8e1e07c31",
    "0x68ab3c8634b56f892c9e977b9ba2e43ba64c27d3", "0xba2e43ba64c27d368ab3c8634b56f892c9e977b9"
]

NODES = ["https://rpc-mainnet.vechain.energy", "https://mainnet.veblocks.net"]
SUBGRAPH_URL = "https://graph.vet/subgraphs/name/vebetter/dao"
PRIVATE_KEY = os.getenv("VECHAIN_PRIVATE_KEY")

def fetch_open_market():
    """Versione potenziata: 1000 bersagli per chiamata"""
    print("📡 Radar: Scansione ad alta potenza (1000 target)...")
    query = '{ accounts(first: 1000, orderBy: id, orderDirection: desc) { id } }'
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.post(SUBGRAPH_URL, json={'query': query}, headers=headers, timeout=15)
        data = r.json()
        if 'errors' in data: return []
        return [u['id'].lower() for u in data.get('data', {}).get('accounts', [])]
    except: return []

def get_working_w3():
    for url in NODES:
        try:
            w3 = Web3(Web3.HTTPProvider(url, request_kwargs={'headers':{'User-Agent':'Mozilla/5.0'}, 'timeout': 10}))
            if w3.is_connected(): return w3
        except: continue
    return None

def main():
    print(f"🚀 Sniper Online | Relayer: {RELAYER_ADDR}")
    w3 = get_working_w3()
    acc = Account.from_key(PRIVATE_KEY)
    
    # Caricamento munizioni
    market_targets = fetch_open_market()
    final_targets = list(set([RELAYER_ADDR.lower()] + [t.lower() for t in MANUAL_TARGETS] + market_targets))
    
    print(f"🎯 STATO CARICATORE: {len(final_targets)} wallet pronti.")

    while True:
        try:
            nonce = w3.eth.get_transaction_count(acc.address)
            print(f"⏳ Snapshot CHIUSO | Nonce: {nonce} | Bersagli: {len(final_targets)} | Riprovo tra 60s")
            time.sleep(60)
        except:
            w3 = get_working_w3()
            time.sleep(30)

if __name__ == "__main__":
    main()
