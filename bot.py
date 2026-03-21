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
RAW_KEY = os.getenv("VECHAIN_PRIVATE_KEY", "").strip()

def fetch_targets():
    """Radar: Recupera i 1000 bersagli"""
    print("📡 Radar: Scansione in corso per 1000 bersagli...", flush=True)
    query = '{ accounts(first: 1000, orderBy: id, orderDirection: desc) { id } }'
    try:
        r = requests.post(SUBGRAPH_URL, json={'query': query}, timeout=15)
        data = r.json()
        if 'data' in data and 'accounts' in data['data']:
            return [u['id'] for u in data['data']['accounts']]
        return []
    except Exception as e:
        print(f"❌ Errore Radar: {e}", flush=True)
        return []

def is_snapshot_open(connector):
    """Sensore: Verifica apertura Snapshot tramite simulazione"""
    try:
        test_data = FUNCTION_SELECTOR + RELAYER_ADDR.lower().replace('0x', '').rjust(64, '0')
        connector.call(RELAYER_ADDR, CONTRACT_ADDR, test_data)
        return True
    except:
        return False

def main():
    print(f"🚀 SNIPER GATLING V2.6 (Real-Time) | Relayer: {RELAYER_ADDR}", flush=True)
    
    # Pulizia e validazione chiave
    clean_key = RAW_KEY[2:] if RAW_KEY.startswith("0x") else RAW_KEY
    
    if not clean_key or len(clean_key) != 64:
        print(f"❌ ERRORE CHIAVE: Lunghezza non valida ({len(clean_key)})", flush=True)
        return

    try:
        connector = Connect(NODE_URL)
        wallet = Wallet(bytes.fromhex(clean_key)) 
        print("✅ Chiave caricata e convertita correttamente.", flush=True)
    except Exception as e:
        print(f"❌ Errore caricamento Wallet: {e}", flush=True)
        return

    # Caricamento munizioni
    targets = fetch_targets()
    if not targets:
        print("❌ Nessun bersaglio trovato. Riprovo tra 10s...", flush=True)
        time.sleep(10)
        return main() # Riprova il caricamento
    
    print(f"🎯 Caricatore: {len(targets)} wallet pronti.", flush=True)

    # Ciclo di guardia
    while True:
        try:
            if is_snapshot_open(connector):
                print("🟢 SEGNALE VERDE: Snapshot APERTO! Inizio Fuoco!", flush=True)
                for i in range(0, len(targets), BATCH_SIZE):
                    batch = targets[i:i + BATCH_SIZE]
                    clauses = []
                    for t in batch:
                        data = FUNCTION_SELECTOR + t.lower().replace('0x', '').rjust(64, '0')
                        clauses.append({"to": CONTRACT_ADDR, "value": 0, "data": data})
                    
                    res = connector.send_transaction(wallet, clauses)
                    print(f"🚀 Batch {i//BATCH_SIZE + 1} inviato! | TxID: {res['id']}", flush=True)
                    time.sleep(1.5)
                
                print("\n✅ MISSIONE COMPIUTA: Tutti i batch completati!", flush=True)
                break
            else:
                # Stampa lo stato ogni 30 secondi per rassicurare che il bot è vivo
                current_time = time.strftime("%H:%M:%S", time.localtime())
                print(f"⏳ [{current_time}] Snapshot CHIUSO | Sentinella in attesa...", flush=True)
                time.sleep(30)
        except Exception as e:
            print(f"🔄 Errore durante il monitoraggio: {e}. Riprovo...", flush=True)
            time.sleep(30)

if __name__ == "__main__":
    main()
