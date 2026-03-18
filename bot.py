import os
import time
import requests
from web3 import Web3
from eth_account import Account

# --- CONFIGURAZIONE ---
RELAYER_ADDR = "0x398897aba2d8e1e07c316e2b5eda2139de25fb0a"
CONTRACT_ADDR = "0x34b56f892c9e977b9ba2e43ba64c27d368ab3c86"
FUNCTION_SELECTOR = "0x56f1612f"
# Usiamo un nodo alternativo più stabile per il proxy
RPC_URL = "https://node-mainnet.vechain.energy" 
SUBGRAPH_URL = "https://graph.vet/subgraphs/name/vebetter/dao"
PRIVATE_KEY = os.getenv("VECHAIN_PRIVATE_KEY")

def fetch_delegators():
    query = '{ users(where: {relayer: "%s"}) { id } }' % RELAYER_ADDR.lower()
    try:
        r = requests.post(SUBGRAPH_URL, json={'query': query}, timeout=10)
        return [u['id'] for u in r.json()['data']['users']]
    except:
        return [RELAYER_ADDR]

def main():
    print(f"🕵️ Relayer {RELAYER_ADDR} in ascolto...")
    if not PRIVATE_KEY:
        print("❌ Manca la Private Key!"); return

    # Connessione con Header per evitare il blocco HTML
    w3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={'headers':{'User-Agent':'Mozilla/5.0'}}))
    acc = Account.from_key(PRIVATE_KEY)
    
    targets = fetch_delegators()
    print(f"✅ Radar: {len(targets)} delegati pronti.")

    while True:
        try:
            # Test di connessione semplice
            nonce = w3.eth.get_transaction_count(acc.address)
            
            # Prepariamo la raffica per i 42+ utenti
            for target in targets:
                payload = FUNCTION_SELECTOR + target.lower().replace('0x', '').zfill(64)
                tx = {
                    'nonce': nonce,
                    'to': w3.to_checksum_address(CONTRACT_ADDR),
                    'value': 0,
                    'gas': 180000,
                    'gasPrice': w3.to_wei(120, 'gwei'),
                    'data': payload,
                    'chainId': 101 # VeChain Mainnet ID
                }
                signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
                w3.eth.send_raw_transaction(signed.rawTransaction)
                print(f"🚀 Voto inviato per: {target}")
                nonce += 1
            
            print("🏁 Ciclo completato."); break

        except Exception as e:
            err = str(e)
            if "revert" in err or "closed" in err or "DOCTYPE" in err:
                print("⏳ Snapshot chiuso o nodo occupato... riprovo tra 30s")
            else:
                print(f"⚠️ Nota: {err[:50]}")
            time.sleep(30)

if __name__ == "__main__":
    main()
