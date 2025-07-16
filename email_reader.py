import imaplib
import email
import re
import traceback
from config import EMAIL_FROM, EMAIL_PASSWORD

def get_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                charset = part.get_content_charset() or 'utf-8'
                try:
                    return part.get_payload(decode=True).decode(charset, errors='replace')
                except Exception:
                    return part.get_payload(decode=True).decode("utf-8", errors="replace")
    else:
        charset = msg.get_content_charset() or 'utf-8'
        try:
            return msg.get_payload(decode=True).decode(charset, errors='replace')
        except Exception:
            return msg.get_payload(decode=True).decode("utf-8", errors="replace")

def decode_subject(subject):
    try:
        decoded_fragments = email.header.decode_header(subject)
        decoded_subject = ''
        for fragment, encoding in decoded_fragments:
            if isinstance(fragment, bytes):
                encoding = encoding or 'utf-8'
                decoded_subject += fragment.decode(encoding, errors='replace')
            else:
                decoded_subject += fragment
        return decoded_subject
    except Exception:
        return subject

def lire_reponse_prix():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        mail.login(EMAIL_FROM, EMAIL_PASSWORD)
        mail.select("inbox")

        # Recherche tous les emails non lus sans critère de sujet (évite erreurs d'encodage)
        status, data = mail.search(None, 'UNSEEN')
        if status != 'OK':
            print("❌ Impossible de chercher les emails.")
            return None, None

        email_ids = data[0].split()

        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            if status != 'OK':
                continue
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject = decode_subject(msg.get("Subject", ""))
            # Filtrer en Python le sujet pour contenir "Réponse de prix"
            if "Réponse de prix" in subject:
                body = get_email_body(msg)
                # Rechercher le motif "Prix pour <matiere>: <prix>"
                match = re.search(r"Prix pour (\w+):\s*([0-9.,]+)", body)
                if match:
                    matiere = match.group(1)
                    prix = float(match.group(2).replace(",", "."))
                    mail.store(email_id, '+FLAGS', '\\Seen')  # Marquer comme lu
                    mail.logout()
                    return matiere, prix

        mail.logout()
        return None, None

    except Exception as e:
        print("❌ Erreur lecture email :")
        traceback.print_exc()
        return None, None