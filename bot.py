import time
from web3 import Web3

# Nodo di VeChain
rpc_url = "https://mainnet.vechain.org"
w3 = Web3(Web3.HTTPProvider(rpc_url))

print("🚀 Bot avviato e in attesa...")

# Invece di chiudersi, facciamo un loop infinito
while True:
    try:
        if w3.is_connected():
            print(f"✅ Connesso! Blocco attuale: {w3.eth.block_number}")
        else:
            print("❌ Disconnesso, riprovo...")
    except Exception as e:
        print(f"⚠️ Errore: {e}")
        
    time.sleep(60) # Aspetta 60 secondi prima del prossimo controllo
