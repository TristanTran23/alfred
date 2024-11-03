import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands.cooldowns import BucketType
from openai import OpenAI

load_dotenv()

def main():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    bot = commands.Bot(command_prefix='/alfred', intents=intents)
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    @bot.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(bot))

    @bot.command()
    async def chat(ctx, message: str):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Alfred, an event organizer for a group of friends. You are helping them to find a place and time that works for everyone. You will suggest time to meet for the group"},
                {"role": "user", "content": message}
            ]
        )
        await ctx.send(response.choices[0].message.content)

    bot.run(os.getenv('DISCORD_TOKEN'), root_logger=True)

if __name__ == '__main__':
    main()