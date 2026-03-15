import sys
import subprocess
import time
from web3 import Web3

# 1. LANCIA IL SERVER WEB COME PROCESSO SEPARATO (render lo vedrà separatamente)
# Creiamo un piccolo file temporaneo per il server web
with open("dummy_server.py", "w") as f:
    f.write("""
from http.server import HTTPServer, SimpleHTTPRequestHandler
server = HTTPServer(('0.0.0.0', 10000), SimpleHTTPRequestHandler)
server.serve_forever()
""")

# Avviamo il server finto come processo separato
subprocess.Popen([sys.executable, "dummy_server.py"])
print("🌐 Server finto avviato in background.")

# 2. ORA IL BOT GIRA DA SOLO, LIBERO E SENZA INTERFERENZE
print("🚀 Bot principale avviato!")
rpc_url = "https://mainnet.vechain.org"
w3 = Web3(Web3.HTTPProvider(rpc_url))

while True:
    try:
        # Questo print apparirà finalmente nei log di Render
        if w3.is_connected():
            print(f"✅ Connesso! Blocco attuale: {w3.eth.block_number}")
        else:
            print("❌ Disconnesso, riprovo...")
    except Exception as e:
        print(f"⚠️ Errore: {e}")
    time.sleep(60)
