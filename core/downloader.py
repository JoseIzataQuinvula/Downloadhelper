import os
import glob
import json
import yt_dlp
import re
import ctypes
import platform
import logging
import unicodedata
from threading import Thread
from kivy.clock import Clock
from .config import FFMPEG_EXE, DOWNLOAD_PATH, QUALITY_PROFILES

logger = logging.getLogger(__name__)

# DEFINIÇÃO DO LOGGER (Deve vir antes do DownloaderCore)
class YDLLogger:
    def debug(self, msg):
        if not msg.startswith('[debug] '):
            logger.debug(msg)
    def info(self, msg): pass
    def warning(self, msg): logger.warning(msg)
    def error(self, msg): logger.error(msg)
    def write(self, msg): pass 
    def flush(self): pass

class DownloaderCore:
    def __init__(self):
        # Base de opções otimizada para evitar bloqueios do YouTube (403 Forbidden)
        self.ydl_opts_base = {
            'logger': YDLLogger(),
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'continuedl': True,
            'nooverwrites': True,
            'ffmpeg_location': FFMPEG_EXE,
            'restrictfilenames': True,
            'socket_timeout': 30,
            'retries': 10,
            # Força o yt-dlp a usar o cliente Android (resolve falha de JS Runtime)
            'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        }

    def _sanitize_name(self, name):
        """Limpa o nome do arquivo para evitar erros de sistema."""
        name = unicodedata.normalize('NFD', name)
        name = "".join([c for c in name if unicodedata.category(c) != 'Mn'])
        name = re.sub(r'[^a-zA-Z0-9\s_-]', '', name)
        name = name.replace(' ', '_').strip('_')
        return name[:50] or "video_download"

    def _get_metadata_path(self, folder_path):
        return os.path.join(os.path.abspath(folder_path), ".metadata.json")

    def _apply_system_hidden(self, file_path):
        """Oculta arquivos de metadados no Windows."""
        try:
            if platform.system() == "Windows":
                ctypes.windll.kernel32.SetFileAttributesW(file_path, 0x02)
        except: pass

    def _save_metadata(self, folder_path, video_id, title):
        """Salva o ID do vídeo para rastreio de downloads futuros."""
        try:
            folder_path = os.path.abspath(folder_path)
            os.makedirs(folder_path, exist_ok=True)
            meta_path = self._get_metadata_path(folder_path)
            if os.path.exists(meta_path) and platform.system() == "Windows":
                ctypes.windll.kernel32.SetFileAttributesW(meta_path, 0x80) # Normaliza antes de gravar
            
            meta = {"id": video_id, "original_title": title}
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=4)
            self._apply_system_hidden(meta_path)
        except Exception as e:
            logger.warning(f"Metadata falhou: {e}")

    def find_folder_by_id(self, video_id):
        """Busca no disco se o vídeo já tem uma pasta associada."""
        if not os.path.exists(DOWNLOAD_PATH): return None
        for entry in os.scandir(DOWNLOAD_PATH):
            if entry.is_dir():
                meta_file = self._get_metadata_path(entry.path)
                if os.path.exists(meta_file):
                    try:
                        with open(meta_file, "r", encoding="utf-8") as f:
                            if json.load(f).get("id") == video_id:
                                return entry.path
                    except: continue
        return None

    def check_existing_status(self, video_id, total_expected=1):
        """Verifica se o download está concluído ou incompleto no disco."""
        folder_path = self.find_folder_by_id(video_id)
        if not folder_path or not os.path.exists(folder_path):
            return "novo", None, 0
        
        valid_exts = ('.mp4', '.mkv', '.webm', '.mp3', '.m4a')
        files = [f for f in os.listdir(folder_path) if f.lower().endswith(valid_exts) and not f.startswith('.')]
        count = len(files)
        
        if count >= total_expected and total_expected > 0:
            return "concluido", folder_path, count
        
        has_temp = any(f.endswith(('.part', '.ytdl')) for f in os.listdir(folder_path))
        return ("incompleto", folder_path, count) if (count > 0 or has_temp) else ("novo", folder_path, 0)

    def get_info(self, url):
        """Extrai informações do vídeo/playlist sem baixar."""
        opts = self.ydl_opts_base.copy()
        opts.update({'extract_flat': 'in_playlist', 'ignoreerrors': True})
        with yt_dlp.YoutubeDL(opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                if not info: return None
                entries = info.get('entries', [])
                info['n_entries'] = len([e for e in entries if e]) if entries else 1
                return info
            except Exception as e:
                logger.error(f"Erro ao obter info: {e}")
                return None

    def start_download(self, url, progress_callback, video_id, title, quality_key="FULL_HD"):
        """Dispara o processo de download em Thread secundária."""
        thread = Thread(target=self._run_download, args=(url, progress_callback, video_id, title, quality_key))
        thread.daemon = True
        thread.start()

    def _run_download(self, url, progress_callback, video_id, title, quality_key):
        """Lógica interna de execução do yt-dlp."""
        dest_folder = self.find_folder_by_id(video_id)
        if not dest_folder:
            clean_name = self._sanitize_name(title)
            dest_folder = os.path.join(DOWNLOAD_PATH, f"{clean_name}_{video_id[:5]}")
            os.makedirs(dest_folder, exist_ok=True)
        
        self._save_metadata(dest_folder, video_id, title)
        profile = QUALITY_PROFILES.get(quality_key, QUALITY_PROFILES["FULL_HD"])
        
        def kivy_progress_hook(d):
            # Cópia profunda para evitar erro de concorrência na Main Thread
            data_copy = d.copy()
            
            if data_copy['status'] == 'downloading':
                p_str = data_copy.get('_percent_str', '0%').replace('%', '').strip()
                try: p_float = float(p_str) / 100
                except: p_float = 0.01
                
                data_copy['ui_status'] = "downloading"
                data_copy['ui_percent'] = p_float
                data_copy['ui_msg'] = f"Baixando: {p_str}% ({data_copy.get('_speed_str', 'N/A')})"
            
            elif data_copy['status'] == 'finished':
                data_copy['ui_status'] = "finished"
                data_copy['ui_percent'] = 0.99 
                data_copy['ui_msg'] = "Processando arquivo..."
            
            Clock.schedule_once(lambda dt: progress_callback(data_copy))

        ydl_opts = {
            **self.ydl_opts_base,
            'format': profile["format"],
            'paths': {'home': str(dest_folder)},
            'outtmpl': '%(title).80s_%(id)s.%(ext)s', 
            'progress_hooks': [kivy_progress_hook],
            'merge_output_format': 'mp4',
            'postprocessor_args': ['-c', 'copy'],
        }

        if quality_key == "AUDIO_ONLY":
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                Clock.schedule_once(lambda dt: progress_callback({'status': 'complete_all'}))
            except Exception as e:
                err_msg = str(e)
                msg = "Erro 403: Bloqueio" if "403" in err_msg else "Falha no Download"
                Clock.schedule_once(lambda dt: progress_callback({'status': 'error', 'msg': msg}))