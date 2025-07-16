import json
import paho.mqtt.client as mqtt
from config import (
    MQTT_BROKER,
    MQTT_PORT,
    MQTT_USERNAME,
    MQTT_PASSWORD,
    MQTT_TOPIC,
    SEUIL_CRITIQUE,
)
from envoi_email import envoyer_email, send_price_reply

# Dictionnaire prix simulés par matière
PRIX_SIMULES = {
    "fer": 87.0,
    "nickel": 90.5,
    "cuivre": 75.2,
    "aluminium": 60.0,
    "zinc": 45.3,
    "plomb": 50.8,
}

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("✅ Connecté au broker MQTT HiveMQ Cloud")
        client.subscribe(MQTT_TOPIC)
        print(f"📡 Abonné au topic : {MQTT_TOPIC}")
    else:
        print("❌ Connexion échouée, code:", rc)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        quantite = payload.get("quantite", -1)
        matiere = payload.get("matiere", "Inconnue")
        print(f"📥 Reçu : {payload}")

        if quantite < SEUIL_CRITIQUE:
            print(f"⚠️  ALERTE : Stock critique pour {matiere} ({quantite}) !")
            envoyer_email(matiere, quantite)  # Envoi de l'alerte email
            prix = PRIX_SIMULES.get(matiere.lower(), 80.0)  # Prix par défaut si matière inconnue
            send_price_reply(matiere, prix)  # Envoi simulé avec prix adapté

    except Exception as e:
        print("❌ Erreur de traitement du message :", e)

def main():
    client = mqtt.Client(client_id="detecteur_seuil", protocol=mqtt.MQTTv311)
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.tls_set()

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_forever()

if __name__ == "__main__":
    main()
