# contract_manager.py

import json
from datetime import datetime

# Charger le TOPIC_ID simulé
with open("config_local.json") as f:
    local_config = json.load(f)
TOPIC_ID = local_config.get("TOPIC_ID", "0.0.999999")

# Simule la finalisation d’un contrat
def finalize_contract(matiere, quantite, prix):
    contrat = {
        "matiere": matiere,
        "quantite": quantite,
        "prix": prix,
        "date": datetime.now().isoformat(),
        "topic_id": TOPIC_ID
    }
    print(f"📄 Contrat généré : {json.dumps(contrat, indent=2)}")
    return contrat

# Simule la publication du contrat sur Hashgraph
def publish_contract_to_hashgraph(contrat):
    print(f"🚀 Contrat publié (simulation) sur Hashgraph Topic {TOPIC_ID}")
    print(json.dumps(contrat, indent=2))
