from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

from app.config import settings


class EmailService:

    @staticmethod
    async def envoyer_recu(destinataire: str, nom: str, numero_recu: str,
                           montant: float, campagne: str) -> bool:
        sujet = f"Reçu fiscal - {settings.app_name}"
        html = f"""
        <html><body style="font-family:Arial,sans-serif;">
        <h2>Merci pour votre don, {nom} !</h2>
        <p>Voici votre reçu fiscal :</p>
        <table border="1" cellpadding="8" style="border-collapse:collapse;">
        <tr><td>Numéro</td><td>{numero_recu}</td></tr>
        <tr><td>Montant</td><td>{montant:.2f} EUR</td></tr>
        <tr><td>Campagne</td><td>{campagne}</td></tr>
        </table>
        <p>Ce reçu fait foi pour votre déclaration fiscale.</p>
        </body></html>
        """

        return await EmailService._envoyer(destinataire, sujet, html)

    @staticmethod
    async def notifier_admin(sujet: str, message: str) -> bool:
        html = f"<html><body><p>{message}</p></body></html>"
        return await EmailService._envoyer(settings.smtp_from, f"[Admin] {sujet}", html)

    @staticmethod
    async def _envoyer(destinataire: str, sujet: str, html: str) -> bool:
        if not settings.smtp_host:
            return True

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = sujet
            msg["From"] = settings.smtp_from
            msg["To"] = destinataire
            msg.attach(MIMEText(html, "html"))

            with SMTP(settings.smtp_host, settings.smtp_port) as smtp:
                if settings.smtp_user:
                    smtp.starttls()
                    smtp.login(settings.smtp_user, settings.smtp_password)
                smtp.send_message(msg)
            return True
        except Exception:
            return False
