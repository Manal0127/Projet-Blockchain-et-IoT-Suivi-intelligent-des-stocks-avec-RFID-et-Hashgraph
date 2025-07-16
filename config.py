# config.py

EMAIL_FROM = "manaloujghi981@gmail.com"            # Ton adresse Gmail       # expéditeur
EMAIL_PASSWORD = "wmrnjgjfkppmzxlo"   # mot de passe Gmail d'application
EMAIL_TO = "manaloujghi27@gmail.com"           # destinataire   # Tu peux te l'envoyer à toi-même pour test
EMAIL_SUBJECT = "Demande de prix"             # sujet par défaut
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Configuration du broker MQTT HiveMQ Cloud
MQTT_BROKER = "ea4978aa1dec426d96d62b82a316fe56.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USERNAME = "hivemq.webclient.1752562013053"
MQTT_PASSWORD = "54*JB;aVhE,3o7vsXnP<"
MQTT_TOPIC = "stock/matiere_premiere/MP_A"

SEUIL_CRITIQUE = 20

# hashgraph
OPERATOR_ID = "0.0.6180551"
OPERATOR_KEY = "302e020100300506032b657004220420b02ff436a6a8cc9b4ff1a24c9c683c292dda261a9504b510f398d0eeae1aada4"  # remplace par ta vraie clé
TOPIC_ID = "0.0.6351894"