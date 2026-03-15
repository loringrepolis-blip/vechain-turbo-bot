import requests
import time

CONTRACT_ADDRESS = "0x34b56f892c9e977b9ba2e43ba64c27d368ab3c86"
NODE_URL = "https://mainnet.vechain.org"

def monitor():
    print("🕵️ Modalità 'Ascolto Profondo' attiva.")
    last_block = 0
    while True:
        try:
            # Chiediamo al nodo l'ultimo blocco
            res = requests.get(f"{NODE_URL}/blocks/best", timeout=5).json()
            current_block = res['number']
            
            if current_block > last_block:
                print(f"🧱 Analisi blocco {current_block} per attività su contratto...")
                # Qui chiediamo al nodo: "Ci sono transazioni verso il contratto in questo blocco?"
                # (Semplificazione logica)
                last_block = current_block
                
        except Exception as e:
            print(f"Attesa...")
        time.sleep(2)

if __name__ == "__main__":
    monitor()
