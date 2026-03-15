from web3 import Web3
import time

# Usa un nodo pubblico o professionale (su Render non verrai bloccato!)
rpc_url = "https://mainnet.vechain.org" 
w3 = Web3(Web3.HTTPProvider(rpc_url))

def main():
    print("🚀 Bot avviato su Render!")
    if w3.is_connected():
        print(f"✅ Connesso! Blocco attuale: {w3.eth.block_number}")
    else:
        print("❌ Errore di connessione.")

if __name__ == "__main__":
    main()
