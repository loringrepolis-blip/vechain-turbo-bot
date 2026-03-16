import os
import time
from web3 import Web3
from eth_account import Account

# --- CONFIGURAZIONE ---
# Usiamo il nodo pubblico ufficiale di VeChain (non blocca i bot)
RPC_URL = "https://mainnet.vechain.org"
CONTRACT_ADDRESS = "0x34b56f892c9e977b9ba2e43ba64c27d368ab3c86"
FUNCTION_SELECTOR = "0x56f1612f"

# Il tuo wallet
TARGET_WALLETS = [
    "0x398897Aba2D8E1e07C316E2b5EdA2139DE25Fb0a", 
]

web3 = Web3(Web3.HTTPProvider(RPC_URL))
PRIVATE_KEY = os.getenv("VECHAIN_PRIVATE_KEY")

def genera_payload(wallet_address):
    clean_address = wallet_address.lower().replace('0x', '')
    return FUNCTION_SELECTOR + clean_address.zfill(64)

def invia_voto(wallet_target, account, nonce):
    payload = genera_payload(wallet_target)
    tx = {
        'nonce': nonce,
        'to': web3.to_checksum_address(CONTRACT_ADDRESS),
        'value': 0,
        'gas': 160000,
        'gasPrice': web3.to_wei(120, 'gwei'),
        'data': payload,
        'chainId': web3.eth.chain_id
    }
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return web3.to_hex(tx_hash)

def main():
    print("🛠️ Avvio sistema...", flush=True)
    if not PRIVATE_KEY:
        print("❌ ERRORE: Chiave privata non trovata!", flush=True)
        return

    account = Account.from_key(PRIVATE_KEY)
    print(f"🕵️ Relayer {account.address} in ascolto...", flush=True)
    
    tentativi = 0
    mentre_aspettiamo = True

    while mentre_aspettiamo:
        tentativi += 1
        try:
            nonce = web3.eth.get_transaction_count(account.address)
            print(f"🔄 Tentativo {tentativi} in corso...", flush=True)
            
            tx_hash = invia_voto(TARGET_WALLETS[0], account, nonce)
            
            print(f"🚀 BERSAGLIO COLPITO! Voto inviato: {tx_hash}", flush=True)
            mentre_aspettiamo = False 

        except Exception as e:
            print(f"⏳ Errore o Snapshot chiuso: {str(e)[:60]}... Riprovo tra 30s", flush=True)
            time.sleep(30)

if __name__ == "__main__":
    main()
