from MethodID import MethodID

# If you create a new command, a few things are important to do
# Make sure to :
#
# Set everything for the get_help method (name, help and usage)
# Add it to the list of commands in Bot.py towards the bottom of the file
# Add a method here to create the help and usage strings

# This class represents a command that the bot can use
# It is not very technical but makes the code a lot cleaner
class Command:

    # Initialization of a command
    # The namd of the command should NOT contain your activation key
    # The method is the method to call when the command is used
    def __init__(self, name=None, help=None, method=None, usage=None, example=None):
        self.name = name
        self.help = help
        self.method = method
        self.usage = usage
        self.example = example

    # Adds a field in the embed object with all the command information
    # The command information are defined below
    async def get_help(self, key, embed):
        name = "**__" + self.name + "__**"
        msg = ''
        msg += self.help + '\n'
        msg += "**Usage: " + key + self.usage + "**\n"
        msg += "Exemple: " + key + self.example
        embed.add_field(name=name, value=msg, inline=False)
        return embed

################################################################################
################################ HELP ##########################################
################################################################################

async def get_help_command(method):
    cmd = Command("help")
    cmd.help = "Affiche cette aide. Permet aussi d'afficher l'aide des autres commandes."
    cmd.method = method
    cmd.usage = "help [command]"
    cmd.example = "help configure"
    return cmd

async def get_register_command(method):
    cmd = Command("register")
    cmd.help = "Permet de commencer le processus d'authetification. Cette commande"
    cmd.help += " doit être utilisée avant d'utiliser les commands mail et code."
    cmd.method = method
    cmd.usage = "register"
    cmd.example = "register"
    return cmd

async def get_mail_command(method):
    cmd = Command("mail")
    cmd.help = "Envoie un mail contenant un code secret à renvoyer au bot à l'adresse donnée."
    cmd.help += " L'adresse doit être valide et l'extension de l'adresse doit être "
    cmd.help += " enregistrée parmis la liste des extensions autorisées. Cette command doit être utilisée "
    cmd.help += "après l'utilisation de la commande register."
    cmd.method = method
    cmd.usage = "mail [adresse-mail]"
    cmd.example = "mail prenom.nom@etu.u-bordeaux.fr"
    return cmd

async def get_check_code_command(method):
    cmd = Command("checkcode")
    cmd.help = "Permet d'être authetifié grâce au code que vous avez reçu avec la command "
    cmd.help += "mail."
    cmd.method = method
    cmd.usage = "checkcode [code]"
    cmd.example = "checkcode 458885"
    return cmd

async def get_configure_command(method):
    cmd = Command("configure")
    cmd.help = "Permet de modifier différentes macro.\n"
    cmd.help += "Liste des macros:\n\n"
    cmd.help += "   **role (set, display)**:\n"
    cmd.help += "       __set [role-name]__: Permet de définir le rôle à donner lors de l'inscription en fonction de son nom.\n"
    cmd.help += "       __display__: Permet d'afficher le nom du rôle.\n\n"
    cmd.help += "   **mail-extension (add, remove)**:\n"
    cmd.help += "       __add [ext]__: Permet d'ajouter une extension de mail valide lors de la vérification.\n"
    cmd.help += "       __remove [ext]__: Permet de retirer une extension valide.\n"
    cmd.method = method
    cmd.usage = "role [opt [value]]"
    cmd.example = "configure role add élève"
    return cmd

################################################################################
################################ GENERATOR OF COMMANDS #########################
################################################################################

async def get_commands(cmd_list):
    # The list of Command objects
    command_list = []

    # For all the command to register (set in Bot.py towards the bottom)
    for cmd in cmd_list:

        # gets the corresponding ID and method
        ID = cmd[1]
        method = cmd[0]

        # Switch but actually Ifs
        if ID == MethodID.HELP:
            command_list.append(await get_help_command(method))

        if ID == MethodID.REGISTER:
            command_list.append(await get_register_command(method))

        if ID == MethodID.MAIL:
            command_list.append(await get_mail_command(method))

        if ID == MethodID.CHECK_CODE:
            command_list.append(await get_check_code_command(method))

        if ID == MethodID.CONFIGURE:
            command_list.append(await get_configure_command(method))

    return command_list
