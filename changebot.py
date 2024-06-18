import discord
import requests

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

TOKEN = 'TOKEN'
SERVER_URL = 'http://localhost:8080/update_log'  # ServerURL (HTTP)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!updatelog'):
        try:
            response = requests.get(SERVER_URL)
            if response.status_code == 200:
                await message.channel.send(f"Update Log:\n{response.text}")
            else:
                await message.channel.send("Failed to retrieve update log.")
        except requests.exceptions.RequestException as e:
            await message.channel.send(f"Error: {e}")

    elif message.content.startswith('!setnews '):
        new_log = message.content[len('!setnews '):]
        try:
            response = requests.post(SERVER_URL, data=new_log)
            if response.status_code == 200:
                await message.channel.send("Update log successfully updated.")
            else:
                await message.channel.send("Failed to update the update log.")
        except requests.exceptions.RequestException as e:
            await message.channel.send(f"Error: {e}")

client.run(TOKEN)
