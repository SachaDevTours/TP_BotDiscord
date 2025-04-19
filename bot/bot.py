import discord
from discord import app_commands
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv
from moderation.analyzer import is_message_inappropriate

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = "http://localhost:8000/rules"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Connecté en tant que {bot.user}")

@bot.tree.command(name="ajouter_sujet", description="Ajoute un sujet à bannir")
@app_commands.describe(sujet="Sujet à bannir")
async def ajouter(interaction: discord.Interaction, sujet: str):
    response = requests.post(API_URL, json={"subject": sujet})
    if response.status_code == 200:
        await interaction.response.send_message(f"Sujet `{sujet}` banni avec succès.")
    else:
        await interaction.response.send_message("Ce sujet est déjà banni.")

@bot.tree.command(name="supprimer_sujet", description="Supprime un sujet banni")
@app_commands.describe(sujet="Sujet à retirer de la liste")
async def supprimer(interaction: discord.Interaction, sujet: str):
    response = requests.delete(API_URL, json={"subject": sujet})
    if response.status_code == 200:
        await interaction.response.send_message(f"Sujet `{sujet}` retiré.")
    else:
        await interaction.response.send_message("Sujet introuvable.")

@bot.tree.command(name="liste_sujets", description="Liste des sujets bannis")
async def liste(interaction: discord.Interaction):
    response = requests.get(API_URL)
    sujets = response.json()
    if sujets:
        await interaction.response.send_message("Sujets bannis :\n- " + "\n- ".join(sujets))
    else:
        await interaction.response.send_message("Aucun sujet banni pour l'instant.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    try:
        sujets = requests.get(API_URL).json()
        if is_message_inappropriate(message.content, sujets):
            await message.delete()
            await message.author.send("Ton message a été supprimé car il traitait d’un sujet interdit.")
            print(f"Message supprimé : {message.content}")
    except Exception as e:
        print(f"Erreur : {e}")

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
