import time
from web3 import Web3

print("🚀 Bot avviato (modalità semplice)...")

# Nodo di VeChain
rpc_url = "https://mainnet.vechain.org"
w3 = Web3(Web3.HTTPProvider(rpc_url))

while True:
    try:
        if w3.is_connected():
            print(f"✅ Connesso! Blocco attuale: {w3.eth.block_number}", flush=True)
        else:
            print("❌ Disconnesso...", flush=True)
    except Exception as e:
        print(f"⚠️ Errore: {e}", flush=True)
        
    time.sleep(60) # Aspetta 60 secondi
