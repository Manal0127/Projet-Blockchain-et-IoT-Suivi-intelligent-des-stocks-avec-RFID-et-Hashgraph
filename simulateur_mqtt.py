#simulateur_mqtt.py
import json
import paho.mqtt.publish as publish

# --- Configuration MQTT ---
MQTT_BROKER = "ea4978aa1dec426d96d62b82a316fe56.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_TOPIC = "stock/matiere_premiere/MP_A"  # IMPORTANT: même topic que simulateur

message = {
    "matiere": "nickel",
    "quantite": 15
}

publish.single(
    MQTT_TOPIC,
    json.dumps(message),
    hostname=MQTT_BROKER,
    port=MQTT_PORT
)

print(f"📤 Message simulé envoyé : {message}")