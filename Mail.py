import smtplib
import os

gmail_user = 'verifmasterbordeaux@gmail.com'
gmail_password = os.getenv('GANDALF_PASSWORD')# None #

async def sendMail(to, code):
    sent_from = gmail_user
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
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print ('Email sent!')
        return True
    except Exception as e:
        print(e)
        print ('Something went wrong...')
    return False
