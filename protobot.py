"""
Author: Konnor Klercke
File: protobot.py
Purpose: Discord bot for my personal server
"""


#####################################
                                    #
import os                           #
import discord                      #
from dotenv import load_dotenv      #
import random                       #
from discord.ext import commands    #
                                    #
#####################################

#########################################
                                        #
bot = commands.Bot(command_prefix='!')  #
TOKEN = os.getenv('DISCORD_TOKEN')      #
VERSION = "a0.1"                        #
ACTIVITY = discord.Game("!help")        #
                                        #
#########################################

load_dotenv()


@bot.event 
async def on_ready():
    """
    Logs a message with bot name and version when the bot starts. Sets the
    bot activity to ACTIVITY.
    """

    print(f'{bot.user.name} {VERSION} has sucessfully connected to Discord.')
    await bot.change_presence(activity = ACTIVITY)
    


@bot.event
async def on_member_join(member):
    """
    Direct-messages a user whenever the join the server
    """

    await member.create_dm()
    await member.dm_channel.send(
        f"Hi {member.name}, welcome to Konnor's Discord server. Please set your "
        "nickname to match the naming scheme used on the server. For example, if "
        "my name was John, my nickname would be \"Protobot | John\". Please also "
        "make sure to read any messages pinned in the #important channel."
    )


@bot.event
async def on_error(event, *args, **kwargs):
    """
    Writes to err.log whenever a message triggers an error
    """

    with open('err.log', 'a', encoding='utf-8') as errfile:
        if event == 'on_message':
            errfile.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


@bot.event
async def on_message(message):
    """
    Allows the bot to respond to user messages rather than commands
    """

    if message.author == bot.user:
        """
        Tells the bot to ignore its own messages
        """

        return 

    if 'im' in message.content.lower() or 'i\'m' in message.content.lower() or 'i am' in message.content.lower():
        """
        Lets the bot tell the famous "Hi x! I'm dad!" joke
        """

        user_message = message.content.split()
        ways_to_say_i_am = ["im", "i'm", "i am"]
        print("Dad joke incoming!")

        for i in range(len(user_message)):
            if len(user_message) - i < 2:
                print("False alarm, user message too short!")
                break
            
            elif user_message[i].lower() in ways_to_say_i_am:
                response = "Hi " + " ".join(user_message[i + 1:]) + "! I'm dad!"
                print(response)
                await message.channel.send(response)
                break

            elif len(user_message) - i < 3:
                print("False alarm, user message too short!")
                break               
            
            elif user_message[i].lower() + " " + user_message[i + 1].lower() in ways_to_say_i_am:
                response = "Hi " + " ".join(user_message[i + 2:]) + "! I'm dad!"
                print(response)
                await message.channel.send(response)
                break

    elif 'happy birthday' in message.content.lower():
        """
        Lets the bot say happy birthday whenever a user says it
        """

        print("Wishing someone a happy birthday!")
        await message.channel.send('Happy Birthday! 🎈🎉🎂')

    await bot.process_commands(message)


@bot.command(name = '99', help = 'Responds with a random Brooklyn 99 quote.')
async def nine_nine(ctx):
    b99_quotes = [
        "I'm the human form of the 💯 emoji.",
        "Bingpot!",
        "Nine-nine!",
        (
            "Cool. Cool cool cool cool cool cool cool, "
            "no doubt no doubt no doubt no doubt."
        ),
        "With all due respect, I am gonna completely ignore everything you just said.",
        (
            "The English language can not fully capture the depth and complexity of my "
            "thoughts, so I’m incorporating emojis into my speech to better express myself. 😉."
        ),
        "I’d like your $8-est bottle of wine, please.",
        "But if you’re here, who’s guarding Hades?"
    ]

    response = random.choice(b99_quotes)
    await ctx.send(response)


@bot.command(name = 'raise-exception', help = 'Logs an exception with message data. Developer use.')
async def raise_exception(ctx):
    await ctx.send('Raising an exception to my console...')
    raise discord.DiscordException

bot.run(TOKEN)