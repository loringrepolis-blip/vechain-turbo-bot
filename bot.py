def check_voting_status():
    """
    Verifica se il contratto accetta voti in questo preciso istante.
    """
    # Il data esadecimale (da recuperare dall'ABI del contratto)
    # Esempio: 0x... (Hex della funzione di controllo)
    payload = {
        "to": CONTRACT_ADDRESS,
        "data": "0x..." # Questo è il selettore della funzione isVotingActive
    }
    
    try:
        # Chiamata al nodo per lo stato corrente
        response = requests.post(f"{NODE_URL}/accounts/{CONTRACT_ADDRESS}", json=payload)
        status = response.json().get("data")
        
        # Se il risultato è '0x000...01' (ovvero true), allora votiamo!
        if status == "0x0000000000000000000000000000000000000000000000000000000000000001":
            return True
    except Exception as e:
        print(f"⚠️ Errore controllo stato voto: {e}")
    return False
