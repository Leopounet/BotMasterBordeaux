import smtplib
import os

################################################################################
################################ VARIABLES #####################################
################################################################################

SENDER = 'verifmasterbordeaux@gmail.com'
PASSWORD = os.getenv('GANDALF_PASSWORD')
SMTP_ADDRESS = 'smtp.gmail.com'
SMTP_CODE = 465

################################################################################
################################ METHODS #######################################
################################################################################

async def sendMail(to, code):
    sent_from = SENDER
    to = [to]
    subject = 'Verification serveur discord Master 1 de Bordeaux'
    # body = 'Hey, what's up?\n\n- You
    body = "Bonjour, \n\n"
    body += "Cet email vous a ete envoye car vous avez demande a devenir un utilisateur verifie sur le serveur M1 informatique u-bordeaux. "
    body += "Si ce n'est pas vous, merci de renvoyer un mail a cette adresse au plus vite.\n\n"
    body += "Votre code secret est : " + str(code) + "\n\nVous avez 5 minutes pour le renvoyer!\n\n"
    body += "Cordialement, \nGandalf"

    email_text = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL(SMTP_ADDRESS, SMTP_CODE)
        server.ehlo()
        server.login(SENDER, PASSWORD)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print ('Email sent!')
        return True
    except Exception as e:
        print(e)
        print ('Something went wrong...')
    return False

async def valid_extension(mail, extensions):
    # extensionProf = '@etu.u-bordeaux.fr'
    # extension = '@u-bordeaux.fr'

    # parsing all the valid extensions
    for extension in extensions:

        # Get the index at which the extension should start
        index = len(mail) - len(extension)

        # Check if the extension is indeed valid
        if extension == mail[index:(index+len(extension))]:
            return True
    return False
