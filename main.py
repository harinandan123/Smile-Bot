from keepalive import keep_alive
import os
from discord.utils import get
import discord
import discord.utils
from typing import Awaitable
import datetime
import requests
import json
from replit import db
from replit import Database
from discord.ext import commands

TOKEN = 'ORSFI4MjEwNTc2ODc2OTI0OTM4.YdVddg.wZqa9JEh1lr6ZNAZsF8vOH8'
db = Database(db_url="https://kv.replit.com/v0/eyJhbGciOiJIUzUxMiIsImlzcyI6ImNvbm1hbiIsImtpZCI6InByb2Q6MSIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjb25tYW4iLCJleHAiOjE2NDg1NzA0MDAsImlhdCI6MTY0ODQ1ODgwMCwiZGF0YWJhc2VfaWQiOiI3ZWYxYmIyMy1jYTc3LTRiYjItOGI3ZC04MDQwZTAwNWE4YWQifQ.gqcjKETfJgUcw-NfrMbtk00NoEdIpHtwesD2xoFlulBH5xqNhsprrotwgFLqjXQFNa2rqG7I-DKclE6suhq6ng")
db['bad_words'] = ["stupid", "idiot", "dumb"]
db['person_sad'] = ["sad", "depressed", "anexiety", "angry"]

client = commands.Bot(command_prefix="!")


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(
        client) + 'And I am in ' + str(len(client.guilds)) + ' servers!')


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = client.get_channel(952166794410487818)
    print(f'{username}: {user_message} ({channel})')
    msg = message.content
    if message.author == client.user:
        return

    if channel.name == 'smile-bot-commands':
        if "inspire" in msg or "inpire me" in msg:
            quote = get_quote()
            await channel.send(quote)

    if "hello" in msg:
        await message.channel.send(f'Hello {username}!')

    if "what is your gender" in msg or "are you a girl" in msg or "are you a boy" in msg or "what gender are you" in msg:
        await channel.send(
            'Well, since I am a bot, I have no gender ;)')

    if any(word in msg for word in db['person_sad']):
        await channel.send(
            f'Dont be sad or depressed {username}! Everyone feels like that atleats once in their life! Its okay to be like that. You can get help from https://www.healthline.com/health/mental-health/depression-and-anxiety and https://www.webmd.com/mental-health/mental-health-managing-anger')
    
    if "morning" in msg or "good morning" in msg:
        await message.channel.send(f'Good Morning {username}!')
        await message.channel.send('How is it going?')
        await message.channel.wait
    if "great" in msg or "good" in msg:
        await message.channel.send(f'Glad to hear that {username}!')

    if "bad" in msg or "not great" in msg or "not good" in msg:
        await message.channel.send('Oh :(')

    if any(word in msg for word in db['bad_words']):
        await channel.send('Please dont use NSWF or bad words here :) '
                           )
        await message.delete()

    if "what is your age" in msg or "your age" in msg:
        await channel.send('Well, I am currently ')

    if "when is your birthday?" in msg or "your birthday" in msg or "your bday" in msg or "when is your bday" in msg:
        await channel.send(
            'I finnaly came alive (not biogolicaly ;) ,in testing progress) on 20th February 2022'
        )
    await client.process_commands(message)


@client.command(name="say")
async def _say(ctx, sentence):
    return await ctx.send(sentence)


# moderation
@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(embed=discord.Embed(title="Kick", description=f'{member} has been kicked', colour=discord.Colour.red()))


@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(embed=discord.Embed(title="Ban", description=f'{member} has been banned', colour=discord.Colour.red()))


@client.command()
@commands.has_permissions(administrator=True)
async def mute(self, ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.add_roles(role)
    await ctx.send(embed=discord.Embed(title="Muted", description=f'{member} has been muted', colour=discord.Colour.red()))


@client.command()
@commands.has_permissions(administrator=True)
async def unban(context, id: int):
    user = await bot.fetch_user(id)
    await context.guild.unban(user)
    await ctx.send(embed=discord.Embed(title="Unban", description=f'{member} has been unbanned', colour=discord.Colour.green()))


@client.command()
@commands.has_permissions(administrator=True)
async def unmute(context, id: int):
    user = await bot.fetch_user(id)
    await context.guild.unmute(user)
    await ctx.send(embed=discord.Embed(title="Unmute", description=f'{member} has been unmuted', colour=discord.Colour.green()))


@client.event
async def on_command_error(context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await context.send(
            "Oh no! Looks like you have missed out an argument for this command."
        )
    if isinstance(error, commands.MissingPermissions):
        await context.send(
            "Oh no! Looks like you Dont have the permissions for this command."
        )
    if isinstance(error, commands.MissingRole):
        await context.send(
            "Oh no! Looks like you Dont have the roles for this command.")

    # bot errors
    if isinstance(error, commands.BotMissingPermissions):
        await context.send(
            "Oh no! Looks like I Dont have the permissions for this command.")
    if isinstance(error, commands.BotMissingRole):
        await context.send(
            "Oh no! Looks like I Dont have the roles for this command.")


@client.command(name="add_word")
@commands.has_permissions(administrator=True)
async def _add_word(ctx, type, word1, word2=None, word3=None):
    if type == "bad_words":
        words = db['bad_words']
        if word1 not in words:
            words.append(word1)
        if word1 != None:
            if word2 not in words:
                words.append(word2)
        if word3 != None:
            if word3 not in words:
                words.append(word3)
        db['bad_words'] = words
        embed = discord.Embed(title="Successful",
                              description="Successfully added the word",
                              color=discord.Color.green())
    elif type == "person_sad":
        words = db['person_sad']
        if word1 not in words:
            words.append(word1)
        if word1 != None:
            if word2 not in words:
                words.append(word2)
        if word3 != None:
            if word3 not in words:
                words.append(word3)
        db['person_sad'] = words
        embed = discord.Embed(title="Successful",
                              description="Successfully added the word",
                              color=discord.Color.green())
    else:
        embed = discord.Embed(
            title="Error",
            description="There was an error while add the words",
            color=discord.Color.red())

    await ctx.reply(embed=embed)


keep_alive()
client.run(TOKEN)
