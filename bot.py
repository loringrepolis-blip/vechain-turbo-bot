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
    """Recupera fino a 1000 bersagli attivi"""
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

def is_snapshot_open(w3, acc, test_target):
    """Il 'Sensore': simula una transazione per vedere se la DAO accetta voti"""
    clean_target = test_target.lower().replace('0x', '').rjust(64, '0')
    tx = {
        'to': Web3.to_checksum_address(CONTRACT_ADDR),
        'from': acc.address,
        'data': FUNCTION_SELECTOR + clean_target
    }
    try:
        w3.eth.call(tx) # Se passa senza errori, siamo APERTI
        return True
    except:
        return False # Se restituisce errore, siamo CHIUSI

def fire_volley(w3, acc, targets):
    """Il 'Grilletto': spara i voti in sequenza"""
    print(f"\n🔥 GRILLETTO PREMUTO! Inizio raffica su {len(targets)} bersagli...")
    nonce = w3.eth.get_transaction_count(acc.address)
    gas_price = w3.eth.gas_price
    success_count = 0
    
    for i, target in enumerate(targets):
        try:
            clean_target = target.lower().replace('0x', '').rjust(64, '0')
            tx = {
                'chainId': w3.eth.chain_id,
                'nonce': nonce,
                'to': Web3.to_checksum_address(CONTRACT_ADDR),
                'data': FUNCTION_SELECTOR + clean_target,
                'gas': 100000, # Copertura di sicurezza per il voto
                'gasPrice': gas_price
            }
            
            signed_tx = acc.sign_transaction(tx)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            print(f"[{i+1}/{len(targets)}] 🎯 Colpito: {target} | TxID: {tx_hash.hex()}")
            nonce += 1
            success_count += 1
            time.sleep(0.3) # Pausa strategica per non far arrabbiare il nodo (Anti-DDoS)
            
        except Exception as e:
            print(f"[{i+1}/{len(targets)}] ❌ Fallito su {target}: Errore di connessione o gas.")
            time.sleep(1) # Se c'è un errore, respira un attimo prima del prossimo
            
    print(f"\n✅ RAFFICA COMPLETATA! Bersagli colpiti con successo: {success_count}/{len(targets)}")

def main():
    print(f"🚀 Sniper Engine ARMATO | Relayer: {RELAYER_ADDR}")
    w3 = get_working_w3()
    if not w3:
        print("❌ ERRORE: Nessun nodo risponde!"); return
        
    acc = Account.from_key(PRIVATE_KEY)
    
    # 1. Caricamento Armi
    market_targets = fetch_open_market()
    final_targets = list(set([RELAYER_ADDR.lower()] + [t.lower() for t in MANUAL_TARGETS] + market_targets))
    print(f"🎯 STATO CARICATORE: {len(final_targets)} wallet pronti.")

    # 2. La Sentinella (Loop di attesa)
    while True:
        try:
            if is_snapshot_open(w3, acc, final_targets[0]):
                print("🟢 SEGNALE VERDE: Lo Snapshot è APERTO!")
                # 3. Fuoco!
                fire_volley(w3, acc, final_targets)
                break # Una volta sparato, il bot esce e si spegne
            else:
                print(f"⏳ Snapshot CHIUSO | In attesa del via libera... Riprovo tra 30s")
                time.sleep(30)
                
        except Exception as e:
            print(f"🔄 Nodo instabile, ricollegamento...")
            w3 = get_working_w3()
            time.sleep(30)

if __name__ == "__main__":
    main()
