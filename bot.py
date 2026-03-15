import time
import sys
from web3 import Web3

def run_bot():
    # 1. Configurazione del Nodo RPC specifico per VeChain (Vechain Energy)
    # È un endpoint ottimizzato per le richieste programmatiche
    rpc_url = "https://node.mainnet.vechain.energy"
    
    print(f"🚀 Inizializzazione bot...")
    print(f"🔗 Connessione a: {rpc_url}")
    
    w3 = Web3(Web3.HTTPProvider(rpc_url))

    # 2. Verifica connessione
    if not w3.is_connected():
        print("❌ Errore: Impossibile connettersi al nodo VeChain.")
        sys.exit(1) # Esce con errore per segnalare il problema su GitHub
    
    print("✅ Connessione stabilita con successo!")

    # 3. Esecuzione del loop di monitoraggio
    # Usiamo un ciclo limitato per il test, così GitHub non lo chiude per timeout
    try:
        for i in range(5):
            block_number = w3.eth.block_number
            print(f"[{time.strftime('%H:%M:%S')}] Blocco attuale: {block_number}", flush=True)
            time.sleep(10) # Attesa di 10 secondi tra un controllo e l'altro
    except Exception as e:
        print(f"⚠️ Errore durante il monitoraggio: {e}")
        sys.exit(1)

    print("--- Termine esecuzione test ---")

if __name__ == "__main__":
    run_bot()
