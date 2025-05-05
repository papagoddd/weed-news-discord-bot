import discord
import requests
import asyncio
import os

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
NEWS_API_KEY = os.getenv("NEWSAPI_KEY")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def fetch_weed_news():
    url = f'https://newsapi.org/v2/everything?q=cannabis+OR+marijuana&sortBy=publishedAt&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data.get("articles", [])[:3]

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)
    while True:
        articles = await fetch_weed_news()
        for article in articles:
            await channel.send(f"📰 **{article['title']}**\n{article['description']}\n🔗 {article['url']}")
        await asyncio.sleep(3600)

client.run(TOKEN)
