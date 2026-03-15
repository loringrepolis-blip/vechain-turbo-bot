import requests
import time
import sys

# --- CONFIGURAZIONE ---
NODE_URL = "https://mainnet.vechain.org"
CONTRACT_ADDRESS = "0x34b56f892c9e977b9ba2e43ba64c27d368ab3c86"

print(f"🚀 RELAYER ATTIVO")
print(f"🎯 Target Contract: {CONTRACT_ADDRESS}")
print(f"⚡ Modalità: Monitoraggio Alta Velocità\n")

def check_contract_activity():
    """
    Verifica se ci sono stati cambiamenti recenti nell'account del contratto.
    In un Relayer reale, qui interrogheremmo gli Event Log per 'NewProposal'.
    """
    url = f"{NODE_URL}/accounts/{CONTRACT_ADDRESS}"
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"⚠️ Errore polling contratto: {e}")
    return None

def monitor_and_race():
    last_block_num = 0
    
    while True:
        try:
            # 1. Otteniamo l'ultimo blocco (Best Block)
            res = requests.get(f"{NODE_URL}/blocks/best", timeout=2)
            if res.status_code == 200:
                data = res.json()
                current_block = data['number']
                
                if current_block > last_block_num:
                    last_block_num = current_block
                    print(f"🧱 Blocco {current_block} rilevato. Analisi snapshot...", flush=True)
                    
                    # 2. CONTROLLO SNAPSHOT / PROPOSTA
                    # Qui inseriremo la chiamata specifica per vedere se il voto è aperto.
                    activity = check_contract_activity()
                    
                    # Se l'attività indica 'Voto Aperto':
                    # lancia_voto_prioritario() 
            
        except Exception as e:
            print(f"❌ Errore di rete: {e}")
        
        # Intervallo di 1 secondo (limite di sicurezza per i nodi pubblici)
        # Se usassimo un nodo dedicato, potremmo scendere a 500ms per essere ancora più veloci.
        time.sleep(1)

if __name__ == "__main__":
    try:
        monitor_and_race()
    except KeyboardInterrupt:
        print("\n🛑 Relayer fermato dall'utente.")
        sys.exit(0)
