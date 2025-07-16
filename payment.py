# payment.py

from hedera import Client, AccountId, PrivateKey, TransferTransaction, Hbar
import config
import sys

# --- Vérification des arguments ---
if len(sys.argv) < 3:
    print("[Erreur] Veuillez fournir la matière et le prix en arguments.")
    print("Exemple : python payment.py nickel 90.5")
    sys.exit(1)

matiere = sys.argv[1]
prix_str = sys.argv[2]

try:
    montant = float(prix_str)
except ValueError:
    print(f"[Erreur] Prix invalide : {prix_str}")
    sys.exit(1)

# --- Initialisation du client Hedera ---
client = Client.forTestnet()
client.setOperator(AccountId.fromString(config.OPERATOR_ID), PrivateKey.fromString(config.OPERATOR_KEY))

def effectuer_paiement(dest_account_id_str, amount_hbar, memo):
    try:
        dest_account_id = AccountId.fromString(dest_account_id_str)

        tx = (
            TransferTransaction()
            .addHbarTransfer(AccountId.fromString(config.OPERATOR_ID), Hbar(-amount_hbar))
            .addHbarTransfer(dest_account_id, Hbar(amount_hbar))
            .setTransactionMemo(memo)
        )

        response = tx.execute(client)
        receipt = response.getReceipt(client)

        print("Statut de la transaction:", receipt.status.toString())
        print("Transaction ID:", response.transactionId.toString())

        transaction_id_str = response.transactionId.toString()
        hashscan_url = f"https://hashscan.io/testnet/transaction/{transaction_id_str}"
        print("Lien HashScan:", hashscan_url)

        return transaction_id_str, hashscan_url

    except Exception as e:
        print("Erreur lors du paiement:", e)
        return None, None

if __name__ == "__main__":
    dest = "0.0.6180961"  # ID du fournisseur, à modifier si besoin
    memo = f"Paiement effectué pour {matiere} : {montant} MAD"
    transaction_id_str, hashscan_url = effectuer_paiement(dest, montant, memo)

    if transaction_id_str and hashscan_url:
        print(f"Transaction ID final: {transaction_id_str}")
        print(f"HashScan URL final: {hashscan_url}")