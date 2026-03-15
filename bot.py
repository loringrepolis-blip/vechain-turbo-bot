import os
import requests
import time
from eth_account import Account

# Legge il Secret che hai già configurato su GitHub
PRIVATE_KEY = os.getenv("VECHAIN_PRIVATE_KEY")
NODE_URL = "https://mainnet.vechain.org"

def main():
    if not PRIVATE_KEY:
        print("❌ ERRORE: Chiave privata non trovata nei Secrets!")
        return

    # Inizializza l'account per la firma
    account = Account.from_key(PRIVATE_KEY)
    print(f"🕵️ Relayer attivo con indirizzo: {account.address}")
    
    # Monitoraggio blocchi
    while True:
        try:
            res = requests.get(f"{NODE_URL}/blocks/best", timeout=5)
            if res.status_code == 200:
                block = res.json()['number']
                print(f"🧱 Blocco: {block} | In attesa dello snapshot...")
        except Exception as e:
            print(f"⚠️ Errore: {e}")
        time.sleep(1)

if __name__ == "__main__":
    main()
