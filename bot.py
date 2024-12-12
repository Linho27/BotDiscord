import os
import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()
ROLE_ID = os.getenv('ROLE_ID')
GUILD_ID = os.getenv('GUILD_ID')
LOG_CHANNEL = os.getenv('LOG_CHANNEL')

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=intents)

@tasks.loop(minutes=1)  
async def verificar_periodicamente():
    guild = bot.get_guild(int(GUILD_ID))
    cargo = discord.utils.get(guild.roles, name="🎟️ ∥ Visitante")
    log_channel = bot.get_channel(int(LOG_CHANNEL))

    membros_kickados = []
    agora = datetime.now(timezone.utc)

    for membro in guild.members:
        if cargo in membro.roles:
            if (agora - membro.joined_at).total_seconds() > 4 * 3600:
                try:
                    await membro.kick(reason="Tempo no servidor excedeu 4 horas com o cargo Visitante.")
                    membros_kickados.append(membro.name)
                except Exception as e:
                    await log_channel.send(f"Erro ao expulsar {membro.name}: {e}")

    if membros_kickados:
        await log_channel.send(f"Os seguintes membros foram expulsos por estarem há mais de 4 horas no servidor com o cargo Visitante: {', '.join(membros_kickados)}")
    else:
        await log_channel.send("Nenhum membro atende aos critérios para expulsão.")

# Iniciar a tarefa periodicamente ao iniciar o bot
@bot.event
async def on_ready():
    print(f'{bot.user} entrou no servidor.')
    verificar_periodicamente.start()  # Inicia a tarefa quando o bot estiver pronto

if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise ValueError("No token found. Make sure DISCORD_TOKEN is set in your environment variables.")
    bot.run(token)