from hedera import Client, TopicCreateTransaction
from config import OPERATOR_ID, OPERATOR_KEY

client = Client.for_testnet()
client.set_operator(OPERATOR_ID, OPERATOR_KEY)

def create_topic():
    tx = TopicCreateTransaction()
    response = tx.execute(client)
    receipt = response.get_receipt(client)
    topic_id = receipt.topic_id
    transaction_id = response.transaction_id

    print(f"✅ Topic ID créé : {topic_id}")
    print(f"🧾 Transaction ID : {transaction_id}")

    return topic_id, transaction_id