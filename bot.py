import os
import time
import requests
from web3 import Web3
from eth_account import Account

# --- CONFIGURAZIONE ---
RELAYER_ADDR = "0x398897aba2d8e1e07c316e2b5eda2139de25fb0a"
CONTRACT_ADDR = "0x34b56f892c9e977b9ba2e43ba64c27d368ab3c86"
FUNCTION_SELECTOR = "0x56f1612f"

# Lista di nodi per evitare il "Nodo occupato"
NODES = [
    "https://rpc-mainnet.vechain.energy",
    "https://mainnet.veblocks.net",
    "https://node-mainnet.vechain.energy"
]

SUBGRAPH_URL = "https://graph.vet/subgraphs/name/vebetter/dao"
PRIVATE_KEY = os.getenv("VECHAIN_PRIVATE_KEY")

def fetch_delegators():
    print("📡 Fase 1: Ricerca delegati nel Radar...")
    # Proviamo la query con indirizzo sia minuscolo che standard
    query = """
    {
      users(where: {relayer: "%s"}) {
        id
      }
    }
    """ % RELAYER_ADDR.lower()
    
    try:
        r = requests.post(SUBGRAPH_URL, json={'query': query}, timeout=15)
        data = r.json()
        users = [u['id'] for u in data.get('data', {}).get('users', [])]
        
        # Se ancora 0, proviamo senza filtro per debug interno
        if not users:
            print("⚠️ Nessun delegato trovato con filtro diretto. Controllo fallback...")
            
        return users
    except Exception as e:
        print(f"⚠️ Errore Radar: {e}")
        return []

def get_working_w3():
    """Tenta di connettersi a uno dei nodi disponibili"""
    for url in NODES:
        try:
            w3 = Web3(Web3.HTTPProvider(url, request_kwargs={'headers':{'User-Agent':'Mozilla/5.0'}, 'timeout': 10}))
            if w3.is_connected():
                print(f"🔗 Connesso a: {url}")
                return w3
        except:
            continue
    return None

def main():
    print(f"🚀 Avvio Relayer Engine per: {RELAYER_ADDR}")
    
    if not PRIVATE_KEY:
        print("❌ Manca la Key!"); return

    w3 = get_working_w3()
    if not w3:
        print("❌ Nessun nodo raggiungibile. GitHub è bloccato."); return

    acc = Account.from_key(PRIVATE_KEY)
    
    # Radar
    delegates = fetch_delegators()
    targets = list(set([RELAYER_ADDR.lower()] + [d.lower() for d in delegates]))
    
    print(f"🎯 Pronti a votare per {len(targets)} wallet.")

    while True:
        try:
            # Refresh connessione se necessario
            if not w3.is_connected():
                w3 = get_working_w3()

            nonce = w3.eth.get_transaction_count(acc.address)
            print(f"⏳ Snapshot chiuso. (Nonce: {nonce}) - Radar attivo su {len(targets)} utenti. Riprovo...")
            time.sleep(60) # Aumentato a 60s per evitare ban dal nodo

        except Exception as e:
            print(f"🔄 Nodo momentaneamente instabile. Cambio rotta... ({str(e)[:50]})")
            w3 = get_working_w3()
            time.sleep(30)

if __name__ == "__main__":
    main()
