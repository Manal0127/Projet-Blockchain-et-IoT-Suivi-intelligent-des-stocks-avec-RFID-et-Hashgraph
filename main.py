#main.py
from email_reader import lire_reponse_prix
from contract_manager import finalize_contract, publish_contract_to_hashgraph
import json
import config
import subprocess
import sys
import os

def generate_env_file():
    with open(".env", "w") as f:
        f.write(f"OPERATOR_ID={config.OPERATOR_ID}\n")
        f.write(f"OPERATOR_KEY={config.OPERATOR_KEY}\n")
        f.write(f"TOPIC_ID={config.TOPIC_ID}\n")
    print("✅ Fichier .env généré pour Node.js")

def enregistrer_json_liste(contrat, fichier):
    anciens = []
    if os.path.exists(fichier):
        try:
            with open(fichier, "r", encoding="utf-8") as f:
                anciens = json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️ Attention : {fichier} est corrompu ou vide, création d'une nouvelle liste.")
            anciens = []

    anciens.append(contrat)

    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(anciens, f, indent=2, ensure_ascii=False)

    print(f"📦 Données enregistrées dans {fichier}")

matiere, prix = lire_reponse_prix()

if matiere and prix:
    print(f"✅ Réponse reçue: {matiere} à {prix} MAD")
    quantite = 15  # simulé ici, dans la réalité à lire depuis détecteur
    contrat = finalize_contract(matiere, quantite, prix)
    publish_contract_to_hashgraph(contrat)
else:
    print("⚠️ Aucun email de réponse valide trouvé.")
    sys.exit(0)

# Publication locale du contrat
enregistrer_json_liste(contrat, "publication_log.json")

generate_env_file()

with open("contrat_a_publier.json", "w", encoding="utf-8") as f:
    json.dump(contrat, f, indent=2, ensure_ascii=False)

print("🚀 Publication sur Hedera Hashgraph en cours...")
subprocess.run([sys.executable, "hedera_publisher.py"])


# ====== Confirmation automatique de réception via RFID ======
#print("🎯 Lancement de la surveillance RFID pour la confirmation de réception...")

# On lance confirm_reception.py et on attend sa fin (bloquant)
#result_confirm = subprocess.run([sys.executable, "confirm_reception.py"], capture_output=True, text=True)
#print("📤 Contenu stdout de confirm_reception.py :")
#"print(result_confirm.stdout)

# Ici tu peux aussi récupérer un retour de confirm_reception.py pour valider la confirmation
#if "Réception confirmée" not in result_confirm.stdout:
    #print("❌ Réception non confirmée, paiement annulé.")
    #sys.exit(1)

# ====== Paiement automatique (après confirmation) ======
print("💸 Lancement du paiement...")
try:
    result = subprocess.run(
        [sys.executable, "payment.py", matiere, str(prix)],
        capture_output=True,
        text=True,
        check=True
    )
    print("📤 Contenu stdout de payment.py :")
    print(result.stdout)

    lines = result.stdout.strip().splitlines()
    transaction_id = ""
    hashscan_url = ""

    for line in lines:
        if "Transaction ID final" in line:
            transaction_id = line.split("Transaction ID final:")[1].strip()
        if "HashScan URL final" in line:
            hashscan_url = line.split("HashScan URL final:")[1].strip()

    if transaction_id:
        print(f"🔗 Transaction HashScan : {hashscan_url}")
        contrat['transaction_id'] = transaction_id
        contrat['hashscan_url'] = hashscan_url

        enregistrer_json_liste(contrat, "paiement_log.json")
    else:
        print("⚠️ Transaction non détectée.")

except subprocess.CalledProcessError as e:
    print("❌ Le paiement a échoué :", e.stderr)