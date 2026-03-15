import time
from web3 import Web3

# Usiamo l'endpoint corretto per le chiamate RPC
# Se questo fallisce, il bot ci dirà esattamente perché
rpc_url = "https://node.mainnet.vechain.energy" 
w3 = Web3(Web3.HTTPProvider(rpc_url))

print("--- AVVIO TEST BOT ---")

if not w3.is_connected():
    print("❌ Errore: Impossibile connettersi al nodo.")
    # Non usiamo sys.exit(1) qui, così vediamo se il resto gira
else:
    print("✅ Connessione riuscita!")
    try:
        block = w3.eth.block_number
        print(f"Blocco attuale: {block}")
    except Exception as e:
        print(f"⚠️ Errore lettura blocco: {e}")

print("--- FINE TEST ---")
