import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from web3 import Web3

# 1. Funzione che avvia il server finto per Render
def run_dummy_server():
    print("🌐 Avvio server finto per Render...")
    server = HTTPServer(('0.0.0.0', 10000), SimpleHTTPRequestHandler)
    server.serve_forever()

# 2. AVVIO IMMEDIATO del server in background (non blocca il codice)
threading.Thread(target=run_dummy_server, daemon=True).start()

# 3. Ora facciamo girare il bot
print("🚀 Bot avviato!")
rpc_url = "https://mainnet.vechain.org"
w3 = Web3(Web3.HTTPProvider(rpc_url))

while True:
    try:
        if w3.is_connected():
            print(f"✅ Connesso! Blocco attuale: {w3.eth.block_number}")
        else:
            print("❌ Disconnesso...")
    except Exception as e:
        print(f"⚠️ Errore: {e}")
    time.sleep(60)
