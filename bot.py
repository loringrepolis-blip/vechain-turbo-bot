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

def fetch_delegators():
    print("📡 Fase 1: Ricerca delegati nel Radar...")
    # Proviamo sia minuscolo che checksummed per sicurezza
    addr_low = RELAYER_ADDR.lower()
    addr_check = Web3.to_checksum_address(RELAYER_ADDR)
    
    query = """
    {
      users(where: {relayer_in: ["%s", "%s"]}) {
        id
      }
    }
    """ % (addr_low, addr_check)
    
    try:
        r = requests.post(SUBGRAPH_URL, json={'query': query}, timeout=15)
        data = r.json()
        users = [u['id'] for u in data.get('data', {}).get('users', [])]
        
        if not users:
            # --- PIANO B: SE IL RADAR È VUOTO, AGGIUNGI QUI GLI INDIRIZZI A MANO ---
            # Se vuoi essere sicuro per lunedì, puoi incollarli qui dentro così:
            # users = ["0xIndirizzo1", "0xIndirizzo2"]
            print("⚠️ Il Radar automatico non risponde correttamente.")
        
        return users
    except Exception as e:
        print(f"⚠️ Errore Radar: {e}")
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
    print(f"🚀 Relayer Engine Online: {RELAYER_ADDR}")
    if not PRIVATE_KEY:
        print("❌ Manca la Key!"); return

    w3 = get_working_w3()
    if not w3:
        print("❌ Rete non raggiungibile."); return

    acc = Account.from_key(PRIVATE_KEY)
    
    # Recupero delegati
    delegates = fetch_delegators()
    # Costruiamo la lista finale: prima TU, poi i delegati
    targets = [RELAYER_ADDR.lower()]
    for d in delegates:
        if d.lower() != RELAYER_ADDR.lower():
            targets.append(d.lower())
    
    print(f"✅ Configurazione completata. Target pronti: {len(targets)}")

    while True:
        try:
            # Controllo connessione e Nonce (per vedere se il bot è vivo)
            nonce = w3.eth.get_transaction_count(acc.address)
            print(f"⏳ Snapshot CHIUSO. (Nonce: {nonce}) - Monitoraggio {len(targets)} wallet... riprovo tra 60s")
            time.sleep(60)

        except Exception as e:
            print(f"🔄 Nodo instabile, ricollego... ({str(e)[:40]})")
            w3 = get_working_w3()
            time.sleep(30)

if __name__ == "__main__":
    main()
