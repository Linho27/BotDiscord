import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()


ROLE_ID = os.getenv('ROLE_ID')
GUILD_ID = os.getenv('GUILD_ID')
LOG_CHANNEL = os.getenv('LOG_CHANNEL')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Dicionário para armazenar o tempo de entrada no cargo
role_check_times = {}

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    check_roles.start()

@bot.event
async def on_member_update(before, after):
    # Verificar se o cargo foi adicionado
    role = discord.utils.get(after.guild.roles, id=ROLE_ID)
    if role in after.roles and role not in before.roles:
        role_check_times[after.id] = datetime.utcnow()

@tasks.loop(seconds=30)
async def check_roles():
    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        return

    role = discord.utils.get(guild.roles, id=ROLE_ID)
    if role is None:
        return

    for member in guild.members:
        if role in member.roles:
            join_time = role_check_times.get(member.id)
            log_channel = bot.get_channel(LOG_CHANNEL)
            if join_time and datetime.utcnow() - join_time > timedelta(minutes=1):
                try:
                    await member.kick(reason="Teve o cargo por mais de 1 minuto.")
                    await log_channel.send(f"Usuário {member.mention} foi kickado por ter o cargo por mais de 1 minuto.")
                    del role_check_times[member.id]
                except Exception as e:
                    await log_channel.send(f"Erro ao tentar kickar {member.mention}: {e}")

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
