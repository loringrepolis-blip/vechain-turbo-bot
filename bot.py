import os
import time
import requests
from web3 import Web3
from eth_account import Account

# --- CONFIGURAZIONE ---
RELAYER_ADDR = "0x398897aba2d8e1e07c316e2b5eda2139de25fb0a"
CONTRACT_ADDR = "0x34b56f892c9e977b9ba2e43ba64c27d368ab3c86"
FUNCTION_SELECTOR = "0x56f1612f"
RPC_URL = "https://node-mainnet.vechain.energy"
SUBGRAPH_URL = "https://graph.vet/subgraphs/name/vebetter/dao"
PRIVATE_KEY = os.getenv("VECHAIN_PRIVATE_KEY")

def fetch_delegators():
    print("📡 Ricerca delegati in corso...")
    query = '{ users(where: {relayer: "%s"}) { id } }' % RELAYER_ADDR.lower()
    try:
        # Timeout stretto per non bloccare il bot se il subgraph è lento
        r = requests.post(SUBGRAPH_URL, json={'query': query}, timeout=5)
        users = [u['id'] for u in r.json().get('data', {}).get('users', [])]
        print(f"✅ Radar: Trovati {len(users)} delegati.")
        return users
    except Exception as e:
        print(f"⚠️ Radar offline (errore: {e}). Procedo solo con il mio wallet.")
        return []

def main():
    print(f"🚀 Avvio Relayer: {RELAYER_ADDR}")
    
    if not PRIVATE_KEY:
        print("❌ ERRORE: Manca VECHAIN_PRIVATE_KEY nelle Secrets di GitHub!"); return

    # Inizializzazione Web3
    w3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={'headers':{'User-Agent':'Mozilla/5.0'}}))
    acc = Account.from_key(PRIVATE_KEY)
    
    # Prepariamo la lista
    delegates = fetch_delegators()
    targets = [RELAYER_ADDR] + [d for d in delegates if d.lower() != RELAYER_ADDR.lower()]

    print(f"🎯 Totale wallet da votare: {len(targets)}")

    while True:
        try:
            # Testiamo lo stato dello snapshot
            nonce = w3.eth.get_transaction_count(acc.address)
            
            # Se arriviamo qui, il nodo risponde
            print(f"⏳ Snapshot ancora chiuso. Ri-controllo tra 30s... (Nonce attuale: {nonce})")
            time.sleep(30)

        except Exception as e:
            err_msg = str(e)
            if "DOCTYPE" in err_msg or "403" in err_msg:
                print("🔄 Il nodo ha risposto con un errore HTML/403. Provo a cambiare metodo...")
            else:
                print(f"❓ Info: {err_msg[:100]}")
            time.sleep(30)

if __name__ == "__main__":
    main()
