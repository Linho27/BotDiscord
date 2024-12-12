import os
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from dotenv import load_dotenv
from datetime import datetime, timezone

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

@bot.command()
async def a(ctx):
    member = ctx.author
    agora = datetime.now(timezone.utc)
    await ctx.send(agora)
    await ctx.send(member.joined_at)

@bot.command()
async def verificar(ctx):
    guild = bot.get_guild(int(GUILD_ID))
    if not guild:
        await ctx.send("Servidor não encontrado.")
        return

    cargo = discord.utils.get(guild.roles, name="🎟️ ∥ Visitante")
    if not cargo:
        await ctx.send("Cargo não encontrado.")
        return

    membros_verificados = []
    for membro in guild.members:
        agora = datetime.now(timezone.utc)
        if cargo in membro.roles:
            if (agora - membro.joined_at).total_seconds() > 4 * 3600:
                membros_verificados.append(membro.mention)

    if membros_verificados:
        await ctx.send(f"Os seguintes membros possuem o cargo e estão há mais de 4 horas no servidor: {', '.join(membros_verificados)}")
    else:
        await ctx.send("Nenhum membro atende aos critérios.")

if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise ValueError("No token found. Make sure DISCORD_TOKEN is set in your environment variables.")
    bot.run(token)
