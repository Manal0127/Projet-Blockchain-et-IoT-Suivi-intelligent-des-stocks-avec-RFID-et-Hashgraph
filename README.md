# 📦 Suivi Intelligent des Stocks avec RFID, MQTT & Hedera Hashgraph

## 🎯 Objectif général

Mettre en œuvre une solution **IoT sécurisée** basée sur la technologie **Hashgraph** et des **smart contracts dynamiques**, permettant de simuler la **gestion automatisée des stocks** de matières premières à l’aide de **tags RFID**.  
Le projet intègre :

- la **détection automatique** via simulateur RFID,
- l’**envoi d’emails** automatisés pour la mise à jour des prix,
- la **génération et publication de contrats intelligents** sur Hedera,
- un **flux agentique** garantissant la réactivité du système.

---

## 🧩 Étapes du Projet

### 1. Simulation RFID
- **But** : Simuler la détection d’une matière première par un capteur RFID.  
- **Fichier utilisé** : `simulateur_rfid.py`  
- **Action** : Envoie un message JSON (`matiere`, `quantite`) au topic MQTT `stock/matiere_premiere/MP_A` via HiveMQ Cloud.

---

### 2. Détection du Seuil Critique
- **But** : Vérifier si la quantité détectée est inférieure au seuil critique (20).  
- **Fichier utilisé** : `detecteur_seuil.py`  
- **Action** : Se connecte au même topic MQTT. Si `quantite < SEUIL_CRITIQUE`, déclenche l’envoi d’un email au fournisseur.

---

### 3. Envoi Email au Fournisseur
- **But** : Demander un prix au fournisseur.  
- **Fichier utilisé** : `envoi_email.py`  
- **Action** : Envoie un email avec une demande de prix pour la matière en stock critique.

---

### 4. Lecture de la Réponse Email (Prix)
- **But** : Lire automatiquement la réponse du fournisseur et extraire le prix.  
- **Fichier utilisé** : `email_reader.py`  
- **Action** : Scanne la boîte mail du client, identifie la réponse et extrait la matière et son prix.

---

### 5. Envoi Prix au Client (Optionnel)
- **But** : Informer le client du prix reçu.  
- **Fichier utilisé** : intégré dans `main.py` ou `email_reader.py`  
- **Action** : Affiche ou transmet le prix à l’utilisateur.

---

### 6. Déclenchement de la Commande (Smart Contract)
- **But** : Générer un contrat intelligent basé sur la matière, quantité et prix.  
- **Fichiers utilisés** :
  - `main.py` – Script principal
  - `contract_manager.py` – Génère le JSON du contrat
  - `hedera_publisher.py` – Publie le contrat sur Hedera Hashgraph  
- **Action** :
  - Génère `contrat_a_publier.json`
  - Publie la transaction sur Hedera (testnet)

---

### 7. Transaction de Confirmation de Commande
- **But** : Confirmer officiellement la commande sur Hedera.  
- **Fichier utilisé** : `hedera_publisher.py`  
- **Action** : Encode le contrat en JSON, publie dans le `TOPIC_ID`, et affiche le lien vers **HashScan**.

---

### 8. (Optionnel) Confirmation de Réception
- **But** : Confirmer que les matières premières ont été livrées.  
- **Fichier utilisé** : `confirm_reception.py`  
- **Action** :
  - Attente de message sur topic `stock/reception`
  - Génère une transaction de confirmation dans Hedera Hashgraph

---

### 9. Paiement Automatique
- **But** : Simuler le paiement du fournisseur après confirmation.  
- **Fichier utilisé** : `payment.py`  
- **Action** :
  - Transfert de HBAR simulé vers le compte fournisseur
  - Ajoute un mémo : `"Paiement effectué pour nickel : 90 MAD"`
  - Affiche lien de la transaction dans **HashScan**

---

## ✅ Conclusion

Ce projet met en œuvre un **système IoT intelligent** pour la gestion des stocks critiques en intégrant des **capteurs simulés**, le **protocole MQTT**, et la **technologie blockchain Hedera Hashgraph**.  
Grâce à une architecture automatisée et sécurisée, chaque étape – de la détection à la transaction – est tracée, transparente et exécutable sans intervention humaine directe.

Le projet constitue une **preuve de concept puissante** des capacités de l’IoT combinées aux **smart contracts** pour des applications industrielles modernes.

---
