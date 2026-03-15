import os
import time
from web3 import Web3
from eth_account import Account

# --- CONFIGURAZIONE ---
RPC_URL = "https://node-mainnet.vechain.energy"
CONTRACT_ADDRESS = "0x34b56f892c9e977b9ba2e43ba64c27d368ab3c86"
FUNCTION_SELECTOR = "0x56f1612f"

# Inserisci qui i wallet target. Domani potrai aggiungerne altri al volo.
TARGET_WALLETS = [
    "0x398897...", # Il tuo wallet Relayer
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
    if not PRIVATE_KEY:
        print("❌ ERRORE: Chiave privata non trovata nei Secrets!", flush=True)
        return

    account = Account.from_key(PRIVATE_KEY)
    print(f"🕵️ Relayer {account.address} attivo e in ascolto...", flush=True)
    
    tentativi = 0
    mentre_aspettiamo = True

    while mentre_aspettiamo:
        tentativi += 1
        try:
            # Recuperiamo il nonce attuale
            nonce = web3.eth.get_transaction_count(account.address)
            
            # Tentativo di voto per il primo target (il tuo o una balena)
            print(f"🔄 Tentativo {tentativi}: Provo a inviare il voto...", flush=True)
            tx_hash = invia_voto(TARGET_WALLETS[0], account, nonce)
            
            print(f"🚀 SNAPSHOT APERTO! Voto inviato: {tx_hash}", flush=True)
            
            # Se il primo passa, processiamo gli altri della lista
            if len(TARGET_WALLETS) > 1:
                for i in range(1, len(TARGET_WALLETS)):
                    nonce += 1
                    h = invia_voto(TARGET_WALLETS[i], account, nonce)
                    print(f"✅ Voto extra inviato per {TARGET_WALLETS[i]}: {h}", flush=True)
            
            print("🏁 Missione completata con successo!", flush=True)
            mentre_aspettiamo = False 

        except Exception as e:
            # Gestione dell'attesa se lo snapshot è ancora chiuso
            print(f"⏳ Snapshot ancora chiuso (o errore: {str(e)[:50]}...). Riprovo tra 30s...", flush=True)
            time.sleep(30)

if __name__ == "__main__":
    main()
