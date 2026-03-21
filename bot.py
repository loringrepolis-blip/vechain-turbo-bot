import os
import time
import requests
from thor_requests.connect import Connect
from thor_requests.wallet import Wallet

# --- CONFIGURAZIONE ---
RELAYER_ADDR = "0x398897aba2d8e1e07c316e2b5eda2139de25fb0a"
CONTRACT_ADDR = "0x34b56f892c9e977b9ba2e43ba64c27d368ab3c86"
FUNCTION_SELECTOR = "0x56f1612f"
BATCH_SIZE = 100  # Spariamo 10 gruppi da 100 voti l'uno

NODE_URL = "https://rpc-mainnet.vechain.energy"
SUBGRAPH_URL = "https://graph.vet/subgraphs/name/vebetter/dao"
PRIVATE_KEY = os.getenv("VECHAIN_PRIVATE_KEY")

def fetch_targets():
    """Radar: Recupera i 1000 bersagli più attivi dal database VeBetterDAO"""
    print("📡 Radar: Scansione in corso per 1000 bersagli...")
    query = '{ accounts(first: 1000, orderBy: id, orderDirection: desc) { id } }'
    try:
        # User-agent per evitare blocchi dal server del database
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.post(SUBGRAPH_URL, json={'query': query}, headers=headers, timeout=15)
        data = r.json()
        if 'data' in data and 'accounts' in data['data']:
            return [u['id'] for u in data['data']['accounts']]
        else:
            print("⚠️ Radar: Risposta inattesa dal Subgraph.")
            return []
    except Exception as e:
        print(f"❌ Errore Radar: {e}")
        return []

def is_snapshot_open(connector):
    """Sensore: Simula un voto per capire se lo snapshot è ufficialmente aperto"""
    try:
        # Prepariamo un dato di test (voto simulato sul tuo relayer)
        test_data = FUNCTION_SELECTOR + RELAYER_ADDR.lower().replace('0x', '').rjust(64, '0')
        # Se la chiamata (call) non dà errore, lo snapshot è APERTO
        connector.call(RELAYER_ADDR, CONTRACT_ADDR, test_data)
        return True
    except:
        # Se il contratto rifiuta il voto (snapshot chiuso), restituisce errore
        return False

def main():
    print(f"🚀 SNIPER GATLING V2.1 | Relayer: {RELAYER_ADDR}")
    if not PRIVATE_KEY:
        print("❌ ERRORE CRITICO: Chiave Privata non trovata nei Secrets!"); return

    # Inizializziamo la connessione alla rete VeChain
    connector = Connect(NODE_URL)
    wallet = Wallet.from_private_key(PRIVATE_KEY)
    
    # 1. Caricamento Bersagli
    targets = fetch_targets()
    if not targets:
        print("❌ Nessun bersaglio trovato. Il bot si ferma per sicurezza."); return
    
    print(f"🎯 Caricatore pieno: {len(targets)} wallet pronti per il Round 91.")

    # 2. Sentinella (Loop di attesa tattica)
    while True:
        try:
            if is_snapshot_open(connector):
                print("🟢 SEGNALE VERDE: Lo Snapshot è APERTO! Inizio Fuoco!")
                
                # 3. Raffica Massiva in Batch da 100
                for i in range(0, len(targets), BATCH_SIZE):
                    batch = targets[i:i + BATCH_SIZE]
                    clauses = []
                    
                    for t in batch:
                        # Codifica del voto per ogni target
                        data = FUNCTION_SELECTOR + t.lower().replace('0x', '').rjust(64, '0')
                        clauses.append({"to": CONTRACT_ADDR, "value": 0, "data": data})
                    
                    try:
                        # Spariamo il Batch di 100 clausole
                        res = connector.send_transaction(wallet, clauses)
                        print(f"🚀 Batch {i//BATCH_SIZE + 1} inviato! | TxID: {res['id']}")
                        time.sleep(1.5) # Pausa strategica per stabilità del nodo
                    except Exception as e:
                        print(f"⚠️ Errore nel Batch {i//BATCH_SIZE + 1}: {e}")
                
                print("\n✅ MISSIONE COMPIUTA: Tutti i batch sono stati sparati!")
                break # Operazione conclusa, il bot si spegne
            else:
                print(f"⏳ Snapshot CHIUSO | Sentinella in attesa... (Controllo ogni 30s)")
                time.sleep(30)
                
        except Exception as e:
            print(f"🔄 Nodo instabile o errore di connessione: {e}. Riprovo...")
            time.sleep(30)

if __name__ == "__main__":
    main()
