import os
import time
from web3 import Web3
from eth_account import Account

# CONFIGURAZIONE
RPC_URL = "https://node-mainnet.vechain.energy"
CONTRACT_ADDRESS = "0x34b56f892c9e977b9ba2e43ba64c27d368ab3c86"
web3 = Web3(Web3.HTTPProvider(RPC_URL))
PRIVATE_KEY = os.getenv("VECHAIN_PRIVATE_KEY")

def trova_wallet_ricchi():
    """
    Questa funzione scansiona la blockchain per trovare chi ha 
    interagito con il contratto recentemente (i potenziali target).
    """
    print("🔍 Scansione blockchain per trovare wallet target...")
    try:
        # Cerchiamo le ultime 100 transazioni verso il contratto
        # (Semplificato: domani il bot leggerà i delegati reali dal contratto)
        return [
            "0x7c07641a70d1c9216b5345f357b7ba501f16c6e", # Esempio di wallet balena
            "0x398897..." # Qui il bot aggiungerà quelli che trova live
        ]
    except:
        return []

def invia_voto(target, account, nonce):
    payload = "0x56f1612f" + target.lower().replace('0x', '').zfill(64)
    tx = {
        'nonce': nonce, 'to': CONTRACT_ADDRESS, 'value': 0,
        'gas': 160000, 'gasPrice': web3.to_wei(120, 'gwei'),
        'data': payload, 'chainId': web3.eth.chain_id
    }
    signed = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    return web3.eth.send_raw_transaction(signed.rawTransaction)

def main():
    account = Account.from_key(PRIVATE_KEY)
    print(f"🚀 Relayer attivo per {account.address}")
    
    mentre_aspettiamo = True
    while mentre_aspettiamo:
        try:
            # 1. Trova i bersagli in automatico
            targets = trova_wallet_ricchi()
            
            # 2. Prova a votare per il primo
            nonce = web3.eth.get_transaction_count(account.address)
            tx_hash = invia_voto(targets[0], account, nonce)
            
            print(f"✅ SNAPSHOT APERTO! Voto inviato: {web3.to_hex(tx_hash)}")
            
            # 3. Se il primo passa, spara per tutti gli altri
            for i in range(1, len(targets)):
                nonce += 1
                invia_voto(targets[i], account, nonce)
                print(f"🔥 Voto extra inviato per: {targets[i]}")
            
            mentre_aspettiamo = False # Lavoro finito
        except Exception as e:
            print("⏳ Snapshot chiuso. Riprovo tra 30 secondi...")
            time.sleep(30)

if __name__ == "__main__":
    main()
