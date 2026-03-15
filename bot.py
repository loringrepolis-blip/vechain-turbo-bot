import sys
from web3 import Web3

# Usiamo l'endpoint specifico per le chiamate RPC di VeChain
rpc_url = "https://node.mainnet.vechain.energy"

print("--- AVVIO BOT ---", flush=True)
print(f"Tentativo di connessione a {rpc_url}...", flush=True)

try:
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    
    if w3.is_connected():
        print("✅ Connessione stabilita!", flush=True)
        block = w3.eth.block_number
        print(f"Blocco attuale: {block}", flush=True)
    else:
        print("❌ Connessione fallita: il nodo non risponde correttamente.", flush=True)
        # Stampiamo più dettagli possibili
        print(f"Provider: {w3.provider}", flush=True)

except Exception as e:
    print(f"⚠️ Errore critico: {str(e)}", flush=True)
    sys.exit(1)

print("--- FINE ESECUZIONE ---", flush=True)
