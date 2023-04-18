import discord
import json
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
intents = discord.Intents.default()
intents.messages = True
intents.guild_messages = True
intents.members = True
intents.message_content = True
intents.reactions = True
intents.moderation = True

bot = commands.Bot(command_prefix='!', intents=intents)
def sauvegarder(element):
    with open(f"data.json", "w") as f:
        json.dump(element, f)

def ouvrir(element):
    with open(f"{element}.json","r") as f:
        return json.load(f)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    points = ouvrir("data")

    if len(points) == 0:
        print("Je suis passé par là.")
        for guild in bot.guilds:
            for member in guild.members:
                points[member.id] = 0
        print(points)
        sauvegarder(points)

@bot.command(name='remove')
@commands.has_permissions(administrator=True)
async def remove(ctx, nbpoints: int,  member: discord.Member = None):
    # Ajout des points au membre ciblé
    if not member:
        member = ctx.author

    points = ouvrir("data")
    user = str(member.id)
    if user in points:
        points[user] -= nbpoints
        sauvegarder(points)
        await ctx.send(f'{nbpoints} Euclecoins :coin: ont été supprimés à {member.mention}.')
    else:
        points[user] = nbpoints
        sauvegarder(points)
        await ctx.send(f'{nbpoints} Euclecoins :coin: ont été supprimés à {member.mention}.')

@bot.command(name='give')
@commands.has_permissions(administrator=True)
async def give(ctx, nbpoints: int,  member: discord.Member = None):
    # Ajout des points au membre ciblé
    if not member:
        member = ctx.author

    points = ouvrir("data")
    user = str(member.id)
    if user in points:
        points[user] += nbpoints
        sauvegarder(points)
        await ctx.send(f'{nbpoints} Euclecoins :coin: ont été ajoutés à {member.mention}.')
    else:
        points[user] = nbpoints
        sauvegarder(points)
        await ctx.send(f'{nbpoints} Euclecoins :coin: ont été ajoutés à {member.mention}.')
@bot.command(name='money')
async def money(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author

    points = ouvrir("data")
    user = str(member.id)
    if user in points:
        await ctx.send(f'{member.mention} possède {points[user]} Euclecoins :coin:.')
    else:
        points[user] = 0
        sauvegarder(points)
        await ctx.send(f'{member.mention} ne possède pas encore de Euclecoins :coin:')


@bot.command(name='nextrole')
async def nextrole(ctx):
    roles = ctx.guild.roles #Récupère tous les rôles du serveur sous forme d'une liste
    role_index = roles.index(ctx.author.top_role) #On récupère l'index de notre rôle.
    next_role_index = role_index + 2  # On saute un rôle

    if next_role_index >= len(roles)-1:  # Si on est au dernier rôle
        await ctx.send(f'Vous avez le statut ({ctx.author.top_role.name}) le plus élevé dans la Hiérarchie du serveur. Félicitations !')
    else:
        await ctx.send(f'Voici le rôle pour votre future promotion: {roles[next_role_index]}.')

@bot.command(name='promote')
async def promote(ctx):
    Argent = ouvrir("rangs")
    points = ouvrir("data")
    roles = ctx.guild.roles #Récupère tous les rôles du serveur sous forme d'une liste
    role_index = roles.index(ctx.author.top_role) #On récupère l'index de notre rôle.
    next_role_index = role_index + 2  # On saute un rôle
    if roles[next_role_index].name == 'Bank Route':
        await ctx.send(f'Vous avez le statut ({ctx.author.top_role.name}) le plus élevé dans la Hiérarchie du serveur. Félicitations !')
        return
    prix = Argent[roles[next_role_index].name]
    identifiant = str(ctx.author.id) #identifiant de l'utilisateur
    possession = points[identifiant] #prix possede par l'utilisateur

    if next_role_index >= len(roles)-1:  # Si on est au dernier rôle
        await ctx.send(f'Vous avez le statut ({ctx.author.top_role.name}) le plus élevé dans la Hiérarchie du serveur. Félicitations !')
    else:
        if prix > possession:
            await ctx.send(f'Le grade {roles[next_role_index]} coûte {prix} :coin:. Vous avez {possession} :coin:. Il vous manque {prix-possession} :coin: !')
        else:
            points[identifiant] -= prix
            sauvegarder(points)
            channel = discord.utils.get(ctx.guild.channels, name="👑•𝐏𝐫𝐨𝐦𝐨𝐭𝐢𝐨𝐧")
            await channel.send(f'**Félicitations ! {ctx.author.name} est passé(e) {roles[next_role_index]} !**')
            await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name=roles[next_role_index].name))

@bot.command(name='pay')
async def pay(ctx, nbcoins: int, member: discord.Member):
    points = ouvrir("data")
    points[str(ctx.author.id)] -= nbcoins
    points[str(member.id)] += nbcoins
    sauvegarder(points)
    await ctx.send(f'{ctx.author.name} a donné {nbcoins} :coin: à {member.name}')

bot.run(os.getenv('DISCORD_TOKEN')) # Remplacez INSERT_YOUR_TOKEN_HERE par votre token de bot Discord