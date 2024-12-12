import os
import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()
ROLE_ID = os.getenv('ROLE_ID')
GUILD_ID = os.getenv('GUILD_ID')
LOG_CHANNEL = os.getenv('LOG_CHANNEL')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())




@bot.command()
@has_permissions(administrator=True)
async def kickMembers(ctx, role: discord.Role, reason: str = None):
    await ctx.reply('Kicking members')

    for member in role.members:
        await member.kick(reason=reason)

    await ctx.reply('Members kicked')

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.name}! 😃")

@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    if before.roles != after.roles:
        log_channel = bot.get_channel(LOG_CHANNEL)
        if log_channel:
            # Obtendo os cargos adicionados e removidos
            before_roles = set(before.roles)
            after_roles = set(after.roles)

            added_roles = after_roles - before_roles
            removed_roles = before_roles - after_roles

            changes = []
            if added_roles:
                changes.append(f'**Adicionados:** {", ".join(role.name for role in added_roles)}')
            if removed_roles:
                changes.append(f'**Removidos:** {", ".join(role.name for role in removed_roles)}')

            if changes:
                await log_channel.send(
                    f"Alteração de cargos para {after.mention}:\n" + "\n".join(changes)
                )









# Run the bot
if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise ValueError("No token found. Make sure DISCORD_TOKEN is set in your environment variables.")
    bot.run(token)
