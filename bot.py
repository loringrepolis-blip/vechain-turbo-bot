import os
from eth_account import Account

# Disabilitiamo i log di avviso delle librerie eth-account
import logging
logging.getLogger('eth_account').setLevel(logging.CRITICAL)

def test_chiave():
    # Recuperiamo la chiave privata dai segreti di GitHub
    private_key = os.getenv("VECHAIN_PRIVATE_KEY")
    
    if not private_key:
        print("❌ ERRORE: La variabile 'VECHAIN_PRIVATE_KEY' non è stata trovata o è vuota!")
        return

    try:
        # Proviamo a convertire la chiave in un account
        account = Account.from_key(private_key)
        print("✅ TEST RIUSCITO!")
        print(f"🔑 Chiave privata caricata correttamente.")
        print(f"👤 Indirizzo pubblico generato: {account.address}")
        print("---")
        print("Il bot è pronto a firmare transazioni con questo indirizzo.")
    except Exception as e:
        print(f"❌ ERRORE: La chiave privata non è valida. Dettagli: {e}")

if __name__ == "__main__":
    test_chiave()
