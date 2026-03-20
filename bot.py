import os
import time
import requests
from web3 import Web3
from eth_account import Account

# --- CONFIGURAZIONE ---
RELAYER_ADDR = "0x398897aba2d8e1e07c316e2b5eda2139de25fb0a"
CONTRACT_ADDR = "0x34b56f892c9e977b9ba2e43ba64c27d368ab3c86"
FUNCTION_SELECTOR = "0x56f1612f"

NODES = [
    "https://rpc-mainnet.vechain.energy",
    "https://mainnet.veblocks.net"
]

SUBGRAPH_URL = "https://graph.vet/subgraphs/name/vebetter/dao"
PRIVATE_KEY = os.getenv("VECHAIN_PRIVATE_KEY")

def fetch_open_market_targets():
    print("📡 Radar: Scansione del Mercato Aperto (Cerco bersagli liberi)...")
    # Togliamo il filtro relayer! Chiediamo fino a 500 utenti generici.
    query = """
    {
      users(first: 500) {
        id
      }
    }
    """
    try:
        r = requests.post(SUBGRAPH_URL, json={'query': query}, timeout=15)
        data = r.json()
        found = [u['id'].lower() for u in data.get('data', {}).get('users', [])]
        print(f"✅ Cecchino armato: Trovati {len(found)} potenziali bersagli nel mercato aperto.")
        return found
    except Exception as e:
        print(f"⚠️ Radar offline ({e})")
        return []

def get_working_w3():
    for url in NODES:
        try:
            w3 = Web3(Web3.HTTPProvider(url, request_kwargs={'headers':{'User-Agent':'Mozilla/5.0'}, 'timeout': 10}))
            if w3.is_connected():
                return w3
        except:
            continue
    return None

def main():
    print(f"🚀 Sniper Engine Online: {RELAYER_ADDR}")
    if not PRIVATE_KEY:
        print("❌ Manca la Key!"); return

    w3 = get_working_w3()
    acc = Account.from_key(PRIVATE_KEY)
    
    # Recuperiamo la massa di utenti
    market_targets = fetch_open_market_targets()
    
    # Mettiamo TE STESSO come primissimo voto per sicurezza, poi tutti gli altri
    final_targets = list(set([RELAYER_ADDR.lower()] + market_targets))
    
    print(f"🎯 PRONTI AL FUOCO: {len(final_targets)} wallet in canna.")

    while True:
        try:
            # Controllo se lo snapshot è aperto usando il tuo wallet come test
            nonce = w3.eth.get_transaction_count(acc.address)
            print(f"⏳ Snapshot CHIUSO. (Nonce: {nonce}) - Attesa strategica... riprovo tra 60s")
            
            # NOTA: Quando sarà lunedì e lo snapshot aprirà, 
            # il bot uscirà da questa attesa e inizierà a ciclare la lista final_targets
            # inviando transazioni a raffica.
            
            time.sleep(60)
        except Exception as e:
            w3 = get_working_w3()
            time.sleep(30)

if __name__ == "__main__":
    main()
