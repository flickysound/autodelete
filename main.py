import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')

@tasks.loop(hours=24)
async def delete_old_messages():
    now = datetime.utcnow()
    cutoff = now - timedelta(hours=24)

    for guild in bot.guilds:
        for channel in guild.text_channels:
            async for message in channel.history(before=cutoff).filter(lambda m: m.author == bot.user):
                await message.delete()

@bot.command()
async def start_cleanup(ctx):
    delete_old_messages.start()
    await ctx.send('Message cleanup task has started.')

@bot.command()
async def stop_cleanup(ctx):
    delete_old_messages.stop()
    await ctx.send('Message cleanup task has stopped.')

bot.run("YOUR_BOT_TOKEN")
