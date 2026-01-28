import re
import logging
import unicodedata
import time # Adicionado para gerar nomes únicos se necessário

# O logger ajuda a monitorar se as URLs estão sendo limpas corretamente
logger = logging.getLogger(__name__)

def get_media_id(url: str) -> tuple:
    """Retorna uma tupla (tipo, id). Tipo pode ser 'playlist' ou 'video'."""
    if not url or not isinstance(url, str):
        return None, None

    if url.lower().startswith(("file://", "/", "c:", "\\", "./", "../")):
        return None, None

    playlist_match = re.search(r"[&?]list=([A-Za-z0-9_-]+)", url)
    if playlist_match:
        return "playlist", playlist_match.group(1)
    
    video_patterns = [
        r'(?:v=|\/|embed\/|shorts\/|youtu\.be\/)([0-9A-Za-z_-]{11})',
        r'^([0-9A-Za-z_-]{11})$' 
    ]
    
    for pattern in video_patterns:
        match = re.search(pattern, url)
        if match:
            v_id = match.group(1)
            if len(v_id) == 11:
                return "video", v_id
    
    return None, None

def normalize_url(url: str) -> str:
    """Reconstrói a URL para eliminar trackers e excessos."""
    if not url: return ""
    url = url.strip()
    
    tipo, midia_id = get_media_id(url)
    
    if tipo == "playlist":
        return f"https://www.youtube.com/playlist?list={midia_id}"
    elif tipo == "video":
        return f"https://www.youtube.com/watch?v={midia_id}"
    
    if "." in url and not url.lower().startswith(("http://", "https://")):
        url = "https://" + url
    
    return url.split()[0] if url else ""

def sanitize_filename(name: str) -> str:
    """Protege o sistema de arquivos contra injeção e nomes reservados."""
    if not name: return "arquivo_sem_nome"
    
    # 1. Normaliza caracteres Unicode (remove acentos)
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    
    # 2. Remove caracteres proibidos pelo SO
    name = re.sub(r'[<>:"/\\|?*]', ' ', name)
    
    # 3. Mantém apenas caracteres ASCII visíveis
    name = "".join(char for char in name if 31 < ord(char) < 127)
    
    # 4. Proteção contra nomes reservados do Windows
    reserved = {
        "CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4",
        "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2",
        "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }
    
    clean_name = " ".join(name.split()).strip().strip('.')
    
    # CORREÇÃO DA LINHA 87: Removemos a dependência de 'midia_id' que não existe aqui
    if not clean_name or clean_name.upper() in reserved:
        clean_name = f"download_{int(time.time())}"
        
    return clean_name[:100]

def format_duration(sec: int) -> str:
    """Converte segundos para formato legível HH:MM:SS."""
    try:
        seconds = abs(int(float(sec)))
        if seconds == 0: return "00:00"
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        if h > 0:
            return f"{h:02d}:{m:02d}:{s:02d}"
        return f"{m:02d}:{s:02d}"
    except:
        return "00:00"

def calculate_completion_percentage(downloaded, total):
    """Calcula progresso para a ProgressBar do Kivy."""
    try:
        d = float(downloaded)
        t = float(total)
        if t <= 0: return 0.0
        percent = (d / t) * 100
        # Retorna entre 0.0 e 100.0, formatado para 1 casa decimal
        return min(100.0, max(0.0, round(percent, 1)))
    except:
        return 0.0