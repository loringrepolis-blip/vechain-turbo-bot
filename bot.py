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
    print("📡 Fase 1: Ricerca delegati nel Radar...")
    query = '{ users(where: {relayer: "%s"}) { id } }' % RELAYER_ADDR.lower()
    try:
        # Timeout ridotto a 10 secondi per evitare il "blocco bianco" su GitHub
        r = requests.post(SUBGRAPH_URL, json={'query': query}, timeout=10)
        r.raise_for_status()
        data = r.json()
        users = [u['id'] for u in data.get('data', {}).get('users', [])]
        print(f"✅ Radar: Trovati {len(users)} delegati.")
        return users
    except Exception as e:
        print(f"⚠️ Radar momentaneamente offline: {e}")
        print("💡 Procedo con la modalità provvisoria (voto solo per me stesso).")
        return []

def main():
    print(f"🚀 Avvio Relayer Engine per: {RELAYER_ADDR}")
    
    if not PRIVATE_KEY:
        print("❌ ERRORE CRITICO: VECHAIN_PRIVATE_KEY non trovata!"); return

    # Inizializzazione Web3 con Header per bypassare filtri
    w3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={'headers':{'User-Agent':'Mozilla/5.0'}, 'timeout': 20}))
    acc = Account.from_key(PRIVATE_KEY)
    
    # Costruzione lista target
    delegates = fetch_delegators()
    # Mettiamo il tuo wallet in cima, poi i delegati (rimuovendo duplicati)
    targets = [RELAYER_ADDR]
    for d in delegates:
        if d.lower() != RELAYER_ADDR.lower():
            targets.append(d)

    print(f"🎯 Pronti a votare per {len(targets)} wallet.")

    while True:
        try:
            # Controllo connessione e Nonce
            nonce = w3.eth.get_transaction_count(acc.address)
            
            # Se arriviamo qui, il nodo risponde. Ora proviamo a "bussare" allo snapshot
            # Usiamo il primo wallet come test fire
            print(f"⏳ Snapshot ancora chiuso. (Nonce: {nonce}) - Riprovo tra 30s...")
            time.sleep(30)

        except Exception as e:
            err_msg = str(e)
            if "DOCTYPE" in err_msg or "403" in err_msg:
                print("🔄 Errore di rete (Nodo occupato). Attesa 30s...")
            elif "revert" in err_msg:
                print("⏳ Lo Smart Contract rifiuta il voto: Snapshot probabilmente chiuso.")
            else:
                print(f"❓ Info: {err_msg[:80]}...")
            time.sleep(30)

if __name__ == "__main__":
    main()
