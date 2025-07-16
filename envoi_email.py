import smtplib
from email.message import EmailMessage
from config import EMAIL_FROM, EMAIL_TO, EMAIL_SUBJECT, SMTP_SERVER, SMTP_PORT, EMAIL_PASSWORD

# Active/désactive l’envoi d’email (utile si tu veux juste tester sans spammer)
ENVOYER_EMAILS = True

def envoyer_email(matiere, quantite):
    if not ENVOYER_EMAILS:
        print(f"⚠️ Envoi d’email désactivé pour {matiere} (quantité: {quantite})")
        return

    msg = EmailMessage()
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg.set_content(
        f"""Bonjour fournisseur,

Le stock de la matière première suivante est critique :

- Matière : {matiere}
- Quantité restante : {quantite} unités

Veuillez nous envoyer le prix actuel pour générer le contrat de commande.

Cordialement,
Le système IoT de gestion de stock.
"""
    )
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)
            print(f"📧 Email envoyé à {EMAIL_TO} pour {matiere}.")
    except smtplib.SMTPResponseException as e:
        if e.smtp_code == 550 and "Daily user sending limit exceeded" in str(e.smtp_error):
            print("❌ Limite quotidienne d’envoi d’emails dépassée chez Gmail. Veuillez attendre ou changer de service SMTP.")
        else:
            print(f"❌ Erreur SMTP lors de l’envoi de l’email : {e.smtp_code} - {e.smtp_error}")
    except Exception as e:
        print(f"❌ Erreur lors de l’envoi de l’email : {e}")

def send_price_reply(matiere, prix):
    if not ENVOYER_EMAILS:
        print(f"⚠️ Envoi d’email désactivé pour la réponse simulée : {matiere} à {prix} MAD")
        return

    msg = EmailMessage()
    msg['Subject'] = f"Réponse de prix - {matiere}"
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_FROM
    msg.set_content(f"Prix pour {matiere}: {prix} MAD")
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print(f"[Fournisseur] Réponse simulée : {matiere} à {prix} MAD")
    except smtplib.SMTPResponseException as e:
        if e.smtp_code == 550 and "Daily user sending limit exceeded" in str(e.smtp_error):
            print("❌ Limite quotidienne d’envoi d’emails dépassée chez Gmail. Veuillez attendre ou changer de service SMTP.")
        else:
            print(f"❌ Erreur SMTP lors de l’envoi de la réponse : {e.smtp_code} - {e.smtp_error}")
    except Exception as e:
        print(f"❌ Erreur lors de l’envoi de la réponse : {e}")