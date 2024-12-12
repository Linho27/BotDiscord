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
    member = ctx.author
    role = discord.utils.get(ctx.guild.roles, name="Teste")
    await member.add_roles(role)
    

@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    log_channel = bot.get_channel(LOG_CHANNEL)
    await log_channel.send('Cargos Alterados')

@bot.command()
async def verificar(ctx):
    """Comando para verificar membros com um cargo específico e entrada há mais de 4 horas."""
    cargo = discord.utils.get(ctx.guild.roles, id=ROLE_ID)
    if not cargo:
        await ctx.send("Cargo não encontrado.")
        return

    agora = datetime.utcnow()
    membros_verificados = []

    for membro in ctx.guild.members:
        if cargo in membro.roles:  # Verifica se o membro tem o cargo
            if membro.joined_at and (agora - membro.joined_at).total_seconds() > 4 * 3600:
                membros_verificados.append(membro.mention)

    if membros_verificados:
        await ctx.send(f"Os seguintes membros possuem o cargo e estão há mais de 4 horas no servidor: {', '.join(membros_verificados)}")
    else:
        await ctx.send("Nenhum membro atende aos critérios.")







# Run the bot
if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise ValueError("No token found. Make sure DISCORD_TOKEN is set in your environment variables.")
    bot.run(token)
