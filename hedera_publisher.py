from dotenv import load_dotenv
import os
import json
from hedera import (
    Client,
    AccountId,
    PrivateKey,
    TopicId,
    TopicMessageSubmitTransaction,
)

load_dotenv()

OPERATOR_ID_STR = os.getenv("OPERATOR_ID")
OPERATOR_KEY_STR = os.getenv("OPERATOR_KEY")
TOPIC_ID_STR = os.getenv("TOPIC_ID")

if not OPERATOR_ID_STR or not OPERATOR_KEY_STR or not TOPIC_ID_STR:
    print("❌ Veuillez configurer OPERATOR_ID, OPERATOR_KEY et TOPIC_ID dans le fichier .env")
    exit(1)

try:
    operator_id = AccountId.fromString(OPERATOR_ID_STR)  # Conversion obligatoire ici
    operator_key = PrivateKey.fromString(OPERATOR_KEY_STR)
    topic_id = TopicId.fromString(TOPIC_ID_STR)
except Exception as e:
    print("❌ Erreur lors de la conversion des IDs :", e)
    exit(1)

client = Client.forTestnet()
client.setOperator(operator_id, operator_key)  # Passer des objets ici

def publish_contract():
    try:
        with open("contrat_a_publier.json", "r", encoding="utf-8") as f:
            contract = json.load(f)

        print("📄 Contrat chargé :", contract)
        print("🧾 Operator ID :", operator_id.toString())
        print("🔑 Operator Key (tronquée) :", OPERATOR_KEY_STR[:10] + "...")
        print("📌 Topic ID utilisé :", topic_id.toString())

        tx = TopicMessageSubmitTransaction() \
            .setTopicId(topic_id) \
            .setMessage(json.dumps(contract))

        response = tx.execute(client)
        receipt = response.getReceipt(client)

        print("✅ Message publié avec succès !")
        print("🧾 Transaction ID :", response.transactionId.toString())
        print("🆔 Topic ID :", topic_id.toString())
        print(f"🔗 Voir sur HashScan : https://hashscan.io/testnet/transaction/{response.transactionId.toString()}")

    except Exception as e:
        print("❌ Erreur lors de la publication :", e)

if __name__ == "__main__":
    publish_contract()