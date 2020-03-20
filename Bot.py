# Work with Python 3.6
import discord
import Mail
import random
import time

TOKEN = os.getenv('TOKEN_DISCORD_GANDALF')

client = discord.Client()

user_code = {}

roleName = "élève"
EXPIRED = 300

class Pending:

    def __init__(self, author, roles, guild):
        self.author = author
        self.roles = roles
        self.guild = guild
        self.timeSent = None
        self.mail = None
        self.code = None

async def usage():
    msg = 'Erreur: Merci de donner votre adresse mail de l\'université de Bordeaux.\n'
    msg += 'Exemple: $register vincent.penelle@u-bordeaux.fr'
    return msg

async def correct_extension(mail):
    extensionProf = '@etu.u-bordeaux.fr'
    extension = '@u-bordeaux.fr'
    for index in range(len(mail)):
        if index + len(extension) == len(mail):
            if extension == mail[index:(index+len(extension))]:
                return True

        if index + len(extensionProf) == len(mail):
            if extensionProf == mail[index:(index+len(extensionProf))]:
                return True

    return False

async def decompose_message(msg, member):
    if str(member.author) not in user_code:
        return "Utilisez la command $register avant d'envoyer votre mail."

    for mem in member.guild.members:
        if mem == member.author:
            for role in mem.roles:
                if role.name == roleName:
                    return 'Vous avez déjà le bon rôle!'

    msg = msg.split(' ')

    if len(msg) <= 1:
        return await usage()

    mail = msg[1]

    if member.timeSent != None and time.time() - member.timeSent <= EXPIRED:
        return 'Un mail a déjà été envoyé il y a moins de 5 minutes'

    if await correct_extension(mail):
        code = random.randint(100000, 1000000)
        if await Mail.sendMail(mail, code):
            member.mail = mail
            member.timeSent = time.time()
            member.code = code
            return 'Mail envoyé!'
    return await usage()


async def check_code(msg, member):
    if str(member.author) not in user_code:
        return "Utilisez la command $register avant d'envoyer votre mail."

    msg = msg.split(' ')

    if len(msg) <= 1:
        return False

    code = int(msg[1])

    if time.time() - member.timeSent >= EXPIRED:
        return False

    if member.code == code:
        return True
    return False

async def configure(msg):
    global roleName
    msg = msg.split(' ')
    del msg[0]

    for index in range(len(msg)):
        if msg[index] == 'role':
            if index + 1 < len(msg):
                roleName = msg[index + 1]
                return True
            else:
                return False

    return False

async def helpMessage(dm):
    msg = '**$help**: Affiche cette aide.\n\n'
    msg += '**$register**: S\'enregistrer sur le serveur.\n\n'
    if dm:
        msg += '**$mail [mail]**: Envoie un mail à l\'adresse donnée si elle est valide. Le mail contient un code secret pour à renvoyer avec la commande code pour gagner un rôle permettant de naviguer sur le serveur.\n\n'
        msg += '**$code [code]**: Donne un rôle permettant de naviguer le serveur si le code est correct. Le code peut être reçu grâce à la commande $register.\n\n'
    msg += '**$configure [option] [value]**: Change les valeurs des macros.\n\n'
    msg += 'Liste des macros:\n'
    msg += '**role**: Le nom du rôle à donner avec la commande $code.'
    return msg

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('$register'):
        user_code[str(message.author)] = Pending(message.author, message.guild.roles, message.guild)
        await message.author.send(await helpMessage(True))

    if message.content.startswith('$mail'):
        msg = await decompose_message(message.content, user_code[str(message.author)])
        await message.channel.send(msg)

    if message.content.startswith('$configure'):
        if message.author.guild_permissions.administrator:
            if await configure(message.content):
                await message.channel.send('Configuration réussie')
            else:
                await message.channel.send('Configuration ratée')

    if message.content.startswith('$code'):
        if await check_code(message.content, user_code[str(message.author)]):
            member = user_code[str(message.author)]
            roles = member.guild.roles
            toSet = None

            for role in roles:
                if role.name == roleName:
                    toSet = role

            for mem in member.guild.members:
                if mem == member.author:
                    await mem.add_roles(toSet)
            await message.channel.send('Role attribué!')
        else:
            await message.channel.send('Code invalide ou expiré.')

    if message.content.startswith('$help'):
        print("kk")
        msg = await helpMessage(False)
        await message.channel.send(msg)

@client.event
async def on_member_join(member):
    user_code[str(member)] = Pending(member, member.guild.roles, member.guild)
    await member.send(await helpMessage(True))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
