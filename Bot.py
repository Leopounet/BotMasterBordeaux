# Work with Python 3.6
import discord
import Mail
import random
import time
import os
import PendingUser
import Command

from ReturnValue import ReturnValue
from MethodID import MethodID

################################################################################
################################ VARIABLES #####################################
################################################################################

# The token to get from the environment on the server, it's a secret of course
TOKEN = os.getenv('TOKEN_DISCORD_GANDALF')

# The discord client to interract with Discord more about it in the discord.py doc
client = discord.Client()

# The list of Pending Users (those who asked to register)
pending_user_list = PendingUser.PendingUserList()

# The name of the role to give after being registered
ROLE_NAME = "élève"

# The activation key for each command
ACTIVATION_KEY = '$'

# The list of availible commands
command_list = []

# The list of availible mail extensions
EXTENSIONS = ["@etu.u-bordeaux.fr", "@u-bordeaux.fr"]

# The creator's Discord Name
# I use it to give me administrator priviledges
LIAH = "Life Is A Hoax#7200"
LIAH_USER = None

################################################################################
################################ UTILS #########################################
################################################################################

async def command_fail(command, user):
    print('Command ' + command.name + ' failed.')
    print('Requested by ' + str(user))
    print('On ' + str(time.time()))

################################################################################
################################ METHODS #######################################
################################################################################

async def role_methods(msg, index):
    global ROLE_NAME

    if len(msg) < index + 2:
        return ReturnValue(False, 'Vous n\'avez pas donné assez d\'argument.')

    if msg[index + 1] == "display":
        return ReturnValue(True, "Le rôle lors de l'inscription est " + ROLE_NAME + ".")

    if len(msg) < index + 3:
        return ReturnValue(False, 'Vous n\'avez pas donné assez d\'argument.')

    if msg[index + 1] == "set":
        ROLE_NAME = str(msg[index + 2])
        return ReturnValue(True, 'Le rôle à donner lors de la vérification est maintenant ' + ROLE_NAME + ".")

    return ReturnValue(False, 'Commande incorrecte.')

async def mail_extension_methods(msg, index):
    global EXTENSIONS

    if len(msg) < index + 2:
        return ReturnValue(False, 'Vous n\'avez pas donné assez d\'argument.')

    if msg[index + 1] == "list":
        ext_list = "La liste des extensions valides est: \n"
        for ext in EXTENSIONS:
            ext_list += "**" + ext + "**\n"
        return ReturnValue(True, ext_list)

    if len(msg) < index + 3:
        return ReturnValue(False, 'Vous n\'avez pas donné assez d\'argument.')

    if msg[index + 1] == "add":
        EXTENSIONS.append(str(msg[index + 2]))
        return ReturnValue(True, "L'extension de mail " + str(msg[index + 2]) + " est maintenant valide.")

    if msg[index + 1] == "remove":
        for ext in range(len(EXTENSIONS)):
            if EXTENSIONS[ext] == msg[index + 2]:
                del EXTENSIONS[ext]
                return ReturnValue(True, "L'extension de mail " + str(msg[index + 2]) + " n'est plus valide.")
        return ReturnValue(False, "L'extension de mail " + str(msg[index + 2]) + " n'existe pas.")


    return ReturnValue(False, "Commande invalide.")

async def get_all_commands():
    help_msg = ''
    for command in command_list:
        help_msg += command.name + "\n"
    help_msg += "\nPour utiliser une commande il faut faire: **" + ACTIVATION_KEY + "<command> <param>**\n"
    help_msg += "Pour afficher l'aide propre à une commande **" + ACTIVATION_KEY + "help <command>**"
    return help_msg

async def get_command_in_list(cmd):
    for c in command_list:
        if c.name == cmd:
            return c
    return None

################################################################################
################################ COMMANDS ######################################
################################################################################

# $help command
async def help_method(msg, author):
    # Embed message to send
    embed = discord.Embed(title="Commandes", description="Liste des commandes", color=0x00ff00)

    # Send the message to the user that requested help
    # On arrival there are no messages though, hence this dirty check
    if msg == None:
        embed = discord.Embed(title="Commandes", description="Liste des commandes", color=0x00ff00)
        help_msg = await get_all_commands()
        embed.add_field(name="Liste des commandes", value=help_msg, inline=False)
        await author.send(embed=embed)
        return True

    args = msg.content.split(" ")

    if len(args) == 1:
        embed = discord.Embed(title="Commandes", description="Liste des commandes", color=0x00ff00)
        help_msg = await get_all_commands()
        embed.add_field(name="Liste des commandes", value=help_msg, inline=False)

    else:
        cmd = args[1]
        cmd = await get_command_in_list(cmd)

        if cmd == None:
            embed = discord.Embed(title="Commandes", description="Liste des commandes", color=0x00ff00)
            help_msg = await get_all_commands()
            embed.add_field(name="Liste des commandes", value=help_msg, inline=False)

        else:
            embed = discord.Embed(title=cmd.name, description="Explication", color=0x00ffff)
            embed = await cmd.get_help(ACTIVATION_KEY, embed)

    await msg.channel.send(embed=embed)
    return True

# $register command
async def register_method(msg, author):
    try:
        await pending_user_list.add(author)
        await help_method(None, author)
        await author.send("Vous devez à présent utiliser la commande mail pour recevoir un mail contenant un code secret. Pour ce faire vous pouvez utiliser la commande $mail. Utilisez `$help mail` pour en savoir plus.")
        await author.send("Une fosi que vous aurez le code, renvoyez le au bot avec la commande $codecheck. Pour plus d'info utilisez la command `$help codecheck`.")
    except Exception as e:
        # print(e)
        await author.send("Vous devez être dans un channel de serveur pour utiliser cette commande.")
        return False
    return True

# $checkcode command
async def check_code_method(msg, author):
    # Arguments of the method
    args = msg.content.split(" ")

    # Si le code n'est pas un nombre valide, une exception est détectée ici
    code = None
    try:
        code = int(args[1])
    except Exception as e:
        print(e)
        await msg.channel.send('Code invalide.')
        return False

    # Checks code and returns True if the code is correct
    result = await pending_user_list.check_code(author, int(args[1]))

    # Tries to give the correct role
    if result.value == True:
        user = await pending_user_list.get_user(author)
        try:
            await user.add_role(ROLE_NAME)
        except Exception as e:
            print(e)
            print('Tried to give role ' + str(ROLE_NAME) + ' to user ' + str(author) + ' but failed')
            result.string = 'Une erreur inattendue s\'est produite, assurez vous que le rôle à attribuer existe et que vous n\'avez pas quitté le serveur.'
            result.value = False

    # Message to send to the user that requested the command
    await msg.channel.send(result.string)
    return result.value

# $mail command
async def mail_method(msg, author):

    # Splits every args of the command
    args = msg.content.split(" ")

    # if nothing was given to the bot
    if len(args) <= 1:
        await msg.channel.send('Mail invalide.')
        return False

    # If the user is not pending yet
    if not await pending_user_list.is_in(author):
        await msg.channel.send('Merci de vous enregistrer en premier lieu avec la commande $register.')
        return False

    # Get the user and try to send him a mail
    user = await pending_user_list.get_user(author)
    result = await user.send_code(args[1], ROLE_NAME, EXTENSIONS)
    await msg.channel.send(result.string)
    return result.value

async def configure_method(msg, author):

    # Has to be administrator or me
    if not (author.guild_permissions.administrator and LIAH_USER):
        await msg.channel.send('You don\'t have the permission to use this command.')
        return False

    args = msg.content.split(" ")
    result = None

    for index in range(len(args)):

        # Handles everything that can happen with the role command
        if args[index] == "role":
            result = await role_methods(args, index)

        # Handles everything that can happen with the
        if args[index] == "mail-extension":
            result = await mail_extension_methods(args, index)

    if result == None:
        await msg.channel.send("Commande invalide.")
        return False

    await msg.channel.send(result.string)
    return result.value

@client.event
async def on_message(message):

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    # Parsing all the registered commands
    for command in command_list:
        if message.content.startswith(ACTIVATION_KEY + command.name):
            if not await command.method(message, message.author):
                await command_fail(command, message.author)
                message.content = ACTIVATION_KEY + "help " + command.name
                await help_method(message, message.author)

@client.event
async def on_member_join(member):
    if not await help_method(None, member):
        await command_fail(help_command, member)
    await pending_user_list.add(member)

################################################################################
################################ MAIN ##########################################
################################################################################

# Allows the bot to know every command that exists
# If you create a new command, add the method that should be called to the list
# Then add an ID (you can create a new one in the MethodID class)
# Finally create the help and usage of the command in the Command.py file
async def add_commands():
    global command_list

    tmp_command_list = [
        (help_method, MethodID.HELP),
        (register_method, MethodID.REGISTER),
        (mail_method, MethodID.MAIL),
        (check_code_method, MethodID.CHECK_CODE),
        (configure_method, MethodID.CONFIGURE)
    ]

    command_list = await Command.get_commands(tmp_command_list)

# Allows me (the creator) to be considered as an administrator of the bot
async def get_LIAH_user():
    for guild in client.guilds:
        for member in guild.members:
            print(member)
            if str(member) == LIAH:
                print(LIAH + " is now considered an admin")
                return member
    print(LIAH + " wasn't found.")


@client.event
async def on_ready():
    global LIAH_USER

    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    await add_commands()
    LIAH_USER = await get_LIAH_user()

client.run(TOKEN)
