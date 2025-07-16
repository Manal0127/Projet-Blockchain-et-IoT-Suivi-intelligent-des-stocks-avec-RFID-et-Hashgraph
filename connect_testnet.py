# connect_testnet.py

from hedera import Client, AccountId, PrivateKey
from config import OPERATOR_ID, OPERATOR_PRIVATE_KEY

def connect_to_testnet():
    client = Client.forTestnet()
    client.setOperator(
        AccountId.fromString(OPERATOR_ID),
        PrivateKey.fromString(OPERATOR_PRIVATE_KEY)
    )
    print("✅ Connecté au testnet Hedera !")
    return client

if __name__ == "__main__":
    connect_to_testnet()