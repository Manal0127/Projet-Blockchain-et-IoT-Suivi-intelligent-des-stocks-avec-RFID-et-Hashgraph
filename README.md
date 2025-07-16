Objectif général
Mettre en oeuvre une solution IoT sécurisée basée sur la technologie Hashgraph et des smart contracts dynamiques, permettant de simuler la gestion automatisée des stocks de matières premières à l’aide de tags RFID. Le projet intègre l’envoi d’emails automatisés pour la mise à jour des prix, la génération de smart contracts mis à jour, et un flux agentique garantissant la réactivité du système.
1.	Simulation 
•	RFID But : Simuler la détection d’une matière première par un capteur RFID. 
•	Fichier utilisé : simulateur_rfid.py 
•	Action : Envoie un message JSON contenant matiere et quantite à un topic MQTT (stock/matiere_premiere/MP_A).
 
2.	Détection seuil critique 
•	But : Vérifier si la quantité détectée est en dessous du seuil critique (20). 
•	Fichier utilisé : detecteur_seuil.py 
•	Action : Se connecte au même topic MQTT Si la quantite < SEUIL_CRITIQUE, passe à l’étape suivante (envoi email).

 
3.	Envoi email fournisseur
•	But : Demander un prix au fournisseur.
•	Fichier utilisé : envoi_email.py
•	Action : Génère et envoie un email contenant une demande de prix de la matière détectée en faible stock.

4.	Réception email et lecture de prix
•	But : Lire automatiquement la réponse du fournisseur et extraire le prix.
•	Fichier utilisé : email_reader.py 
•	Action : Scanne la boîte mail du client Extrait la matière et le prix de la réponse reçue.

6.	Envoi Prix au client (automatique) 
•	But : Informer le client du prix reçu. 
•	Fichier utilisé : Optionnel, peut être intégré dans email_reader.py ou main.py avec un renvoi du prix à l’acheteur.

7.	Déclenchement de commande (Transaction) 
•	But : Générer le contrat à partir des infos de matière, quantité et prix. 
•	Fichiers utilisés : 
main.py : pilote central 
contract_manager.py : crée le JSON du contrat 
hedera_publisher.py : publie ce contrat sur Hedera
•	Action : 
Crée un fichier contrat_a_publier.json 
Publie sur Hashgraph (testnet) via Hedera SDK
8.	Transaction de confirmation de commande 
•	But : Assurer qu’une transaction Hedera valide le contrat. 
•	Fichier utilisé : hedera_publisher.py 
•	Action : 
Encode le contrat en JSON 
Le publie sur un TopicId Hedera 
Affiche le HashScan de la transaction

9.	Confirmation de réception (automatique ou manuelle) 
•	But : S’assurer que la matière a été livrée. 
•	Fichier utilisé : confirm_reception.py (optionnel si étape supprimée) 
•	Action : 
Attente de message MQTT sur stock/reception 
Génère une transaction de confirmation sur Hashgraph

10.	Transaction de Paiement 
•	But : Effectuer le paiement du fournisseur via Hedera (simulateur). 
•	Fichier utilisé : payment.py 
•	Action : 
Effectue un transfert de HBAR avec un memo = "Paiement effectué pour nickel : 90 MAD" 
Affiche la transaction dans HashScan
