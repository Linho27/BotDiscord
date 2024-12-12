import os
import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()

ROLE_ID = os.getenv('ROLE_ID')
GUILD_ID = os.getenv('GUILD_ID')
LOG_CHANNEL = os.getenv('LOG_CHANNEL')

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
@has_permissions(administrator=True)
async def kickMembers(ctx, role: discord.Role, reason: str = None):
    await ctx.reply('Kicking members')

    for member in role.members:
        await member.kick(reason=reason)

    await ctx.reply('Members kicked')

@tasks.loop(minutes=10)
async def verificar():
    guild = discord.utils.get(bot.guilds, id=int(GUILD_ID))
    if not guild:
        print("Guild not found.")
        return

    cargo = discord.utils.get(guild.roles, name="Teste")
    if not cargo:
        print("Role 'Teste' not found.")
        return

    membros_verificados = []
    agora = datetime.now(timezone.utc)

    for membro in guild.members:
        if cargo in membro.roles:
            if (agora - membro.joined_at).total_seconds() > 4 * 3600:
                membros_verificados.append(membro.mention)

    log_channel = discord.utils.get(guild.text_channels, id=int(LOG_CHANNEL))
    if log_channel:
        if membros_verificados:
            await log_channel.send(f"Os seguintes membros possuem o cargo e estão há mais de 4 horas no servidor: {', '.join(membros_verificados)}")
        else:
            await log_channel.send("Nenhum membro atende aos critérios.")
    else:
        print("Log channel not found.")

@verificar.before_loop
async def before_verificar():
    await bot.wait_until_ready()

verificar.start()

if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise ValueError("No token found. Make sure DISCORD_TOKEN is set in your environment variables.")
    bot.run(token)
