# BOT-DJzada

Link direto para convite: https://discord.com/oauth2/authorize?client_id=1308152466231136349

Este é um bot de música para o Discord que permite que os usuários toquem músicas de vídeos do YouTube em canais de voz. O bot é simples de configurar e usa a biblioteca `discord.py` para interagir com a API do Discord, além de `yt-dlp` para fazer download e streaming de vídeos.

## Funcionalidades

- **Play**: Toca músicas diretamente do YouTube.
- **Fila**: Exibe a fila de músicas.
- **Pular**: Pula a música atual.
- **Pausar**: Pausa a música atual.
- **Continuar**: Retoma a música pausada.
- **Comando de Ajuda**: Exibe uma lista de comandos disponíveis.

## Requisitos

Este bot foi desenvolvido utilizando as seguintes bibliotecas:

- `discord.py` – Biblioteca principal para interação com a API do Discord.
- `discord.py[voice]` – Extensão para funcionalidades de áudio (necessária para tocar música em canais de voz).
- `python-dotenv` – Para carregar variáveis de ambiente de um arquivo `.env`.
- `PyNaCl` – Biblioteca necessária para funcionalidades de voz no Discord.
- `yt-dlp` – Ferramenta para fazer download e streaming de vídeos do YouTube, substituindo o `youtube-dl`.
- `ffmpeg` – Requisito para processamento de áudio e vídeo.

### Como instalar

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2. Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Crie um arquivo `.env` na raiz do projeto e adicione seu token do Discord e o ID do bot:
    ```
    DISCORD_TOKEN=seu_token_do_discord
    BOT_ID=seu_bot_id
    ```

5. Certifique-se de que o `ffmpeg` esteja instalado no seu sistema e disponível no PATH.

## Como usar

1. Execute o bot:
    ```bash
    python main.py
    ```

2. No Discord, convide o bot para seu servidor e use os seguintes comandos:

- `/play [nome ou link do YouTube]` – Toca a música no canal de voz.
- `/fila` – Exibe a fila de músicas.
- `/pular` – Pula a música atual.
- `/pausar` – Pausa a música atual.
- `/continuar` – Retoma a música pausada. (Em desenvolvimento)
- `/ajuda` – Exibe uma lista de comandos disponíveis. (Em desenvolvimento)

