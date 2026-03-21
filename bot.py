import os
import time
import requests
from thor_requests.connect import Connect
from thor_requests.wallet import Wallet

# --- CONFIGURAZIONE ---
RELAYER_ADDR = "0x398897aba2d8e1e07c316e2b5eda2139de25fb0a"
CONTRACT_ADDR = "0x34b56f892c9e977b9ba2e43ba64c27d368ab3c86"
FUNCTION_SELECTOR = "0x56f1612f"
BATCH_SIZE = 100 

NODE_URL = "https://rpc-mainnet.vechain.energy"
SUBGRAPH_URL = "https://graph.vet/subgraphs/name/vebetter/dao"
PRIVATE_KEY = os.getenv("VECHAIN_PRIVATE_KEY")

def fetch_targets():
    """Radar: Recupera i 1000 bersagli più attivi"""
    print("📡 Radar: Scansione in corso per 1000 bersagli...")
    query = '{ accounts(first: 1000, orderBy: id, orderDirection: desc) { id } }'
    try:
        r = requests.post(SUBGRAPH_URL, json={'query': query}, timeout=15)
        data = r.json()
        if 'data' in data and 'accounts' in data['data']:
            return [u['id'] for u in data['data']['accounts']]
        return []
    except Exception as e:
        print(f"❌ Errore Radar: {e}")
        return []

def is_snapshot_open(connector):
    """Sensore: Controlla se lo snapshot è aperto"""
    try:
        test_data = FUNCTION_SELECTOR + RELAYER_ADDR.lower().replace('0x', '').rjust(64, '0')
        connector.call(RELAYER_ADDR, CONTRACT_ADDR, test_data)
        return True
    except:
        return False

def main():
    print(f"🚀 SNIPER GATLING V2.2 | Relayer: {RELAYER_ADDR}")
    if not PRIVATE_KEY:
        print("❌ ERRORE: Chiave Privata mancante!"); return

    #thor-requests gestisce tutto internamente
    connector = Connect(NODE_URL)
    wallet = Wallet.from_private_key(PRIVATE_KEY)
    
    targets = fetch_targets()
    if not targets:
        print("❌ Nessun bersaglio trovato."); return
    
    print(f"🎯 Caricatore: {len(targets)} wallet pronti.")

    while True:
        try:
            if is_snapshot_open(connector):
                print("🟢 APERTO! Inizio Fuoco!")
                for i in range(0, len(targets), BATCH_SIZE):
                    batch = targets[i:i + BATCH_SIZE]
                    clauses = []
                    for t in batch:
                        data = FUNCTION_SELECTOR + t.lower().replace('0x', '').rjust(64, '0')
                        clauses.append({"to": CONTRACT_ADDR, "value": 0, "data": data})
                    
                    res = connector.send_transaction(wallet, clauses)
                    print(f"🚀 Batch {i//BATCH_SIZE + 1} inviato! | TxID: {res['id']}")
                    time.sleep(1.5)
                
                print("\n✅ MISSIONE COMPIUTA!")
                break
            else:
                print(f"⏳ CHIUSO | In attesa... (Controllo ogni 30s)")
                time.sleep(30)
        except Exception as e:
            print(f"🔄 Errore connessione: {e}. Riprovo...")
            time.sleep(30)

if __name__ == "__main__":
    main()
