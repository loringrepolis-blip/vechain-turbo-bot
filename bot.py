import requests
from web3 import Web3

# Usiamo una sessione con un User-Agent "finto" per sembrare un browser
class CustomHTTPProvider(Web3.HTTPProvider):
    def make_request(self, method, params):
        headers = {'User-Agent': 'Mozilla/5.0'}
        # Sostituiamo il metodo di richiesta standard con uno che usa 'requests'
        response = requests.post(self.endpoint_uri, json={'jsonrpc':'2.0', 'method':method, 'params':params, 'id':1}, headers=headers)
        return response.json()

# Endpoint ufficiale
rpc_url = "https://mainnet.vechain.org"
w3 = Web3(CustomHTTPProvider(rpc_url))

print("--- TENTATIVO CON HEADER BROWSER ---")

if w3.is_connected():
    print(f"✅ Connesso! Blocco: {w3.eth.block_number}")
else:
    print("❌ Ancora fallito. Il nodo sta bloccando la connessione.")
