// publish_contract.js

const {
  Client,
  TopicMessageSubmitTransaction,
} = require("@hashgraph/sdk");
require("dotenv").config();
const fs = require("fs");

// Charger config depuis .env
const operatorId = process.env.OPERATOR_ID;
const operatorKey = process.env.OPERATOR_KEY;
const topicId = process.env.TOPIC_ID;

if (!operatorId || !operatorKey || !topicId) {
  console.error("❌ OPERATOR_ID, OPERATOR_KEY et TOPIC_ID doivent être définis dans .env");
  process.exit(1);
}

// ✅ Afficher les valeurs pour débogage
console.log("🧾 Operator ID :", operatorId);
console.log("🔑 Operator Key (tronquée) :", operatorKey.slice(0, 10) + "...");
console.log("📌 Topic ID utilisé :", topicId);

// Initialiser client testnet
const client = Client.forTestnet().setOperator(operatorId, operatorKey);

// Fonction pour publier un message sur Hedera
async function publishMessage(message) {
  try {
    const tx = new TopicMessageSubmitTransaction({
      topicId: topicId,
      message: JSON.stringify(message),
    });

    const submitTx = await tx.execute(client);
    const receipt = await submitTx.getReceipt(client);

    console.log("✅ Message publié avec succès !");
    console.log("🧾 Transaction ID :", submitTx.transactionId.toString());
    console.log("🆔 Topic ID :", topicId);

    // 🔗 Afficher le lien HashScan pour la transaction
    console.log(`🔗 Voir sur HashScan : https://hashscan.io/testnet/transaction/${submitTx.transactionId.toString()}`);

  } catch (err) {
    console.error("❌ Erreur lors de la publication :", err);
  }
}

// Fonction principale
async function main() {
  try {
    const contract = JSON.parse(fs.readFileSync("contrat_a_publier.json"));
    await publishMessage(contract);
  } catch (err) {
    console.error("❌ Erreur de lecture du fichier contrat :", err.message);
  }
}

main();
