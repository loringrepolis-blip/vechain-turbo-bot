import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from web3 import Web3

# 1. Avviamo un piccolo server web finto che soddisfa Render
def run_dummy_server():
    server = HTTPServer(('0.0.0.0', 10000), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# 2. Ora facciamo girare il tuo bot come al solito
rpc_url = "https://mainnet.vechain.org"
w3 = Web3(Web3.HTTPProvider(rpc_url))

print("🚀 Bot avviato senza errori di porta!")

while True:
    try:
        if w3.is_connected():
            print(f"✅ Connesso! Blocco attuale: {w3.eth.block_number}")
        else:
            print("❌ Disconnesso...")
    except Exception as e:
        print(f"⚠️ Errore: {e}")
    time.sleep(60)
