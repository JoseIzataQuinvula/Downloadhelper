import os
import sys
import platform
import logging
from pathlib import Path

# --- 1. AJUSTE DE CAMINHOS (CRÍTICO PARA .EXE E KIVY) ---
def get_resource_path():
    """ Retorna o caminho para recursos (KV, Assets) lidando com PyInstaller. """
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent

def get_app_dir():
    """ Retorna a pasta real onde o executável ou script reside. """
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent

RESOURCE_DIR = get_resource_path().absolute()
BASE_DIR = get_app_dir().absolute()

KV_DIR = RESOURCE_DIR / "kv"
ASSETS_DIR = RESOURCE_DIR / "assets"
FFMPEG_DIR = RESOURCE_DIR / "ffmpeg"

# Logs na pasta oculta do usuário
LOG_DIR = Path.home() / ".download_helper" / "logs"

# --- 2. CONFIGURAÇÃO DE LOGGING ---
def setup_logging():
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_file = LOG_DIR / "app.log"
        handlers = [
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(str(log_file), encoding='utf-8')
        ]
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=handlers
        )
    except Exception as e:
        print(f"Erro ao configurar log: {e}")
        logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)])

setup_logging()
logger = logging.getLogger(__name__)

# --- 3. LOCALIZAÇÃO DO FFMPEG ---
def get_ffmpeg_path():
    system = platform.system()
    exe_name = "ffmpeg.exe" if system == "Windows" else "ffmpeg"
    internal_ffmpeg = FFMPEG_DIR / exe_name
    
    if internal_ffmpeg.exists():
        # Resolve e converte para string para compatibilidade total com yt-dlp
        return str(internal_ffmpeg.resolve())
    return exe_name 

FFMPEG_EXE = get_ffmpeg_path()

# --- 4. CONFIGURAÇÃO DE DOWNLOADS ---
try:
    # Blindagem para usuários com acentos (ex: José)
    DOWNLOAD_PATH = (Path.home() / "Downloads" / "DownloadHelper").resolve()
except Exception:
    DOWNLOAD_PATH = (BASE_DIR / "downloads").resolve()

# --- 5. PERFIS DE QUALIDADE OTIMIZADOS ---
# Ajustado para priorizar MP4/M4A, garantindo união rápida (Merge) e arquivos leves.
QUALITY_PROFILES = {
    "ULTRA_4K": {
        "label": "Ultra HD (4K)", 
        "description": "Qualidade máxima (Lento)",
        "format": "bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best", 
        "ext": "mp4"
    },
    "FULL_HD": {
        "label": "Full HD (1080p)", 
        "description": "Padrão de alta qualidade",
        "format": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best", 
        "ext": "mp4"
    },
    "HD_720P": {
        "label": "HD (720p)", 
        "description": "Rápido e leve (Recomendado)",
        "format": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best", 
        "ext": "mp4"
    },
    "SD_480P": {
        "label": "SD (480p)", 
        "description": "Econômico e veloz",
        "format": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best", 
        "ext": "mp4"
    },
    "AUDIO_ONLY": {
        "label": "Música (MP3)", 
        "description": "Apenas áudio",
        "format": "bestaudio/best", 
        "ext": "mp3"
    }
}

# --- 6. UTILITÁRIOS ---
def get_kv_file(filename):
    return str((KV_DIR / filename).resolve())

def get_asset_file(filename):
    path = ASSETS_DIR / filename
    return str(path.resolve()) if path.exists() else filename

def init_folders():
    try:
        if not DOWNLOAD_PATH.exists():
            DOWNLOAD_PATH.mkdir(parents=True, exist_ok=True)
            logger.info(f"Pasta criada: {DOWNLOAD_PATH}")
    except Exception as e:
        logger.error(f"Erro ao criar pastas: {e}")

init_folders()