import discord
from discord.ext import commands
import requests
import json
import os
from flask import Flask
from threading import Thread

# Configuration from environment variables (Render will set these)
TOKEN = os.getenv('MTQ4MjU1OTA0MjE3NzIwNDMwNA.GnfQ08.nUv0Dz_OrQguZNCtr4GifAZL_LXkjP3V5TzI2M')  # Render will set this
BIN_ID = os.getenv('69b61733c3097a1dd5271c0b')        # Render will set this
API_KEY = os.getenv('$2a$10$cIzufEulpNYuqlwxpHBtAOgkJIrHFNY32AmutbCMCue/VBwG1NJxW')      # Render will set this
JSONBIN_URL = f'https://api.jsonbin.io/v3/b/{69b61733c3097a1dd5271c0b}'

# Create a simple web server to keep Render happy
app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Setup bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def get_user_list():
    headers = {'X-Master-Key': API_KEY}
    response = requests.get(JSONBIN_URL, headers=headers)
    return response.json()['record']

def update_user_list(data):
    headers = {
        'X-Master-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    requests.put(JSONBIN_URL, json=data, headers=headers)

@bot.event
async def on_ready():
    print(f'{bot.user} is online!')

@bot.command(name='whitelist')
@commands.has_permissions(administrator=True)
async def whitelist_user(ctx, roblox_id: int):
    data = get_user_list()
    
    if roblox_id in data['blacklisted']:
        data['blacklisted'].remove(roblox_id)
    
    if roblox_id not in data['whitelisted']:
        data['whitelisted'].append(roblox_id)
        update_user_list(data)
        await ctx.send(f"✅ User `{roblox_id}` whitelisted!")
    else:
        await ctx.send(f"ℹ️ User `{roblox_id}` already whitelisted.")

@bot.command(name='blacklist')
@commands.has_permissions(administrator=True)
async def blacklist_user(ctx, roblox_id: int):
    data = get_user_list()
    
    if roblox_id in data['whitelisted']:
        data['whitelisted'].remove(roblox_id)
    
    if roblox_id not in data['blacklisted']:
        data['blacklisted'].append(roblox_id)
        update_user_list(data)
        await ctx.send(f"❌ User `{roblox_id}` blacklisted!")
    else:
        await ctx.send(f"ℹ️ User `{roblox_id}` already blacklisted.")

@bot.command(name='remove')
@commands.has_permissions(administrator=True)
async def remove_user(ctx, roblox_id: int):
    data = get_user_list()
    removed = False
    
    if roblox_id in data['whitelisted']:
        data['whitelisted'].remove(roblox_id)
        removed = True
    if roblox_id in data['blacklisted']:
        data['blacklisted'].remove(roblox_id)
        removed = True
    
    if removed:
        update_user_list(data)
        await ctx.send(f"🗑️ User `{roblox_id}` removed from all lists.")
    else:
        await ctx.send(f"ℹ️ User `{roblox_id}` not found in any list.")

@bot.command(name='check')
async def check_user(ctx, roblox_id: int):
    data = get_user_list()
    
    if roblox_id in data['whitelisted']:
        await ctx.send(f"✅ User `{roblox_id}` is **whitelisted**")
    elif roblox_id in data['blacklisted']:
        await ctx.send(f"❌ User `{roblox_id}` is **blacklisted**")
    else:
        await ctx.send(f"❓ User `{roblox_id}` is not in any list")

@bot.command(name='list')
@commands.has_permissions(administrator=True)
async def show_lists(ctx):
    data = get_user_list()
    
    whitelist = ", ".join([f"`{id}`" for id in data['whitelisted']]) or "None"
    blacklist = ", ".join([f"`{id}`" for id in data['blacklisted']]) or "None"
    
    await ctx.send(f"**✅ Whitelisted:** {whitelist}")
    await ctx.send(f"**❌ Blacklisted:** {blacklist}")
    await ctx.send(f"**Total:** {len(data['whitelisted'])} whitelisted | {len(data['blacklisted'])} blacklisted")

# Start the web server and bot
keep_alive()
bot.run(TOKEN)
