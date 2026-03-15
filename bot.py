import discord
import os
from flask import Flask
from threading import Thread

# Configuration
TOKEN = os.getenv('MTQ4MjU1OTA0MjE3NzIwNDMwNA.GnfQ08.nUv0Dz_OrQguZNCtr4GifAZL_LXkjP3V5TzI2M')

# Flask web server
app = Flask('')
@app.route('/')
def home():
    return "Bot is testing connection..."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# Simple Discord bot
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("✅✅✅ SUCCESS! Bot connected to Discord!")
    print(f"Bot name: {client.user.name}")
    print(f"Bot ID: {client.user.id}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == '!test':
        await message.channel.send('Bot is working!')

# Start
keep_alive()
print("Attempting to connect to Discord...")
client.run(TOKEN)
