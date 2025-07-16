# connect_hashgraph.py

from hedera import Client, PrivateKey, AccountId
from config import OPERATOR_ID, OPERATOR_PRIVATE_KEY

def connect_to_testnet():
    client = Client.for_testnet()
    client.set_operator(
        AccountId.from_string(OPERATOR_ID),
        PrivateKey.from_string(OPERATOR_PRIVATE_KEY)
    )
    print("✅ Connecté au réseau testnet de Hashgraph.")
    return client

# Test simple
if __name__ == "__main__":
    client = connect_to_testnet()