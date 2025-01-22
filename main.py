import os
import logging
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Carrega variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Inicialização do bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!!", intents=intents, application_id=int(os.getenv("BOT_ID")))


@bot.event
async def on_ready():
    """Evento acionado quando o bot está pronto."""
    logging.info(f"Bot {bot.user.name} está online!")
    print(f"Bot {bot.user.name} está online!")
    
    os.getenv("DISCORD_TOKEN")
    # Envia uma mensagem de boas-vindas e assinatura para o Discord
    channel = bot.get_channel(1308160946878808085)  # Substitua pelo ID do canal onde deseja a mensagem
    if channel:
        await channel.send("DJzada está on.")
    else:
        logging.error("Canal não encontrado!")

@bot.command()
@commands.is_owner()
async def sync(ctx, guild: str = None):
    """Sincroniza os comandos do bot com o Discord."""
    try:
        if guild is None:
            await bot.tree.sync()
            message = "Comandos globais sincronizados com sucesso!"
        else:
            guild_obj = discord.Object(id=int(guild))
            await bot.tree.sync(guild=guild_obj)
            message = f"Comandos sincronizados com sucesso no servidor ID: {guild}"
        await ctx.send(f"**{message}**")
    except Exception as e:
        logging.error(f"Erro ao sincronizar comandos: {e}")
        await ctx.send(f"**Erro ao sincronizar comandos: {e}**")


async def main():
    """Carrega extensões e inicia o bot."""
    async with bot:
        cogs_path = './cogs'
        if os.path.exists(cogs_path):
            for filename in os.listdir(cogs_path):
                if filename.endswith('.py'):
                    try:
                        await bot.load_extension(f'cogs.{filename[:-3]}')
                        logging.info(f"Extensão carregada: {filename}")
                    except Exception as e:
                        logging.error(f"Erro ao carregar a extensão {filename}: {e}")
        else:
            logging.warning(f"O diretório '{cogs_path}' não foi encontrado.")

        # Inicia o bot com o token
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            logging.error("O token do bot não foi encontrado no arquivo .env.")
            return
        await bot.start(token)


# Inicia o evento principal
if __name__ == "__main__":
    asyncio.run(main())
