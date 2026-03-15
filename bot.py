import sys
import traceback
from web3 import Web3

def run_bot():
    print("🚀 Bot avviato su Render...")
    
    # Nodo pubblico ufficiale di VeChain (Mainnet)
    rpc_url = "https://mainnet.vechain.org"
    
    print(f"🔗 Connessione in corso a: {rpc_url}")
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    
    # Verifica della connessione
    if w3.is_connected():
        print("✅ Connessione stabilita con successo!")
        block_number = w3.eth.block_number
        print(f"📦 Blocco attuale sulla blockchain VeChain: {block_number}")
    else:
        # Se fallisce, solleviamo un errore per vederlo nei log
        raise Exception("❌ Impossibile connettersi al nodo VeChain.")

if __name__ == "__main__":
    try:
        run_bot()
    except Exception as e:
        print("❌ ERRORE CRITICO RILEVATO:")
        traceback.print_exc()
        sys.exit(1) # Questo dice a Render che il bot ha avuto un problema
