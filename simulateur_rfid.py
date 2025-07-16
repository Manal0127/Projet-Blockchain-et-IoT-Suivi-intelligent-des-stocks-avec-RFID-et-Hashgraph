import paho.mqtt.client as mqtt
import json
import random
import time

# Configuration du broker MQTT HiveMQ Cloud
MQTT_BROKER = "ea4978aa1dec426d96d62b82a316fe56.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USERNAME = "hivemq.webclient.1752562013053"
MQTT_PASSWORD = "54*JB;aVhE,3o7vsXnP<"
MQTT_TOPIC = "stock/matiere_premiere/MP_A"

# Liste des matières
matieres = [
    {"code": "MP_A", "nom": "fer"},
    {"code": "MP_B", "nom": "cuivre"},
    {"code": "MP_C", "nom": "aluminium"},
    {"code": "MP_D", "nom": "zinc"},
    {"code": "MP_E", "nom": "nickel"},
    {"code": "MP_F", "nom": "plomb"},
]

def publish_random_stock():
    client = mqtt.Client(client_id="simulateur_stock", protocol=mqtt.MQTTv311)
    
    # 🔐 Authentification sécurisée pour HiveMQ Cloud
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.tls_set()  # Active TLS (sécurisé)

    # Connexion au broker
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_start()

    while True:
        mp = random.choice(matieres)
        quantite = random.randint(0, 100)
        payload = {
            "matiere": mp["nom"],
            "quantite": quantite
        }
        payload_str = json.dumps(payload)
        client.publish(MQTT_TOPIC, payload_str)
        print(f"📤 Publié sur {MQTT_TOPIC} : {payload_str}")
        time.sleep(5)

if __name__ == "__main__":
    print("🚀 Démarrage du simulateur RFID MQTT...")
    publish_random_stock()