import requests
import time
import os

# Usiamo un timeout molto basso (3 secondi)
TIMEOUT = 3 

def monitor():
    print("🕵️ Modalità 'Fast-Fail' attiva.")
    try:
        # Aggiungiamo timeout=TIMEOUT
        res = requests.get("https://mainnet.vechain.org/blocks/best", timeout=TIMEOUT)
        if res.status_code == 200:
            block = res.json()['number']
            print(f"✅ Connessione ok! Blocco: {block}")
        else:
            print(f"❌ Errore nodo: {res.status_code}")
    except requests.exceptions.Timeout:
        print("⚠️ Timeout! Il nodo non risponde entro 3 secondi.")
    except Exception as e:
        print(f"⚠️ Errore generico: {e}")

if __name__ == "__main__":
    monitor()
