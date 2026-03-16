import os
import time
from web3 import Web3
from eth_account import Account

# --- CONFIGURAZIONE AGGIORNATA ---
# Usiamo il nodo ufficiale di VeChain
RPC_URL = "https://mainnet.vechain.org" 
CONTRACT_ADDRESS = "0x34b56f892c9e977b9ba2e43ba64c27d368ab3c86"
FUNCTION_SELECTOR = "0x56f1612f"

# Aggiungiamo un "travestimento" (User-Agent) per non farci bloccare dal nodo
web3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={'headers': {'User-Agent': 'Mozilla/5.0'}}))
PRIVATE_KEY = os.getenv("VECHAIN_PRIVATE_KEY")
