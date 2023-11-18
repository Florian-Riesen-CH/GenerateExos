import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Définissez les informations de connexion
smtp_server = "smtp.office365.com"
port = 587  # Pour le démarrage TLS
sender_email = "pj01tjy@eduvaud.ch"

def sendEmail(subject:str, receiver_email: str, smtp_password:str, html:str, filename:str, attachmentfilePath:str):
    # Créez un message MIMEMultipart et configurez les en-têtes
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Ajoutez les parties text et HTML au message MIMEMultipart
    part2 = MIMEText(html, "html")
    message.attach(part2)

    # Spécifiez le nom du fichier à joindre
    attachment = open(attachmentfilePath, "rb")  # Ouvrez le fichier en mode lecture binaire

    # Instanciez MIMEBase et encodez le fichier en base64
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)

    # Ajoutez les en-têtes au fichier attaché
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # Attachez la pièce jointe avec le message MIMEMultipart
    message.attach(part)

    # Essayez de vous connecter au serveur SMTP et envoyez l'e-mail
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # Activez la sécurité TLS
        server.login(sender_email, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("L'e-mail a été envoyé avec succès à ",receiver_email," !")
    except Exception as e:
        print(f"Une erreur est survenue: {e}")
    finally:
        server.quit()

