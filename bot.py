import requests
import os
import time

# Usiamo eth_account per la firma, è lo standard industriale
# Inseriscilo in requirements.txt: requests, eth-account
from eth_account import Account

NODE_URL = "https://mainnet.vechain.org"
CONTRACT_ADDRESS = "0x34b56f892c9e977b9ba2e43ba64c27d368ab3c86"

def monitor():
    print("🕵️ Relayer in ascolto. Pronto per lo snapshot.")
    while True:
        try:
            # Monitoraggio super veloce
            res = requests.get(f"{NODE_URL}/blocks/best", timeout=2)
            if res.status_code == 200:
                block = res.json()['number']
                print(f"🧱 Blocco: {block}")
                
                # QUI aggiungeremo la logica di controllo dello stato voto
                # E se il voto è aperto, chiameremo la funzione di invio
        except Exception as e:
            print(f"⚠️ Errore: {e}")
        time.sleep(1)

if __name__ == "__main__":
    monitor()
