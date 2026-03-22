import time
import requests
import os
from thor_devkit import transaction, abi
from thor_devkit.cry import secp256k1
from eth_utils import to_checksum_address

# =========================================================
# 1. CONFIGURAZIONE RPC (RIDONDANZA)
# =========================================================
RPC_NODES = [
    "https://mainnet.vechain.org",
    "https://node-mainnet.vechain.energy",
    "https://sync-mainnet.vechain.org"
]

# =========================================================
# 2. BERSAGLI (45 VETERANI + BALENA)
# =========================================================
TARGET_VOTERS = [
    "0x6Fd6FF266bc7091D78A2FEd1Bd42dEb20d4e80c0", "0x2e5fB6686e1254fc9AefB07661E605951d514b86",
    "0x50507A0A67762c2Ac08D7cdC797556c1AfF4CD43", "0x495CA57B013B8905d011FCAFb4734af056D5378B",
    "0x061ba2F1BA032322c51F68dfDDF611eEb2ce7389", "0x25A9f09d5e615a51187A08DeFcBe4768Cbc8cC9B",
    "0x5460EeCe04562b4C4eD19fe903f39D3DDa70F614", "0x4616E04B034E691fe2af932A023286F71fbD3a19",
    "0x89496Fba13C3A818eb07E1bC1Bb7aAc01D84d952", "0x316CeCef82E9cf471406F9D0839c4C69676Cd651",
    "0x003dF460FBf8e9950a7B8B5D4BcDb06bf88a7A3d", "0x15ac4852195492aE7C4dA22a32f6Bb6E660D7722",
    "0x2DE475D950ceAc562BE0862C548C4cBa7649bDf8", "0x201b2D9a290c19c1f950D076Cc3bd28ADDd57BCD",
    "0xcd0dCE2a0ecbA8A5b43ffbC65b03528F1f11e3A6", "0x4Cf9EEC522750dE69e0C69866a1f624a292f147A",
    "0x2c04f421753bC29f50F58C3a944Cac46EdC99A41", "0xd66098064675b5AD9e7C544e6D36640146CF53a0",
    "0x68E162405821e4fDdA4637daF2F012428B16E207", "0x351625959c647A4D2d0D3F0Cec696ddac384018c",
    "0x3558982C3Df4974CF1b2E597b1F0803b342D3758", "0xed0508F3a8508845d5eBF3b601b006e237082bfF",
    "0x4D7401E8f5Ad7B561B1b43cE6499EE8CBdB8537A", "0x708AfCaF3e2F02Ed9b872398e7a7F021DE0Ca67b",
    "0x9657b64864560Ef13d4dDf889E35C17D45092AD3", "0x98A8A68A729Fc986A22F29aaABA77434EF52fD17",
    "0x21c224Bc8d030CC4dbe3eF2938a99a12B668B9F4", "0x67Db2c452fd27102Af7976657179BB6B5AFC67E7",
    "0xC9280f569572097428352a5dC28C28204172Be49", "0x8ABd92b3dF629a2F40aC68B1063Ff32cdaea0604",
    "0x115427b433F877A28f589956CF2Fe4Fd6FDde3Eb", "0x1c93BeEd795aE65d1F1bDbcd2F1bCf24a5647AF1",
    "0x6Aa55DF947125DB8D69Cf7297533AB6F7B09Af4f", "0x5d224C69fB973ec2fDA71612Fc826a30FE5eED59",
    "0x2205D7686503bb2f12f8d3abfA4476121B693917", "0xE49ec1F782A9fC2297ED0f83848CaD281cDD34E5",
    "0x3Fa88eAAf3Ab227cf1046D42C329a0D9546229B6", "0xC95569603d63b1833bFe1f03D7E0783244405769",
    "0xCDa56ea1dd570b3344D2233F8f1E378997995D4b", "0x29C1D55F4Ec41B29dF0F484F23224F108F3827EC",
    "0x02C6185360d6A5aECD50bf54f5371249D3627dec", "0x7eC8D7DDAb8413Cc392A0fd38933986213ce51ec",
    "0x6f9bbE9393Cc977A4478242CCf1DD5709d50F608", "0xE12fe2032Df88Ff1FfdCDaf9cA8dC0334F1BE5f3",
    "0xd4d13a8983edF3e45830a341DcB2eF1d405DEe5B",
    "0x155532F95117CF298CA293C7572830d48B89AE27" # LA BALENA
]

CONTRACT_DAO = "0x89A00Bb0947a30FF95BEEf77a66AEDe3842Fe5B7"
ROUND_ID = 91 
DRY_RUN = True # <--- CAMBIARE IN FALSE PER DOMATTINA

# =========================================================
# 3. LOGICA DI SUPPORTO (DALLA VERSIONE TEST FUNZIONANTE)
# =========================================================

def get_block_ref():
    for node in RPC_NODES:
        try:
            res = requests.get(f"{node}/blocks/best", timeout=5)
            return res.json()['id'][:18]
        except:
            continue
    return "0x0000000000000000"

def codifica_voto_infallibile(voto_abi, voter, round_id):
    v_clean = to_checksum_address(voter.strip().lower())
    # Usiamo la lista, che ha dimostrato di funzionare nel test
    return "0x" + voto_abi.encode([v_clean, round_id]).hex()

def prepara_camion(private_key_hex):
    voto_abi = abi.Function({
        "type": "function",
        "name": "castVoteOnBehalfOf",
        "inputs": [
            {"type": "address", "name": "voter"},
            {"type": "uint256", "name": "roundId"}
        ],
        "outputs": [],
        "stateMutability": "nonpayable"
    })

    pk_clean = private_key_hex.strip().replace("0x", "")
    clauses = []
    
    print(f"⚙️ Impacchettamento di {len(TARGET_VOTERS)} voti...")
    for voter in TARGET_VOTERS:
        payload = codifica_voto_infallibile(voto_abi, voter, ROUND_ID)
        clauses.append({"to": CONTRACT_DAO, "value": 0, "data": payload})

    tx = transaction.Transaction({
        "chainTag": 0x4a,
        "blockRef": get_block_ref(),
        "expiration": 32,
        "clauses": clauses,
        "gasPriceCoef": 128,
        "gas": 30000 * len(clauses) + 150000,
        "dependsOn": None,
        "nonce": int(time.time())
    })
    
    priv_key_bytes = bytes.fromhex(pk_clean)
    tx.set_signature(secp256k1.sign(tx.get_signing_hash(), priv_key_bytes))
    return tx

def lancia_sniper(tx):
    raw_tx = "0x" + tx.encode().hex()
    if DRY_RUN:
        return {"status": "Simulazione completata con successo."}

    for nodo in RPC_NODES:
        try:
            res = requests.post(f"{nodo}/transactions", json={"raw": raw_tx}, timeout=5)
            if res.status_code == 200:
                return res.json()
        except:
            continue
    return {"error": "Tutti i nodi hanno fallito l'invio."}

if __name__ == "__main__":
    pk = os.getenv("VECHAIN_PRIVATE_KEY") 
    if pk:
        print("🔑 Chiave rilevata correttamente.")
        try:
            camion = prepara_camion(pk)
            risultato = lancia_sniper(camion)
            print(f"✅ RISULTATO: {risultato}")
        except Exception as e:
            print(f"❌ Errore critico: {e}")
    else:
        print("❌ ERRORE: Secret non trovato.")
