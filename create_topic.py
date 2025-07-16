from hedera import Client, TopicCreateTransaction, AccountId, PrivateKey
from config import OPERATOR_ID, OPERATOR_KEY
import json

# Convertir la chaîne OPERATOR_ID en AccountId
operator_account_id = AccountId.fromString(OPERATOR_ID)

# Convertir la chaîne OPERATOR_KEY en PrivateKey
operator_private_key = PrivateKey.fromString(OPERATOR_KEY)

# Initialiser le client Hedera testnet
client = Client.forTestnet()
client.setOperator(operator_account_id, operator_private_key)

def create_topic():
    try:
        print("⏳ Création d'un topic Hedera HCS en cours...")

        # Créer le topic
        tx = TopicCreateTransaction()
        response = tx.execute(client)

        # Attendre confirmation
        receipt = response.getReceipt(client)

        # Récupérer le topic ID et transaction ID
        topic_id = receipt.topicId
        transaction_id = response.transactionId

        # Afficher les IDs lisiblement
        print(f"✅ Topic créé avec ID : {topic_id.toString()}")
        print(f"🧾 Transaction ID     : {transaction_id.toString()}")

        # Enregistrer le TOPIC_ID dans un fichier local
        with open("config_local.json", "w") as f:
            json.dump({"TOPIC_ID": topic_id.toString()}, f, indent=2)
            print("💾 Topic ID sauvegardé dans config_local.json")

        return topic_id, transaction_id

    except Exception as e:
        print(f"❌ Erreur lors de la création du topic : {e}")

if __name__ == "__main__":
    create_topic()