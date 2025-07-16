#confirm_reception.py
import paho.mqtt.client as mqtt
from hedera import Client, AccountId, PrivateKey, TopicMessageSubmitTransaction
from datetime import datetime
import json
import config

# --- Configuration MQTT ---
MQTT_BROKER = "ea4978aa1dec426d96d62b82a316fe56.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_TOPIC = "stock/matiere_premiere/MP_A"  # IMPORTANT: même topic que simulateur

# --- Initialisation Hedera Client ---
client = Client.forTestnet()
client.setOperator(
    AccountId.fromString(config.OPERATOR_ID),
    PrivateKey.fromString(config.OPERATOR_KEY)
)

# --- Callback quand un message est reçu ---
def on_message(client_mqtt, userdata, msg):
    try:
        payload = msg.payload.decode()
        print(f"📥 Message reçu sur '{msg.topic}': {payload}")

        data = json.loads(payload)
        matiere = data.get("matiere")
        quantite = data.get("quantite", 0)

        if not matiere or quantite <= 0:
            print("⚠️ Message incomplet ou invalide :", data)
            return

        confirmation = {
            "type": "reception_confirmation",
            "matiere": matiere,
            "quantite": quantite,
            "date": datetime.now().isoformat()
        }

        message_json = json.dumps(confirmation, ensure_ascii=False)

        transaction = TopicMessageSubmitTransaction() \
            .setTopicId(config.TOPIC_ID) \
            .setMessage(message_json) \
            .execute(client)

        receipt = transaction.getReceipt(client)
        transaction_id = transaction.transactionId.toString()

        print(f"✅ Réception confirmée pour {matiere} ({quantite} unités)")
        print(f"🔗 Voir sur HashScan : https://hashscan.io/testnet/transaction/{transaction_id}")

    except json.JSONDecodeError:
        print("❌ Erreur : Payload JSON invalide :", payload)
    except Exception as e:
        print("❌ Erreur lors de la publication sur Hedera :", e)

# --- Démarrage du client MQTT ---
client_mqtt = mqtt.Client()
client_mqtt.on_message = on_message

print(f"📡 Connexion au broker MQTT {MQTT_BROKER}:{MQTT_PORT}...")
client_mqtt.connect(MQTT_BROKER, MQTT_PORT, 60)

client_mqtt.subscribe(MQTT_TOPIC)
print(f"📶 Abonné au topic '{MQTT_TOPIC}' pour surveiller les réceptions RFID...\n")

client_mqtt.loop_forever()