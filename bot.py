import requests

print("--- CONNESSIONE NATIVA VECHAIN (REST API) ---", flush=True)

# L'indirizzo ufficiale per chiedere qual è l'ultimo blocco
url = "https://mainnet.vechain.org/blocks/best"

try:
    # Facciamo la richiesta al nodo
    response = requests.get(url, timeout=10)
    
    # Se il nodo risponde "OK" (codice 200)
    if response.status_code == 200:
        data = response.json()
        block_number = data.get("number")
        print(f"✅ VITTORIA! Connesso alla blockchain di VeChain.", flush=True)
        print(f"🧱 Blocco attuale: {block_number}", flush=True)
        print(f"⏰ Timestamp del blocco: {data.get('timestamp')}", flush=True)
    else:
        print(f"❌ Errore dal server. Codice: {response.status_code}", flush=True)
        print(f"Dettaglio: {response.text}", flush=True)

except Exception as e:
    print(f"⚠️ Errore di rete: {e}", flush=True)

print("--- FINE TEST ---", flush=True)
