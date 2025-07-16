# generate_env.py

import config

def generate_env_file():
    with open(".env", "w") as f:
        f.write(f"OPERATOR_ID={config.OPERATOR_ID}\n")
        f.write(f"OPERATOR_KEY={config.OPERATOR_KEY}\n")
        f.write(f"HEDERA_TOPIC_ID={config.HEDERA_TOPIC_ID}\n")
    print("✅ Fichier .env généré avec succès !")

if __name__ == "__main__":
    generate_env_file()