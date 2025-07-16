import subprocess
import config

def generate_env_file():
    with open(".env", "w") as f:
        f.write(f"OPERATOR_ID={config.OPERATOR_ID}\n")
        f.write(f"OPERATOR_KEY={config.OPERATOR_KEY}\n")
        f.write(f"TOPIC_ID={config.TOPIC_ID}\n")
    print("✅ Fichier .env généré avec succès !")

def run_node_script():
    print("🚀 Lancement de publish_contract.js via Node.js ...")
    result = subprocess.run(["node", "publish_contract.js"], capture_output=True, text=True)
    print("---- Sortie du script Node.js ----")
    print(result.stdout)
    if result.stderr:
        print("---- Erreurs éventuelles ----")
        print(result.stderr)

if __name__ == "__main__":
    generate_env_file()
    run_node_script()