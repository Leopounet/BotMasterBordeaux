import time
import Mail
import random

from ReturnValue import ReturnValue

# This class represents a User that should be registered
class PendingUser:

    # Initialisation of a new PendingUser
    # author is an User/Member object of discord.py
    # roles is the list of roles availible in the guild in asked for the command
    # guild is the guild in which the role should be set
    def __init__(self, author, roles, guild):
        self.author = author
        self.roles = roles
        self.guild = guild
        self.timeSent = None
        self.mail = None
        self.code = None
        self.time_before_expiration = 300

    # Get the role object from the name of the role
    async def get_role(self, role):
        for r in self.guild.roles:
            if r.name == role:
                return r
        return None

    # Add the role to the user
    # The role given is a string, not a role Object
    async def add_role(self, role):
         for mem in self.guild.members:
             if mem == self.author:
                 r = await self.get_role(role)
                 if r != None:
                     await mem.add_roles(r)

    # Checks if the user has the role given in parameter
    # The role is a string, not a role Object
    async def has_role(self, role):
        for mem in self.guild.members:
            if mem == self.author:
                for r in mem.roles:
                    if r.name == role:
                        return True
        return False

    # Sends a code via email to the user
    async def send_code(self, mail, role, extensions):

        # If the user already have the role, he doesn't have to do that
        if await self.has_role(role):
            return ReturnValue(False, 'Vous avez déjà le rôle!')

        # If the user has already recevied a mail less than 5 minutes ago
        # no other mail are sent
        if self.timeSent != None and time.time() - self.timeSent <= self.time_before_expiration:
            return ReturnValue(False, 'Un mail a déjà été envoyé il y a moins de 5 minutes')

        # If the mail has a valid extension
        if await Mail.valid_extension(mail, extensions):

            # Generate a random code
            code = random.randint(100000, 1000000)

            # Send the mail
            if await Mail.sendMail(mail, code):

                # Store the infos
                self.mail = mail
                self.timeSent = time.time()
                self.code = code
                return ReturnValue(True, 'Mail envoyé!')
        return ReturnValue(False, 'Le mail n\'est pas valide.')


class PendingUserList:

    def __init__(self):
        self.pending_list = {}

    async def add(self, user):
        self.pending_list[str(user)] = PendingUser(user, user.guild.roles, user.guild)

    async def remove(self, user):
        if str(user) in pending_list:
            del self.pending_list[str(user)]
        else:
            print('Tried to remove user: ' + str(user) + ' but was not successful')

    async def is_in(self, user):
        if str(user) in self.pending_list:
            return True
        return False

    async def get_user(self, user):
        if await self.is_in(user):
            return self.pending_list[str(user)]
        return None

    # Check if the code sent by the user is correct
    async def check_code(self, user, code):
        # If the user is registered
        if await self.is_in(user):

            # Get the user
            pending_user = await self.get_user(user)

            # If the code he received is still valid
            if time.time() - pending_user.timeSent <= pending_user.time_before_expiration:

                # If the code he sent is valid
                if pending_user.code == code:
                    return ReturnValue(True, 'Rôle attribué!')

                # Invalid code error
                else:
                    print('User ' + str(user) + ' tried to send an invalid code')
                    return ReturnValue(False, 'Code invalide.')

            # Expired code error
            else:
                print('User ' + str(user) + ' tried to send an expired code')
                return ReturnValue(False, 'Votre code a expiré.')

        # Not registered user error
        print('User ' + str(user) + ' tried to send a code but was not registered')
        return ReturnValue(False, 'Merci de vous enregistrer en premier lieu.')
