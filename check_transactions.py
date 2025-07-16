# check_transactions.py

import requests

ACCOUNT_ID = "0.0.6180551"
BASE_URL = "https://testnet.mirrornode.hedera.com/api/v1"

def get_transactions(account_id):
    url = f"{BASE_URL}/accounts/{account_id}/transactions?limit=5&order=desc"
    response = requests.get(url)

    if response.status_code == 200:
        transactions = response.json()["transactions"]
        print(f"\n🔎 Dernières transactions Hedera pour {account_id} :\n")

        for tx in transactions:
            print(f"🧾 Transaction ID : {tx['transaction_id']}")
            print(f"📦 Type          : {tx['name']}")
            print(f"📆 Timestamp     : {tx['consensus_timestamp']}")
            print(f"💸 Transferts     : {tx.get('transfers', 'N/A')}")
            print("─" * 40)
    else:
        print("❌ Erreur API :", response.text)

if __name__ == "__main__":
    get_transactions(ACCOUNT_ID)