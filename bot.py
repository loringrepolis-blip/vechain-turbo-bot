import requests
import time

NODE_URL = "https://mainnet.vechain.org"

def monitor():
    print("🕵️ Relayer in ascolto. Pronto per lo snapshot.")
    try:
        res = requests.get(f"{NODE_URL}/blocks/best", timeout=5)
        if res.status_code == 200:
            block = res.json()['number']
            print(f"✅ Connessione ok! Blocco corrente: {block}")
        else:
            print(f"❌ Errore nodo: {res.status_code}")
    except Exception as e:
        print(f"⚠️ Errore: {e}")

if __name__ == "__main__":
    monitor()
