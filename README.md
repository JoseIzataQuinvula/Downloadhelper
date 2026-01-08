Markdown

# DownloadHelper - YouTube Download Manager

Este repositório contém o código-fonte do DownloadHelper, uma ferramenta de código aberto desenvolvida em Python para o gerenciamento avançado de downloads do YouTube. O projeto foca em precisão de status de arquivos e suporte a operações retomáveis (pausa/continuação).

## Visão Geral

O DownloadHelper foi projetado para oferecer uma interface de gestão de downloads estável. A lógica principal permite o processamento de vídeos individuais e playlists, garantindo integridade de dados através da sincronização com os binários do FFmpeg e um sistema de monitoramento de disco em tempo real.

---

## Arquitetura de Pastas

A organização do diretório segue o padrão de distribuição para executáveis Python:

* **Raiz:** Ponto de entrada (`download_helper.py`), dependências (`requirements.txt`) e configuração de build.
* **ffmpeg/:** Binários obrigatórios (`ffmpeg.exe`, `ffprobe.exe`) para muxing e conversão de mídia.
* **assets/:** Recursos visuais e identidade gráfica (`icon.png`).
* **dist/:** (Gerado) Contém o executável final empacotado para o usuário.

---

## Especificações Técnicas

O desenvolvimento priorizou a portabilidade e a automação de processos de mídia:

* **Linguagem:** Python 3.x com processamento assíncrono para UI e downloads.
* **Dependências:** Gerenciadas via `requirements.txt` (incluindo `yt-dlp` ou similar).
* **Processamento de Mídia:** Integração nativa com FFmpeg para alta fidelidade de áudio e vídeo.
* **Distribuição:** Compilação via PyInstaller para geração de executável único (Self-contained).

---

## Demonstração da Interface

### Interface Principal
![Visualização da Interface](./assets/preview.png)

---

## Procedimentos de Instalação e Uso

Para configurar o ambiente de desenvolvimento localmente:

1. **Clone o repositório:**
```bash
git clone [https://github.com/JoseIzataQuinvula/download-helper.git](https://github.com/JoseIzataQuinvula/download-helper.git)
cd download-helper
Instale as dependências:

Bash

pip install -r requirements.txt
Execução: Certifique-se de que os binários do FFmpeg estão na pasta raiz e execute:

Bash

python download_helper.py
Build de Distribuição
Para gerar o executável final para Windows:

Bash

pyinstaller --onefile --noconsole --add-data "assets;assets" --add-data "ffmpeg;ffmpeg" --icon=assets/icon.png download_helper.py

---

### Tópicos Sugeridos para o GitHub
Para este projeto, use estas tags para atrair o público certo:

`python` `youtube-downloader` `ffmpeg` `pyinstaller` `gui` `open-source` `download-manager` `clean-code` `jose-izata-quivula` `angola-tech`



**Precisa que eu ajude com a lógica do comando PyInstaller ou quer passar para o ajuste de outro projeto?**
