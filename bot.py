import os
import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from dotenv import load_dotenv
from datetime import datetime, timezone

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém o ID do servidor e do canal de log das variáveis de ambiente
GUILD_ID = os.getenv('GUILD_ID')
LOG_CHANNEL = os.getenv('LOG_CHANNEL')

# Configura os intents necessários para o bot
intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Definindo a tarefa que será executada a cada 10 minutos
@tasks.loop(minutes=10)  
async def kicker():
    # Obtém o servidor usando o ID armazenado em GUILD_ID
    guild = bot.get_guild(int(GUILD_ID))
    
    # Busca o cargo com o nome "🎟️ ∥ Visitante" dentro do servidor
    cargo = discord.utils.get(guild.roles, name="🎟️ ∥ Visitante")
    
    # Obtém o canal de log onde serão enviadas mensagens de erro ou informações
    log_channel = bot.get_channel(int(LOG_CHANNEL))

    # Lista para armazenar os nomes dos membros expulsos
    membros_kickados = []
    
    # Obtém o horário atual (em UTC)
    agora = datetime.now(timezone.utc)

    # Loop para verificar todos os membros do servidor
    for membro in guild.members:
        # Verifica se o membro tem o cargo "🎟️ ∥ Visitante"
        if cargo in membro.roles:
            # Verifica se o membro está no servidor há mais de 4 horas
            if (agora - membro.joined_at).total_seconds() > 4 * 3600:
                try:
                    # Expulsa o membro do servidor
                    await membro.kick(reason="Tempo no servidor excedeu 4 horas com o cargo 🎟️ ∥ Visitante.")
                    # Adiciona o nome do membro à lista de expulsos
                    membros_kickados.append(membro.name)
                except Exception as e:
                    # Envia uma mensagem para o canal de log se houver um erro ao expulsar o membro
                    await log_channel.send(f"Erro ao expulsar {membro.name}: {e}")

    # Se houver membros expulsos, envia uma mensagem de log com os nomes dos expulsos
    if membros_kickados:
        await log_channel.send(
            f"O(s) seguinte(s) membro(s) foram/foi expulso(s) por estar(em) há mais de 4 horas no servidor com o cargo 🎟️ ∥ Visitante: {', '.join(membros_kickados)}"
        )

# Evento que ocorre quando o bot se conecta e fica pronto para uso
@bot.event
async def on_ready():
    print(f'{bot.user}.')  # Exibe o nome do bot no console
    kicker.start()  # Inicia o loop de expulsão de membros

# Função principal para rodar o bot
if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')  # Obtém o token do bot das variáveis de ambiente
    
    if not token:
        raise ValueError("No token.")  # Garante que o token esteja presente

    bot.run(token)  # Inicia o bot com o token obtido    