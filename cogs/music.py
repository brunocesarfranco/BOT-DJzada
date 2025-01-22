import discord
from discord import app_commands
from discord.ext import commands
from yt_dlp import YoutubeDL  # Substituindo youtube-dl por yt-dlp

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.is_playing = False
        self.music_queue = []
        self.YDL_OPTIONS = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'source_address': '0.0.0.0',
        }
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn',
        }
        self.vc = None

    def search_yt(self, item):
        self.YDL_OPTIONS['cookiefile'] = 'cookies.txt'  # Adiciona o caminho para o arquivo de cookies

        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{item}", download=False)['entries'][0]
            except Exception as e:
                print(f"Error searching YouTube: {e}")
                return False
        return {'source': info['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            if self.vc is None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False
            if self.vc:
                await self.vc.disconnect()

    @app_commands.command(name="ajuda", description="Mostre um comando de ajuda.")
    async def help(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        helptxt = (
            "`/ajuda` - Veja esse guia!\n"
            "`/play` - Toque uma música do YouTube!\n"
            "`/fila` - Veja a fila de músicas na Playlist\n"
            "`/pular` - Pule para a próxima música da fila\n"
            "`/pausar` - Pausa a música atual. (Em desenvolvimento)\n"
            "`/continuar` - Continua a música pausada. (Em desenvolvimento)"
        )
        embedhelp = discord.Embed(
            colour=1646116,
            title=f'Comandos do {self.client.user.name}',
            description=helptxt
        )
        try:
            embedhelp.set_thumbnail(url=self.client.user.avatar.url)
        except:
            pass
        await interaction.followup.send(embed=embedhelp)

    @app_commands.command(name="play", description="Toca uma música do YouTube.")
    @app_commands.describe(busca="Digite o nome ou o link da música no YouTube")
    async def play(self, interaction: discord.Interaction, busca: str):
        await interaction.response.defer(thinking=True)
        try:
            voice_channel = interaction.user.voice.channel
        except:
            embedvc = discord.Embed(
                colour=1646116,
                description='Para tocar uma música, primeiro se conecte a um canal de voz.'
            )
            await interaction.followup.send(embed=embedvc)
            return
        song = self.search_yt(busca)
        if not song:
            embedvc = discord.Embed(
                colour=12255232,
                description='Algo deu errado! Tente novamente com outro nome ou link.'
            )
            await interaction.followup.send(embed=embedvc)
        else:
            embedvc = discord.Embed(
                colour=32768,
                description=f"Você adicionou a música **{song['title']}** à fila!"
            )
            await interaction.followup.send(embed=embedvc)
            self.music_queue.append([song, voice_channel])
            if not self.is_playing:
                await self.play_music()

    @app_commands.command(name="fila", description="Mostra as atuais músicas da fila.")
    async def q(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        retval = "\n".join(f"**{i+1} -** {m[0]['title']}" for i, m in enumerate(self.music_queue))
        embedvc = discord.Embed(
            colour=1646116 if retval else 12255232,
            description=retval or "Não existem músicas na fila no momento."
        )
        await interaction.followup.send(embed=embedvc)

    @app_commands.command(name="pular", description="Pula a atual música que está tocando.")
    @app_commands.default_permissions(manage_channels=True)
    async def pular(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        if self.vc and self.vc.is_playing():
            self.vc.stop()
            await self.play_music()
            embedvc = discord.Embed(
                colour=1646116,
                description="Você pulou a música."
            )
            await interaction.followup.send(embed=embedvc)

    @app_commands.command(name="pausar", description="Pausa a música que está tocando.")
    async def pausar(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        if not self.vc or not self.vc.is_connected():
            embedvc = discord.Embed(
                colour=12255232,
                description="O bot não está conectado a nenhum canal de voz."
            )
        elif not self.vc.is_playing():
            embedvc = discord.Embed(
                colour=12255232,
                description="Não há nenhuma música tocando no momento para pausar."
            )
        else:
            # Pausa a música
            self.vc.pause()
            embedvc = discord.Embed(
                colour=1646116,
                description="A música foi pausada com sucesso."
            )
            self.is_playing = False  # Atualiza o estado de reprodução

        await interaction.followup.send(embed=embedvc)

    @app_commands.command(name="continuar", description="Continua a música pausada.")
    async def continuar(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        if not self.vc or not self.vc.is_connected():
            embedvc = discord.Embed(
                colour=12255232,
                description="O bot não está conectado a nenhum canal de voz."
            )
        elif self.vc.is_playing():
            embedvc = discord.Embed(
                colour=12255232,
                description="A música já está tocando, não há nada para continuar."
            )
        else:
            # Retoma a música
            self.vc.resume()
            embedvc = discord.Embed(
                colour=1646116,
                description="A música foi retomada com sucesso."
            )
            self.is_playing = True  # Atualiza o estado de reprodução

        await interaction.followup.send(embed=embedvc)

async def setup(client):
    await client.add_cog(Music(client))
