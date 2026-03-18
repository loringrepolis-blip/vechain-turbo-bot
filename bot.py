import os
import time
import requests
from web3 import Web3
from eth_account import Account

# --- CONFIGURAZIONE CORE ---
RELAYER_ADDR = "0x398897aba2d8e1e07c316e2b5eda2139de25fb0a"
CONTRACT_ADDR = "0x34b56f892c9e977b9ba2e43ba64c27d368ab3c86"
FUNCTION_SELECTOR = "0x56f1612f" # castVote(address)

# Lista nodi per ridondanza (Anti-Ban)
NODES = [
    "https://mainnet.vechain.org",
    "https://node-mainnet.vechain.energy",
    "https://mainnet.veblocks.net"
]

# Endpoint per il Radar (Subgraph VeBetterDAO)
SUBGRAPH_URL = "https://graph.vet/subgraphs/name/vebetter/dao"

PRIVATE_KEY = os.getenv("VECHAIN_PRIVATE_KEY")

def get_web3():
    """Ruota tra i nodi se uno fallisce"""
    for url in NODES:
        try:
            w3 = Web3(Web3.HTTPProvider(url, request_kwargs={'timeout': 10}))
            if w3.is_connected(): return w3
        except: continue
    return None

def fetch_delegators():
    """RADAR: Chiede al Subgraph chi ha delegato a questo Relayer"""
    query = """
    {
      users(where: {relayer: "%s"}) {
        id
      }
    }
    """ % RELAYER_ADDR.lower()
    
    try:
        response = requests.post(SUBGRAPH_URL, json={'query': query})
        data = response.json()
        # Estrae gli indirizzi dalla risposta
        delegators = [u['id'] for u in data['data']['users']]
        return delegators
    except Exception as e:
        print(f"⚠️ Errore Radar: {e}. Uso solo il mio wallet.")
        return [RELAYER_ADDR]

def main():
    print(f"📡 RADAR ATTIVATO per Relayer: {RELAYER_ADDR}")
    w3 = get_web3()
    if not w3 or not PRIVATE_KEY:
        print("❌ Errore configurazione (Nodo o Private Key).")
        return

    acc = Account.from_key(PRIVATE_KEY)
    
    # 1. Recupera la lista automatica (i tuoi 42 utenti + nuovi)
    targets = fetch_delegators()
    if RELAYER_ADDR.lower() not in targets:
        targets.insert(0, RELAYER_ADDR) # Aggiungi te stesso se non in lista
    
    print(f"✅ Trovati {len(targets)} wallet deleganti. Inizio monitoraggio...")

    while True:
        try:
            # Controllo rapido: prova a inviare il primo voto
            nonce = w3.eth.get_transaction_count(acc.address)
            
            # Prepariamo il payload per il primo target
            payload = FUNCTION_SELECTOR + targets[0].lower().replace('0x', '').zfill(64)
            
            tx = {
                'nonce': nonce,
                'to': w3.to_checksum_address(CONTRACT_ADDR),
                'value': 0,
                'gas': 180000,
                'gasPrice': w3.to_wei(150, 'gwei'), # Gas aggressivo per priorità
                'data': payload,
                'chainId': 101
            }

            signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
            
            print(f"🎯 SNAPSHOT APERTO! Voto inviato per {targets[0]}: {w3.to_hex(tx_hash)}")

            # Se il primo va a buon fine, spara a raffica per tutti gli altri
            for i in range(1, len(targets)):
                nonce += 1
                payload = FUNCTION_SELECTOR + targets[i].lower().replace('0x', '').zfill(64)
                tx['nonce'] = nonce
                tx['data'] = payload
                signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
                w3.eth.send_raw_transaction(signed.rawTransaction)
                print(f"🚀 Voto automatico inviato per delegante: {targets[i]}")
            
            print("🏁 Operazione conclusa con successo!")
            break

        except Exception as e:
            error_msg = str(e)
            if "revert" in error_msg or "closed" in error_msg:
                print("⏳ Snapshot chiuso... riprovo tra 30s")
            elif "403" in error_msg:
                print("🔄 Nodo bloccato. Ruoto connessione...")
                w3 = get_web3()
            else:
                print(f"❓ Info: {error_msg[:60]}...")
            
            time.sleep(30)

if __name__ == "__main__":
    main()
