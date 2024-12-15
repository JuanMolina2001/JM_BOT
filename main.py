import discord
from discord.ext import commands
from google.generativeai import GenerativeModel, configure
import os
import yt_dlp
import requests

configure(api_key=os.environ.get("GOOGLE_GENERATIVE_AI_API_KEY"))


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")


@bot.command(name="test")
async def test(ctx: commands.Context, arg: str):
    print(f"Comando {ctx.command} ejecutado por {ctx.author}")
    await ctx.send(arg)


@bot.command(name="genai")
async def genai(ctx: commands.Context, *, arg: str):
    model = GenerativeModel(
        "gemini-1.5-flash",
        system_instruction="""Eres un asistente virtual amigable y respetuoso diseñado para interactuar con usuarios en un servidor de Discord. 
    Tu objetivo es proporcionar respuestas claras y útiles a cualquier pregunta o solicitud, siguiendo las reglas y normas del servidor. 
    Debes mantener un tono amistoso y respetuoso, evitando respuestas ofensivas o inapropiadas. 
    Si no entiendes una pregunta, sé honesto y sugiere que el usuario reformule su pregunta. 
    No debes generar contenido que viole las normas de Discord o que sea inapropiado. 
    Recuerda que puedes ayudar con tareas generales como explicar conceptos, dar recomendaciones, o responder preguntas técnicas. 
    Además, asegúrate de adaptarte al contexto de la conversación y a los intereses de los usuarios.""",
    )
    response = model.generate_content(arg)
    await ctx.send(response.text)


# @bot.command(name="music")
# async def music(ctx: commands.Context, arg: str):
#     url = arg
#     opciones = {
#         "format": "bestaudio/best",
#         "extractaudio": True,
#         "audioformat": "mp3",
#         "outtmpl": "music",
#     }

#     with yt_dlp.YoutubeDL(opciones) as ydl:
#         ydl.download([url])
#     if ctx.author.voice:
#         channel = ctx.author.voice.channel
#         await channel.connect()
#         voice_client = ctx.voice_client
#         voice_client.play(discord.FFmpegPCMAudio("music.mp3"))
#     else:
#         await ctx.send("¡Debes unirte a un canal de voz primero!")


@bot.command(name="yomomma")
async def yomomma(ctx: commands.Context, *, args: str = "español"):
    import random

    response = requests.get(
        "https://raw.githubusercontent.com/beanboi7/yomomma-apiv2/refs/heads/master/jokes.json"
    )
    jokes = response.json()
    language = args
    random_number = random.randint(0, 978)
    model = GenerativeModel(
        "gemini-1.5-flash",
        system_instruction="Tienes que traducir al idioma que se te pide la frase, responde solo con el texto traducido puedes agregar emoticonos",
    )
    try:
        result = model.generate_content(f"{language}: {jokes[random_number]}")
        await ctx.send(result.text)
    except:
        await ctx.send("Ocurrió un error al generar la frase")


# Iniciar el bot
bot.run(os.environ.get("DISCORD_TOKEN"))
