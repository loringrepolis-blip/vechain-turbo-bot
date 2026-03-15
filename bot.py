import os
import time
import requests
from thor_requests.connect import ThorClient
from thor_requests.wallet import Wallet
from thor_requests.transactions import TransactionConfig

# --- CONFIGURAZIONE ---
NODE_URL = "https://mainnet.vechain.org"
CONTRACT_ADDRESS = "0x34b56f892c9e977b9ba2e43ba64c27d368ab3c86"

# Recupero chiave da GitHub Secrets
PRIVATE_KEY = os.getenv("VECHAIN_PRIVATE_KEY")

def main():
    if not PRIVATE_KEY:
        print("❌ ERRORE: Chiave privata non trovata nei Secrets di GitHub!")
        return

    # Inizializza il client VeChain
    connector = ThorClient(endpoint=NODE_URL)
    wallet = Wallet.from_private_key(PRIVATE_KEY)
    
    print(f"🕵️ Relayer avviato.")
    print(f"✅ Indirizzo firmatario: {wallet.address}")
    
    # Monitoraggio blocchi (La base del nostro ciclo di gara)
    last_block = 0
    while True:
        try:
            res = requests.get(f"{NODE_URL}/blocks/best", timeout=5)
            if res.status_code == 200:
                block_data = res.json()
                current_block = block_data['number']
                
                if current_block > last_block:
                    last_block = current_block
                    print(f"🧱 Blocco: {current_block} - Relayer in ascolto...", flush=True)
                    
                    # Qui aggiungeremo tra poco la logica per rilevare l'apertura del voto
                    
            time.sleep(1) # Polling ogni secondo
            
        except Exception as e:
            print(f"⚠️ Errore durante il monitoraggio: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
