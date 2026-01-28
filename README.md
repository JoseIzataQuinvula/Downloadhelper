# DownloadHelper - YouTube Download Manager

Este repositório contém o código-fonte do **DownloadHelper**, uma ferramenta de código aberto desenvolvida em Python para o gerenciamento avançado de downloads do YouTube. O projeto foca em precisão de status de arquivos e suporte a operações retomáveis (pausa/continuação).

## 🚀 Visão Geral (v1.0.1 - Windows Edition)

O DownloadHelper foi projetado para oferecer uma interface de gestão de downloads estável. A lógica principal permite o processamento de vídeos individuais e playlists, garantindo integridade de dados através da sincronização com os motores do `yt-dlp`, binários do `FFmpeg` e um sistema de monitoramento em tempo real.

---

## 📂 Arquitetura de Pastas (Estrutura Completa)

A organização do diretório segue o padrão de separação de responsabilidades para facilitar a manutenção e o porte entre plataformas:

* **Raiz:** Contém o ponto de entrada (`main.py`), dependências (`requirements.txt`) e scripts de build (`downloadhelper.spec`, `buildozer.spec`, `setup.iss`).
* **core/:** Lógica de processamento, configurações e funções auxiliares.
* **ui/ & kv/:** Separação da lógica de comportamento (Python) e design visual (Kivy Language).
* **ffmpeg/:** Pasta destinada aos binários de conversão de mídia (necessários para a versão desktop). **Nota: Os arquivos .exe não são incluídos no repositório devido ao tamanho.**
* **assets/:** Identidade gráfica, ícones e recursos visuais para todas as plataformas.

---

## ⚙️ Especificações Técnicas

O desenvolvimento priorizou a portabilidade e a automação de processos de mídia:

* **Linguagem:** Python 3.13+ com framework Kivy/KivyMD.
* **Processamento de Mídia:** Integração nativa com FFmpeg para alta fidelidade de áudio e vídeo.
* **Multiplataforma:**
* **Windows:** Compilação via PyInstaller e instalador profissional via Inno Setup.
* **Android:** Geração de APK via Buildozer (Linux/Ubuntu) - *Em breve*.

---

## 🖼️ Demonstração da Interface

### Interface Principal

![Visualização da Interface](./assets/preview.png)

---

## 🛠️ Procedimentos de Instalação e Uso

### Para Desenvolvedores (Rodar via Código)

1. **Clone o repositório:**

```bash
git clone [https://github.com/JoseIzataQuinvula/download-helper.git](https://github.com/JoseIzataQuinvula/download-helper.git)
cd download-helper
Instale as dependências:

Bash
pip install -r requirements.txt
Configuração do FFmpeg (Obrigatório para Windows local): Como os binários executáveis são muito grandes para o GitHub, você deve baixá-los manualmente:

Baixe os binários em ffmpeg.org.

Coloque ffmpeg.exe, ffplay.exe e ffprobe.exe dentro da pasta ffmpeg/.

Execução:

Bash
python main.py
📦 Compilação e Distribuição
Para Windows (EXE)
A versão v1.0.1 foca na integridade do sistema Windows. Para gerar o executável:

Bash
pyinstaller --noconfirm downloadhelper.spec
Para gerar o instalador profissional (.exe), utilize o Inno Setup com o arquivo setup.iss.

Para Android (APK)
Em um ambiente Linux (Ubuntu), utilize o Buildozer para gerar o pacote móvel:

Bash
buildozer android debug
📜 Licença
Este projeto é de código aberto sob a licença MIT. Sinta-se à vontade para contribuir!

Desenvolvido por José Izata Quivula.
